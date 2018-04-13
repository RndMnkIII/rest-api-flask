# -*- coding: utf-8 -*-
import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

#creamos una tabla
usersddlqry = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(usersddlqry)

user = (1, 'Javier', 'xxxx') #tupla
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

users = [
    (2, 'rolf', 'asdf'),
    (3, 'ana', 'xxx')
]
cursor.executemany(insert_query, users)

select_qur = "SELECT * FROM users"
for row in cursor.execute(select_qur):
    print(row)

connection.commit() #se graban cambios en data.db
connection.close()
