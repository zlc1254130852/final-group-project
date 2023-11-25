from flask import Blueprint
from flask import render_template
from flask import request
from AI_chat import openai_client
from d_id_talk import generate_video

video_chat_bp = Blueprint('video_chat', __name__)

@video_chat_bp.route('/video_chat',methods=['GET'])
def video_chat():
    return render_template("video.html")

@video_chat_bp.route('/video',methods=['GET'])
def video():
    question = request.args.get("question")
    print(question)
    response = openai_client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": question}],
    )

    result=generate_video(response.choices[0].message.content)
    return result