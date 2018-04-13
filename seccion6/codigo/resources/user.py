# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.user import UserModel

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

        if UserModel.find_by_username(data['username']):
            return {'message': "El usuario '{}' ya existe.".format(data['username'])}, 400

        user = UserModel(**data) #por cada clave en data desempaqueta un valor, pasandolos directamente como argumentos al constructor de UserModel
        user.save_to_db()

        return {"message":"Usuario creado con éxito!"}, 201
