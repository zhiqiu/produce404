from sqlalchemy import create_engine

__all__ = ["DEBUG", "PORT", "engine", "appID", "appSecret"]

DEBUG = True

# debug server-client communitation
DEBUG_COMMUNITATION = True

# flask port
PORT = 80

# database engine. Use sqlite3 for debug
engine = create_engine('sqlite:///foo.db?check_same_thread=False', echo=DEBUG)

# app config
appID = "appID"

appSecret = "appSecret"

try:
    from localConfig import *
except:
    pass