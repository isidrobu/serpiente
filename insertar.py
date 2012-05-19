#!/usr/python
# -*- coding: utf-8 -*-

import MySQLdb


# Establecemos la conexión
Conexion = MySQLdb.connect(host='localhost', user='root',passwd='root', db='serpiente')


# Creamos el cursor
micursor = Conexion.cursor()


#creamos los 10 registro iniciales
micursor.execute("INSERT INTO Puntos (id,Nombre,Puntuacion) VALUES (1, \"Isidro\",50);")
micursor.execute("INSERT INTO Puntos (id,Nombre,Puntuacion) VALUES (2, \"Pepe\",70);")
micursor.execute("INSERT INTO Puntos (id,Nombre,Puntuacion) VALUES (4, \"Ojo\",10);")
micursor.execute("INSERT INTO Puntos (id,Nombre,Puntuacion) VALUES (5, \"Jesus\",20);")

Conexion.commit()
micursor.close () 
Conexion.close () 
