from createTables import tables, createAllTable

testUser = {
    "openid": "o6_bmjrPTlm6_2sgVt7hMZOPfL2M",
    "name": "user name",
    "age": "18",
    "gender": "F",
    "address": "你心里",
    "birthday": "2000-05-20",
    "create_time": "2018-07-09 05:36:33.294922"
}

testAudio = {
    "audio_id": "1",
    "url": "http://audio.com",
    "img": "http://audio.com",
    "intro": "for test",
    "location": "广东 深圳",
    "create_time": "2018-07-09 05:36:33.294922"
}

testComment = {
    "comment_id": "1",
    "audio_id": "2",
    "user": testUser,
	"text": "我要评论",
	"date": "date format",
	"like_num": 100,
	"isliked": True,
	"replyto": testUser,
}

testTag = {
    "audiotag_id": "2",
    "text": "心情"
}

testMedal = {
    "medai_id": "3",
	"name": "10万点赞徽章",
	"img_url": "http://image.com",
	"text": "10万点赞徽章",
	"achieved": True
}

testFeed = {
    "user": testUser,
    "audio": testAudio,
    "tags": [testTag] * 10,
    "like_num": 1000,
    "comment_num": 233,
    "isliked": True,
    "iscollected": True
}

testCollection = {
    "collection_id": "4",
    "name": "收藏夹",
    "creator_openid": '1'
}


def makeTestDatabase(session):
    for i in range(10):
        tables["user"](**{
            "openid": "openid%d"%i,
            "name": "name%d"%i,
            "age": i,
            "gender": "M" if i % 2 else "F",
            "address": "address%d"%i,
            "birthday": "1999-9-%d"%(i+1),
        }).create(session)
    
    for i in range(10):
        tables["audio"](**{
            "url": "http://ws.stream.qqmusic.qq.com/M500001VfvsJ21xFqb.mp3?guid=ffffffff82def4af4b12b3cd9337d5e7&uin=346897220&vkey=6292F51E1E384E061FF02C31F716658E5C81F5594D561F2E88B854E81CAAB7806D5E4F103E55D33C16F3FAC506D1AB172DE8600B37E43FAD&fromtag=46",
            "intro": "intro%d"%i,
            "img": "http://y.gtimg.cn/music/photo_new/T002R300x300M000003rsKF44GyaSk.jpg?max_age=2592000",
            "location": "location%d"%i,
        }).create(session)
    
    for i in range(10):
        tables["audiotag"](**{
            "tagname": "tagname%d"%i
        }).create(session)

    for i in range(10):
        tables["medal"](**{
            "name": "name%d"%i,
            "img_url": "img_url%d"%i,
            "condition": i,
        }).create(session)
    
    for i in range(9):
        tables["comment"](**{
            "text": "text%d"%i,
            "audio_id": i,
            "user_openid": "openid%d"%i,
            "replyto": "openid%d"%(i+1),
        }).create(session)
    
    for i in range(10):
        tables["collection"](**{
            "name": "name%d"%i,
            "user_openid": "openid%d"%i,
        }).create(session)
    
    for i in range(10):
        tables["r_user_create_audio"](**{
            "user_openid": "openid%d"%i,
            "audio_id": i,
        }).create(session)

    for i in range(10):
        tables["r_audio_has_audiotag"](**{
            "audio_id": i,
            "audiotag_id": i,
        }).create(session)

    for i in range(10):
        tables["r_user_has_medal"](**{
            "user_openid": "openid%d"%i,
            "medal_id": i,
        }).create(session)

    for i in range(9):
        tables["r_user1_follow_user2"](**{
            "user1": "openid%d"%i,
            "user2": "openid%d"%(i+1),
        }).create(session)

    for i in range(10):
        tables["r_audio_in_collection"](**{
            "audio_id": i,
            "collection_id": i,
        }).create(session)

    for i in range(10):
        tables["r_user_like_audio"](**{
            "user_openid": "openid%d"%i,
            "audio_id": i,
        }).create(session)
