from sqlalchemy import create_engine

__all__ = ["DEBUG", "PORT", "engine", "appID", "appSecret"]

DEBUG = True

# debug server-client communitation
DEBUG_COMMUNITATION = True

# flask port
PORT = 2345

# database engine. Use sqlite3 for debug
engine = create_engine('sqlite:///foo.db?check_same_thread=False', echo=DEBUG)

# app config
appID = "appID"

appSecret = "appSecret"

try:
    from localConfig import *
except:
    pass


# config for app key
class Config(object):
    def __init__(self):
        pass

    COMMON_POLICY = r'''{"statement": [{"action": ["name/cos:*"],"effect": "allow","resource":"*"}],"version": "2.0"}'''


    POLICY = COMMON_POLICY
    DURATION_SECOND = 1800
    SECRET_ID = 'AKIDhHfrSwvKEwSnz1AVxJZifQzSmtpYpqiP'
    SECRET_KEY = 'd5LPHyTmtnV1CPUQBvXxCFJFzXxEMJ4i'


