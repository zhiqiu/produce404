import requests
import urllib
import re
import json
import time

# document.querySelectorAll(".item-row .btn_get_url").forEach((u)=>console.log(u.getAttribute("cdnurl")))

decodeURI = urllib.parse.unquote

regex = re.compile("http.*/(.*?).mp3$")

requestURL = "http://404.ladyrick.com/debugapi/"

def getFileName(url):
    m = regex.match(decodeURI(url))
    if m:
        return m.group(1)
    else:
        raise Exception("Can't get file name.")


res = requests.get(requestURL + "audiochannel")
if json.loads(res.text)["resp"]:
    raise Exception("already exists.")


def make(urls, img, category):
    print("###############################################")
    print(category)

    time.sleep(0.1)
    res = requests.post(requestURL + "audiochannel", data={"name": category})
    print(res.text)
    channel_id = json.loads(res.text)["resp"]["channel_id"]
    img = img.replace("create404-cos-1253746840.file.myqcloud.com","cos.ladyrick.com")

    for u in urls:
        u = u.replace("create404-cos-1253746840.file.myqcloud.com","cos.ladyrick.com")
        audioname = getFileName(u)
        audio = {
            "url": u,
            "name": audioname,
            "intro": "",
            "img": img,
            "location": "",
            "duration": 9999,
        }
        print(audioname)
        time.sleep(0.1)
        res = requests.post(requestURL + "audio", data=audio)
        print(res.text)
        
        audio_id = json.loads(res.text)["resp"]["audio_id"]
        usercreateaudio = {
            "user_openid": "system",
            "audio_id": audio_id,
        }
        time.sleep(0.1)
        res = requests.post(requestURL + "r_user_create_audio", data=usercreateaudio)
        print(res.text)

        audioinaudiochannel = {
            "audio_id": audio_id,
            "channel_id": channel_id,
        }
        time.sleep(0.1)
        res = requests.post(requestURL + "r_audio_in_audiochannel", data=audioinaudiochannel)
        print(res.text)



category = "动物植物"

urls = [
"http://cos.ladyrick.com/audio/%E5%8A%A8%E7%89%A9%E6%A4%8D%E7%89%A9/Echoes%20of%20Nature%20-%20Songbirds.mp3",
"http://cos.ladyrick.com/audio/%E5%8A%A8%E7%89%A9%E6%A4%8D%E7%89%A9/%E7%99%BE%E6%85%95%E4%B8%89%E7%9F%B3%20-%20%E4%BE%97%E7%94%B0%E5%B0%8F%E5%A4%9C%E6%9B%B2.mp3",
"http://cos.ladyrick.com/audio/%E5%8A%A8%E7%89%A9%E6%A4%8D%E7%89%A9/%E9%A3%8E%E6%BD%AE%E5%94%B1%E7%89%87%20-%20%E6%98%9F%E5%A4%9C.mp3",
"http://cos.ladyrick.com/audio/%E5%8A%A8%E7%89%A9%E6%A4%8D%E7%89%A9/%E9%A3%8E%E6%BD%AE%E5%94%B1%E7%89%87%20-%20%E6%99%A8%E9%B8%9F%E4%B9%8B%E6%AD%8C%20%28%E7%BA%AF%E8%87%AA%E7%84%B6%E5%A3%B0%E9%9F%B3%29.mp3",
"http://cos.ladyrick.com/audio/%E5%8A%A8%E7%89%A9%E6%A4%8D%E7%89%A9/%E9%A3%8E%E6%BD%AE%E5%94%B1%E7%89%87%20-%20%E6%A2%A6.mp3",
]

img = "http://cos.ladyrick.com/audio/%E5%8A%A8%E7%89%A9%E6%A4%8D%E7%89%A9/animal_plant.jpg"

make(urls, img, category)

###################

category = "海浪瀑布"

urls = [
"http://cos.ladyrick.com/audio/%E6%B5%B7%E6%B5%AA%E7%80%91%E5%B8%83/Dan%20Gibson%20-%20Sweeping%20the%20Sandy%20Shore.mp3",
"http://cos.ladyrick.com/audio/%E6%B5%B7%E6%B5%AA%E7%80%91%E5%B8%83/Echoes%20of%20Nature%20-%20Low%20Tide.mp3",
"http://cos.ladyrick.com/audio/%E6%B5%B7%E6%B5%AA%E7%80%91%E5%B8%83/Echoes%20of%20Nature%20-%20Pleasant%20Beach.mp3",
"http://cos.ladyrick.com/audio/%E6%B5%B7%E6%B5%AA%E7%80%91%E5%B8%83/The%20Nature%20Sounds%20Society%20Japan%20-%20Beach%20and%20Motorbike.mp3",
"http://cos.ladyrick.com/audio/%E6%B5%B7%E6%B5%AA%E7%80%91%E5%B8%83/The%20Nature%20Sounds%20Society%20Japan%20-%20Summer%20Wave%201.mp3",
]

