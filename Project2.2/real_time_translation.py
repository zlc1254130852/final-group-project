from flask import Blueprint
from flask import render_template
from setting import socketio
from voice import Client, init_ws

real_time_translation_bp = Blueprint('real_time_translation', __name__)

client=Client()

@real_time_translation_bp.route('/voice', methods=['GET'])
def voice():
    return render_template("voice.html")

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