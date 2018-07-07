from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from createTables import createAllTable, Tables
from config import DEBUG

__all__ = ["StatusCode", "API"]

class StatusCode():
    SUCCESS = "success"
    NOT_FOUND = "not found"
    INTERNAL_ERROR = "internal error"


class API():
    def __init__(self, engine):
        base = createAllTable(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def getUser(self, uuid):
        try:
            user = self.session.query(Tables.User).filter_by(uuid=uuid).first()
        except Exception as e:
            return {"status": StatusCode.INTERNAL_ERROR, "error": str(e) if DEBUG else "Internal error occured."}
        else:
            if user:
                return {"status": StatusCode.SUCCESS, "content": user.toDict()}
            else:
                return {"status": StatusCode.NOT_FOUND, "error": "Not found."}

    def addUser(self, **kwargs):
        print(kwargs)
        try:
            newUser = Tables.User(**kwargs)
            newUser.create(self.session)
        except Exception as e:
            return {"status": StatusCode.INTERNAL_ERROR, "error": str(e) if DEBUG else "Internal error occured."}
        else:
            return {"status": StatusCode.SUCCESS}