img = "http://cos.ladyrick.com/audio/%E6%B5%B7%E6%B5%AA%E7%80%91%E5%B8%83/seawave_waterfall.jpg"

make(urls, img, category)

###################

category = "山水林间"

urls = [
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E5%B1%B1%E6%B0%B4%E8%87%AA%E7%84%B6/Dan%20Gibson%20-%20Dawn%20by%20a%20Gentle%20Stream%20%28The%20Ultimate%20Water%20Treatment%20Experience%29%20%5BPro%5D.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E5%B1%B1%E6%B0%B4%E8%87%AA%E7%84%B6/Dan%20Gibson%20-%20The%20Natural%20World.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E5%B1%B1%E6%B0%B4%E8%87%AA%E7%84%B6/Echoes%20of%20Nature%20-%20Pebble%20Beach.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E5%B1%B1%E6%B0%B4%E8%87%AA%E7%84%B6/Echoes%20of%20Nature%20-%20Small%20Rapid.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E5%B1%B1%E6%B0%B4%E8%87%AA%E7%84%B6/Echoes%20of%20Nature%20-%20Streamside%20Songbirds.mp3",
]

img = "http://create404-cos-1253746840.file.myqcloud.com/audio/%E5%B1%B1%E6%B0%B4%E8%87%AA%E7%84%B6/muntain_water.jpg"

make(urls, img, category)

###################

category = "自然气候"

urls = [
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E8%87%AA%E7%84%B6%E6%B0%94%E5%80%99/Deep%20Sleep%20Music%20-%20Rain%20and%20Thunder.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E8%87%AA%E7%84%B6%E6%B0%94%E5%80%99/Echoes%20of%20Nature%20-%20Jamboree.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E8%87%AA%E7%84%B6%E6%B0%94%E5%80%99/Echoes%20of%20Nature%20-%20Rain%20With%20Pygmy%20Owl.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E8%87%AA%E7%84%B6%E6%B0%94%E5%80%99/The%20Nature%20Sounds%20Society%20Japan%20-%20Sayama%20Rain%203%28Demo%29%20-%20demo.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E8%87%AA%E7%84%B6%E6%B0%94%E5%80%99/%EC%9D%B4%ED%8E%99%ED%84%B0%20-%20%EB%B9%84%EC%99%80%20%EB%B2%88%EA%B0%9C.mp3",
]

img = "http://create404-cos-1253746840.file.myqcloud.com/audio/%E8%87%AA%E7%84%B6%E6%B0%94%E5%80%99/nature_weather.jpg"

make(urls, img, category)

###################

category = "机器轰鸣"

urls = [
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E6%9C%BA%E5%99%A8%E5%B7%A5%E4%BD%9C/%E5%89%AA%E8%8D%89%E6%9C%BA%E5%A3%B0%E9%9F%B3.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E6%9C%BA%E5%99%A8%E5%B7%A5%E4%BD%9C/%E5%8C%85%E6%89%8E%E6%9C%BA%E5%92%94%E5%9A%93%E5%A3%B0.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E6%9C%BA%E5%99%A8%E5%B7%A5%E4%BD%9C/%E5%8C%BB%E9%99%A2%E7%9B%91%E8%A7%86%E5%99%A8%E6%8A%A5%E8%AD%A6%E5%A3%B0.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E6%9C%BA%E5%99%A8%E5%B7%A5%E4%BD%9C/%E5%90%B8%E5%B0%98%E5%99%A8%E5%A3%B0%E9%9F%B3.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E6%9C%BA%E5%99%A8%E5%B7%A5%E4%BD%9C/%E5%A4%8D%E5%8D%B0%E6%9C%BA%E7%9A%84%E5%A3%B0%E9%9F%B3.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E6%9C%BA%E5%99%A8%E5%B7%A5%E4%BD%9C/%E6%9C%BA%E5%99%A8%E5%89%8A%E9%93%85%E7%AC%94%E9%9F%B3%E6%95%88.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E6%9C%BA%E5%99%A8%E5%B7%A5%E4%BD%9C/%E6%B6%A1%E8%BD%AE%E6%9C%BA%E7%9A%84%E5%A3%B0%E9%9F%B3.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E6%9C%BA%E5%99%A8%E5%B7%A5%E4%BD%9C/%E6%B6%B2%E5%8E%8B%E6%9C%BA%E5%90%AF%E5%8A%A8%E5%A3%B0.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E6%9C%BA%E5%99%A8%E5%B7%A5%E4%BD%9C/%E8%BE%93%E9%80%81%E6%9C%BA%E7%9A%84%E5%A3%B0%E9%9F%B3.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E6%9C%BA%E5%99%A8%E5%B7%A5%E4%BD%9C/%E9%A9%AC%E8%BE%BE%E5%A3%B0.mp3",
]

