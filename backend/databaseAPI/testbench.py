from .defineTables import *

def makeTestDatabase(session):

    for i in range(1, 10):
        User(**{
            "openid": "openid%d" % i,
            "nickName": "张若天%d号" % i,
            "gender": 1,
            "language": "en",
            "city": "Shijiazhuang",
            "province": "Hebei",
            "country": "China",
            "avatarUrl": "https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLJ1VBQSSEkJyDiaO6JZjic7VCmnmwfZWeDGJ2Bt4zV3dT8NkB8BdpSrw9DOlgxUguWZfcHDj7hlULQ/132"
        }).create(session)

    for i in range(1, 100):
        Audio(**{
            "url": "http://ws.stream.qqmusic.qq.com/M500001VfvsJ21xFqb.mp3?guid=ffffffff82def4af4b12b3cd9337d5e7&uin=346897220&vkey=6292F51E1E384E061FF02C31F716658E5C81F5594D561F2E88B854E81CAAB7806D5E4F103E55D33C16F3FAC506D1AB172DE8600B37E43FAD&fromtag=46",
            "name": "name%d"%i,
            "intro": "intro%d"%i,
            "img": "http://y.gtimg.cn/music/photo_new/T002R300x300M000003rsKF44GyaSk.jpg?max_age=2592000",
            "location": "location%d"%i,
            "duration": i,
        }).create(session)
    
    for i in range(1, 10):
        AudioTag(**{
            "tagname": "tagname%d"%i
        }).create(session)

    for i in range(1, 10):
        Medal(**{
            "name": "name%d"%i,
            "img_url": "img_url%d"%i,
            "condition": i,
        }).create(session)
    
    for i in range(1, 9):
        Comment(**{
            "text": "text%d"%i,
            "audio_id": i,
            "user_openid": "openid%d"%i,
            "replyto": "openid%d"%(i+1) if i % 2 else "",
        }).create(session)
    
    for i in range(1, 10):
        Collection(**{
            "name": "name%d"%i,
            "user_openid": "openid%d"%i,
        }).create(session)
    
    for i in range(1, 100):
        R_User_Create_Audio(**{
            "user_openid": "openid%d"%(i % 9 + 1),
            "audio_id": i,
        }).create(session)

    for i in range(1, 10):
        R_Audio_Has_AudioTag(**{
            "audio_id": i,
            "audiotag_id": i,
        }).create(session)

    for i in range(1, 10):
        R_User_Has_Medal(**{
            "user_openid": "openid%d"%i,
            "medal_id": i,
        }).create(session)

    for i in range(1, 9):
        R_User1_Follow_User2(**{
            "user1": "openid%d"%i,
            "user2": "openid%d"%(i+1),
        }).create(session)

    for i in range(1, 10):
        R_Audio_In_Collection(**{
            "audio_id": i,
            "collection_id": i,
        }).create(session)

    for i in range(1, 10):
        R_User_Like_Audio(**{
            "user_openid": "openid%d"%i,
            "audio_id": i,
        }).create(session)

    for i in range(1, 9):
        R_User_Like_Comment(**{
            "user_openid": "openid%d"%i,
            "comment_id": i,
        }).create(session)

    for i in range(1, 100):
        Message(**{
            "user_openid": "openid%d" % (i % 9 + 1),
            "msg_src": "system" if i % 5 == 0 else "openid%d" % ((i+1) % 9 + 1),
            "action": i % 5,
            "sysmsg": "这是一条系统消息",
            "audio_id": i,
        }).create(session)

    print("All test objects created successfully.")
