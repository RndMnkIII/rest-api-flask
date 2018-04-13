# -*- coding: utf-8 -*-
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
from models.store import StoreModel

#tenemos dos endpoints para el recurso  /item
class Item(Resource):
    #parser es un atributo estático de la clase (no se instancia con los objetos como se haría con self.parser)
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cannot be left blank!')
    parser.add_argument('store_id', type=int, required=True, help='Every item needs a store id!')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Artículo no encontrado!'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "Un artículo con nombre '{}' ya existe.".format(name)}, 400 #Bad request

        data = Item.parser.parse_args() #parser es un atributo estático de la clase Item, no se instancia

        if not StoreModel.find_by_id(data['store_id']):
            return {'message': "No existe store con id '{}'.".format(data['store_id'])}, 400 #Bad request

        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {'message':'Ocurrió un error interno insertando el artículo'}, 500 #Internal Server Error

        return item.json(), 201 #Código de Estado 201 (CREADO)

    #usar en código de producción: @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            try:
                item.delete_from_db()
            except:
                return {"message":"Ocurrió un error interno eliminando el artículo"}, 500 #Internal Server Error

                return {'message':'Artículo eliminado'}
        else:
            return {'message': "El artículo con nombre '{}' NO existe.".format(name)}, 400 #Bad request

    #@jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        if not StoreModel.find_by_id(data['store_id']):
            return {'message': "No existe store con id '{}'.".format(data['store_id'])}, 400 #Bad request
            
        item = ItemModel.find_by_name(name)

        if item is None:
            #item = ItemModel(name, data['price'], data['store_id']) #lo mismo con item = ItemModel(name, **data)
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items' : [item.json() for item in ItemModel.query.all()]} #Status: 200 OK
