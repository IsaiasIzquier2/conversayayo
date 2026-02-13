import sqlite3

nombreDB = "Prueba1"

def crear_DB():

    conexion = sqlite3.connect(nombreDB)
    cursor = conexion.cursor()

    return conexion, cursor

def cerrar_bd(conexion):
    
    conexion.commit()
    conexion.close()


def crear_tabla():

    conexion, cursor = crear_DB()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alumnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            edad INTEGER
                )


    """)

    conexion.commit()