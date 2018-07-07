from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from createTables import createAllTable, Tables

class StatusCode():
    SUCCESS = 0
    NOT_FOUND = -1
    INTERNAL_ERROR = -2

class NotFound():
    def toDict():
        return {}

class API():
    def __init__(self, engine):
        base = createAllTable(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def getUser(self, id):
        try:
            user = self.session.query(Tables.User).filter_by(id=id).first()
        except Exception as e:
            return {"status": StatusCode.INTERNAL_ERROR, "error": str(e)}
        else:
            if user:
                return {"status": StatusCode.SUCCESS, "content": user.toDict()}
            else:
                return {"status": StatusCode.NOT_FOUND, "error": "Not found."}

    def addUser(self, **kwargs):
        try:
            newUser = Tables.User(**kwargs)
            newUser.create(self.session)
        except Exception as e:
            return {"status": StatusCode.INTERNAL_ERROR, "error": str(e)}
        else:
            return {"status": StatusCode.SUCCESS}
