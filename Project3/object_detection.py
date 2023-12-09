# coding: utf-8
from flask import Blueprint
from flask import render_template
from flask import request
import base64
import json
from api_key import OBJECT_DETECTION_APPID, OBJECT_DETECTION_API_KEY
from baidu_translation import baidu_translate
from login_check import check_login
from object_detection_2 import obj_detection

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

    base64_data = base64.b64encode(file.read()).decode()

    result=obj_detection(base64_data)

    result2=[]

    counter=0
    for i in json.loads(result)["Labels"]:
        if counter==0:
            result2.append(baidu_translate(i["Name"], target_lang='en',from_lang="zh"))
            counter += 1
        else:
            result2.append("\n" + baidu_translate(i["Name"], target_lang='en', from_lang="zh"))

        result2.append(baidu_translate(i["Name"], target_lang=to_lang, from_lang="zh"))

    return {"result": result2}
