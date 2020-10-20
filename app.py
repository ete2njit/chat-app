# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models 
from chatbot import Chatbot
from flask import request

SEND_ALL_MESSAGES_CHANNEL   = 'send all messages'
SEND_ONE_MESSAGE_CHANNEL    = 'send one message'
RECEIVE_MESSAGE_CHANNEL     = 'new message input'
SEND_ALL_USERS_CHANNEL      = 'all users'
NEW_USER_CHANNEL            = 'new user'
USER_LOGIN_REQUEST_CHANNEL  = 'user login'
LOGIN_GRANTED_CHANNEL       = 'grant login'

userPH="user"
userkeyPH="key"

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

database_uri = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app


db.create_all()
db.session.commit()

users = []
client_user_dict = {}
client_userimage_dict = {}
client_userkey_dict = {}

bot = Chatbot()
users.append(bot.name)


def send_one_message(name, image, key, message):
    socketio.emit(SEND_ONE_MESSAGE_CHANNEL, {
        "message": (message, name, key, image),
    })
    return
    

def get_all_messages():
    all_messages = [ \
        (db_message.content, db_message.user, db_message.userkey, db_message.userimage) for db_message \
        in db.session.query(models.Message).all()]
        
    return all_messages
    

@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    
    
@socketio.on(USER_LOGIN_REQUEST_CHANNEL)
def login_requested(data):
    
    username = ""
    userimage = ""
    userkey = ""

    if(data['type'] == "Google"):
        username = data['data']['profileObj']['name']
        userkey = "GOOGLE" + data['data']['profileObj']['googleId']
        userimage = data['data']['profileObj']['imageUrl']
        
        socketio.emit(LOGIN_GRANTED_CHANNEL, {
            'username': username,
            'userkey': userkey
        }, room = request.sid)
        
    else: 
        return

    
    client_userimage_dict[request.sid] = userimage
    client_userkey_dict[request.sid] = userkey
    client_user_dict[request.sid] = username
    print(username + " logged in")
    
    socketio.emit(SEND_ALL_USERS_CHANNEL, {
        'allUsers': users
    }, room=request.sid)
    
    users.append(username)
    
    socketio.emit('user connected', {
        'name': str(username)
    })
    
    socketio.emit(SEND_ALL_MESSAGES_CHANNEL, {
        'allMessages': get_all_messages()
    }, room=request.sid)
    

@socketio.on('disconnect')
def on_disconnect():
    if request.sid in client_user_dict:
        socketio.emit('user disconnected', {
            'name': client_user_dict[request.sid]
        });
        users.remove(client_user_dict[request.sid])
        print (client_user_dict[request.sid] + ' has disconnected!')
        

@socketio.on(RECEIVE_MESSAGE_CHANNEL)
def on_new_message(data):
    print("Got an event for new message input with data:", data)
    
    name = client_user_dict[request.sid]
    key  = client_userkey_dict[request.sid]
    image = client_userimage_dict[request.sid]
    message = data["message"]
    
    db.session.add(models.Message(name, image, key, message));
    
    send_one_message(name, image, key, message)
    
    if bot.isCommand(data["message"]):
        botmessage = bot.process(data["message"])
        db.session.add(models.Message(bot.name, bot.image, bot.key, botmessage))
        send_one_message(bot.name, bot.image, bot.key, botmessage)
    db.session.commit();
    
    

@app.route('/')
def index():
    return flask.render_template("index.html")

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
