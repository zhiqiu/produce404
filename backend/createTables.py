from sqlalchemy import Column, String, Integer, Date, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from utils import DataFormatException
from datetime import date, datetime
import re

__all__ = ["createAllTable", "tables"]


def createAllTable(engine):
    Base.metadata.create_all(engine)
    return Base

# common super class

Base = declarative_base()

class Creatable():
    def create(self, session):
        self.create_time = datetime.utcnow()
        session.add(self)
        session.commit()

    def __str__(self):
        return json.dumps(self.toDict())
    
    def toDict(self):
        returnDict = {}
        for fr in self.outputFields:
            data = getattr(self, fr)
            if data.__class__.__name__ in ["date", "datetime"]:
                returnDict[fr] = str(data)
            else:
                returnDict[fr] = data
        return returnDict


def commonInitClass(self, **kwargs):
    missedFields = []
    for rf in self.requiredFields:
        if rf not in kwargs:
            missedFields.append(rf)
        else:
            setattr(self, rf, kwargs[rf])
    if missedFields:
        raise DataFormatException("Missing fields. (%s) are required." % (",".join(missedFields)))

dateRexp = re.compile(r"([\d]{4})-([\d]{1,2})-([\d]{1,2})")

# entity tables:

class User(Base, Creatable):
    __tablename__ = "user"

    openid = Column(String(28), primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String(1), default="U")  # M: male, F: female, U: unset
    address = Column(String)
    birthday = Column(Date)
    create_time = Column(TIMESTAMP)

    requiredFields = ["openid","name","age","gender","address","birthday"]
    outputFields = requiredFields + ["create_time"]

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)
        try:
            self.age = int(self.age)
        except:
            raise DataFormatException("age must be an integer.")
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
    __tablename__ = "audio"

    audio_id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String)  # oss url
    intro = Column(String(30))
    img = Column(String)
    location = Column(String)
    create_time = Column(TIMESTAMP)

    requiredFields = ["url", "intro", "img", "location"]
    outputFields = ["audio_id"] + requiredFields + ["create_time"]

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)


class AudioTag(Base, Creatable):
    __tablename__ = "audiotag"

    audiotag_id = Column(Integer, primary_key=True, autoincrement=True)
    tagname = Column(String(5))
    create_time = Column(TIMESTAMP)

    requiredFields = ["tagname"]
    outputFields = ["audiotag_id"] + requiredFields + ["create_time"]

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)

class Medal(Base, Creatable):
    __tablename__ = "medal"

    medal_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    img_url = Column(String)  # oss url
    condition = Column(Integer)
    create_time = Column(TIMESTAMP)

    requiredFields = ["name", "img_url", "condition"]
    outputFields = ["medal_id"] + requiredFields + ["create_time"]

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)
        try:
            self.condition = int(self.condition)
        except:
            raise DataFormatException("condition must be an integer.")


class Comment(Base, Creatable):
    __tablename__ = "comment"

    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)
    audio_id = Column(ForeignKey("audio.audio_id"))
    # user1 reply to user2, or user1 reply the sound (when user2 == user1)
    user_openid = Column(ForeignKey("user.openid"))
    replyto = Column(ForeignKey("user.openid"))
    create_time = Column(TIMESTAMP)

    requiredFields = ["text", "audio_id", "user_openid", "replyto"]
    outputFields = ["comment_id"] + requiredFields + ["create_time"]

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)


class Collection(Base, Creatable):
    __tablename__ = "collection"

    collection_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    user_openid = Column(ForeignKey("user.openid"))
    create_time = Column(TIMESTAMP)

    requiredFields = ["name", "user_openid"]
    outputFields = ["collection_set_id"] + requiredFields + ["create_time"]

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)

class Forward(Base, Creatable):
    __tablename__ = "forward"

    forward_id = Column(Integer, primary_key=True, autoincrement=True)
    user_openid = Column(ForeignKey("user.openid"))
    audio_id = Column(ForeignKey("audio.audio_id"))
    destination = Column(String)
    create_time = Column(TIMESTAMP)

    requiredFields = ["user_openid", "audio_id", "destination"]
    outputFields = ["forward_id"] + requiredFields + ["create_time"]

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)

# relationship tables:

class R_User_Create_Audio(Base, Creatable):
    __tablename__ = "r_user_create_audio"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_openid = Column(ForeignKey("user.openid"))
    audio_id = Column(ForeignKey("audio.audio_id"))
    create_time = Column(TIMESTAMP)

    requiredFields = ["user_openid", "audio_id"]
    outputFields = requiredFields + ["create_time"]

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)
        try:
            self.audio_id = int(self.audio_id)
        except:
            raise DataFormatException("audio_id must be an integer.")

class R_Audio_Has_AudioTag(Base, Creatable):
    __tablename__ = "r_audio_has_audiotag"

    id = Column(Integer, primary_key=True, autoincrement=True)
    audio_id = Column(ForeignKey("audio.audio_id"))
    audiotag_id = Column(ForeignKey("audiotag.audiotag_id"))
    create_time = Column(TIMESTAMP)

    requiredFields = ["audio_id", "audiotag_id"]
    outputFields = requiredFields + ["create_time"]

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)
        try:
            self.audio_id = int(self.audio_id)
        except:
            raise DataFormatException("audio_id must be an integer.")
        try:
            self.audiotag_id = int(self.audiotag_id)
        except:
            raise DataFormatException("audiotag_id must be an integer.")

class R_User_Has_Medal(Base, Creatable):
    __tablename__ = "r_user_has_medal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_openid = Column(ForeignKey("user.openid"))
    medal_id = Column(ForeignKey("medal.medal_id"))
    create_time = Column(TIMESTAMP)

    requiredFields = ["user_openid", "medal_id"]
    outputFields = requiredFields + ["create_time"]

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)
        try:
            self.medal_id = int(self.medal_id)
        except:
            raise DataFormatException("medal_id must be an integer.")

class R_User1_Follow_User2(Base, Creatable):
    __tablename__ = "r_user1_follow_user2"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # user1 follows user2
    user1 = Column(ForeignKey("user.openid"))
    user2 = Column(ForeignKey("user.openid"))
    create_time = Column(TIMESTAMP)

    requiredFields = ["user1", "user2"]
    outputFields = requiredFields + ["create_time"]

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)

class R_Audio_In_Collection(Base, Creatable):
    __tablename__ = "r_audio_in_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    audio_id = Column(ForeignKey("audio.audio_id"))
    collection_id = Column(ForeignKey("collection.collection_id"))
    create_time = Column(TIMESTAMP)

    requiredFields = ["audio_id", "collection_id"]
    outputFields = requiredFields + ["create_time"]

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)
        try:
            self.audio_id = int(self.audio_id)
        except:
            raise DataFormatException("audio_id must be an integer.")
        try:
            self.collection_id = int(self.collection_id)
        except:
            raise DataFormatException("collection_id must be an integer.")

class R_User_Like_Audio(Base, Creatable):
    __tablename__ = "r_user_like_audio"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_openid = Column(ForeignKey("user.openid"))
    audio_id = Column(ForeignKey("audio.audio_id"))
    create_time = Column(TIMESTAMP)

    requiredFields = ["user_openid", "audio_id"]
    outputFields = requiredFields + ["create_time"]

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)
        try:
            self.audio_id = int(self.audio_id)
        except:
            raise DataFormatException("audio_id must be an integer.")

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
}
