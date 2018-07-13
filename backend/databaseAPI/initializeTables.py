from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
from .defineTables import Base, User
from .testbench import makeTestDatabase
from .config import Config

__all__ = ["initializeTables"]

def initializeTables(engine):
    createTables(engine)

    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        # create system users
        for sysuser in User.__systemUser__:
            session.add(User(**{
                "openid": sysuser,
                "nickName": sysuser,
                "gender": 1,
                "language": "zh-cn",
                "city": "Beijing",
                "province": "Beijing",
                "country": "China",
                "avatarUrl": "none",
            }))
        session.commit()
        if Config.DEBUG:
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