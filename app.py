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

SEND_ALL_MESSAGES_CHANNEL = 'send all messages'
SEND_ONE_MESSAGE_CHANNEL = 'send one message'


userPH="user"
userkeyPH="key"


app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)


sql_user = os.environ['SQL_USER']
sql_pwd = os.environ['SQL_PASSWORD']

database_uri = 'postgresql://{}:{}@localhost/postgres'.format(sql_user, sql_pwd)

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app


db.create_all()
db.session.commit()

users = []
client_user_dict = {}
bot = Chatbot()
users.append(bot.name)

def emit_all_messages():
    all_messages = get_all_messages()
    
    socketio.emit(SEND_ALL_MESSAGES_CHANNEL, {
        "allMessages": all_messages
    })
    

def get_all_messages():
    all_messages = [ \
        (db_message.content, db_message.user) for db_message \
        in db.session.query(models.Message).all()]
        
    return all_messages
    
    
@socketio.on('request all users')
def request_all_users():
    socketio.emit('all users', {
        'allUsers': users
    })


@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    
    
@socketio.on('new user')
def on_new_user(data):
    client_user_dict[request.sid] = data['name']
    print(data['name'] + " logged in")
    
    socketio.emit('all users', {
        'allUsers': users
    }, room=request.sid)
    
    users.append(data['name'])
    
    socketio.emit('user connected', {
        'name': str(data['name'])
    })
    
    socketio.emit(SEND_ALL_MESSAGES_CHANNEL, {
        'allMessages': get_all_messages()
    }, room = request.sid)
    

@socketio.on('disconnect')
def on_disconnect():
    if request.sid in client_user_dict:
        socketio.emit('user disconnected', {
            'name': client_user_dict[request.sid]
        });
        users.remove(client_user_dict[request.sid])
        print (client_user_dict[request.sid] + ' has disconnected!')

@socketio.on('new message input')
def on_new_message(data):
    print("Got an event for new message input with data:", data)
    
    db.session.add(models.Message(client_user_dict[request.sid], userkeyPH, data["message"]));
    
    socketio.emit(SEND_ONE_MESSAGE_CHANNEL, {
        'message': [(data["message"], client_user_dict[request.sid])]
    })
    
    if bot.isCommand(data["message"]):
        botmessage = bot.process(data["message"])
        db.session.add(models.Message(bot.name, bot.key, botmessage))
        socketio.emit(SEND_ONE_MESSAGE_CHANNEL, {
            'message': [(botmessage, bot.name)]
        })
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
