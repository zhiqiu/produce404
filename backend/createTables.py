from sqlalchemy import Column, String, Integer, CHAR, Date, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


__all__ = ["createAllTable", "Tables"]


def createAllTable(engine):
    Base.metadata.create_all(engine)
    return Base


# common super class

Base = declarative_base()

class Creatable():
    def create(self, session):
        session.add(self)
        session.commit()
    
    def __str__(self):
        string = "<" + self.__class__.__name__ + "(id=" + self.id.__str__()
        for fr in self.requiredFields:
            string += "," + fr + "=" + getattr(self, fr).__str__()
        string += ")>"
        return string
    
    def toDict(self):
        returnDict = {"id": self.id}
        for fr in self.requiredFields:
            returnDict[fr] = getattr(self, fr).__str__()
        return returnDict


def commonInitClass(self, **kwargs):
    for rf in self.requiredFields:
        if rf not in kwargs:
            raise Exception("Error! \"%s\" field is required." % rf)
        setattr(self, rf, kwargs[rf])


# entity tables:

class User(Base, Creatable):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String)
    name = Column(String)
    age = Column(Integer)
    gender = Column(CHAR(1), default="U")  # M: male, F: female, U: unset
    address = Column(String)
    birthday = Column(Date)

    requiredFields = ["uuid","name","age","gender","address","birthday"]

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)


class Sound(Base, Creatable):
    __tablename__ = "sound"

    id = Column(Integer, primary_key=True, autoincrement=True)
    URI = Column(String)  # oss uri
    caption = Column(String(30))
    address = Column(String)

    requiredFields = ["URI", "caption", "address"]

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)


class SoundTag(Base, Creatable):
    __tablename__ = "soundtag"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tagname = Column(String(5))

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)

class Medal(Base, Creatable):
    __tablename__ = "medal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10))
    pictureURI = Column(String)  # oss uri
    condition = Column(Integer)

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)


class Comment(Base, Creatable):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)
    soundid = Column(Integer, ForeignKey("sound.id"))
    timestrap = Column(BigInteger)
    # user1 reply to user2, or user1 reply the sound (when user2 == user1)
    user1 = Column(Integer, ForeignKey("user.id"))
    user2 = Column(Integer, ForeignKey("user.id"))

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)

class Forward(Base, Creatable):
    __tablename__ = "forward"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey("user.id"))
    soundid = Column(Integer, ForeignKey("sound.id"))
    destination = Column(String)
    timestrap = Column(BigInteger)

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)

# relationship tables:

class R_User_Sound(Base, Creatable):
    __tablename__ = "r_user_sound"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey("user.id"))
    soundid = Column(Integer, ForeignKey("sound.id"))

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)

class R_Sound_SoundTag(Base, Creatable):
    __tablename__ = "r_sound_soundtag"

    id = Column(Integer, primary_key=True, autoincrement=True)
    soundid = Column(Integer, ForeignKey("sound.id"))
    soundtagid = Column(Integer, ForeignKey("soundtag.id"))

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)

class R_User_Medal(Base, Creatable):
    __tablename__ = "r_user_medal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey("user.id"))
    medalid = (Integer, ForeignKey("medal.id"))

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)

class R_Follow(Base, Creatable):
    __tablename__ = "r_follow"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # user1 follows user2
    user1 = Column(Integer, ForeignKey("user.id"))
    user2 = Column(Integer, ForeignKey("user.id"))

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)

class R_Favorite_Sound(Base, Creatable):
    __tablename__ = "r_favorite_sound"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey("user.id"))
    soundid = Column(Integer, ForeignKey("sound.id"))

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)

class R_Interested_Soundtag(Base, Creatable):
    __tablename__ = "r_interested_soundtag"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey("user.id"))
    soundtagid = Column(Integer, ForeignKey("soundtag.id"))

    def __init__(self, **kwargs):
        commonInitClass(self, **kwargs)

class Tables():
    User = User
    Sound = Sound
    SoundTag = SoundTag
    Medal = Medal
    Comment = Comment
    Forward = Forward
    R_User_Sound = R_User_Sound
    R_Sound_SoundTag = R_Sound_SoundTag
    R_User_Medal = R_User_Medal
    R_Follow = R_Follow
    R_Favorite_Sound = R_Favorite_Sound
    R_Interested_Soundtag = R_Interested_Soundtag



if __name__ == "__main__":
    from sqlalchemy import create_engine
    # use sqlite database to debug locally
    engine = create_engine('sqlite:///foo.db', echo=True)
    Base = createAllTable(engine)
