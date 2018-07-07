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
                if hasattr(tableClass, field):
                    return {"status": StatusCode.INTERNAL_ERROR, "error": "Invalid field name: %s." % field}

            filterResult = self.session.query(tableClass)
            for field in kwargs:
                filterResult.filter(getattr(tableClass,field)==kwargs[field])
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
                if hasattr(tableClass, field):
                    return {"status": StatusCode.INTERNAL_ERROR, "error": "Invalid field name: %s." % field}

            newContent = tableClass(**kwargs)
            newContent.create(self.session)
        except DataFormatException as e:
            return {"status": StatusCode.INTERNAL_ERROR, "error": str(e)}
        except Exception as e:
            return {"status": StatusCode.INTERNAL_ERROR, "error": str(e) if DEBUG else "Internal error occured."}
        else:
            return {"status": StatusCode.SUCCESS}

''' wasted code
#########################################################################

    def getUser(self, uuid):
        return self.commonGetAPI(self, Tables.User, "uuid", uuid, getOne=True)

    def addUser(self, **kwargs):
        return self.commonAddAPI(self, Tables.User, **kwargs)

#########################################################################

    def getSound(self, id):
        return self.commonGetAPI(self, Tables.Sound, "id", id, getOne=True)

    def addSound(self, **kwargs):
        return self.commonAddAPI(self, Tables.Sound, **kwargs)

#########################################################################

    def getSoundTag(self, id):
        return self.commonGetAPI(self, Tables.SoundTag, "id", id, getOne=True)
    
    def addSoundTag(self, **kwargs):
        return self.commonAddAPI(self, Tables.SoundTag, **kwargs)

#########################################################################

    def getMedal(self, id):
        return self.commonGetAPI(self, Tables.Medal, "id", id, getOne=True)
    
    def addMedal(self, **kwargs):
        return self.commonAddAPI(self, Tables.Medal, **kwargs)

#########################################################################

    def getComment(self, id):
        return self.commonGetAPI(self, Tables.Comment, "id", id, getOne=True)
    
    def addComment(self, **kwargs):
        return self.commonAddAPI(self, Tables.Comment, **kwargs)

#########################################################################

    def getForward(self, id):
        return self.commonGetAPI(self, Tables.Forward, "id", id, getOne=True)
    
    def addForward(self, **kwargs):
        return self.commonAddAPI(self, Tables.Forward, **kwargs)
    
#########################################################################

    def get_R_User_Sound_by_User(self, useruuid):
        return self.commonGetAPI(self, Tables.R_User_Sound, "useruuid", useruuid, getOne=False)
    
    def get_R_User_Sound_by_Sound(self, useruuid):
        return self.commonGetAPI(self, Tables.R_User_Sound, "soundid", soundid, getOne=False)

    def set_R_User_Sound(self, **kwargs):
        return self.commonAddAPI(self, Tables.Forward, **kwargs)

#########################################################################

    def get_R_Sound_SoundTag_by_Sound(self, soundid):
        return self.commonGetAPI(self, Tables.R_Sound_SoundTag, "soundid", soundid, getOne=False)

    def get_R_Sound_SoundTag_by_SoundTag(self, soundtagid):
        return self.commonGetAPI(self, Tables.R_Sound_SoundTag, "soundtagid", soundtagid, getOne=False)

    def set_R_Sound_SoundTag(self, **kwargs):
        return self.commonAddAPI(self, Tables.R_Sound_SoundTag, **kwargs)

#########################################################################

    def get_R_User_Medal_by_User(self, useruuid):
        return self.commonGetAPI(self, Tables.R_User_Medal, "useruuid", useruuid, getOne=False)

    def get_R_User_Medal_by_Medal(self, medalid):
        return self.commonGetAPI(self, Tables.R_User_Medal, "medalid", medalid, getOne=False)

    def set_R_User_Medal(self, **kwargs):
        return self.commonAddAPI(self, Tables.R_User_Medal, **kwargs)

'''