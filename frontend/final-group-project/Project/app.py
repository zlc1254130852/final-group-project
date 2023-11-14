# -*- encoding:utf-8 -*-
# main.py
from flask import Flask, redirect, render_template
from flask import request, Response
# from flask import json
import openai
import hashlib
import hmac
import base64
from socket import *
import json, time, threading
from websocket import create_connection
import websocket
from urllib.parse import quote
import logging
# import importlib,sys
import requests
import random
from hashlib import md5
from flask_socketio import SocketIO

openai.api_key = ""

app_id = ""
api_key = ""
# Set your own appid/appkey.
appid = ''
appkey = ''

# For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
from_lang = 'en'
to_lang =  'zh'

endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path

# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

class Client():
    def __init__(self):
        self.end_tag = "{\"end\": true}"

    def send(self, data):
        self.ws.send(data)
        time.sleep(0.04)

    def stop_send(self):
        self.ws.send(bytes(self.end_tag.encode('utf-8')))
        print("send end tag success")

    def recv(self):
        try:
            while self.ws.connected:
                result = str(self.ws.recv())
                if len(result) == 0:
                    print("receive result end")
                    self.ws.close()
                    print("connection closed")
                    break
                result_dict = json.loads(result)

                if result_dict["action"] == "started":
                    print("handshake success, result: " + result)
                    socketio.emit('reply', {"result": " \n----------------\nconnected\n----------------\n", "end": 1})

                if result_dict["action"] == "result":
                    result_1 = result_dict
                    result_2 = json.loads(result_1["data"])
                    result_3 = ""
                    end_tag = ""
                    end=len(result_2["cn"]["st"]["rt"][0]["ws"])
                    result_4=result_2["cn"]["st"]["rt"][0]["ws"]
                    for i in range(0,end):
                        result_3 += result_4[i]["cw"][0]["w"]
                    end_tag = result_2["cn"]["st"]["ed"]

                    if end_tag == "0":
                        socketio.emit('reply', {"result": result_3, "end": 0})

                    else:
                        socketio.emit('reply',{"result":result_3,"end":1})

                        if result_3[0] in [',','.','?','!']:
                            if len(result_3)>1:
                                result_3=result_3[1:len(result_3)]
                            else:
                                result_3=" "
                        salt = random.randint(32768, 65536)
                        # Build request
                        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                        sign = make_md5(appid + result_3 + str(salt) + appkey)
                        payload = {'appid': appid, 'q': result_3, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}
                        r = requests.post(url, params=payload, headers=headers)
                        result = r.json()
                        if "trans_result" in result:
                            socketio.emit('reply', {"result": " "+result["trans_result"][0]["dst"],"end":1})

                if result_dict["action"] == "error":
                    print("rtasr error: " + result)
                    self.ws.close()
                    return

        except websocket.WebSocketConnectionClosedException:
            print("receive result end")

    def close(self):
        self.ws.close()
        print("connection closed")

print("Server ready")

app = Flask(__name__)
socketio = SocketIO(app)

ctrler=[1,1]

logging.basicConfig()
client=Client()

@socketio.on('play')
def play(req):
    base_url = "ws://rtasr.xfyun.cn/v1/ws"
    ts = str(int(time.time()))
    tt = (app_id + ts).encode('utf-8')
    md5 = hashlib.md5()
    md5.update(tt)
    baseString = md5.hexdigest()
    baseString = bytes(baseString, encoding='utf-8')

    apiKey = api_key.encode('utf-8')
    signa = hmac.new(apiKey, baseString, hashlib.sha1).digest()
    signa = base64.b64encode(signa)
    signa = str(signa, 'utf-8')
    client.end_tag = "{\"end\": true}"

    client.ws = create_connection(base_url + "?appid=" + app_id + "&ts=" + ts + "&signa=" + quote(signa)  + "&lang=en")
    client.ws.settimeout(60)
    client.trecv = threading.Thread(target=client.recv)
    client.trecv.start()

@socketio.on('update')
def update(data):
    client.send(data)

@socketio.on('stop')
def stop(req):
    client.stop_send()
    socketio.emit('reply', {"result": " \n----------------\nstopped\n----------------\n", "end": 1})

@app.route('/chat', methods=['GET'])
def chat():
    return render_template("chat.html")

@app.route('/chat2', methods=['GET'])
def chat2():
    return render_template("chat2.html")

@app.route('/voice', methods=['GET'])
def voice():
    return render_template("voice.html")

@app.route('/translator', methods=['GET'])
def translator():
    return render_template("translator.html")

@app.route('/abort', methods=['GET'])
def abort():
    opt = request.args.get("option")
    ctrler[int(opt)]=1
    return ""

@app.route('/chat', methods=['POST'])
def answer():
    opt=request.json["option"]
    ctrler[opt]=0
    history=eval(request.json["history"])

    # get_data = request.args.to_dict()
    # msg1 = get_data.get('question')
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{"role":"system","content":request.json["system"]}]+history[:-1]+[{"role":"user","content":request.json["question"]}],
        stream=True
    )

    # return response["choices"][0]["message"]["content"]
    def generate():
        for trunk in response:
            # print(trunk)
            if ctrler[opt]==0:
                # print("running")
                yield json.dumps(trunk) + '\n'
            else:
                return

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
    }

    return Response(generate(), mimetype="text/event-stream", headers=headers)

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True)



    














