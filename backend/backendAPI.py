from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from createTables import createAllTable, Tables, DataFormatException
from config import DEBUG, appID, appSecret
import json
import requests
from Crypto.Cipher import AES
import base64
from binascii import b2a_hex, a2b_hex

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

class Pycrypto():
    def __init__(self, key):
        self.mode = AES.MODE_CBC
        self.key = (key * 16)[0:16]
        self.cryptor = AES.new(self.key, self.mode, self.key)

    #加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, text):
        #这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        print(text)
        length = 16
        textBytes = text.encode("utf-8")
        count = len(textBytes)
        add = length - (count % length)
        textBytes = textBytes + (b'\0' * add)
        print(textBytes)

        cipherBytes = self.cryptor.encrypt(textBytes)
        print(cipherBytes)
        #因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        #所以这里统一把加密后的字符串转化为16进制字符串
        cipherText = base64.b64encode(cipherBytes).decode("utf-8")
        print(cipherText)
        return cipherText
     
    #解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, cipherText):
        print(cipherText)
        cipherBytes = base64.b64decode(cipherText.encode("utf-8"))
        print(cipherBytes)
        textBytes = self.cryptor.decrypt(cipherBytes)
        print(textBytes)
        text = textBytes.rstrip(b'\0').decode("utf-8")
        print(text)
        return text

class API():
    def __init__(self, engine):
        base = createAllTable(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    allAPI = {
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
            # Fix me
            token = {"openid": openID, "session_key": sessionKey}
            return Status.success({
                "token": json.dumps(token),
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
                feeds:[
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
                feeds:[
                    "feed1"
                ]
            })
    
    def getMyFeeds(self,form):
        '''
        按用户获取feeds
        {
            action: 'get_my_feed',
        }
        {
            feed: feed{}
        }
        '''
        if DEBUG_COMMUNITATION:
            return Status.success({
                feeds:[
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
    Py = Pycrypto("ASddsaas")
    t = "asdfghjkl呵呵哒"
    e = Py.encrypt(t)
    Py.decrypt(e)