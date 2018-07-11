from sqlalchemy import Column, String, Integer, Date, TIMESTAMP, BOOLEAN, ForeignKey
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base
from utils import DataFormatException, jsonDumps
from datetime import date, datetime
import re, json, time

__all__ = [
    "createAllTable",
    "tables",
    "User",
    "Audio",
    "AudioTag",
    "Medal",
    "Comment",
    "Collection",
    "Forward",
    "R_User_Create_Audio",
    "R_Audio_Has_AudioTag",
    "R_User_Has_Medal",
    "R_User1_Follow_User2",
    "R_Audio_In_Collection",
    "R_User_Like_Audio",
    "R_User_Like_Comment",
]

tablePrefix = "t16_"

def createAllTable(engine):
    try:
        Base.metadata.create_all(engine)
    except:
        print("Create failed. Try again in 5 seconds.")
        time.sleep(5)
        createAllTable(engine)

# common super class

Base = declarative_base()

class Creatable():
    def create(self, session):
        self.create_time = datetime.utcnow()
        session.add(self)
        try:
            session.commit()
        except:
            session.rollback()

    def merge(self, session):
        session.merge(self)
        try:
            session.commit()
        except:
            session.rollback()

    @classmethod
    def checkExist(cls, session, pkey):
        classObj = cls
        className = classObj.__name__
        primaryKey = classObj.__primaryKey__
        findResult = session.query(classObj).filter(and_(
            classObj.deleted == False,
            getattr(classObj, primaryKey) == pkey
        )).count()

        if not findResult:
            raise Exception(className + " doesn't exists.")

    def toDict(self):
        if self.__class__.__name__ == "User" and self.openid in ["system", "nobody"]:
            return {"openid": self.openid}
        returnDict = {}
        for fr in self.__allFields__:
            data = getattr(self, fr)
            if data.__class__.__name__ in ["date", "datetime"]:
                returnDict[fr] = str(data)
            else:
                returnDict[fr] = data
        if self.__class__.__name__ == "User":
            returnDict["age"] = date.today().year - self.birthday.year
        return returnDict

    def __str__(self):
        return jsonDumps(self.toDict())


    def commonInitClass(self, **kwargs):
        missedFields = []
        for rf in self.__requiredFields__:
            if rf not in kwargs:
                missedFields.append(rf)
        if missedFields:
            raise DataFormatException("Missing fields. (%s) are required." % (",".join(missedFields)))
        for f in kwargs:
            if f in self.__allFields__:
                fieldType = getattr(self.__class__, f).type
                if fieldType.__class__ == String and fieldType.length < len(kwargs[f]):
                    raise DataFormatException("Field %s's max length is %d, but get %d." % (f, fieldType.length, len(kwargs[f])))
                elif fieldType.__class__ == Integer:
                    try:
                        setattr(self, f, int(kwargs[f]))
                    except:
                        raise DataFormatException(f + " must be an integer.")
                else:
                    setattr(self, f, kwargs[f])


dateRexp = re.compile(r"([\d]{4})-([\d]{1,2})-([\d]{1,2})")

# entity tables:

class User(Base, Creatable):
    __tablename__ = tablePrefix + "user"

    openid = Column(String(28), primary_key=True)
    name = Column(String(64))
    gender = Column(String(1), default="U")  # M: male, F: female, U: unset
    img = Column(String(512))
    address = Column(String(128))
    birthday = Column(Date)
    create_time = Column(TIMESTAMP)
    deleted = Column(BOOLEAN, default=False)

    __primaryKey__ = "openid"
    __requiredFields__ = ["openid","name","gender","img","address","birthday"]
    __allFields__ = __requiredFields__ + ["create_time", "deleted"]

    def __init__(self, **kwargs):
        self.commonInitClass(**kwargs)
        if self.gender not in ["M", "F", "U"]:
            raise DataFormatException("gender must be one of M/F/U for Male/Female/Unset")
        m = dateRexp.match(self.birthday)
        if not m:
            raise DataFormatException("birthday format error: YYYY-MM-DD")
        year = int(m.group(1))
        month = int(m.group(2))
        day = int(m.group(3))
        try:
            self.birthday = date(year, month, day)
        except Exception as e:
            raise DataFormatException(e)


