from sqlalchemy import create_engine
import os

__all__ = ["DEBUG", "PORT", "engine", "appID", "appSecret", "DEBUG_COMMUNITATION", "Config"]

DEBUG = True

# debug server-client communitation
DEBUG_COMMUNITATION = True

# flask port
PORT = 24135

# database engine. Use sqlite3 for debug
curdir = os.path.abspath(os.path.dirname(__file__))
databaseFile = os.path.join(curdir, "..", "foo.db")
# engine = create_engine("sqlite:///%s?check_same_thread=False" % databaseFile, echo=False)

# use mysql for production environment.
# engine = create_engine("mysql+pymysql://root:create404mysql@172.16.16.7/create404?charset=utf8mb4", pool_recycle=3600, echo=False)
engine = create_engine("mysql+pymysql://dba:create404mysql@ladyrick.com/create404?charset=utf8", pool_recycle=3600, echo=False)

# app config
appID = "appID"

appSecret = "appSecret"



# config for app key
class Config(object):
    def __init__(self):
        pass

    COMMON_POLICY = r'''{"statement": [{"action": ["name/cos:*"],"effect": "allow","resource":"*"}],"version": "2.0"}'''


    POLICY = COMMON_POLICY
    DURATION_SECOND = 1800
    SECRET_ID = 'AKIDhHfrSwvKEwSnz1AVxJZifQzSmtpYpqiP'
    SECRET_KEY = 'd5LPHyTmtnV1CPUQBvXxCFJFzXxEMJ4i'


