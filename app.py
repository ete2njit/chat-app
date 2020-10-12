# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models 
from flask import request

MESSAGE_RECEIVED_CHANNEL = 'message received'



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

def emit_all_messages(channel):
    all_messages = [ \
        (db_message.content, db_message.user) for db_message \
        in db.session.query(models.Message).all()]
        
    socketio.emit(channel, {
        'allMessages': all_messages
    })
    
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
    
    emit_all_messages(MESSAGE_RECEIVED_CHANNEL)
    
    
    
@socketio.on('request all users')
def request_all_users():
    socketio.emit('all users', {
        'allUsers': users
    })


@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    

@socketio.on('disconnect')
def on_disconnect():
    socketio.emit('user disconnected', {
        'name': client_user_dict[request.sid]
    });
    users.remove(client_user_dict[request.sid])
    print (client_user_dict[request.sid] + ' has disconnected!')

@socketio.on('new message input')
def on_new_message(data):
    print("Got an event for new message input with data:", data)
    
    db.session.add(models.Message(client_user_dict[request.sid], userkeyPH, data["message"]));
    db.session.commit();
    
    emit_all_messages(MESSAGE_RECEIVED_CHANNEL)

@app.route('/')
def index():
    emit_all_messages(MESSAGE_RECEIVED_CHANNEL)

    return flask.render_template("index.html")

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
