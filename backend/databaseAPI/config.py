from sqlalchemy import create_engine
import os

__all__ = ["Config"]

# config for app key
class Config(object):
    def __init__(self):
        pass

    COMMON_POLICY = r'''{"statement": [{"action": ["name/cos:*"],"effect": "allow","resource":"*"}],"version": "2.0"}'''

    POLICY = COMMON_POLICY
    DURATION_SECOND = 1800
    SECRET_ID = 'AKIDhHfrSwvKEwSnz1AVxJZifQzSmtpYpqiP'
    SECRET_KEY = 'd5LPHyTmtnV1CPUQBvXxCFJFzXxEMJ4i'

    # debug switch
    DEBUG = True

    # debug server-client communitation
    DEBUG_COMMUNITATION = False

    # make test database
    DEBUG_MAKETESTDATABASE = True

    # use mysql for production environment.
    engine = create_engine("mysql+pymysql://root:create404mysql@172.16.16.7/produce404?charset=utf8mb4", pool_recycle=3600, echo=False, isolation_level="AUTOCOMMIT")
    # engine = create_engine("mysql+pymysql://dba:create404mysql@ladyrick.com/create404?charset=utf8mb4", pool_recycle=3600, echo=False, isolation_level="AUTOCOMMIT")

    # app config
    appID = "wx19f70940784cb04e"

    appSecret = "d397d9df1ed61029259668a26b5172b8"

