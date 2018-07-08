from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from createTables import createAllTable, Tables, DataFormatException
from config import DEBUG, appID, appSecret
import json
import requests

__all__ = ["API"]

DEBUG_COMMUNITATION = True

class Status():
    def success(resp=None):
        if resp:
            return {
                "err": "ok",
                "resp": resp
            }
        else:
            return {
                "err": "ok"
            }
    
    def notFound():
        return {
            "err": "not found"
        }
    
    def internalError(exception):
        return {
            "err": str(exception) if DEBUG else "internal error occured."
        }
    
    def dataFormatError(exception):
        return {
            "err": "DataFormatError: " + str(exception)
        }

class Encrypt():
    def encrypt(self, text):
        cipherText = text
        return cipherText

    def decrypt(self, cipherText):
        text = cipherText
        return text

class API():
    def __init__(self, engine):
        base = createAllTable(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    allAPI = {
        "login": "login",
        "get_index": "getIndex",
        "like_audio": "likeAudio",
        "get_comments": "getComments",
        "post_comment": "postComment",
        "get_collection_set_name": "getCollectionSetName",
        "add_collection_set": "addCollectionSet",
        "add_collection": "addCollection",
        "get_explore": "getExplore",
        "get_one_feed": "getOneFeed",
        "get_my_feed": "getMyFeeds",
        "post_audio": "postAudio",
        "get_medal": "getMedal",
    }

    def commonGetAPI(self, tableName, **kwargs):
        try:
            if not hasattr(Tables, tableName):
                return Status.internalError("Table %s doesn't exists." % tableName)

            tableClass = getattr(Tables, tableName)

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
            if not hasattr(Tables, tableName):
                return Status.internalError("Table %s doesn't exists." % tableName)

            tableClass = getattr(Tables, tableName)

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
                encryptor = Encrypt()
                origialText = encryptor.decrypt(form["token"])
                tokenObject = json.loads(originalText)
                form["openid"] = tokenObject["openid"]
                form["sessionKey"] = tokenObject["session_key"]
            return getattr(self, API.allAPI[action])(form)
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

            return Status.success({
                "token": token,
                "first_time": True
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
            audio: audio{},
            audio_next: audio{}
        }
        // 上一首前端记录
        '''

        if DEBUG_COMMUNITATION:
            return Status.success({
                "audio": "audio",
                "audio_next": "audio_next"
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
                    "comment1",
                    "comment2"
                ]
            })
    
    def postComment(self, form):
        '''
        觅声_发表评论
        {
            action: 'post_comment',
            audio_id: '',
            text:''
        }
        {
            err:'ok'
        }
        '''
        if DEBUG_COMMUNITATION:
            return Status.success()
    
    def getCollectionSetName(self, form):
        '''
        觅声_收藏_显示所有收藏夹
        {
            action: 'get_collection_set_name'
        }
        {
            collection_set: [
                {
                    collection_id: '',
                    collection_name: ''
                }
            ]
        }
        '''
        if DEBUG_COMMUNITATION:
            return Status.success({
                "collection_set": [
                    "collection1"
                ]
            })

    def addCollectionSet(self, form):
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

    def addCollection(self, form):
        '''
        觅声_收藏_增加收藏
        {
            action: 'add_collection',
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
                    "feed1"
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
                "feeds":[
                    "feed1"
                ]
            })
    
    def getMyFeeds(self,form):
        '''
        按用户获取feeds
        {
            action: 'get_my_feed',
            last_audio_id: ''
        }
        {
            feed: [feed{}]
        }
        '''
        if DEBUG_COMMUNITATION:
            return Status.success({
                "feeds":[
                    "feed1"
                ]
            })

    def postAudio(self, form):
        '''
        上传一个音频
        {
            action: 'post_audio',
            feed{}
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
            err:'ok',
            medals: [
                medal{
                },
                medal{
                }
            ]
        }
        '''
        if DEBUG_COMMUNITATION:
            return Status.success({
                "medals": [
                    "medal"
                ]
            })



if __name__ == "__main__":
    for f in dir(API):
        print(getattr(API, f).__doc__)
    # Py = Pycrypto("ASddsaas")
    # t = "asdfghjkl呵呵哒"
    # e = Py.encrypt(t)
    # Py.decrypt(e)