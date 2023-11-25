from flask import Blueprint
from openai import OpenAI
from api_key import OPENAI_API_KEY
from flask import render_template
from flask import request, Response
import json
from pydub import AudioSegment
import scipy.io.wavfile as wav

AI_chat_bp = Blueprint('AI_chat', __name__)

openai_client = OpenAI(api_key=OPENAI_API_KEY)

ctrler=[1,1]

@AI_chat_bp.route('/chat', methods=['GET'])
def chat():
    return render_template("chat.html")

@AI_chat_bp.route('/chat', methods=['POST'])
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

@AI_chat_bp.route('/abort', methods=['GET'])
def abort():
    opt = request.args.get("option")
    ctrler[int(opt)]=1
    return ""

@AI_chat_bp.route('/translator', methods=['GET'])
def translator():
    return render_template("translator.html")

@AI_chat_bp.route('/play4', methods=['POST'])
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

def generate_AI_chat(ctrler,opt,response):
    for trunk in response:
        if ctrler[opt]==0:
            yield json.dumps({'delta':trunk.choices[0].delta.content,'finish_reason':trunk.choices[0].finish_reason}) + "\n"
        else:
            return

def generate_bwav(bwav):
    for i in range(len(bwav)//1024+1):
        if (i+1)*1024>len(bwav):
            tmp=[]
            for j in range(1024-len(bwav)%1024):
                tmp.append(0)

            yield bwav[i*1024:len(bwav)]+bytes(tmp)
        else:
            yield bwav[i*1024:(i+1)*1024]