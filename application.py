import os

from flask import Flask, render_template, request, url_for, redirect
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Global variables for channels and messages
channel_rooms = ["general", "chat"]
channel_messages = [{"channel": "general", "body": "Welcome to the General Channel",
                     "date_time": "timestamp", "display_name": "DisplayName"}]


@app.route("/", methods=["GET", "POST"])
def index():
    # ISSUE: AT 26/6/20 NOT ALLOWING USER TO CREATE NEW CHANNEL
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Receiving input from index page to create new channel in channel_rooms
        # if channel name available add to channel_rooms otherwise return error message
        if request.form.get("ChannelName") not in channel_rooms:
            channel_rooms.append(request.form.get("ChannelName"))
            return render_template("index.html", channel_rooms=channel_rooms)
        else:
            return render_template("error.html", message="Channel name not available")
    # If come to this page via GET (as by clicking a link or via redirect)
    else:
        return render_template("index.html", channel_rooms=channel_rooms)


@app.route("/channels/<channel_name>", methods=["GET", "POST"])
def view_channel(channel_name):
    # This route displays messages for the given channel_name
    return render_template("view_channel.html", channel=channel_name, channel_messages=channel_messages)

# This is a test route for getting SocketIO working
@app.route("/vote")
def vote_index():
    return render_template("vote_index.html")

# This is a test route for getting SocketIO working
@socketio.on("submit vote")
def vote(data):
    selection = data["selection"]
    emit("announce vote", {"selection": selection}, broadcast=True)
