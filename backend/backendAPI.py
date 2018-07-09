from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func
from createTables import createAllTable, tables
from config import DEBUG, DEBUG_COMMUNITATION, appID, appSecret
from utils import DataFormatException, Status, Encrypt
from testbench import *
import json, requests

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
        "login": "login",
        "get_index": "getIndex",
        "like_audio": "likeAudio",
        "get_comments": "getComments",
        "post_comment": "postComment",
        "get_collection": "getCollections",
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
                form["openid"] = "openid"
                form["session_key"] = "123"
            return getattr(self, API.action2API[action])(form)
        except Exception as e:
            return Status.internalError(e)


    #############################   API   #############################

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
            if not self.session.query(User.openid).filter(User.openid == openID):
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

        User = tables["user"]
        Audio = tables["audio"]
        R_U_A = tables["R_User_Create_Audio"]

        # 不同的数据库类型有不同的随机查询方式
        if self.dbName == "sqlite":
            randfunc = func.random()
        else:
            # for mysql
            randfunc = func.rand()

        # 随机查询两个audio
        randTwoAudios = self.session.query(Audio).order_by(randfunc).limit(2).all()
        audio_ids = [audio.audio_id for audio in randTwoAudios]

        # 查询对应的user，tag，以及其他信息，组装成feed
        self.session.query(User, R_U_A)

        return Status.success({
            "feed": randTwoAudios[0].toDict(),
            "feed_next": randTwoAudios[1].toDict(),
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

        if DEBUG_COMMUNITATION:
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
        if DEBUG_COMMUNITATION:
            return Status.success({
                "comments": [
                    testComment,
                    testComment,
                    testComment,
                    testComment,
                ]
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
        if DEBUG_COMMUNITATION:
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
        if DEBUG_COMMUNITATION:
            return Status.success({
                "collections": [
                    testCollection,
                    testCollection,
                    testCollection,
                ]
            })

    def addCollection(self, form):
        '''
        觅声_收藏_增加收藏夹
        {
            action: 'add_collection_set',
            collection_name : ''
        }
        {
            err: 'ok'
        }
        '''
        if DEBUG_COMMUNITATION:
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
        if DEBUG_COMMUNITATION:
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
        if DEBUG_COMMUNITATION:
            return Status.success({
                "feed": testFeed
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
        if DEBUG_COMMUNITATION:
            return Status.success({
                "feeds":[
                    testFeed
                ]
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
        if DEBUG_COMMUNITATION:
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
        if DEBUG_COMMUNITATION:
            return Status.success({
                "medals": [
                    testMedal,
                    testMedal,
                    testMedal,
                    testMedal,
                ]
            })
