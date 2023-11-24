# -*- encoding:utf-8 -*-
# main.py
from flask import render_template
from flask import request, Response
import base64
# from socket import *
import json

from assess import send_assess
from transform import pcm2wav
from voice import Client, init_ws
from setting import app, socketio

from openai import OpenAI
from pydub import AudioSegment
import scipy.io.wavfile as wav
import requests

from d_id_talk import generate_video
from assess2 import send_to_assess
from text_summary import text_summarizing
from object_detection import object_detect
from excel_query import excel_find
from baidu_translation import baidu_translate
from stream_generation import generate_bwav,generate_AI_chat,generate_dify_speaking,generate_dify_writing

OPENAI_API_KEY = ""

SPEECH_ASSESSMENT_APPID=''
SPEECH_ASSESSMENT_APISecret=''
SPEECH_ASSESSMENT_APIKey=''

BAIDU_TRANSLATION_APPID = ''
BAIDU_TRANSLATION_APPKEY = ''

D_ID_TALK_API_KEY = ""

OBJECT_DETECTION_APPID = ""
OBJECT_DETECTION_API_KEY = ""

IFLY_REAL_TIME_TRANSCRITION_API_ID = ""
IFLY_REAL_TIME_TRANSCRITION_API_KEY = ""

Tencent_SecretId=""
Tencent_SecretKey=""

DIFY_API_KEY_WRITING = ''
DIFY_API_KEY_SPEAKING = ""

print("Server ready")

ctrler=[1,1]

client=Client()

openai_client = OpenAI(api_key=OPENAI_API_KEY)

file = []
text = []

file3 = []

@app.route('/upload2',methods=['GET'])
def upload2():
    return render_template("upload2.html")

@app.route('/file2',methods=['POST'])
def save_file2():
    data = request.files

    file = data['file']

    buffer_data = file.read()
    with open("static/"+file.filename, 'wb+') as f:
        f.write(buffer_data)

    result = object_detect("static/"+file.filename,file.filename)

    result2 = ""

    for i in json.loads(result.decode('utf-8'))["data"]["fileList"][0]["labels"]:
        tmp = excel_find(i)
        tmp2 = baidu_translate(tmp)
        result2 += tmp + " " + tmp2

        result2 +="\n"

    return {"result":result2}

@app.route('/text_summary', methods=['GET'])
def text_summary():
    return render_template("text_summary.html")

@app.route('/summarize', methods=['POST'])
def summarize():
    result = text_summarizing(request.values["text"])
    print(result)
    return {'result': result}

@app.route('/reading/<id>',methods=['GET'])
def reading(id):
    return render_template("reading"+id+".html")

@app.route('/listening/<id>',methods=['GET'])
def listening(id):
    return render_template("listening"+id+".html")

@app.route('/upload',methods=['GET'])
def upload():
    return render_template("upload.html")

@app.route('/file',methods=['POST'])
def save_file():
    data = request.files

    file = data['file']

    buffer_data = file.read()
    with open("static/en/"+file.filename, 'wb+') as f:
        f.write(buffer_data)

    form=1
    if file.filename[-4:]==".pcm":
        form=1
    elif file.filename[-4:]==".wav":
        form=2
    elif file.filename[-4:]==".mp3":
        form=3

    result=send_to_assess(base64.b64encode(buffer_data).decode(),form)
    print(result)

    f.close()
    audio_file = open("static/en/"+file.filename, "rb")

    transcript = openai_client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )
    audio_file.close()
    print(transcript)

    socketio.emit('reply5', transcript+"\n")

    socketio.emit('reply5', 'PronAccuracy: ' + str(json.loads(result)['PronAccuracy']) + "\nPronFluency: " + str(
        json.loads(result)['PronFluency'])+"\n\nWaiting for the response...\n\n")

    headers = {'Authorization': DIFY_API_KEY_SPEAKING, 'Content-Type': 'application/json'}
    payload = {'inputs': {}, 'query': transcript, 'response_mode': 'streaming',
               'conversation_id': '', 'user': 'abc-123'}

    response = requests.post("https://api.dify.ai/v1/chat-messages", data=json.dumps(payload),
                             headers=headers)
    generate_dify_speaking(response)

    return ""

@app.route('/video_chat',methods=['GET'])
def video_chat():
    return render_template("video.html")

@app.route('/video',methods=['GET'])
def video():
    question = request.args.get("question")
    print(question)
    response = openai_client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": question}],
    )

    result=generate_video(response.choices[0].message.content)
    return result

@app.route('/play4', methods=['POST'])
def play4():
    print(request.json["msg"])
    speech_file_path = "static/en/example4.mp3"
    response = openai_client.audio.speech.create(
        model="tts-1",
        voice=request.json["opt"].lower(),
        input=request.json["msg"]
    )
    print("response done")
    response.stream_to_file(speech_file_path)
    sound = AudioSegment.from_mp3(speech_file_path)
    sound.export("static/en/example4.wav", format="wav")
    rt, wavsignal = wav.read('static/en/example4.wav')

    bwav=bytes(wavsignal)

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no'
    }

    return Response(generate_bwav(bwav), mimetype="text/event-stream", headers=headers)

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

        socketio.emit('reply5', transcript+"\n")

        if 'type' in data:
            with open("static/en/example3.pcm", "rb") as f:
                base64_data = base64.b64encode(f.read()).decode()
                print(type(base64_data))
                result = send_to_assess(base64_data,1)
                socketio.emit('reply5', 'PronAccuracy: ' + str(json.loads(result)['PronAccuracy']) + "\nPronFluency: " + str(
        json.loads(result)['PronFluency'])+"\n\nWaiting for the response...\n\n")

            headers = {'Authorization': DIFY_API_KEY_SPEAKING, 'Content-Type': 'application/json'}
            payload = {'inputs': {}, 'query': transcript, 'response_mode': 'streaming',
                       'conversation_id': '', 'user': 'abc-123'}

            response = requests.post("https://api.dify.ai/v1/chat-messages", data=json.dumps(payload),
                                     headers=headers)

            generate_dify_speaking(response)

        else:

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
        file_popped=file.pop()
        file_popped.close()

        file_path = r"static/en/example.pcm"
        to_path = r"static/en/example.wav"
        pcm2wav(file_path, to_path)
        recv_message=send_assess(text[-1])
        text.pop()
        socketio.emit('reply2', {"result": " "+recv_message, "end": 1})

    else:
        file[-1].write(data)

@app.route('/assess', methods=['GET'])
def assess():
    return render_template("assess.html")

@socketio.on('play')
def play(req):
    init_ws(client,req['to_lang'])

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

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no'
    }

    return Response(generate_AI_chat(ctrler,opt,response), mimetype="text/event-stream", headers=headers)

@app.route('/chat2', methods=['POST'])
def answer2():
    headers = {'Authorization': DIFY_API_KEY_WRITING, 'Content-Type': 'application/json'}
    payload = {'inputs': {}, 'query': request.json["query"], 'response_mode': 'streaming', 'conversation_id': '', 'user': 'abc-123'}

    response = requests.post("https://api.dify.ai/v1/chat-messages", data=json.dumps(payload), headers=headers)

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no'
    }

    return Response(generate_dify_writing(response), mimetype="text/event-stream", headers=headers)

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True)
