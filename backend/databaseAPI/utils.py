from .config import Config
import platform
import json

__all__ = ["DataFormatException", "Status", "Encrypt", "jsonDumps", "jsonLoads"]

# 自定义的jsonDumps函数
def jsonDumps(data, **kwargs):
    return json.dumps(data, ensure_ascii=False, separators=(',', ':'), **kwargs)

def jsonLoads(string, **kwargs):
    return json.loads(string, encoding="utf-8", **kwargs)

# 自定义数据格式错误Exception
class DataFormatException(Exception):
    pass


# 用于生成返回值的类
class Status():
    def success(*args):
        if len(args):
            return {
                "err": "ok",
                "resp": args[0]
            }
        else:
            return {
                "err": "ok"
            }

    def notFound():
        return {
            "err": "not found"
        }

    def internalError(*args):
        if len(args) > 1:
            exception = args[0]
            errormsg = args[1]
        elif isinstance(args[0], Exception):
            exception = args[0]
            errormsg = ""
        else:
            exception = ""
            errormsg = args[0]

        errormsg = errormsg or "internal error occured."

        if Config.DEBUG or isinstance(exception, DataFormatException):
            return {
                "err": "%s %s" % (errormsg, str(exception))
            }
        else:
            return {
                "err": errormsg
            }


if platform.system() == "Windows" and Config.DEBUG:
    class PlatformEncrypt():
        # in order to keep the same call format.
        def __init__(self, key):
            pass
        def encrypt(self, text):
            return text
        def decrypt(self, cipherText):
            return cipherText
else:
    from Crypto.Cipher import AES
    import base64
    # 加密工具: AES-CBC-128
    class PlatformEncrypt():
        def __init__(self, key):
            self.mode = AES.MODE_CBC
            self.key = (key * 16)[0:16]

        # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
        def encrypt(self, text):
            # 这里密钥key 长度必须为16(AES-128),24(AES-192)或32(AES-256)Bytes长度.目前AES-128足够用
            length = 16
            textBytes = text.encode("utf-8")
            count = len(textBytes)
            if count % length:
                add = length - (count % length)
                textBytes = textBytes + (b'\0' * add)

            cipherBytes = AES.new(self.key, self.mode, self.key).encrypt(textBytes)
            # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
            # 所以这里统一把加密后的字符串转化为16进制字符串
            cipherText = base64.b64encode(cipherBytes).decode("utf-8")
            cipherText = cipherText.replace("+","-").replace("/","_")
            return cipherText

        # 解密后，去掉补足的空格用strip() 去掉
        def decrypt(self, cipherText):
            cipherText = cipherText.replace("_","/").replace("-","+")
            cipherBytes = base64.b64decode(cipherText.encode("utf-8"))
            textBytes = AES.new(self.key, self.mode, self.key).decrypt(cipherBytes)
            text = textBytes.rstrip(b'\0').decode("utf-8")
            return text

Encrypt = PlatformEncrypt