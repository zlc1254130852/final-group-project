# -*- coding: utf-8 -*-
import json
import uuid
import base64

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.soe.v20180724 import soe_client, models
from api_key import Tencent_SecretId, Tencent_SecretKey

from setting import socketio
from transform import pcm2wav
from AI_chat import openai_client
from api_key import DIFY_API_KEY_SPEAKING
from stream_generation import generate_dify_speaking

import requests

file3 = []

@socketio.on('play3')
def play3(req):
    file3.append(open("static/en/example3.pcm", "wb"))

@socketio.on('update3')
def update3(data):
    if not file3:
        return

    if type(data)==dict:

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

def send_to_assess(f,form):
    SecretId=Tencent_SecretId
    SecretKey=Tencent_SecretKey

    cred = credential.Credential(SecretId, SecretKey)

    client = soe_client.SoeClient(cred, "")

    req = models.TransmitOralProcessWithInitRequest()

    SessionId = str(uuid.uuid1())

    if type(f)==str:
        base64_data = f
    else:
        base64_data = base64.b64encode(f.read()).decode()

    params = {
        "SeqId": 1,
        "IsEnd": 1,
        "VoiceFileType": form,
        "VoiceEncodeType": 1,
        "UserVoiceData": base64_data,
        "SessionId": SessionId,
        "RefText": "",
        "WorkMode": 1,
        "EvalMode": 3,
        "ServerType": 0,
        "ScoreCoeff": 1.0
    }
    req.from_json_string(json.dumps(params))
    try:

        resp = client.TransmitOralProcessWithInit(req)

        return resp.to_json_string()

    except TencentCloudSDKException as err:
        return err

