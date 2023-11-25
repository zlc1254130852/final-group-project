# -*- encoding:utf-8 -*-
# main.py
from flask import request
import base64
import json

from setting import app, socketio

import requests

from assess2 import send_to_assess
from stream_generation import generate_dify_speaking
from api_key import DIFY_API_KEY_SPEAKING
from AI_chat import openai_client
from voice import Client, init_ws

print("Server ready")

client=Client()

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

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True)