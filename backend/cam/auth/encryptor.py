# -*- coding:utf-8 -*-
import hashlib
import hmac
from cam.auth.tools import Tools
from urllib import parse
import string
import base64
import urllib

class Encryptor(object):

    def __init__(self, secret_key):
        self.__secret_key = secret_key

    def encrypt(self, method, path, key_values):
        #print(key_values)
        #print(self.__secret_key)
        #print(type(self.__secret_key))
        #key_values = sorted(key_values.iteritems(), key=lambda d: d[0])
        #source = urllib.urlencode(key_values)
        source = Tools.flat_params(key_values)
        source = method + path + '?' + source
        #print(source)
        #print(type(source))
        sign = hmac.new(self.__secret_key.encode('utf-8'), source.encode('utf-8'), hashlib.sha1).digest()
        sign_ = base64.b64encode(sign).rstrip()
        return parse.quote(sign_)






