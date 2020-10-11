# models.py
import flask_sqlalchemy
from app import db


class Usps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(120))
    
    def __init__(self, a):
        self.address = a
        
    def __repr__(self):
        return '<Usps address: %s>' % self.address 

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(120))
    userkey = db.Column(db.String(120))
    content = db.Column(db.String(1024))
    
    def __init__(self, user, userkey, message):
        self.user = user
        self.userkey = userkey
        self.content = message
        
    def __repr__(self):
        return '<Message by user %s with content: %s>' % (self.user, self.content, )

