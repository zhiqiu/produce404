from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from createTables import createAllTable, Tables, DataFormatException
from config import DEBUG, appID, appSecret
import json

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


class API():
    def __init__(self, engine):
        base = createAllTable(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
    
    allAPI = {
        "login": "login",

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
        request:
            {
                action: "login",
                code: "code"
            }
        response:
            {
                token: "token",
                first_time: false
            }
        '''
        
        '''
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

        jsCode = form["code"]

        url = "https://api.weixin.qq.com/sns/jscode2session"
        params = {
            "appid": appID,
            "secret": appSecret,
            "js_code": jsCode,
            "grant_type": "authorization_code"
        }

        try:
            return {
                "token": "I am token",
                "first_time": True
            }
            res = request.get(url, params=params)
            resJson = json.loads(res.text)["token"]
            openID = resJson["openid"]
            sessionKey = resJson["session_key"]
        except:
            pass