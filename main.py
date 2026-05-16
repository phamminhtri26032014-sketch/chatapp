from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "chat_secret_2026"

socketio = SocketIO(app, cors_allowed_origins="*")

online_users = set()

@app.route("/")
def index():
    return render_template("chat.html")


@socketio.on("join")
def join(data):
    name = data.get("name")
    if name:
        online_users.add(name)
    emit("online_users", list(online_users), broadcast=True)


@socketio.on("message_from_client")
def message(data):
    emit("message_from_server", data, broadcast=True)


@socketio.on("typing")
def typing(data):
    emit("typing", data, broadcast=True)


@socketio.on("disconnect")
def disconnect():
    emit("online_users", list(online_users), broadcast=True)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)