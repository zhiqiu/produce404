from sqlalchemy import and_
from .defineTables import *

__all__ = ["allMedalClasses"]

allMedalClasses = []

def medalmeta(cls, bases, attrs):
    newclass = type(cls, bases, attrs)
    allMedalClasses.append(newclass)
    return newclass

# class AllMedals(metaclass=medalmeta):

class Medal1(metaclass=medalmeta):
    # 点赞数达到1
    __medal_name__ = "获得首个点赞"
    __text__ = "获得%d/1个点赞"
    __img_url__ = "http://cos.ladyrick.com/medal1.png"

    @classmethod
    def check(cls, user, session):
        requiredNum = 1
        if not hasattr(user, "likenum"):
            user.likenum = session.query(User.openid).filter(and_(
                R_User_Like_Audio.deleted == False,
                User.openid == R_User_Like_Audio.user_openid,
                R_User_Like_Audio.audio_id == Audio.audio_id,
                R_User_Create_Audio.user_openid == user.openid,
                R_User_Create_Audio.audio_id == Audio.audio_id
            )).count()
        state = user.likenum >= requiredNum
        text = cls.__medal_name__ if state else cls.__text__%user.likenum
        return state, text


class Medal2(metaclass=medalmeta):
    # 点赞数达到30
    __medal_name__ = "获得30个点赞"
    __text__ = "获得%d/30个点赞"
    __img_url__ = "http://cos.ladyrick.com/medal2.png"

    @classmethod
    def check(cls, user, session):
        requiredNum = 30
        if not hasattr(user, "likenum"):
            user.likenum = session.query(User.openid).filter(and_(
                R_User_Like_Audio.deleted == False,
                User.openid == R_User_Like_Audio.user_openid,
                R_User_Like_Audio.audio_id == Audio.audio_id,
                R_User_Create_Audio.user_openid == user.openid,
                R_User_Create_Audio.audio_id == Audio.audio_id
            )).count()
        state = user.likenum >= requiredNum
        text = cls.__medal_name__ if state else cls.__text__%user.likenum
        return state, text


class Medal3(metaclass=medalmeta):
    # 点赞数达到100
    __medal_name__ = "获得100个点赞"
    __text__ = "获得%d/100个点赞"
    __img_url__ = "http://cos.ladyrick.com/medal3.png"

    @classmethod
    def check(cls, user, session):
        requiredNum = 100
        if not hasattr(user, "likenum"):
            user.likenum = session.query(User.openid).filter(and_(
                R_User_Like_Audio.deleted == False,
                User.openid == R_User_Like_Audio.user_openid,
                R_User_Like_Audio.audio_id == Audio.audio_id,
                R_User_Create_Audio.user_openid == user.openid,
                R_User_Create_Audio.audio_id == Audio.audio_id
            )).count()
        state = user.likenum >= requiredNum
        text = cls.__medal_name__ if state else cls.__text__%user.likenum
        return state, text


class Medal4(metaclass=medalmeta):
    # 点赞数达到500
    __medal_name__ = "获得500个点赞"
    __text__ = "获得%d/500个点赞"
    __img_url__ = "http://cos.ladyrick.com/medal3.png"

    @classmethod
    def check(cls, user, session):
        requiredNum = 500
        if not hasattr(user, "likenum"):
            user.likenum = session.query(User.openid).filter(and_(
                R_User_Like_Audio.deleted == False,
                User.openid == R_User_Like_Audio.user_openid,
                R_User_Like_Audio.audio_id == Audio.audio_id,
                R_User_Create_Audio.user_openid == user.openid,
                R_User_Create_Audio.audio_id == Audio.audio_id
            )).count()
        state = user.likenum >= requiredNum
        text = cls.__medal_name__ if state else cls.__text__%user.likenum
        return state, text