class Audio(Base, Creatable):
    __tablename__ = tablePrefix + "audio"

    audio_id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(512))  # oss url
    name = Column(String(64))
    intro = Column(String(32))
    img = Column(String(512))
    location = Column(String(64))
    create_time = Column(TIMESTAMP)
    deleted = Column(BOOLEAN, default=False)
    duration = Column(Integer)

    __primaryKey__ = "audio_id"
    __requiredFields__ = ["url", "name", "intro", "img", "location", "duration"]
    __allFields__ = ["audio_id"] + __requiredFields__ + ["create_time", "deleted"]

    def __init__(self, **kwargs):
        self.commonInitClass(**kwargs)


class AudioTag(Base, Creatable):
    __tablename__ = tablePrefix + "audiotag"

    audiotag_id = Column(Integer, primary_key=True, autoincrement=True)
    tagname = Column(String(16))
    create_time = Column(TIMESTAMP)
    deleted = Column(BOOLEAN, default=False)

    __primaryKey__ = "audiotag_id"
    __requiredFields__ = ["tagname"]
    __allFields__ = ["audiotag_id"] + __requiredFields__ + ["create_time", "deleted"]

    def __init__(self, **kwargs):
        self.commonInitClass(**kwargs)
        

class Medal(Base, Creatable):
    __tablename__ = tablePrefix + "medal"

    medal_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64))
    img_url = Column(String(512))  # oss url
    condition = Column(Integer)
    create_time = Column(TIMESTAMP)
    deleted = Column(BOOLEAN, default=False)

    __primaryKey__ = "medal_id"
    __requiredFields__ = ["name", "img_url", "condition"]
    __allFields__ = ["medal_id"] + __requiredFields__ + ["create_time", "deleted"]

    def __init__(self, **kwargs):
        self.commonInitClass(**kwargs)


class Comment(Base, Creatable):
    __tablename__ = tablePrefix + "comment"

    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(128))
    audio_id = Column(ForeignKey(tablePrefix + "audio.audio_id"))
    # user1 reply to user2, or user1 reply the sound (when user2 == nobody)
    user_openid = Column(ForeignKey(tablePrefix + "user.openid"))
    replyto = Column(ForeignKey(tablePrefix + "user.openid"))
    create_time = Column(TIMESTAMP)
    deleted = Column(BOOLEAN, default=False)

    __primaryKey__ = "comment_id"
    __requiredFields__ = ["text", "audio_id", "user_openid", "replyto"]
    __allFields__ = ["comment_id"] + __requiredFields__ + ["create_time", "deleted"]

    def __init__(self, **kwargs):
        if "replyto" not in kwargs or kwargs["replyto"] == "":
            kwargs["replyto"] = "nobody"
        self.commonInitClass(**kwargs)


class Collection(Base, Creatable):
    __tablename__ = tablePrefix + "collection"

    collection_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(16))
    user_openid = Column(ForeignKey(tablePrefix + "user.openid"))
    create_time = Column(TIMESTAMP)
    deleted = Column(BOOLEAN, default=False)

    __primaryKey__ = "collection_id"
    __requiredFields__ = ["name", "user_openid"]
    __allFields__ = ["collection_id"] + __requiredFields__ + ["create_time", "deleted"]

    def __init__(self, **kwargs):
        self.commonInitClass(**kwargs)


class Forward(Base, Creatable):
    __tablename__ = tablePrefix + "forward"

    forward_id = Column(Integer, primary_key=True, autoincrement=True)
    user_openid = Column(ForeignKey(tablePrefix + "user.openid"))
    audio_id = Column(ForeignKey(tablePrefix + "audio.audio_id"))
    destination = Column(String(16))
    create_time = Column(TIMESTAMP)
    deleted = Column(BOOLEAN, default=False)

    __primaryKey__ = "forward_id"
    __requiredFields__ = ["user_openid", "audio_id", "destination"]
    __allFields__ = ["forward_id"] + __requiredFields__ + ["create_time", "deleted"]

    def __init__(self, **kwargs):
        self.commonInitClass(**kwargs)

# relationship tables:

class R_User_Create_Audio(Base, Creatable):
    __tablename__ = tablePrefix + "r_user_create_audio"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_openid = Column(ForeignKey(tablePrefix + "user.openid"))
    audio_id = Column(ForeignKey(tablePrefix + "audio.audio_id"))
    create_time = Column(TIMESTAMP)
    deleted = Column(BOOLEAN, default=False)

    __primaryKey__ = "id"
    __requiredFields__ = ["user_openid", "audio_id"]
    __allFields__ = ["id"] + __requiredFields__ + ["create_time", "deleted"]

    def __init__(self, **kwargs):
        self.commonInitClass(**kwargs)


