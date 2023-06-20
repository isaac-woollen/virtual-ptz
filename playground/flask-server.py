from flask import Flask, render_template, session, request, jsonify
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on("message")
def handle_message(data):
    print(data)
    socketio.emit("response", "hello from server")


if __name__ == "__main__":
    socketio.run(app)
