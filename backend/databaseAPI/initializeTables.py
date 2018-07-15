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
        Session = sessionmaker(bind=engine)
        session = Session()
        # create system users
        for sysuser in User.__systemUser__:
            session.add(User(**{
                "openid": sysuser,
                "nickName": sysuser,
                "gender": 0,
                "language": "",
                "city": "",
                "province": "",
                "country": "",
                "avatarUrl": "",
            }))

        session.add(CMSUser(**{
            "id": 1,
            "email": "admin@admin.com",
            "password": "21232f297a57a5a743894a0e4a801fc3",
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