class R_Audio_Has_AudioTag(Base, Creatable):
    __tablename__ = tablePrefix + "r_audio_has_audiotag"

    id = Column(Integer, primary_key=True, autoincrement=True)
    audio_id = Column(ForeignKey(tablePrefix + "audio.audio_id"))
    audiotag_id = Column(ForeignKey(tablePrefix + "audiotag.audiotag_id"))
    create_time = Column(TIMESTAMP)
    deleted = Column(BOOLEAN, default=False)

    __primaryKey__ = "id"
    __requiredFields__ = ["audio_id", "audiotag_id"]
    __allFields__ = ["id"] + __requiredFields__ + ["create_time", "deleted"]

    def __init__(self, **kwargs):
        self.commonInitClass(**kwargs)

class R_User_Has_Medal(Base, Creatable):
    __tablename__ = tablePrefix + "r_user_has_medal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_openid = Column(ForeignKey(tablePrefix + "user.openid"))
    medal_id = Column(ForeignKey(tablePrefix + "medal.medal_id"))
    create_time = Column(TIMESTAMP)
    deleted = Column(BOOLEAN, default=False)

    __primaryKey__ = "id"
    __requiredFields__ = ["user_openid", "medal_id"]
    __allFields__ = ["id"] + __requiredFields__ + ["create_time", "deleted"]

    def __init__(self, **kwargs):
        self.commonInitClass(**kwargs)


class R_User1_Follow_User2(Base, Creatable):
    __tablename__ = tablePrefix + "r_user1_follow_user2"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # user1 follows user2
    user1 = Column(ForeignKey(tablePrefix + "user.openid"))
    user2 = Column(ForeignKey(tablePrefix + "user.openid"))
    create_time = Column(TIMESTAMP)
    deleted = Column(BOOLEAN, default=False)

    __primaryKey__ = "id"
    __requiredFields__ = ["user1", "user2"]
    __allFields__ = ["id"] + __requiredFields__ + ["create_time", "deleted"]

    def __init__(self, **kwargs):
        self.commonInitClass(**kwargs)


class R_Audio_In_Collection(Base, Creatable):
    __tablename__ = tablePrefix + "r_audio_in_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    audio_id = Column(ForeignKey(tablePrefix + "audio.audio_id"))
    collection_id = Column(ForeignKey(tablePrefix + "collection.collection_id"))
    create_time = Column(TIMESTAMP)
    deleted = Column(BOOLEAN, default=False)

    __primaryKey__ = "id"
    __requiredFields__ = ["audio_id", "collection_id"]
    __allFields__ = ["id"] + __requiredFields__ + ["create_time", "deleted"]

    def __init__(self, **kwargs):
        self.commonInitClass(**kwargs)


class R_User_Like_Audio(Base, Creatable):
    __tablename__ = tablePrefix + "r_user_like_audio"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_openid = Column(ForeignKey(tablePrefix + "user.openid"))
    audio_id = Column(ForeignKey(tablePrefix + "audio.audio_id"))
    create_time = Column(TIMESTAMP)
    deleted = Column(BOOLEAN, default=False)

    __primaryKey__ = "id"
    __requiredFields__ = ["user_openid", "audio_id"]
    __allFields__ = ["id"] + __requiredFields__ + ["create_time", "deleted"]

    def __init__(self, **kwargs):
        self.commonInitClass(**kwargs)


class R_User_Like_Comment(Base, Creatable):
    __tablename__ = tablePrefix + "r_user_like_comment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_openid = Column(ForeignKey(tablePrefix + "user.openid"))
    comment_id = Column(ForeignKey(tablePrefix + "comment.comment_id"))
    create_time = Column(TIMESTAMP)
    deleted = Column(BOOLEAN, default=False)

    __primaryKey__ = "id"
    __requiredFields__ = ["user_openid", "comment_id"]
    __allFields__ = ["id"] + __requiredFields__ + ["create_time", "deleted"]

    def __init__(self, **kwargs):
        self.commonInitClass(**kwargs)


# all tables dict
tables = {
    "user": User,
    "audio": Audio,
    "audiotag": AudioTag,
    "medal": Medal,
    "comment": Comment,
    "collection": Collection,
    "forward": Forward,
    "r_user_create_audio": R_User_Create_Audio,
    "r_audio_has_audiotag": R_Audio_Has_AudioTag,
    "r_user_has_medal": R_User_Has_Medal,
    "r_user1_follow_user2": R_User1_Follow_User2,
    "r_audio_in_collection": R_Audio_In_Collection,
    "r_user_like_audio": R_User_Like_Audio,
    "r_user_like_comment": R_User_Like_Comment,
}
