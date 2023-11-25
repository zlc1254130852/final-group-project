from flask import Flask
from flask_socketio import SocketIO
from blueprint import build_blueprint

app = Flask(__name__)
socketio = SocketIO(app)

build_blueprint(app)

