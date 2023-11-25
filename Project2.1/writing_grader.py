from flask import Blueprint
from flask import render_template
from flask import request, Response
import json, time
from api_key import DIFY_API_KEY_WRITING
import requests

writing_grader_bp = Blueprint('writing_grader_translation', __name__)

@writing_grader_bp.route('/chat2', methods=['GET'])
def chat2():
    return render_template("chat2.html")

@writing_grader_bp.route('/chat2', methods=['POST'])
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

def generate_dify_writing(response):
    tmp = ""
    for trunk in response:
        tmp += trunk.decode('utf-8').split("\n\n")[0]
        print(trunk.decode('utf-8'))
        print("---------------------")
        if len(trunk.decode('utf-8').split("\n\n")) >= 2:
            tmp2 = tmp[:].strip()
            tmp = trunk.decode('utf-8').split("\n\n")[-1]
            time.sleep(0.1)
            if len(tmp2) >= 6 and tmp2[0:6] == "data: ":
                yield tmp2
        elif len(trunk.decode('utf-8')) >= 2 and trunk.decode('utf-8')[-2:] == "}\n":
            tmp3 = tmp[:].strip()
            tmp = ""
            time.sleep(0.1)
            if len(tmp2) >= 6 and tmp2[0:6] == "data: ":
                yield tmp3