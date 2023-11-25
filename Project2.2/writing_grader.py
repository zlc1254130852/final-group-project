from flask import Blueprint
from flask import render_template
from flask import request, Response
import json
from api_key import DIFY_API_KEY_WRITING
import requests
from stream_generation import generate_dify_writing

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