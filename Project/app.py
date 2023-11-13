# -*- encoding:utf-8 -*-
# main.py
from flask import render_template
from flask import request, Response
import hashlib
import hmac
import base64
from socket import *
import json, time, threading
from websocket import create_connection
from urllib.parse import quote
import logging
from assess import send_assess
from transform import pcm2wav
from voice import Client, app_id, api_key
from setting import app, socketio
from openai import OpenAI
from pydub import AudioSegment
import scipy.io.wavfile as wav
import requests

OPENAI_API_KEY = ""

print("Server ready")

ctrler=[1,1]

logging.basicConfig()
client=Client()

openai_client = OpenAI(api_key=OPENAI_API_KEY)

file = []
text = []

file3 = []

@app.route('/play4', methods=['POST'])
def play4():
    print(request.json["msg"])
    speech_file_path = "static/en/example4.mp3"
    response = openai_client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=request.json["msg"]
    )
    print("response done")
    response.stream_to_file(speech_file_path)
    sound = AudioSegment.from_mp3(speech_file_path)
    sound.export("static/en/example4.wav", format="wav")
    rt, wavsignal = wav.read('static/en/example4.wav')

    bwav=bytes(wavsignal)

    def generate():
        # time.sleep(0.04)
        for i in range(len(bwav)//1024+1):
            if (i+1)*1024>len(bwav):
                tmp=[]
                for j in range(1024-len(bwav)%1024):
                    tmp.append(0)

                yield bwav[i*1024:len(bwav)]+bytes(tmp)
            else:
                yield bwav[i*1024:(i+1)*1024]

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no'
    }

    return Response(generate(), mimetype="text/event-stream", headers=headers)

@socketio.on('play3')
def play3(req):
    file3.append(open("static/en/example3.pcm", "wb"))

@socketio.on('update3')
def update3(data):
    if not file3:
        return

    if type(data)==dict:
        # time.sleep(6)
        file_popped=file3.pop()
        file_popped.close()

        file_path = r"static/en/example3.pcm"
        to_path = r"static/en/example3.wav"
        pcm2wav(file_path, to_path)

        audio_file = open("static/en/example3.wav", "rb")
        transcript = openai_client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )

        socketio.emit('reply3', {"result": " "+transcript, "end": 1})

    else:
        file3[-1].write(data)

@socketio.on('play2')
def play2(req):
    file.append(open("static/en/example.pcm", "wb"))
    text.append(req['text'])

@socketio.on('update2')
def update2(data):
    if not file:
        return

    if type(data)==dict:
        # time.sleep(6)
        file_popped=file.pop()
        file_popped.close()

        file_path = r"static/en/example.pcm"
        to_path = r"static/en/example.wav"
        pcm2wav(file_path, to_path)
        recv_message=send_assess(text[-1])
        text.pop()
        # print(recv_message)
        socketio.emit('reply2', {"result": " "+recv_message, "end": 1})

    else:
        file[-1].write(data)

@app.route('/assess', methods=['GET'])
def assess():
    return render_template("assess.html")

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
    client.to_lang = req['to_lang']

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

    response = openai_client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{"role":"system","content":request.json["system"]}]+history[:-1]+[{"role":"user","content":request.json["question"]}],
        stream=True
    )

    def generate():
        for trunk in response:
            if ctrler[opt]==0:
                yield json.dumps({'delta':trunk.choices[0].delta.content,'finish_reason':trunk.choices[0].finish_reason}) + "\n"
            else:
                return

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no'
    }

    return Response(generate(), mimetype="text/event-stream", headers=headers)

@app.route('/chat2', methods=['POST'])
def answer2():
    # print(request.json["query"])
    headers = {'Authorization': '', 'Content-Type': 'application/json'}
    payload = {'inputs': {}, 'query': request.json["query"], 'response_mode': 'streaming', 'conversation_id': '', 'user': 'abc-123'}

    response = requests.post("https://api.dify.ai/v1/chat-messages", data=json.dumps(payload), headers=headers)

    def generate():
        tmp=""
        for trunk in response:
            tmp += trunk.decode('utf-8').split("\n\n")[0]
            print(trunk.decode('utf-8'))
            print("---------------------")
            if len(trunk.decode('utf-8').split("\n\n"))==2:
                tmp2=tmp[:]
                tmp=trunk.decode('utf-8').split("\n\n")[1]
                time.sleep(0.1)
                yield tmp2

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no'
    }

    return Response(generate(), mimetype="text/event-stream", headers=headers)
    # return r.json()

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True)



    














