#!/usr/bin/env python
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

bot_conversation = db.Table('bot_conversation',
    db.Column('conversation_id', db.Integer, db.ForeignKey('conversations.id'), primary_key=True),
    db.Column('bot_id', db.Integer, db.ForeignKey('bot.id'), primary_key=True)
)


class Bot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    year_of_birth = db.Column(db.Integer)
    sex = db.Column(db.String(1))
    request_token = db.Column(db.String(256))
    cookie = db.Column(db.String(1024))
    default = db.Column(db.Boolean)

    def __repr__(self):
        return self.name


class Conversations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    token = db.Column(db.String(128), index=True, unique=True)
    domain = db.Column(db.String(128), index=True, unique=True)
    bot = db.relationship('Bot', secondary=bot_conversation, lazy='subquery',
                           backref=db.backref('bots', lazy=True))

    def __repr__(self):
        return self.token

    def __str__(self):
        return self.name


class Message(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    text = db.Column(db.Text(), index=True)

    def __repr__(self):
        return self.text