# models.py
import flask_sqlalchemy
from app import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(120))
    userkey = db.Column(db.String(120))
    userimage = db.Column(db.String(512))
    content = db.Column(db.String(1024))
    
    def __init__(self, user, userimage, userkey, message):
        self.user = user
        self.userimage = userimage
        self.userkey = userkey
        self.content = message
        
    def __repr__(self):
        return '<Message by user %s with content: %s>' % (self.user, self.content, )

