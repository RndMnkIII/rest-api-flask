# -*- coding: utf-8 -*-
#Aplicación sección 4
#Editor: Atom 1.25.1
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'periquito' #esto deberia obtenerse de una variable de entorno
api = Api(app)
jwt = JWT(app, authenticate, identity) #crea endpoint /auth al que enviaremos username y password

items=[]

#tenemos dos endpoints para el recurso  /item
class Item(Resource):
    #parser es un atributo estático de la clase (no se instancia con los objetos como se haría con self.parser)
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cannot be left blank!')

    @jwt_required()
    def get(self, name):
        #for item in items:
        #    if item['name'] == name:
        #        return item #flaskk_restful no necesita ejecutar jsonfy
        #return {'item': None}, 404 #Código de Estado 404 (NO ENCONTRADO)
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        global items
        #Enfoque de Errores Primero (Error First Approach)
        #primero buscamos errores y finalizamos si encontramos alguno
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "Un artículo con nombre '{}' ya existe.".format(name)}, 400
        #una vez que se han descartado todos los errores, realizamos la tarea deseada
        data = Item.parser.parse_args() #parser es un atributo estático de la clase Item, no se instancia
        #data = request.get_json() #sin Content-Type application/json da error
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201 #Código de Estado 201 (CREADO)

    #usar en código de producción: @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message':'Artículo eliminado'}

    #@jwt_required()
    def put(self, name):
        global items
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name':name, 'price':data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(host='0.0.0.0', port=5000, debug=True)
