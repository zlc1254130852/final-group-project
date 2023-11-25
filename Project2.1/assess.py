# -*- coding:utf-8 -*-
#
#   author: iflytek
#
#   Windows + Python3.7
#
#   cffi==1.12.3
#   gevent==1.4.0
#   greenlet==0.4.15
#   pycparser==2.19
#   six==1.12.0
#   websocket==0.2.1
#   websocket-client==0.56.0

from builtins import Exception, str

import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import xml.etree.ElementTree as ET
from api_key import SPEECH_ASSESSMENT_APPID, SPEECH_ASSESSMENT_APISecret, SPEECH_ASSESSMENT_APIKey
from setting import socketio
from transform import pcm2wav

STATUS_FIRST_FRAME = 0
STATUS_CONTINUE_FRAME = 1
STATUS_LAST_FRAME = 2

SUB = "ise"
ENT = "en_vip"

CATEGORY = "read_sentence"

recv_message=[""]

file = []
text = []

@socketio.on('play2')
def play2(req):
    file.append(open("static/en/example.pcm", "wb"))
    text.append(req['text'])

@socketio.on('update2')
def update2(data):
    if not file:
        return

    if type(data)==dict:
        file_popped=file.pop()
        file_popped.close()

        file_path = r"static/en/example.pcm"
        to_path = r"static/en/example.wav"
        pcm2wav(file_path, to_path)
        message=send_assess(text[-1])
        text.pop()
        socketio.emit('reply2', {"result": " "+message, "end": 1})

    else:
        file[-1].write(data)

class Ws_Param(object):

    def __init__(self, APPID, APIKey, APISecret, AudioFile, Text):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.AudioFile = AudioFile
        self.Text = Text

        self.CommonArgs = {"app_id": self.APPID}

        self.BusinessArgs = {"category": CATEGORY, "sub": SUB, "ent": ENT, "cmd": "ssb", "auf": "audio/L16;rate=16000",
                             "aue": "raw", "text": self.Text, "ttp_skip": True, "aus": 1}


    def create_url(self):

        url = 'ws://ise-api.xfyun.cn/v2/open-ise'

        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        signature_origin = "host: " + "ise-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/open-ise " + "HTTP/1.1"

        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        v = {
            "authorization": authorization,
            "date": date,
            "host": "ise-api.xfyun.cn"
        }

        url = url + '?' + urlencode(v)

        return url

def on_message(ws, message):
    try:
        code = json.loads(message)["code"]
        sid = json.loads(message)["sid"]
        if code != 0:
            errMsg = json.loads(message)["message"]
            print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
            ws.close()

        else:
            data = json.loads(message)["data"]
            status = data["status"]
            result = data["data"]
            if (status == 2):
                xml = base64.b64decode(result)

                print(xml.decode("utf-8"))
                tree=xml.decode("utf-8")
                root=ET.fromstring(tree)

                recv_message.clear()

                chapter_result=root.find("read_sentence").find("rec_paper").find("read_chapter")

                accuracy_score=str(chapter_result.get("accuracy_score"))
                standard_score=str(chapter_result.get("standard_score"))
                fluency_score=str(chapter_result.get("fluency_score"))
                integrity_score=str(chapter_result.get("integrity_score"))
                total_score=str(chapter_result.get("total_score"))

                recv_message.append("accuracy_score: "+accuracy_score
                                    +"\nstandard_score: "+standard_score
                                    +"\nfluency_score: "+fluency_score
                                    +"\nintegrity_score: "+integrity_score
                                    +"\ntotal_score: "+total_score)
                ws.close()

    except Exception as e:
        print("receive msg,but parse exception:", e)
        ws.close()


def on_error(ws, error):
    print("### error:", error)


def on_close(ws, a, b):
    print("### closed ###")
    # print(a)
    # print(b)


def send_assess(text):

    def on_open(ws):
        def run(*args):
            frameSize = 1280
            intervel = 0.04
            status = STATUS_FIRST_FRAME

            with open(wsParam.AudioFile, "rb") as fp:
                while True:
                    buf = fp.read(frameSize)

                    if not buf:
                        status = STATUS_LAST_FRAME


                    if status == STATUS_FIRST_FRAME:
                        d = {"common": wsParam.CommonArgs,
                             "business": wsParam.BusinessArgs,
                             "data": {"status": 0}}
                        d = json.dumps(d)
                        ws.send(d)
                        status = STATUS_CONTINUE_FRAME

                    elif status == STATUS_CONTINUE_FRAME:
                        d = {"business": {"cmd": "auw", "aus": 2, "aue": "raw"},
                             "data": {"status": 1, "data": str(base64.b64encode(buf).decode())}}
                        ws.send(json.dumps(d))

                    elif status == STATUS_LAST_FRAME:
                        d = {"business": {"cmd": "auw", "aus": 4, "aue": "raw"},
                             "data": {"status": 2, "data": str(base64.b64encode(buf).decode())}}
                        ws.send(json.dumps(d))
                        time.sleep(1)
                        break

                    time.sleep(intervel)

        thread.start_new_thread(run, ())

    time1 = datetime.now()


    wsParam = Ws_Param(APPID=SPEECH_ASSESSMENT_APPID, APISecret=SPEECH_ASSESSMENT_APISecret,
                       APIKey=SPEECH_ASSESSMENT_APIKey,
                       AudioFile='static/en/example.pcm', Text=text)

    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open

    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    time2 = datetime.now()
    print(time2 - time1)
    # ws.close()
    return recv_message[0]

