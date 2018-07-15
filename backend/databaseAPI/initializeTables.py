from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
from .defineTables import Base, User, CMSUser
from .testbench import makeTestDatabase
from .config import Config

__all__ = ["initializeTables"]

def initializeTables(engine):
    createTables(engine)

    try:
        # create system users
        Session = sessionmaker(bind=engine)
        session = Session()
      
        session.add(User(**{
            "openid": "system",
            "nickName": "声小觅",
            "gender": 2,
            "language": "",
            "city": "",
            "province": "",
            "country": "",
            "avatarUrl": "http://create404-cos-1253746840.file.myqcloud.com/system_user_avatar.png",
        }))
        session.add(User(**{
            "openid": "deleted",
            "nickName": "该用户已注销",
            "gender": 0,
            "language": "",
            "city": "",
            "province": "",
            "country": "",
            "avatarUrl": "http://create404-cos-1253746840.file.myqcloud.com/deleted_user_avatar.png",
        }))
        session.add(User(**{
            "openid": "nobody",
            "nickName": "非用户",
            "gender": 0,
            "language": "",
            "city": "",
            "province": "",
            "country": "",
            "avatarUrl": "http://create404-cos-1253746840.file.myqcloud.com/nobody_user_avatar.png",
        }))

        session.add(CMSUser(**{
            "id": 1,
            "email": "admin@admin.com",
            "password": "21232f297a57a5a743894a0e4a801fc3",
        }))

        session.commit()
        if Config.DEBUG_MAKETESTDATABASE:
            makeTestDatabase(session)
    except Exception as e:
        if Config.DEBUG:
            print(e)
        session.rollback()

def createTables(engine):
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        if Config.DEBUG:
            print(e)
        print("Create failed. Try again in 5 seconds.")
        time.sleep(5)
        createTables(engine)