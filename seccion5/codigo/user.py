# -*- coding: utf-8 -*-
import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,)) #los parametros siempre se tienen que pasar como una tupla

        row = result.fetchone()

        if row:
            user = cls(*row) #equivalente a cls(row[0], row[1], row[2])
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_userid(cls, userid):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (userid,)) #los parametros siempre se tienen que pasar como una tupla

        row = result.fetchone()

        if row:
            user = cls(*row) #equivalente a cls(row[0], row[1], row[2])
        else:
            user = None

        connection.close()
        return user

class CurUser(Resource):
    @jwt_required()
    def get(self):
        user = current_identity
        print("Identidad: Id: {} Username: {}".format(user.id, user.username))
        return {'userid': user.id, 'username':user.username}

class UserRegister(Resource):
    #parser es un atributo estático de la clase (no se instancia con los objetos como se haría con self.parser)
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='This field cannot be left blank!')
    parser.add_argument('password', type=str, required=True, help='This field cannot be left blank!')

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {'message': "El usuario '{}' ya existe.".format(data['username'])}, 400


        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES (null, ?, ?)"
        cursor.execute(query, (data['username'], data['password'],))
        connection.commit()
        connection.close()
        return {"message":"Usuario creado con éxito!"}, 201