img = "http://create404-cos-1253746840.file.myqcloud.com/audio/%E6%9C%BA%E5%99%A8%E5%B7%A5%E4%BD%9C/machine.jpg"

make(urls, img, category)

###################

category = "交通工具"

urls = [
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/Atsushi%20Umebori%20-%20Boost%20Sound%20%28AE86%20Sprinter%20Trueno%20GT-APEX%20%28Early%20Type%29%20Takumi%20Fujiwara%29.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/Atsushi%20Umebori%20-%20Boost%20Sound%20%28AE86%20Sprinter%20Trueno%20GT-APEX%20%28Late%20Type%29%20Shinji%20Inui%29.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/Atsushi%20Umebori%20-%20Boost%20Sound%20%28BNR32%20Skyline%20GT-R%20Rin%20Hojo%29.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/Atsushi%20Umebori%20-%20Boost%20Sound%20%28CT9A%20Lancer%20Evolution%20VII%20GSR%20Kobayakawa%29.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/Atsushi%20Umebori%20-%20Boost%20Sound%20%28FD3S%20RX-7%20Type%20R%20Keisuke%20Takahashi%29.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/Atsushi%20Umebori%20-%20Boost%20Sound%20%28JZA80%20Supra%20RZ%20Hideo%20Minagawa%29.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/Atsushi%20Umebori%20-%20Boost%20Sound%20%28NA1%20NSX%20Go%20Hojo%29.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/Atsushi%20Umebori%20-%20Boost%20Sound%20%28NB8C%20Road%20Star%20RS%20Satoshi%20Omiya%29.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/Atsushi%20Umebori%20-%20Boost%20Sound%20%28S15%20Silvia%20Spec-R%20Hiroya%20Okuyama%29.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/Atsushi%20Umebori%20-%20Boost%20Sound%20%28Z33%20Fairlady%20Z%20Version%20S%20Ryuji%20Ikeda%29.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/Atsushi%20Umebori%20-%20Boost%20Sound%20%28ZZW30%20MR-S%20S%20Edition%20Kai%20Kogashiwa%29.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/Atsushi%20Umebori%20-%20Ignition%20~%20Exhaust%20Sound%20%28AE86%20Sprinter%20Trueno%20GT-APEX%20%28Late%20Type%29%20Shinji%20Inui%29.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/Atsushi%20Umebori%20-%20Ignition%20~%20Exhaust%20Sound%20%28BNR32%20Skyline%20GT-R%20Rin%20Hojo%29.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/Atsushi%20Umebori%20-%20Ignition%20~%20Exhaust%20Sound%20%28CT9A%20Lancer%20Evolution%20VII%20GSR%20Kobayakawa%29.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/Atsushi%20Umebori%20-%20Ignition%20~%20Exhaust%20Sound%20%28FC3S%20RX-7%20Infini%20III%20Ryosuke%20Takahashi%29.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/Atsushi%20Umebori%20-%20Ignition%20~%20Exhaust%20Sound%20%28JZA80%20Supra%20RZ%20Hideo%20Minagawa%29.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/Atsushi%20Umebori%20-%20Ignition%20~%20Exhaust%20Sound%20%28NA1%20NSX%20Go%20Hojo%29.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/Atsushi%20Umebori%20-%20Ignition%20~%20Exhaust%20Sound%20%28NB8C%20Road%20Star%20RS%20Satoshi%20Omiya%29.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/Atsushi%20Umebori%20-%20Ignition%20~%20Exhaust%20Sound%20%28S15%20Silvia%20Spec-R%20Hiroya%20Okuyama%29.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/Atsushi%20Umebori%20-%20Ignition%20~%20Exhaust%20Sound%20%28Z33%20Fairlady%20Z%20Version%20S%20Ryuji%20Ikeda%29.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/Atsushi%20Umebori%20-%20Ignition%20~%20Exhaust%20Sound%20%28ZZW30%20MR-S%20S%20Edition%20Kai%20Kogashiwa%29.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/%E6%91%A9%E6%89%98%E8%BD%A6%E5%90%AF%E5%8A%A8%E6%97%B6%E7%9A%84%E5%A3%B0%E9%9F%B3.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/%E6%B1%BD%E8%BD%A6%E5%BC%95%E6%93%8E%E5%A3%B0.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/%E7%89%B9%E6%96%AF%E6%8B%89%E7%A2%B0%E6%92%9E%E9%9F%B3%E6%95%88.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/%E8%88%B9%E8%B5%B7%E9%94%9A%E7%9A%84%E5%A3%B0%E9%9F%B3.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/%E9%A3%9E%E6%9C%BA%E5%BC%95%E6%93%8E%E5%A3%B0.mp3",
]

