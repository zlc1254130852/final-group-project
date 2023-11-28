from flask import Blueprint
from flask import render_template
from flask import request, Response
from login_check import check_login

from pydub import AudioSegment
import scipy.io.wavfile as wav
from stream_generation import generate_AI_chat, generate_bwav

AI_chat_bp = Blueprint('AI_chat', __name__)

openai_client = {}

ctrler = {}

@AI_chat_bp.route('/chat', methods=['GET'])
def chat():
    user_info = check_login()  # check which user is logged in.

    if user_info:  # if there is a logged-in user
        return render_template("chat.html", current_user=user_info.login_name)
    else:
        return render_template("chat.html")

@AI_chat_bp.route('/chat', methods=['POST'])
def answer():
    current_user=request.json["current_user"]
    if current_user not in ctrler:
        ctrler[current_user]=[1,1]
    opt=request.json["option"]
    ctrler[current_user][opt]=0
    history=eval(request.json["history"])

    response = openai_client[current_user].chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{"role":"system","content":request.json["system"]}]+history[:-1]+[{"role":"user","content":request.json["question"]}],
        stream=True
    )

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no'
    }

    return Response(generate_AI_chat(ctrler[current_user],opt,response), mimetype="text/event-stream", headers=headers)

@AI_chat_bp.route('/abort', methods=['POST'])
def abort():
    req = request.values
    current_user=req["current_user"]
    opt = req["option"]
    ctrler[current_user][int(opt)]=1
    return ""

@AI_chat_bp.route('/translator', methods=['GET'])
def translator():
    user_info = check_login()  # check which user is logged in.

    if user_info:  # if there is a logged-in user
        return render_template("translator.html", current_user=user_info.login_name)
    else:
        return render_template("translator.html")

@AI_chat_bp.route('/play4', methods=['POST'])
def play4():
    print(request.json["msg"])
    speech_file_path = "static/en/e4xample"+request.json["current_user"]+".mp3"
    response = openai_client[request.json["current_user"]].audio.speech.create(
        model="tts-1",
        voice=request.json["opt"].lower(),
        input=request.json["msg"]
    )
    print("response done")
    response.stream_to_file(speech_file_path)
    sound = AudioSegment.from_mp3(speech_file_path)
    sound.export("static/en/e4xample"+request.json["current_user"]+".wav", format="wav")
    rt, wavsignal = wav.read('static/en/e4xample'+request.json["current_user"]+'.wav')

    bwav=bytes(wavsignal)

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no'
    }

    return Response(generate_bwav(bwav), mimetype="text/event-stream", headers=headers)