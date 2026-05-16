from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chat_secret'

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet"
)

users = set()

@app.route("/")
def index():
    return render_template("chat.html")

@socketio.on("join")
def join(data):
    name = data.get("name")
    if name:
        users.add(name)
        socketio.emit("online_users", list(users), broadcast=True)

@socketio.on("message_from_client")
def handle_message(data):
    socketio.emit("message_from_server", data, broadcast=True)

@socketio.on("disconnect")
def disconnect():
    socketio.emit("online_users", list(users), broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)