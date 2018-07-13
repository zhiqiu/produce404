from sqlalchemy import Column, String, Integer, TIMESTAMP, BOOLEAN, ForeignKey
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from .utils import DataFormatException, jsonDumps

__all__ = [
    "Base",
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
    "Message",
]

tablePrefix = "t40_"

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
            if data.__class__.__name__ in ["datetime"]:
                returnDict[fr] = str(data)
            else:
                returnDict[fr] = data
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


# entity tables:

class User(Base, Creatable):
    __tablename__ = tablePrefix + "user"

    openid = Column(String(28), primary_key=True)
    nickName = Column(String(64))
    gender = Column(Integer, default=1)  # Male: 1, Female: 0
    language = Column(String(32), default="zh-cn")
    city = Column(String(64))
    province = Column(String(64))
    country = Column(String(64))
    avatarUrl = Column(String(512))
    create_time = Column(TIMESTAMP)
    deleted = Column(BOOLEAN, default=False)

    __primaryKey__ = "openid"
    __requiredFields__ = ["openid","nickName","gender","language","city","province","country","avatarUrl"]
    __allFields__ = __requiredFields__ + ["create_time", "deleted"]

    __systemUser__ = ["system", "nobody", "deleted"]

    def __init__(self, **kwargs):
        self.commonInitClass(**kwargs)
        if self.gender not in [0, 1]:
            raise DataFormatException("gender must be 1 or 0 for Male/Female")
    
    def toDict(self):
        returnDict = {}
        returnDict["openid"] = self.openid
        returnDict["name"] = self.nickName
        returnDict["gender"] = ["F", "M"][self.gender]
        returnDict["img"] = self.avatarUrl
        returnDict["address"] = "%s, %s" % (self.city, self.province)
        returnDict["create_time"] = str(self.create_time)
        returnDict["deleted"] = self.deleted
        return returnDict


class Audio(Base, Creatable):
    __tablename__ = tablePrefix + "audio"

    audio_id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(512))  # oss url
    name = Column(String(64))
    intro = Column(String(32))
    img = Column(String(512))
    location = Column(String(64))
    create_time = Column(TIMESTAMP)
    reviewed = Column(BOOLEAN, default=False)
    deleted = Column(BOOLEAN, default=False)
    duration = Column(Integer)

    __primaryKey__ = "audio_id"
    __requiredFields__ = ["url", "name", "intro", "img", "location", "duration"]
    __allFields__ = ["audio_id"] + __requiredFields__ + ["create_time", "deleted", "reviewed"]

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


class Message(Base, Creatable):
    __tablename__ = tablePrefix + "message"
    __actionDict__ = {
        "system": 0,
        "like audio": 1,
        "post comment": 2,
        "follow": 3,
        "reply comment": 4,
    }

    msg_id = Column(Integer, primary_key=True, autoincrement=True)
    user_openid = Column(ForeignKey(tablePrefix + "user.openid"))
    msg_src = Column(ForeignKey(tablePrefix + "user.openid"))
    action = Column(Integer)
    sysmsg = Column(String(64), default="")
    audio_id = Column(ForeignKey(tablePrefix + "audio.audio_id"))
    isread = Column(BOOLEAN, default=False)
    create_time = Column(TIMESTAMP)
    deleted = Column(BOOLEAN, default=False)

    __primaryKey__ = ["msg_id"]
    __requiredFields__ = ["user_openid","msg_src","sysmsg","action","audio_id"]
    __allFields__ = ["msg_id"] + __requiredFields__ + ["isread","create_time", "deleted"]

    def __init__(self, **kwargs):
        if "action" not in kwargs or kwargs["action"] not in self.__actionDict__.values():
            raise DataFormatException("action is required. " + jsonDumps(self.__actionDict__))
        self.commonInitClass(**kwargs)
    
    def getTextFormat(self):
        return {
            0: self.sysmsg,
            1: "{}点赞了你发布的声音{}",
            2: "{}评论了你发布的声音{}",
            3: "{}关注了你",
            4: "{}回复了你在声音{}下的评论",
        }[self.action]


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
    "message": Message,
}
