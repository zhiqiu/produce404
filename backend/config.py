from sqlalchemy import create_engine


DEBUG = True

# flask port
PORT = 80

# database engine. Use sqlite3 for debug
engine = create_engine('sqlite:///foo.db?check_same_thread=False', echo=DEBUG)

# app config
appID = "appID"

appSecret = "appSecret"

try:
    import localConfig
    PORT = localConfig.PORT
    engine = localConfig.engine
    appID = localConfig.appID
    appSecret = localConfig.appSecret
except:
    pass
