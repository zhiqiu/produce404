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


class API():
    def __init__(self, engine):
        base = createAllTable(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def commonGetAPI(self, tableName, **kwargs):
        try:
            if not hasattr(Tables, tableName):
                return {"status": StatusCode.INTERNAL_ERROR, "error": "Table %s doesn't exists." % tableName}

            tableClass = getattr(Tables, tableName)

            for field in kwargs:
                if not hasattr(tableClass, field):
                    return {"status": StatusCode.INTERNAL_ERROR, "error": "Invalid field name: %s." % field}

            filterResult = self.session.query(tableClass).filter_by(**kwargs)
            content = filterResult.all()
        except Exception as e:
            return {"status": StatusCode.INTERNAL_ERROR, "error": str(e) if DEBUG else "Internal error occured."}
        else:
            if not content:
                return {"status": StatusCode.NOT_FOUND, "error": "Not found."}
            return {"status": StatusCode.SUCCESS, "content": [c.toDict() for c in content]}

    def commonAddAPI(self, tableName, **kwargs):
        try:
            if not hasattr(Tables, tableName):
                return {"status": StatusCode.INTERNAL_ERROR, "error": "Table %s doesn't exists." % tableName}

            tableClass = getattr(Tables, tableName)

            for field in kwargs:
                if not hasattr(tableClass, field):
                    return {"status": StatusCode.INTERNAL_ERROR, "error": "Invalid field name: %s." % field}

            newContent = tableClass(**kwargs)
            newContent.create(self.session)
        except DataFormatException as e:
            return {"status": StatusCode.INTERNAL_ERROR, "error": "DataFormatError: " + str(e)}
        except Exception as e:
            return {"status": StatusCode.INTERNAL_ERROR, "error": str(e) if DEBUG else "Internal error occured."}
        else:
            return {"status": StatusCode.SUCCESS}
