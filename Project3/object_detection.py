# coding: utf-8
from flask import Blueprint
from flask import render_template
from flask import request
import requests
import time
import hashlib
import base64
import json
from api_key import OBJECT_DETECTION_APPID, OBJECT_DETECTION_API_KEY
from excel_query import excel_find
from baidu_translation import baidu_translate
from login_check import check_login

URL = "http://tupapi.xfyun.cn/v1/currency"

APPID = OBJECT_DETECTION_APPID
API_KEY = OBJECT_DETECTION_API_KEY

object_detection_bp = Blueprint('object_detection', __name__)

@object_detection_bp.route('/upload2',methods=['GET'])
def upload2():
    user_info = check_login()  # check which user is logged in.

    if user_info:  # if there is a logged-in user
        return render_template("upload2.html", current_user=user_info.login_name)
    else:
        return render_template("upload2.html")

@object_detection_bp.route('/file2',methods=['POST'])
def save_file2():
    data = request.files

    file = data['file']

    form=request.form
    to_lang = form.get('to_lang')
    current_user=form.get('user')

    buffer_data = file.read()
    with open("static/"+"picture"+current_user, 'wb+') as f:
        f.write(buffer_data)

    result = object_detect("static/"+"picture"+current_user,"picture"+current_user)

    result2 = ""

    for i in json.loads(result.decode('utf-8'))["data"]["fileList"][0]["labels"]:
        tmp = excel_find(i)
        tmp2 = baidu_translate(tmp, to_lang)
        result2 += tmp + " " + tmp2

        result2 +="\n"

    return {"result":result2}


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
