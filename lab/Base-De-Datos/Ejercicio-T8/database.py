import sqlite3


def conectar_bd(nombre_db="Base-de-Datos"):

    conexion = sqlite3.connect(nombre_db)
    cursor = conexion.cursor()

    return conexion, cursor

def cerrar_bd(conexion):
    
    

    conexion.commit()
    conexion.close()




def crear_tabla():

    conexion, cursor = conectar_bd()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alumnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            edad INTEGER
                )


    """)

    conexion.commit()


    


