import sqlite3
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

#tenemos dos endpoints para el recurso  /item
class Item(Resource):
    #parser es un atributo estático de la clase (no se instancia con los objetos como se haría con self.parser)
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cannot be left blank!')

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Artículo no encontrado!'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        qur = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(qur, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    def post(self, name):
        #Enfoque de Errores Primero (Error First Approach)
        #primero buscamos errores y finalizamos si encontramos alguno
        if self.find_by_name(name):
            return {'message': "Un artículo con nombre '{}' ya existe.".format(name)}, 400 #Bad request
        #una vez que se han descartado todos los errores, realizamos la tarea deseada
        data = Item.parser.parse_args() #parser es un atributo estático de la clase Item, no se instancia
        #data = request.get_json() #sin Content-Type application/json da error
        item = {'name': name, 'price': data['price']}

        try:
            self.insert(item)
        except:
            return {"message":"Ocurrió un error interno insertando el artículo"}, 500 #Internal Server Error

        return item, 201 #Código de Estado 201 (CREADO)

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

    #usar en código de producción: @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message':'Artículo eliminado'}

    #@jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = self.find_by_name(name)
        updated_item = {'name':name, 'price':data['price']}
        if item is None:
            try:
                self.insert(item)
            except:
                {"message":"Ocurrió un error interno insertando el artículo"}, 500 #Internal Server Error
        else:
            try:
                self.update(updated_item)
            except:
                {"message":"Ocurrió un error interno actualizando el artículo"}, 500 #Internal Server Error
        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        items = []
        result = cursor.execute(query)
        for row in result:
            items.append({'name':row[0], 'price': row[1]})

        connection.close()
        return {'items': items}
