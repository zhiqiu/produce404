from config import DEBUG
from Crypto.Cipher import AES
import base64

# 自定义数据格式错误Exception
class DataFormatException(Exception):
    pass

# 用于生成返回值的类
class Status():
    def success(resp=None):
        if resp:
            return {
                "err": "ok",
                "resp": resp
            }
        else:
            return {
                "err": "ok"
            }
    
    def notFound():
        return {
            "err": "not found"
        }
    
    def internalError(exception):
        return {
            "err": str(exception) if DEBUG else "internal error occured."
        }
    
    def dataFormatError(exception):
        return {
            "err": "DataFormatError: " + str(exception)
        }

# 加密工具: AES-CBC-128
class Encrypt():
    def __init__(self, key):
        self.mode = AES.MODE_CBC
        self.key = (key * 16)[0:16]

    #加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, text):
        #这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        length = 16
        textBytes = text.encode("utf-8")
        count = len(textBytes)
        if count % length:
            add = length - (count % length)
            textBytes = textBytes + (b'\0' * add)

        cipherBytes = AES.new(self.key, self.mode, self.key).encrypt(textBytes)
        #因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        #所以这里统一把加密后的字符串转化为16进制字符串
        cipherText = base64.b64encode(cipherBytes).decode("utf-8")
        return cipherText
     
    #解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, cipherText):
        cipherBytes = base64.b64decode(cipherText.encode("utf-8"))
        textBytes = AES.new(self.key, self.mode, self.key).decrypt(cipherBytes)
        text = textBytes.rstrip(b'\0').decode("utf-8")
        return text