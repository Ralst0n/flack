import os

from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["CACHE_TYPE"] = "null"
socketio = SocketIO(app)

channels = []

@app.route("/", methods=['GET','POST'])
def index():
    if len(channels) == 0:
        session['last_channel'] = None

     # If request is post, get the display name & add it to user sesisons
    if request.method == 'POST':
        session['username'] = request.form.get('name')
    # else:
    #      return f"request is {request.method} does it equal 'POST'? {request.method == 'POST'}"    
    # If there is a username & previous channel redirect user to channel
    if session.get('username') and session.get('last_channel'):
        return redirect( url_for("channel", name=session.get('last_channel')) )

    # If user logged in but no channel selected take to list of channels
    elif (session.get('username')):
        return redirect( url_for("channel_list"))

    # If not logged in take to form to create display name
    else :
        return render_template('index.html')

@app.route("/channel/<string:name>")
def channel(name):
    if session.get('username'):
        # Go to the channel page if it exists
        if channel_exists(name):
            session['last_channel'] = name
            return render_template('channel.html', channel=get_channel(name), user=session['username'])
        # Otherwise go to the channels list page and show available channels
        message="No channel with that name exists. You can create it or find another option below"
        flash(message)
        return redirect(url_for('channel_list'))
    return render_template('index.html')
   
@app.route("/create", methods=["POST"])
def create_channel():
    name = request.form.get("channel-name").lower()
    # If the channel doesn't exist, create it and go to the channels pages
    if not channel_exists(name.lower()):
        add_channel(name.lower())
        return redirect(url_for('channel', name=name))
    flash('Can not use the name of an existing Channel')
    return redirect(url_for("channel_list"))

@app.route("/channels")
def channel_list():
    '''Return page with list of channels'''
    # Clear last channel if the user comes back to this page
    session['last_channel'] = None
    if session.get('username'):
        return render_template("channels.html", channels=channels)
    return render_template('index.html')

@socketio.on("message sent")
def on_update(data):
    channel = get_channel(data['channel'])
    index = channels.index(channel)
    message = {
        "sender": session['username'],
        "timestamp": datetime.now().strftime("%m/%d/%y %I:%M%p"),
        "content": data['message']
    }

    # keep only up to 100 messages in a channel
    messages = channels[index]['messages']
    if len(messages) >= 100:
        channels[index]['messages'] = messages[1:]

    channels[index]['messages'].append(message)
    emit("chat updated", message, broadcast=True)

@socketio.on("new user")
def update_users(data):
    channel = get_channel(data['channel'])
    index = channels.index(channel)
    # add the user that joined to the users list
    if data['name'] not in channels[index]['users']:
        channels[index]['users'].append(data['name'])
        # send the user name back with the emit
        socketio.emit("user added", data['name'], broadcast=True)
     
@socketio.on("user left")
def remove_user(data):
    channel = get_channel(data['channel'])
    index = channels.index(channel)
    name = data['name']
    # verify name in users, if it is, remove it from users.
    if data['name'] in channels[index]['users']:
        channels[index]['users'].pop(channels[index]['users'].index(name))

    socketio.emit("gone", data['name'], broadcast=True)

def channel_exists(name):
    ''' iterates through channel array to see if a channel with the given name exist'''
    for channel in channels:
        if channel['name'] == name:
            return True
    return False

def add_channel(name):
    # Adds a new channel with a name, a list of messages and a list of current users
    channels.append({'name': name, 'messages':[], 'users': []})

def get_channel(name):
    '''Get channel object by iterating through channels and matching name property'''
    for channel in channels:
        if channel['name'] == name:
            return channel