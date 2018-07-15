from sqlalchemy import and_, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func
import urllib.request
import requests
from .defineTables import *
from .initializeTables import initializeTables
from .config import Config
from .utils import DataFormatException, Status, Encrypt, jsonDumps, jsonLoads
from cam.auth.cam_url import CamUrl
from .defineMedals import allMedalClasses
import os
import math

__all__ = ["API"]

class API():
    def __init__(self, engine):
        self.dbName = engine.name
        initializeTables(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.initRecommandSystem()

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
        "get_msg": "getMessage",
        "read_msg": "readMsg"
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
            return Status.success([c.toDict() for c in content])
        except Exception as e:
            return Status.internalError(e)

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
            primaryKey = getattr(newContent, tableClass.__primaryKey__)
            return Status.success({tableClass.__primaryKey__: primaryKey})
        except Exception as e:
            return Status.internalError(e)    

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
            if action not in API.action2API:
                return Status.internalError("invalid action: " + action)
            if Config.DEBUG_COMMUNITATION:
                form["openid"] = "openid1"
                form["session_key"] = "session_key"
            elif action not in ["login", "signcos"]:
                try:
                    encryptor = Encrypt(Config.appSecret)
                    originalText = encryptor.decrypt(form["token"])
                    tokenObject = jsonLoads(originalText)
                    form["openid"] = tokenObject["openid"]
                    form["sessionKey"] = tokenObject["session_key"]
                except Exception as e:
                    return Status.internalError(e, "invalid token.")
            return getattr(self, API.action2API[action])(form)
        except Exception as e:
            try:
                self.session.rollback()
            except Exception as e:
                return Status.internalError(e)
            return Status.internalError(e)

    def initRecommandSystem(self):
        '''
        Audio Vector:
        {
            audio_id: [1,2,1,3,4,2,1,3,] # length == len(recTags)
        }

        User Vector:
        {
            user_id: [3,1,2,4,1,2,3,1,] # length == len(recTags)
        }
        '''
        self.audioVec = {}
        self.userVec = {}
        curdir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(curdir, "audioVector.json"),"r", encoding="utf-8") as f:
            jsonObj = jsonLoads(f.read())

        recommandTags = jsonObj["recommandTags"]
        tagsNum = len(recommandTags)

        for k, v in jsonObj["audioHasTags"].items():
            self.audioVec[int(k)] = [0] * tagsNum
            sumsquare = math.sqrt(len(v))
            for i in v:
                self.audioVec[int(k)][i] = 1/sumsquare


        for i in range(10):
            # 查询点赞用户
            for audio_id in self.audioVec:
                users = [t[0] for t in self.session.query(User.openid).filter(and_(
                    R_User_Like_Audio.audio_id == audio_id,
                    R_User_Like_Audio.deleted == False
                )).all()]
                print(users)

                for user in users:
                    self.userVec[user] = [0] * tagsNum
                    likedVideos = []



        print(self.audioVec)
        
        # openids = self.session.query(User.openid).all()



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
            action: 'get_user_info
        }
        {
            user: user{}
        }
        '''
        openid = form["openid"]
        user = self.session.query(User).filter(and_(
            User.deleted == False,
            User.openid == openid
        )).first()

        unread_msg_num = self.session.query(Message.msg_id).filter(and_(
            Message.user_openid == openid,
            Message.isread == False,
            Message.deleted == False
        )).count()

        if user:
            return Status.success({
                "user": user.toDict(),
                "unread_msg_num": unread_msg_num
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
            "token": "iamtoken",
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
            openid = resJson["openid"]
            sessionKey = resJson["session_key"]
        except Exception as e:
            return Status.internalError(e, "invalid code. response: " + res.text)

        # 加密 openid 和 session_key 获得token
        encryptor = Encrypt(Config.appSecret)
        token = {"openid": openid, "session_key": sessionKey}
        token = encryptor.encrypt(jsonDumps(token))

        # 查询数据库，检测是否首次登陆
        firstTime = False
        if not self.session.query(User.openid).filter(User.openid == openid).count():
            firstTime = True

        return Status.success({
            "token": token,
            # "first_time": firstTime
            "first_time": True
        })

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

        feedlen = len(feeds)

        return Status.success({
            "feed": feeds[0] if feedlen > 0 else "",
            "feed_next": feeds[1] if feedlen > 1 else "",
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

        msg_src = self.session.query(R_User_Create_Audio.user_openid).filter(and_(
            R_User_Create_Audio.audio_id == audio_id
        )).first()[0]
        print(msg_src)
        # 为audio创建者发送一条提醒消息
        Message(
            user_openid=msg_src,
            msg_src=openid,
            action=Message.__actionDict__["like audio"],
            sysmsg="点赞事件",
            audio_id=audio_id,
        ).create(self.session)

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
        if "reply_to_user_openid" in form:
            replyto = form["reply_to_user_openid"]

        Audio.checkExist(self.session, audio_id)
        
        if replyto:
            User.checkExist(self.session, replyto)

        Comment(audio_id=audio_id,
                user_openid=openid,
                replyto=replyto,
                text=form["text"]
                ).create(self.session)


        msg_src = self.session.query(R_User_Create_Audio.user_openid).filter(and_(
            R_User_Create_Audio.audio_id == audio_id
        )).first()[0]

        # 为audio创建者发送一条提醒消息
        Message(
            user_openid=msg_src,
            msg_src=openid,
            action=Message.__actionDict__["post comment"],
            sysmsg="",
            audio_id=audio_id,
        ).create(self.session)

        # 如果是回复别人，则为被回复者也发送一条提醒消息
        if replyto and replyto not in User.__systemUser__:
            Message(
                user_openid=replyto,
                msg_src=openid,
                sysmsg="",
                action=Message.__actionDict__["post comment"],
                audio_id=audio_id,
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

        self.session.commit()

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
        name = form["collection_name"].strip()
        if not name:
            return Status.internalError("Collection name must not be empty.")
        if self.session.query(Collection.collection_id).filter(and_(
            Collection.deleted == False,
            Collection.user_openid == openid,
            Collection.name == name
        )).count():
            return Status.internalError("Collection already exists.")

        Collection(user_openid=openid,name=name).create(self.session)

        return Status.success()

    def deleteCollection(self, form):
        '''
        觅声_收藏_删除收藏夹
        {
            action: 'delete_collection',
            collection_id: ''
        }
        {
            err: 'ok'
        }
        '''

        openid = form["openid"]
        collection_id = form["collection_id"]
        collection = self.session.query(Collection.collection_id).filter(and_(
            Collection.deleted == False,
            Collection.user_openid == openid,
            Collection.collection_id == collection_id
        )).first()
        if not collection:
            raise Exception("It's not your collection.")
        if collection.name == Collection.__defaultCollection__:
            raise Exception("It's not allowed to delete default collection.")
        collection.deleted = True
        collection.merge(self.session)
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
            Collection.deleted == False,
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
                raise DataFormatException("last_audio_id must be an integer or empty.")

        findAudios = self.session.query(User, Audio).filter(and_(
            User.deleted == False,
            Audio.deleted == False,
            R_User_Create_Audio.deleted == False,
            User.openid == R_User_Create_Audio.user_openid,
            R_User_Create_Audio.audio_id == Audio.audio_id,
        ))

        if last_audio_id:
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
                raise DataFormatException("last_audio_id must be an integer or empty.")
        findAudios = self.session.query(User, Audio).filter(and_(
            User.openid == openid,
            Audio.deleted == False,
            R_User_Create_Audio.deleted == False,
            User.openid == R_User_Create_Audio.user_openid,
            R_User_Create_Audio.audio_id == Audio.audio_id,
        ))

        if last_audio_id:
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

        user = self.session.query(User).filter(User.openid == form["openid"]).first()

        medals = []
        for m in allMedalClasses:
            name = m.__medal_name__
            img_url = m.__img_url__
            achieved, text = m.check(user, self.session)
            medal = {
                "name": name,
                "img_url": img_url,
                "text": text,
                "achieved": achieved
            }
            medals.append(medal)

        return Status.success({
            "medals": medals
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
        openid = form["openid"]
        userObj = jsonLoads(form["user"])
        userObj["openid"] = openid
        user = User(**userObj)
        # 检查有没有默认收藏集。如果没有，则添加一个默认收藏集
        if not self.session.query(Collection.collection_id).filter(and_(
            Collection.deleted == False,
            Collection.name == Collection.__defaultCollection__,
            Collection.user_openid == openid
        )).count():
            Collection(user_openid=openid, name=Collection.__defaultCollection__).create(self.session)
        user.merge(self.session)

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

        # 数据库中必定已存在记录，所以直接修改deleted列标记已删除即可。
        like.deleted = True
        like.merge(self.session)

        return Status.success()

    def getMessage(self, form):
        '''
        获取用户所有系统消息
        {
            action: 'get_msg',
            last_msg_id: ''
        }

        {
            msgs: [msg{}]
        }
        '''
        openid = form["openid"]
        last_msg_id = ""
        if "last_msg_id" in form:
            last_msg_id = form["last_msg_id"]
            try:
                if last_msg_id:
                    last_msg_id = int(last_msg_id)
            except:
                raise DataFormatException("last_msg_id must be an integer or empty.")

        findMessages = self.session.query(User, Message, Audio.name, Audio.audio_id).filter(and_(
            Audio.audio_id == Message.audio_id,
            User.openid == Message.msg_src,
            or_(Message.user_openid == openid,
            Message.action == Message.__actionDict__["broadcast"])
        ))

        if last_msg_id:
            findMessages = findMessages.filter(Message.msg_id < last_msg_id)

        # 每次显示20条
        findMessages = findMessages.order_by(Message.msg_id.desc()).limit(20).all()

        msgs = []
        mad = Message.__actionDict__
        for user, msg, audioName, audio_id in findMessages:
            msg_ = {
                "msg_id": msg.msg_id,
                "user": user.toDict(),
                "text": msg.getTextFormat().format(user.nickName, audioName),
                "isread": msg.isread,
                "deleted": msg.deleted,
                "audio_id": audio_id if msg.action in [mad["like audio"], mad["post comment"], mad["reply comment"]] else -1
            }
            msgs.append(msg_)

        return Status.success({
            "msgs": msgs
        })
    
    def readMsg(self, form):
        '''
        消息标记为已读
        {
            action: 'read_msg',
            msg_id: ''
        }
        {
            err: 'ok'
        }
        '''
        openid = form["openid"]
        msg_id = form["msg_id"]
        msg = self.session.query(Message).filter(and_(
            Message.msg_id == msg_id,
            Message.user_openid == openid
        )).first()

        if msg:
            msg.isread = True
            msg.merge(self.session)
            return Status.success()
        else:
            return Status.internalError("It's not your msg or msg doesn't exists.")
