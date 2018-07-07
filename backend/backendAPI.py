from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from createTables import createAllTable, Tables, DataFormatException
from config import DEBUG

__all__ = ["StatusCode", "API"]

class StatusCode():
    SUCCESS = "success"
    NOT_FOUND = "not found"
    INTERNAL_ERROR = "internal error"

def commonGetAPI(self, table, filterName, filterValue, getOne=True):
    try:
        kwargs = {filterName: filterValue}
        filterResult = self.session.query(table).filter_by(**kwargs)
        if getOne:
            content = filterResult.first()
        else:
            content = filterResult.all()
    except Exception as e:
        return {"status": StatusCode.INTERNAL_ERROR, "error": str(e) if DEBUG else "Internal error occured."}
    else:
        if not content:
            return {"status": StatusCode.NOT_FOUND, "error": "Not found."}
        if getOne:
            return {"status": StatusCode.SUCCESS, "content": content.toDict()}
        else:
            return {"status": StatusCode.SUCCESS, "content": [c.toDict() for c in content]}

def commonAddAPI(self, table, **kwargs):
    try:
        newContent = table(**kwargs)
        newContent.create(self.session)
    except DataFormatException as e:
        return {"status": StatusCode.INTERNAL_ERROR, "error": str(e)}
    except Exception as e:
        return {"status": StatusCode.INTERNAL_ERROR, "error": str(e) if DEBUG else "Internal error occured."}
    else:
        return {"status": StatusCode.SUCCESS}


class API():
    def __init__(self, engine):
        base = createAllTable(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def getUser(self, uuid):
        return commonGetAPI(self, Tables.User, "uuid", uuid, getOne=True)

    def addUser(self, **kwargs):
        return commonAddAPI(self, Tables.User, **kwargs)

    def getSound(self, id):
        return commonGetAPI(self, Tables.Sound, "id", id, getOne=True)

    def addSound(self, **kwargs):
        return commonAddAPI(self, Tables.Sound, **kwargs)