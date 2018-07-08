from sqlalchemy import create_engine

try:
    import localConfig
except:

    DEBUG = True

    # flask port
    PORT = 80

    # database engine. Use sqlite3 for debug
    engine = create_engine('sqlite:///foo.db?check_same_thread=False', echo=DEBUG)

    # app config
    appID = "appID"

    appSecret = "appSecret"
