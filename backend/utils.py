from config import DEBUG

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

# 加密工具
class Encrypt():
    def encrypt(self, text):
        cipherText = text
        return cipherText

    def decrypt(self, cipherText):
        text = cipherText
        return text