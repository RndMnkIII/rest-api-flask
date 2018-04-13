# -*- coding: utf-8 -*-
import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    #columns names must match self.id, self.username, self.password names

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first() #SELECT * FROM users WHRE username=username LIMIT 1

    @classmethod
    def find_by_userid(cls, userid):
        return cls.query.filter_by(id=userid).first() #SELECT * FROM users WHRE id=userid LIMIT 1