img = "http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/vehicle.jpg"

make(urls, img, category)

###################

category = "古典艺术"

urls = [
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BC%A0%E7%BB%9F%E4%B9%90%E5%99%A8/%E5%BA%94%E6%98%8E%20-%20%E8%B8%8F%E9%9B%AA%E5%AF%BB%E6%A2%85.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BC%A0%E7%BB%9F%E4%B9%90%E5%99%A8/%E5%BC%A0%E8%8E%89%20-%20%E5%BA%B7%E5%AE%9A%E6%83%85%E6%AD%8C.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BC%A0%E7%BB%9F%E4%B9%90%E5%99%A8/%E5%BC%A0%E9%93%81%20-%20%E9%9B%A8%E4%B8%8D%E6%B4%92%E8%8A%B1%E8%8A%B1%E4%B8%8D%E5%BC%80.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BC%A0%E7%BB%9F%E4%B9%90%E5%99%A8/%E6%9D%9C%E8%81%AA%20-%20%E6%A2%A7%E6%A1%90%E6%A0%91.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BC%A0%E7%BB%9F%E4%B9%90%E5%99%A8/%E6%9D%9C%E8%81%AA%20-%20%E7%8E%9B%E4%BE%9D%E6%8B%89.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BC%A0%E7%BB%9F%E4%B9%90%E5%99%A8/%E7%8E%8B%E4%BC%9F%20-%20%E8%92%99%E5%8F%A4%E5%B0%8F%E5%A4%9C%E6%9B%B2.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BC%A0%E7%BB%9F%E4%B9%90%E5%99%A8/%E7%BE%A4%E6%98%9F%20-%20%E6%98%A5%E6%80%9D.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BC%A0%E7%BB%9F%E4%B9%90%E5%99%A8/%E8%B5%B5%E4%B8%80%20-%20%E9%98%BF%E6%8B%89%E6%9C%A8%E6%B1%97.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BC%A0%E7%BB%9F%E4%B9%90%E5%99%A8/%E9%97%B5%E6%83%A0%E8%8A%AC%20-%20%E7%8C%AE%E8%8A%B1.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BC%A0%E7%BB%9F%E4%B9%90%E5%99%A8/%E9%9C%8D%E6%B0%B8%E5%88%9A%20-%20%E7%BE%8E%E4%B8%BD%E7%9A%84%E5%A7%91%E5%A8%98.mp3",
]

img = "http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BC%A0%E7%BB%9F%E4%B9%90%E5%99%A8/old_art.jpg"

make(urls, img, category)

###################

category = "现代乐器"

urls = [
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E7%8E%B0%E4%BB%A3%E4%B9%90%E5%99%A8/Arven%20-%20Cercle%20d%27Emeraude.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E7%8E%B0%E4%BB%A3%E4%B9%90%E5%99%A8/Bond%20-%20Pump%20It.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E7%8E%B0%E4%BB%A3%E4%B9%90%E5%99%A8/DJ%20Okawari%20-%20Luv%20Letter.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E7%8E%B0%E4%BB%A3%E4%B9%90%E5%99%A8/Edvin%20Marton%20-%20Rio%20Carneval.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E7%8E%B0%E4%BB%A3%E4%B9%90%E5%99%A8/Robert%20Mendoza%20-%20Rather%20Be.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E7%8E%B0%E4%BB%A3%E4%B9%90%E5%99%A8/Simply%20Three%20-%20Secrets.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E7%8E%B0%E4%BB%A3%E4%B9%90%E5%99%A8/Vitamin%20String%20Quartet%20-%20Alejandro.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E7%8E%B0%E4%BB%A3%E4%B9%90%E5%99%A8/Vitamin%20String%20Quartet%20-%20Poker%20Face.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E7%8E%B0%E4%BB%A3%E4%B9%90%E5%99%A8/Yo-Yo%20Ma%20-%20Libertango.mp3",
"http://create404-cos-1253746840.file.myqcloud.com/audio/%E7%8E%B0%E4%BB%A3%E4%B9%90%E5%99%A8/%E8%B4%9D%E5%A4%9A%E8%8A%AC%20-%20%E6%82%B2%E6%80%86%E5%A5%8F%E9%B8%A3%E6%9B%B2.mp3",
]

img = "http://create404-cos-1253746840.file.myqcloud.com/audio/%E7%8E%B0%E4%BB%A3%E4%B9%90%E5%99%A8/morden_instrument.jpg"

make(urls, img, category)