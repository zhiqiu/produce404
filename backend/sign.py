# -*- coding:utf-8 -*-

from cam.auth.cam_url import CamUrl
import urllib.request
from config import Config
from flask import Blueprint

sign = Blueprint('signcos', __name__)

@sign.route('/')
def signcos():
    policy = Config.POLICY
    secret_id = Config.SECRET_ID
    secret_key = Config.SECRET_KEY
    duration = Config.DURATION_SECOND
    url_generator = CamUrl(policy, duration, secret_id, secret_key)
    
    real_url = url_generator.url()
    print(real_url)
    proxy_handler = urllib.request.ProxyHandler({'https': '10.14.87.100:8080'})
    opener = urllib.request.build_opener()
    r = opener.open(real_url)
    response = str(r.read())
    #print(response)
    return response
