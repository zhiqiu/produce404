from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func
from createTables import *
from config import Config
from utils import DataFormatException, Status, Encrypt, jsonDumps, jsonLoads
from testbench import makeTestDatabase
import requests
from cam.auth.cam_url import CamUrl
import urllib.request


__all__ = ["API"]


class API():
    def __init__(self, engine):
        self.dbName = engine.name
        createAllTable(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        try:
            # create system users: system, nobody
            for sysuser in ["system", "nobody"]:
                self.session.add(User(**{
                    "openid": sysuser,
                    "nickName": sysuser,
                    "gender": 1,
                    "language": "zh-cn",
                    "city": "Beijing",
                    "province": "Beijing",
                    "country": "China",
                    "avatarUrl": "none",
                }))
            self.session.commit()
            if Config.DEBUG:
                makeTestDatabase(self.session)
        except Exception as e:
            if Config.DEBUG:
                print(e)
            self.session.rollback()

    action2API = {
        "signcos": "signcos",
        "get_user_info": "getUserInfo",
        "set_user_info": "setUserInfo",
        "login": "login",
        "get_index": "getIndex",
        "like_audio": "likeAudio",
        "get_comments": "getComments",
        "post_comment": "postComment",
        "get_collections": "getCollections",
        "get_collection_content": "getCollectionContent",
        "add_collection": "addCollection",
        "add_into_collection": "addIntoCollection",
        "get_explore": "getExplore",
        "get_one_feed": "getOneFeed",
        "get_my_feed": "getMyFeeds",
        "post_audio": "postAudio",
        "get_medal": "getMedal",
        "dislike_audio": "dislikeAudio",
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
    

    def packFeed(self, openid, user, audio):
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

        return {
            "user": user.toDict(),
            "audio": audio.toDict(),
            "tags": [tag.toDict() for tag in tags],
            "like_num": like_num,
            "comment_num": comment_num,
            "isliked": isliked,
            "iscollected": iscollected,
        }

    def postCallAPI(self, form):
        if not form:
            return Status.internalError("Missing form data")
        try:
            action = form["action"]
            if Config.DEBUG_COMMUNITATION:
                form["openid"] = "openid1"
                form["session_key"] = "session_key"
            elif action != "login":
                try:
                    encryptor = Encrypt()
                    originalText = encryptor.decrypt(form["token"])
                    print(originalText)
                    tokenObject = jsonLoads(originalText)
                    form["openid"] = tokenObject["openid"]
                    form["sessionKey"] = tokenObject["session_key"]
                except Exception as e:
                    raise Exception("invalid token")
            return getattr(self, API.action2API[action])(form)
        except Exception as e:
            try:
                self.session.rollback()
            except Exception as e:
                return Status.internalError(e)
            return Status.internalError(e)


    #############################   API   #############################

    def signcos(self, form):
        '''
        签名服务API
        {
            action: 'signcos'
        }
        '''
        policy = Config.POLICY
        secret_id = Config.SECRET_ID
        secret_key = Config.SECRET_KEY
        duration = Config.DURATION_SECOND
        url_generator = CamUrl(policy, duration, secret_id, secret_key)
        real_url = url_generator.url()
        print(real_url)
        proxy_handler = urllib.request.ProxyHandler({'https': '10.14.87.100:8080'})
        opener = urllib.request.build_opener()
        r = opener.open(real_url)
        response = r.read()
        return jsonLoads(response.decode("utf-8"))

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
            return Status.success({
                "user": user.toDict()
                })
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

        if Config.DEBUG_COMMUNITATION:
            return Status.success({
                "token": "Iamtoken.",
                "first_time": True
            })

        jsCode = form["code"]

        url = "https://api.weixin.qq.com/sns/jscode2session"
        params = {
            "appid": Config.appID,
            "secret": Config.appSecret,
            "js_code": jsCode,
            "grant_type": "authorization_code"
        }

        try:
            res = requests.get(url, params=params)
            resJson = jsonLoads(res.text)
            openID = resJson["openid"]
            sessionKey = resJson["session_key"]

            # 加密 openid 和 session_key 获得token
            encryptor = Encrypt()
            token = {"openid": openID, "session_key": sessionKey}
            print("111111111111111111111111111")
            print(token)
            token = encryptor.encrypt(jsonDumps(token))

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

        print(randTwoAudios)
        # 查询对应的user，tag，以及其他信息，组装成feed
        openid = form["openid"]
        feeds = [self.packFeed(openid, user, audio) for user, audio in randTwoAudios]

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
        like.merge(self.session)

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


            reply_to_openid = com["replyto"]
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
        replyto = ""
        if "reply_to_openid" in form:
            replyto = form["reply_to_user_openid"]

        Audio.checkExist(self.session, audio_id)
        
        if replyto:
            User.checkExist(self.session, replyto)

        Comment(audio_id=audio_id,
                user_openid=openid,
                replyto=replyto,
                text=form["text"]
                ).create(self.session)
        
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

    def getCollectionContent(self, form):
        '''
        觅声_收藏_显示收藏夹内容
        {
            action: 'get_collection_content',
            collection_id: id
        }
        {
            feeds: [
                feed{}...
            ]
        }
        '''
        openid = form["openid"]
        collection_id = form["collection_id"]
        Collection.checkExist(self.session, collection_id)

        if not self.session.query(Collection.collection_id).filter(and_(
            Collection.user_openid == openid,
            Collection.collection_id == collection_id
        )).first():
            raise Exception("It's not your collection.")

        findAudio = self.session.query(User, Audio).filter(and_(
            User.deleted == False,
            Audio.deleted == False,
            R_User_Create_Audio.deleted == False,
            R_Audio_In_Collection.deleted == False,
            User.openid == R_User_Create_Audio.user_openid,
            R_User_Create_Audio.audio_id == Audio.audio_id,
            Audio.audio_id == R_Audio_In_Collection.audio_id,
            R_Audio_In_Collection.collection_id == collection_id
        )).all()

        feeds = [self.packFeed(openid, user, audio) for user, audio in findAudio]
        return Status.success({
            "feeds": feeds
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
        if self.session.query(Collection.collection_id).filter(and_(
            Collection.deleted == False,
            Collection.user_openid == openid,
            Collection.name == name
        )).count():
            return Status.internalError("Collection already exists.")

        Collection(user_openid=openid,name=name).create(self.session)

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

        Audio.checkExist(self.session, audio_id)
        Collection.checkExist(self.session, collection_id)

        R_Audio_In_Collection(audio_id=audio_id, collection_id=collection_id).create(self.session)

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
        openid = form["openid"]
        last_audio_id = ""
        if "last_audio_id" in form:
            last_audio_id = form["last_audio_id"]
            try:
                if last_audio_id:
                    last_audio_id = int(last_audio_id)
            except:
                raise DataFormatException("last_audio_id must be an integer or empty string")

        findAudios = self.session.query(User, Audio).filter(and_(
            User.openid != openid,
            User.deleted == False,
            Audio.deleted == False,
            R_User_Create_Audio.deleted == False,
            User.openid == R_User_Create_Audio.user_openid,
            R_User_Create_Audio.audio_id == Audio.audio_id,
        ))

        if last_audio_id != "":
            findAudios = findAudios.filter(Audio.audio_id < last_audio_id)

        # 每次显示10条
        findAudios = findAudios.order_by(Audio.audio_id.desc()).limit(10).all()

        feeds = [self.packFeed(openid, user, audio) for user, audio in findAudios]
        
        return Status.success({
            "feeds": feeds
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
            R_User_Create_Audio.audio_id == Audio.audio_id,
            Audio.audio_id == audio_id
        )).first()

        feed = self.packFeed(openid, user, audio)

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
        last_audio_id = ""
        if "last_audio_id" in form:
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
            findAudios = findAudios.filter(Audio.audio_id < last_audio_id)

        # 每次显示10条
        findAudios = findAudios.order_by(Audio.audio_id.desc()).limit(10).all()

        feeds = [self.packFeed(openid, user, audio) for user, audio in findAudios]
        
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
        audio = jsonLoads(form["audio"])
        tags = jsonLoads(form["tags"])
        audioObj = Audio(**audio)
        audioObj.create(self.session)
        R_User_Create_Audio(user_openid=openid, audio_id=audioObj.audio_id).create(self.session)
        for tag in tags:
            tagObj = AudioTag(**tag)
            tagObj.create(self.session)
            R_Audio_Has_AudioTag(audio_id=audioObj.audio_id,
                audiotag_id=tagObj.audiotag_id).create(self.session)

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

    def setUserInfo(self, form):
        '''
        设置用户信息
        {
            "action": "set_user_info",
            "user": user{}
        }
        {
            "err": "ok"
        }
        '''

        print(form)
        openid = form["openid"]
        user = jsonLoads(form["user"])
        user["openid"] = openid
        User(**user).merge(self.session)

        return Status.success()
    
    def dislikeAudio(self, form):
        '''
        取消赞：
        {
            action: 'dislike_audio',
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

        # 数据库中必定已存在记录，所以直接修改deleted列即可。
        like.deleted = False
        like.merge(self.session)

        return Status.success()