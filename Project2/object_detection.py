# coding: utf-8
import requests
import time
import hashlib
import base64
from app import OBJECT_DETECTION_APPID, OBJECT_DETECTION_API_KEY

URL = "http://tupapi.xfyun.cn/v1/currency"

APPID = OBJECT_DETECTION_APPID
API_KEY = OBJECT_DETECTION_API_KEY


def getHeader(image_name):
    curTime = str(int(time.time()))
    param = "{\"image_name\":\"" + image_name + "\"}"
    paramBase64 = base64.b64encode(param.encode('utf-8'))
    tmp = str(paramBase64, 'utf-8')

    m2 = hashlib.md5()
    m2.update((API_KEY + curTime + tmp).encode('utf-8'))
    checkSum = m2.hexdigest()

    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
    }
    return header

def getBody(filePath):
    binfile = open(filePath, 'rb')
    data = binfile.read()
    return data

def object_detect(FilePath, ImageName):
    r = requests.post(URL,data=getBody(FilePath), headers=getHeader(ImageName))
    print(r.content)
    return r.content
