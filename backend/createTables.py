from sqlalchemy import Column, String, Integer, CHAR, BigInteger, Date, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, datetime
import re

__all__ = ["createAllTable", "Tables", "DataFormatException"]


def createAllTable(engine):
    Base.metadata.create_all(engine)
    return Base

class DataFormatException(Exception):
    pass

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
        for fr in self.outputFields:
            returnDict[fr] = getattr(self, fr).__str__()
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
    gender = Column(CHAR(1), default="U")  # M: male, F: female, U: unset
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
            raise DataFormatException("Age must be an integer.")
        if self.gender not in ["M", "F", "U"]:
            raise DataFormatException("Gender must be one of M/F/U for Male/Female/Unset")
        m = dateRexp.match(self.birthday)
        if not m:
            raise DataFormatException("Date format error.")
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
    name = Column(String(10))
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
            raise DataFormatException("Condition must be an integer.")


class Comment(Base, Creatable):
    __tablename__ = "comment"

    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)
    audio_id = Column(Integer, ForeignKey("audio.audio_id"))
    # user1 reply to user2, or user1 reply the sound (when user2 == user1)
    user_openid = Column(Integer, ForeignKey("user.openid"))
    replyto = Column(Integer, ForeignKey("user.openid"))
    create_time = Column(TIMESTAMP)

    requiredFields = ["text", "audio_id", "user_openid", "replyto"]
    outputFields = ["comment_id"] + requiredFields + ["create_time"]

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)


class Forward(Base, Creatable):
    __tablename__ = "forward"

    forward_id = Column(Integer, primary_key=True, autoincrement=True)
    user_openid = Column(Integer, ForeignKey("user.openid"))
    audio_id = Column(Integer, ForeignKey("audio.audio_id"))
    destination = Column(String)
    create_time = Column(TIMESTAMP)

    requiredFields = ["user_openid", "audio_id", "destination"]
    outputFields = ["forward_id"] + requiredFields + ["create_time"]

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)
        try:
            self.timestrap = int(self.timestrap)
        except:
            raise DataFormatException("Timestrap must be an integer.")

# relationship tables:

class R_User_Audio(Base, Creatable):
    __tablename__ = "r_user_audio"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_openid = Column(Integer, ForeignKey("user.openid"))
    audio_id = Column(Integer, ForeignKey("audio.audio_id"))
    create_time = Column(TIMESTAMP)

    requiredFields = ["user_openid", "audio_id"]
    outputFields = requiredFields + ["create_time"]

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)

class R_Audio_AudioTag(Base, Creatable):
    __tablename__ = "r_audio_audiotag"

    id = Column(Integer, primary_key=True, autoincrement=True)
    audio_id = Column(Integer, ForeignKey("audio.audio_id"))
    audiotag_id = Column(Integer, ForeignKey("audiotag.audiotag_id"))
    create_time = Column(TIMESTAMP)

    requiredFields = ["audio_id", "audiotag_id"]
    outputFields = requiredFields + ["create_time"]

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)

class R_User_Medal(Base, Creatable):
    __tablename__ = "r_user_medal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_openid = Column(Integer, ForeignKey("user.openid"))
    medal_id = (Integer, ForeignKey("medal.medal_id"))
    create_time = Column(TIMESTAMP)

    requiredFields = ["user_openid", "medal_id"]
    outputFields = requiredFields + ["create_time"]

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)

class R_Follow(Base, Creatable):
    __tablename__ = "r_follow"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # user1 follows user2
    user1 = Column(Integer, ForeignKey("user.openid"))
    user2 = Column(Integer, ForeignKey("user.openid"))
    create_time = Column(TIMESTAMP)

    requiredFields = ["user1", "user2"]
    outputFields = requiredFields + ["create_time"]

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)

class R_Favorite_Audio(Base, Creatable):
    __tablename__ = "r_favorite_audio"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_openid = Column(Integer, ForeignKey("user.openid"))
    audio_id = Column(Integer, ForeignKey("audio.audio_id"))
    create_time = Column(TIMESTAMP)

    requiredFields = ["user_openid", "audio_id"]
    outputFields = requiredFields + ["create_time"]

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)

class R_Interested_AudioTag(Base, Creatable):
    __tablename__ = "r_interested_audiotag"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_openid = Column(Integer, ForeignKey("user.openid"))
    audio_id = Column(Integer, ForeignKey("audio.audio_id"))
    create_time = Column(TIMESTAMP)

    requiredFields = ["user_openid", "audio_id"]
    outputFields = requiredFields + ["create_time"]

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)

Tables = {
    "User": User,
    "Audio": Audio,
    "AudioTag": AudioTag,
    "Medal": Medal,
    "Comment": Comment,
    "Forward": Forward,
    "R_User_Audio": R_User_Audio,
    "R_Audio_AudioTag": R_Audio_AudioTag,
    "R_User_Medal": R_User_Medal,
    "R_Follow": R_Follow,
    "R_Favorite_Audio": R_Favorite_Audio,
    "R_Interested_AudioTag": R_Interested_AudioTag,
}
