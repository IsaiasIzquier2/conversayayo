import sqlite3
from database import crear_tabla
from operaciones import insertar_alumnos, mostrar_alumnos

# Crear tabla
crear_tabla()

# Insertar alumnos
alumnos = [(input("Añade el nombre del nuevo alumno: "), int(input("Añade la edad del nuevo alumno: "))), ("Luis", 22)]
insertar_alumnos(alumnos)

# Mostrar alumnos
for a in mostrar_alumnos():
    print(a)