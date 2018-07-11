from sqlalchemy import create_engine
import os

__all__ = ["DEBUG", "PORT", "engine", "appID", "appSecret"]

DEBUG = True

# debug server-client communitation
DEBUG_COMMUNITATION = True

# flask port
PORT = 2345

# database engine. Use sqlite3 for debug
curdir = os.path.abspath(os.path.dirname(__file__))
databaseFile = os.path.join(curdir, "..", "foo.db")
engine = create_engine("sqlite:///%s?check_same_thread=False" % databaseFile, echo=DEBUG)

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


