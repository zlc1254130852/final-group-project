from flask import Blueprint
from flask import render_template
from setting import socketio
from transform import pcm2wav
from assess import send_assess

oral_assessment_bp = Blueprint('oral_assessment', __name__)

file = []
text = []

@oral_assessment_bp.route('/assess', methods=['GET'])
def assess():
    return render_template("assess.html")

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
        message=send_assess(text[-1])
        text.pop()
        socketio.emit('reply2', {"result": " "+message, "end": 1})

    else:
        file[-1].write(data)