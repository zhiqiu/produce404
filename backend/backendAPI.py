from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func
from createTables import *
from config import DEBUG, DEBUG_COMMUNITATION, appID, appSecret
from utils import DataFormatException, Status, Encrypt
from testbench import *
import json
import requests


__all__ = ["API"]


class API():
    def __init__(self, engine):
        self.dbName = engine.name
        base = createAllTable(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        if DEBUG:
            try:
                makeTestDatabase(self.session)
            except Exception as e:
                self.session.rollback()
                print(e)

    action2API = {
        "get_user_info": "getUserInfo",
        "login": "login",
        "get_index": "getIndex",
        "like_audio": "likeAudio",
        "get_comments": "getComments",
        "post_comment": "postComment",
        "get_collections": "getCollections",
        "add_collection": "addCollection",
        "add_into_collection": "addIntoCollection",
        "get_explore": "getExplore",
        "get_one_feed": "getOneFeed",
        "get_my_feed": "getMyFeeds",
        "post_audio": "postAudio",
        "get_medal": "getMedal",
    }

    def commonGetAPI(self, tableName, **kwargs):
        try:
            if tableName not in tables:
                return Status.internalError("Table %s doesn't exists." % tableName)

            tableClass = tables[tableName]

            for field in kwargs:
                if not hasattr(tableClass, field):
                    return Status.internalError("Invalid field name: %s." % field)

            filterResult = self.session.query(tableClass).filter_by(**kwargs)
            content = filterResult.all()
        except Exception as e:
            return Status.internalError(e)
        else:
            if not content:
                return Status.notFound()
            return Status.success([c.toDict() for c in content])

    def commonAddAPI(self, tableName, **kwargs):
        try:
            if tableName not in tables:
                return Status.internalError("Table %s doesn't exists." % tableName)

            tableClass = tables[tableName]

            for field in kwargs:
                if not hasattr(tableClass, field):
                    return Status.internalError("Invalid field name: %s." % field)

            newContent = tableClass(**kwargs)
            newContent.create(self.session)
        except DataFormatException as e:
            return Status.dataFormatError(e)
        except Exception as e:
            return Status.internalError(e)
        else:
            return Status.success()

    
    def postCallAPI(self, form):
        if not form:
            return Status.internalError("Missing form data")
        try:
            action = form["action"]
            if action != "login" and not DEBUG_COMMUNITATION:
                try:
                    encryptor = Encrypt()
                    origialText = encryptor.decrypt(form["token"])
                    tokenObject = json.loads(originalText)
                    form["openid"] = tokenObject["openid"]
                    form["sessionKey"] = tokenObject["session_key"]
                except Exception as e:
                    raise Exception("invalid token")
            else:
                form["openid"] = "openid1"
                form["session_key"] = "123"
            return getattr(self, API.action2API[action])(form)
        except Exception as e:
            return Status.internalError(e)


    #############################   API   #############################

    def getUserInfo(self, form):
        '''
        获取自己的信息
        {
            token:
        }
        {
            user: user{}
        }
        '''
        user = self.session.query(User).filter(and_(
            User.deleted == False,
            User.openid == form["openid"]
        )).first()

        if user:
            return user.toDict()
        else:
            raise Exception("User does't exists.")

    def login(self, form):
        '''
        觅声_登录
        {
            action: "login",
            code: "code"
        }
        {
            token: "token",
            first_time: false
        }

        //获取openid和session_key:
        request:
        https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code
        response:
        正常返回的JSON数据包
        //{
            "openid": "OPENID",
            "session_key": "SESSIONKEY",
        }

        //满足UnionID返回条件时，返回的JSON数据包
        {
            "openid": "OPENID",
            "session_key": "SESSIONKEY",
            "unionid": "UNIONID"
        }
        //错误时返回JSON数据包(示例为Code无效)
        {
            "errcode": 40029,
            "errmsg": "invalid code"
        }
        '''

        if DEBUG_COMMUNITATION:
            return Status.success({
                "token": "I am token.",
                "first_time": True
            })

        jsCode = form["code"]

        url = "https://api.weixin.qq.com/sns/jscode2session"
        params = {
            "appid": appID,
            "secret": appSecret,
            "js_code": jsCode,
            "grant_type": "authorization_code"
        }

        try:
            res = requests.get(url, params=params)
            resJson = json.loads(res.text)
            openID = resJson["openid"]
            sessionKey = resJson["session_key"]

            # 加密 openid 和 session_key 获得token
            encryptor = Encrypt()
            token = {"openid": openID, "session_key": sessionKey}
            token = encryptor.encrypt(json.dumps(token))

            # 查询数据库，检测是否首次登陆
            firstTime = False
            User = tables["user"]
            if not self.session.query(User).filter(User.openid == openID):
                firstTime = True

            return Status.success({
                "token": token,
                "first_time": firstTime
            })
        except Exception as e:
            return Status.internalError("invalid code")

    def getIndex(self, form):
        '''
        觅声首页：
        {
            action: 'get_index',
            listentype: 'diff'/'like',
            channel: 'unset'/'channel_name',
        }
        {
            feed: feed{},
            feed_next: feed{}
        }
        // 上一首由前端记录
        '''

        # 不同的数据库类型有不同的随机查询方式
        if self.dbName == "sqlite":
            randfunc = func.random()
        else:
            # for mysql
            randfunc = func.rand()

        # 随机查询两个audio
        randTwoAudios = self.session.query(User, Audio).filter(and_(
            User.deleted == False,
            Audio.deleted == False,
            R_User_Create_Audio.deleted == False,
            User.openid == R_User_Create_Audio.user_openid,
            R_User_Create_Audio.audio_id == Audio.audio_id
        )).order_by(randfunc).limit(2).all()

        # 查询对应的user，tag，以及其他信息，组装成feed
        openid = form["openid"]
        feeds = []
        for user, audio in randTwoAudios:
            audio_id = audio.audio_id

            tags = self.session.query(AudioTag).filter(and_(
                AudioTag.deleted == False,
                R_Audio_Has_AudioTag.deleted == False,
                AudioTag.audiotag_id == R_Audio_Has_AudioTag.audiotag_id,
                R_Audio_Has_AudioTag.audio_id == audio_id
            )).all()

            like_num = self.session.query(User.openid).filter(and_(
                User.openid == R_User_Like_Audio.user_openid,
                R_User_Like_Audio.deleted == False,
                R_User_Like_Audio.audio_id == audio_id,
                )).count()

            comment_num = self.session.query(Comment.comment_id).filter(and_(
                Comment.deleted == False,
                Comment.audio_id == audio_id
                )).count()

            isliked = bool(self.session.query(R_User_Like_Audio.user_openid).filter(and_(
                R_User_Like_Audio.user_openid == openid,
                R_User_Like_Audio.deleted == False,
                R_User_Like_Audio.audio_id == audio_id,
                )).count())

            iscollected = bool(self.session.query(Collection).filter(and_(
                Collection.deleted == False,
                R_Audio_In_Collection.deleted == False,
                Collection.user_openid == openid,
                Collection.collection_id == R_Audio_In_Collection.collection_id,
                R_Audio_In_Collection.audio_id == audio_id
            )).first())
            feeds.append({
                "user": user.toDict(),
                "audio": audio.toDict(),
                "tags": [tag.toDict() for tag in tags],
                "like_num": like_num,
                "comment_num": comment_num,
                "isliked": isliked,
                "iscollected": iscollected,
                "collections": [c.toDict() for c in collections],
            })

        return Status.success({
            "feed": feeds[0],
            "feed_next": feeds[1],
        })

    def likeAudio(self, form):
        '''
        点赞：
        {
            action: 'like_audio',
            audio_id: ''
        }
        {
            err: 'ok'
        }
        '''

        openid = form["openid"]
        audio_id = form["audio_id"]

        Audio.checkExist(self.session, audio_id)

        like = self.session.query(R_User_Like_Audio).filter(and_(
            R_User_Like_Audio.user_openid == openid,
            R_User_Like_Audio.audio_id == audio_id
        )).first()

        if like:
            # 数据库中已存在记录，只需修改deleted列即可。
            like.deleted = False
        else:
            like = R_User_Like_Audio(user_openid=openid, audio_id=audio_id)
        like.merge()
        
        return Status.success()
    
    def getComments(self, form):
        '''
        觅声_获取评论
        {
            action: 'get_comments',
            audio_id: ''
        }
        {
            comments:[
                comment{},
                comment{},...
            ]
        }
        '''

        openid = form["openid"]
        audio_id = form["audio_id"]

        Audio.checkExist(self.session, audio_id)

        comments = self.session.query(Comment).filter(and_(
            Comment.deleted == False,
            Comment.audio_id == audio_id
        )).all()

        detailedComments = []
        for c in comments:
            com = c.toDict()
            openid = com["user_openid"]
            del com["user_openid"]
            user = self.session.query(User).filter(User.openid == openid).first()
            com["user"] = user.toDict()
            
            if com["replyto"]:
                reply_to_openid = com["replyto"]
                del com["replyto"]
                user = self.session.query(User).filter(User.openid == reply_to_openid).first()
                com["replyto"] = user.toDict()
            
            like_num = self.session.query(R_User_Like_Comment).filter(and_(
                R_User_Like_Comment.deleted == False,
                R_User_Like_Comment.comment_id == com["comment_id"]
            )).count()

            com["like_num"] = like_num

            isliked = bool(self.session.query(User.openid).filter(and_(
                User.openid == openid,
                User.openid == R_User_Like_Comment.user_openid,
                R_User_Like_Comment.deleted == False,
                R_User_Like_Comment.comment_id == com["comment_id"]
            )).count())

            com["isliked"] = isliked

            detailedComments.append(com)

        return Status.success({
            "comments": detailedComments
        })

    def postComment(self, form):
        '''
        觅声_发表评论
        {
            action: 'post_comment',
            audio_id: '',
            reply_to_user_openid: '',
            text:''
        }
        {
            err:'ok'
        }
        '''

        openid = form["openid"]
        audio_id = form["audio_id"]
        replyto = form["reply_to_user_openid"]

        Audio.checkExist(self.session, audio_id)
        
        if replyto:
            User.checkExist(self.session, replyto)

        Comment(audio_id=audio_id,
                user_openid=openid,
                replyto=replyto,
                text=form["text"]
                ).create()
        
        return Status.success()
    
    def getCollections(self, form):
        '''
        觅声_收藏_显示所有收藏夹
        {
            action: 'get_collections'
        }
        {
            collections: [
                collection{},
                collection{},
            ]
        }
        '''

        openid = form["openid"]

        collections = self.session.query(Collection).filter(and_(
            Collection.deleted == False,
            Collection.user_openid == openid
        )).all()

        return Status.success({
            "collections": [c.toDict() for c in collections]
        })

    def addCollection(self, form):
        '''
        觅声_收藏_增加收藏夹
        {
            action: 'add_collection',
            collection_name : ''
        }
        {
            err: 'ok'
        }
        '''
        
        openid = form["openid"]
        name = form["collection_name"]
        Collection(user_openid=openid,name=name).create()

        return Status.success()

    def addIntoCollection(self, form):
        '''
        觅声_收藏_增加收藏
        {
            action: 'add_into_collection',
            audio_id: '',
            collection_id: ''
        }
        {
            err: 'ok'
        }
        '''
        
        openid = form["openid"]
        audio_id = form["audio_id"]
        Audio.checkExist(self.session, audio_id)
        collection_id = form["collection_id"]
        Collection.checkExist(self.session, collection_id)

        if not self.session.query(Collection.collection_id).filter(and_(
            Collection.user_openid == openid,
            Collection.collection_id == collection_id
        )).first():
            raise Exception("It's not your collection.")

        Audio.checkExist(audio_id)
        Collection.checkExist(collection_id)

        R_Audio_In_Collection(audio_id=audio_id, collection_id=collection_id).create()

        return Status.success()

    def getExplore(self, form):
        '''
        发现_显示10条
        {
            action: 'get_explore',
            last_audio_id: '',
        }
        {
            feeds: [
                feed{},
                feed{}
            ]// 10条
        }
        '''
        if DEBUG_COMMUNITATION:
            return Status.success({
                "feeds":[
                    testFeed,
                    testFeed,
                    testFeed,
                ]
            })

    def getOneFeed(self, form):
        '''
        获取1条feed
        {
            action: 'get_one_feed',
            audio_id: ''
        }
        {
            feed: feed{}
        }
        '''
        
        openid = form["openid"]
        audio_id = form["audio_id"]

        Audio.checkExist(self.session, audio_id)

        user, audio = self.session.query(User, Audio).filter(and_(
            User.deleted == False,
            Audio.deleted == False,
            R_User_Create_Audio.deleted == False,
            User.openid == R_User_Create_Audio.user_openid,
            R_User_Create_Audio.audio_id == Audio.audio_id
        )).first()

        tags = self.session.query(AudioTag).filter(and_(
            AudioTag.deleted == False,
            R_Audio_Has_AudioTag.deleted == False,
            AudioTag.audiotag_id == R_Audio_Has_AudioTag.audiotag_id,
            R_Audio_Has_AudioTag.audio_id == audio_id
        )).all()

        like_num = self.session.query(User.openid).filter(and_(
            User.openid == R_User_Like_Audio.user_openid,
            R_User_Like_Audio.deleted == False,
            R_User_Like_Audio.audio_id == audio_id,
            )).count()

        comment_num = self.session.query(Comment.comment_id).filter(and_(
            Comment.deleted == False,
            Comment.audio_id == audio_id
            )).count()

        isliked = bool(self.session.query(R_User_Like_Audio.user_openid).filter(and_(
            R_User_Like_Audio.user_openid == openid,
            R_User_Like_Audio.deleted == False,
            R_User_Like_Audio.audio_id == audio_id,
            )).count())

        iscollected = bool(self.session.query(Collection).filter(and_(
            Collection.deleted == False,
            R_Audio_In_Collection.deleted == False,
            Collection.user_openid == openid,
            Collection.collection_id == R_Audio_In_Collection.collection_id,
            R_Audio_In_Collection.audio_id == audio_id
        )).first())

        feed = {
            "user": user.toDict(),
            "audio": audio.toDict(),
            "tags": [tag.toDict() for tag in tags],
            "like_num": like_num,
            "comment_num": comment_num,
            "isliked": isliked,
            "iscollected": iscollected,
            "collections": [c.toDict() for c in collections],
        }

        return Status.success({
            "feed": feed
        })
    
    def getMyFeeds(self,form):
        '''
        按用户获取feeds
        {
            action: 'get_my_feed',
            last_audio_id: ''
        }
        {
            feeds: [
                feed{}
            ]
        }
        '''

        openid = form["openid"]
        last_audio_id = form["last_audio_id"]
        try:
            if last_audio_id:
                last_audio_id = int(last_audio_id)
        except:
            raise DataFormatException("last_audio_id must be an integer or empty string")
        findAudios = self.session.query(User, Audio).filter(and_(
            User.openid == openid,
            Audio.deleted == False,
            R_User_Create_Audio.deleted == False,
            User.openid == R_User_Create_Audio.user_openid,
            R_User_Create_Audio.audio_id == Audio.audio_id,
        ))

        if last_audio_id != "":
            findAudios = findAudios.finter(Audio.audio_id < last_audio_id)

        # 每次显示10条
        findAudios = findAudios.order_by(Audio.audio_id.desc()).limit(10).all()

        feeds = []
        for user, audio in findAudios:
            audio_id = audio.audio_id

            tags = self.session.query(AudioTag).filter(and_(
                AudioTag.deleted == False,
                R_Audio_Has_AudioTag.deleted == False,
                AudioTag.audiotag_id == R_Audio_Has_AudioTag.audiotag_id,
                R_Audio_Has_AudioTag.audio_id == audio_id
            )).all()

            like_num = self.session.query(User.openid).filter(and_(
                User.openid == R_User_Like_Audio.user_openid,
                R_User_Like_Audio.deleted == False,
                R_User_Like_Audio.audio_id == audio_id,
                )).count()

            comment_num = self.session.query(Comment.comment_id).filter(and_(
                Comment.deleted == False,
                Comment.audio_id == audio_id
                )).count()

            isliked = bool(self.session.query(R_User_Like_Audio.user_openid).filter(and_(
                R_User_Like_Audio.user_openid == openid,
                R_User_Like_Audio.deleted == False,
                R_User_Like_Audio.audio_id == audio_id,
                )).count())

            iscollected = bool(self.session.query(Collection).filter(and_(
                Collection.deleted == False,
                R_Audio_In_Collection.deleted == False,
                Collection.user_openid == openid,
                Collection.collection_id == R_Audio_In_Collection.collection_id,
                R_Audio_In_Collection.audio_id == audio_id
            )).first())
            feeds.append({
                "user": user.toDict(),
                "audio": audio.toDict(),
                "tags": [tag.toDict() for tag in tags],
                "like_num": like_num,
                "comment_num": comment_num,
                "isliked": isliked,
                "iscollected": iscollected,
                "collections": [c.toDict() for c in collections],
            })
        
        return Status.success({
            "feeds": feeds
        })

    def postAudio(self, form):
        '''
        上传一个音频
        {
            action: 'post_audio',
            audio: audio{},
            tags: [tag{}...]
        }
        {
            err: 'ok'
        }
        '''

        openid = form["openid"]
        audio = json.loads(form["audio"])
        tags = json.loads(form["tags"])
        audioObj = Audio(**audio)
        audioObj.create()
        for tag in tags:
            tagObj = AudioTag(tag)
            tagObj.create()
            R_Audio_Has_AudioTag(audio_id=audioObj.audio_id,
                audiotag_id=tagObj.audiotag_id).create()
        
        return Status.success()
    
    def getMedal(self, form):
        '''
        获取用户的徽章
        {
            action: 'get_medal',
        }
        {
            medals: [
                medal{},
                medal{}
            ]
        }
        '''

        openid = form["openid"]
        medals = self.session.query(Medal).filter(and_(
            Medal.deleted == False,
            R_User_Has_Medal.deleted == False,
            R_User_Has_Medal.user_openid == openid,
            R_User_Has_Medal.medal_id == Medal.medal_id
        )).all()

        return Status.success({
            "medals": [m.toDict() for m in medals]
        })
