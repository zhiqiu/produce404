import requests
from utils import jsonDumps, jsonLoads
from config import Config

url = "http://127.0.0.1:%d/api" % Config.PORT
debugurl = "http://127.0.0.1:%d/debugapi/" % Config.PORT

def test(params):
    print("#"*100)
    print("\naction:", params["action"])
    print("\n\nparams:\n\n", params)
    res = requests.get(url, params=params)
    jsonRes = jsonLoads(res.text)
    print("\n\nresponse:\n\n", jsonDumps(jsonRes, indent=2))
    print("\n" + "#"*100)

def debugtest(table, params):
    print("#"*100)
    print("\ntable name:", table.lower())
    print("\n\nparams:\n\n", params)
    res = requests.get(debugurl+table, params=params)
    jsonRes = jsonLoads(res.text)
    print("\n\nresponse:\n\n", jsonDumps(jsonRes, indent=2))
    print("\n" + "#"*100)

test({
    "action": "get_user_info",
    "token": "123"
})

test({
    "action": "set_user_info",
    "user": jsonDumps({
        "nickName": "张若天😂",
        "gender": 1,
        "language": "en",
        "city": "Shijiazhuang",
        "province": "Hebei",
        "country": "China",
        "avatarUrl": "https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLJ1VBQSSEkJyDiaO6JZjic7VCmnmwfZWeDGJ2Bt4zV3dT8NkB8BdpSrw9DOlgxUguWZfcHDj7hlULQ/132"
    })
})

test({
    "action": "get_user_info",
    "token": "123"
})

test({
    "action": "login",
    "code": "345"
})

test({
    "action": "get_index",
    "listentype": "like",
    "channel": "channel_name"
})

test({
    "action": "like_audio",
    "audio_id": 2
})

debugtest("r_user_like_audio",{
    "user_openid": "openid1"
})

test({
    "action": "post_comment",
    "audio_id": 2,
    "reply_to_user_openid": "",
    "text": "hahahahahahhhhhhhhhhhhh"
})

test({
    "action": "get_comments",
    "audio_id": 2
})

test({
    "action": "add_collection",
    "collection_name": "collection name"
})

test({
    "action": "get_collections"
})

test({
    "action": "add_into_collection",
    "collection_id": 3,
    "audio_id": 4
})

test({
    "action": "add_into_collection",
    "collection_id": 10,
    "audio_id": 4
})

test({
    "action": "get_collection_content",
    "collection_id": 8
})

test({
    "action": "get_collection_content",
    "collection_id": 10
})

test({
    "action": "get_explore",
})

test({
    "action": "get_explore",
    "last_audio_id": "2"
})

test({
    "action": "get_one_feed",
    "audio_id": 3
})

test({
    "action": "get_my_feed",
    "last_audio_id": 2
})

test({
    "action": "get_my_feed"
})

test({
    "action": "post_audio",
    "audio": jsonDumps({
            "url": "http://ws.stream.qqmusic.qq.com/M500001VfvsJ21xFqb.mp3?guid=ffffffff82def4af4b12b3cd9337d5e7&uin=346897220&vkey=6292F51E1E384E061FF02C31F716658E5C81F5594D561F2E88B854E81CAAB7806D5E4F103E55D33C16F3FAC506D1AB172DE8600B37E43FAD&fromtag=46",
            "name": "testaudio",
            "intro": "testintro",
            "img": "http://y.gtimg.cn/music/photo_new/T002R300x300M000003rsKF44GyaSk.jpg?max_age=2592000",
            "location": "test location",
            "duration": "10",
        }),
    "tags": jsonDumps([
        {
            "tagname": "testtag"
        }
    ])
})

test({
    "action": "get_my_feed"
})

test({
    "action": "get_medal"
})