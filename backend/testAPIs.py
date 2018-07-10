import requests
import json

url = "http://127.0.0.1:24135/api"
debugurl = "http://127.0.0.1:24135/debugapi/"

def test(params):
    print("#"*100)
    print("\naction:", params["action"])
    print("\n\nparams:\n\n", params)
    res = requests.get(url, params=params)
    jsonRes = json.loads(res.text)
    print("\n\nresponse:\n\n", json.dumps(jsonRes, indent=2))
    print("\n" + "#"*100)

def debugtest(table, params):
    print("#"*100)
    print("\ntable name:", table.lower())
    print("\n\nparams:\n\n", params)
    res = requests.get(debugurl+table, params=params)
    jsonRes = json.loads(res.text)
    print("\n\nresponse:\n\n", json.dumps(jsonRes, indent=2))
    print("\n" + "#"*100)

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
    "action": "get_comments",
    "audio_id": 2
})