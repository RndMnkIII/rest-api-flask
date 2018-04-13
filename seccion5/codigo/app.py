# -*- coding: utf-8 -*-
#Aplicación sección 4
#Editor: Atom 1.25.1
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from datetime import timedelta

from security import authenticate, identity as identity_function
from user import UserRegister, CurUser
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'periquito' #esto deberia obtenerse de una variable de entorno
api = Api(app)
jwt = JWT(app, authenticate, identity_function) #crea endpoint /auth al que enviaremos username y password

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({'access_token': access_token.decode('utf-8'), 'user_id': identity.id})

app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(CurUser, '/user')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
