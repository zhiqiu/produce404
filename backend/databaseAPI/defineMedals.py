from sqlalchemy import and_
from .defineTables import *

__all__ = ["allMedalClasses"]

allMedalClasses = []


def getUserLikeNum(session, user):
    if not hasattr(user, "likenum"):
        videolikednum = session.query(User.openid).filter(and_(
            R_User_Like_Audio.deleted == False,
            Audio.deleted == False,
            R_User_Create_Audio.deleted == False,
            User.openid == R_User_Like_Audio.user_openid,
            R_User_Like_Audio.audio_id == Audio.audio_id,
            R_User_Create_Audio.user_openid == user.openid,
            R_User_Create_Audio.audio_id == Audio.audio_id
        )).count()
        commentlikednum = session.query(User.openid).filter(and_(
            R_User_Like_Comment.deleted == False,
            Comment.deleted == False,
            Audio.deleted == False,
            R_User_Create_Audio.deleted == False,
            User.openid == R_User_Like_Comment.user_openid,
            Comment.comment_id == R_User_Like_Comment.comment_id,
            Comment.audio_id == Audio.audio_id,
            R_User_Create_Audio.user_openid == user.openid,
            R_User_Create_Audio.audio_id == Audio.audio_id
        )).count()
        user.likenum = videolikednum + commentlikednum
    return user.likenum


def getUserCommentNum(session, user):
    if not hasattr(user, "commentnum"):
        user.commentnum = session.query(Comment.comment_id).filter(and_(
            Comment.deleted == False,
            Audio.deleted == False,
            R_User_Create_Audio.deleted == False,
            Audio.audio_id == Comment.audio_id,
            R_User_Create_Audio.audio_id == Audio.audio_id,
            R_User_Create_Audio.user_openid == user.openid
        )).count()
    return user.commentnum


def medalmeta(cls, bases, attrs):
    newclass = type(cls, bases, attrs)
    allMedalClasses.append(newclass)
    return newclass

# class AllMedals(metaclass=medalmeta):


class MedalFirstLike(metaclass=medalmeta):
    # 获得首个点赞
    __medal_name__ = "获得首个点赞"
    __img_url__ = "http://cos.ladyrick.com/medal1.png"

    @classmethod
    def check(cls, user, session):
        requiredNum = 1
        likenum = getUserLikeNum(session, user)
        state = likenum >= requiredNum
        text = cls.__medal_name__ if state else "获得%d/%d个点赞" % (likenum, requiredNum)
        return state, text


class Medal30Like(metaclass=medalmeta):
    # 点赞数达到30
    __medal_name__ = "获得30个点赞"
    __img_url__ = "http://cos.ladyrick.com/medal2.png"

    @classmethod
    def check(cls, user, session):
        requiredNum = 30
        likenum = getUserLikeNum(session, user)
        state = likenum >= requiredNum
        text = cls.__medal_name__ if state else "获得%d/%d个点赞" % (likenum, requiredNum)
        return state, text


class Medal100Like(metaclass=medalmeta):
    # 点赞数达到100
    __medal_name__ = "获得100个点赞"
    __img_url__ = "http://cos.ladyrick.com/medal3.png"

    @classmethod
    def check(cls, user, session):
        requiredNum = 100
        likenum = getUserLikeNum(session, user)
        state = likenum >= requiredNum
        text = cls.__medal_name__ if state else "获得%d/%d个点赞" % (likenum, requiredNum)
        return state, text


class Medal500Like(metaclass=medalmeta):
    # 点赞数达到500
    __medal_name__ = "获得500个点赞"
    __img_url__ = "http://cos.ladyrick.com/medal4.png"

    @classmethod
    def check(cls, user, session):
        requiredNum = 500
        likenum = getUserLikeNum(session, user)
        state = likenum >= requiredNum
        text = cls.__medal_name__ if state else "获得%d/%d个点赞" % (likenum, requiredNum)
        return state, text


class MedalFirstComment(metaclass=medalmeta):
    # 获得首条评论
    __medal_name__ = "获得首条评论"
    __img_url__ = "http://cos.ladyrick.com/medal5.png"

    @classmethod
    def check(cls, user, session):
        requiredNum = 1
        commentnum = getUserCommentNum(session, user)
        state = commentnum >= requiredNum
        text = cls.__medal_name__ if state else "获得%d/%d条评论" % (commentnum, requiredNum)
        return state, text


class Medal30Comment(metaclass=medalmeta):
    # 获得30条评论
    __medal_name__ = "获得30条评论"
    __img_url__ = "http://cos.ladyrick.com/medal6.png"

    @classmethod
    def check(cls, user, session):
        requiredNum = 30
        commentnum = getUserCommentNum(session, user)
        state = commentnum >= requiredNum
        text = cls.__medal_name__ if state else "获得%d/%d条评论" % (commentnum, requiredNum)
        return state, text
