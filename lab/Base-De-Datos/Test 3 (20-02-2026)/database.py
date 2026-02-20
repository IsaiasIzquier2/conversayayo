import sqlite3

nombreDB = "Test-3.db"

def crear_DB():
    conexion = sqlite3.connect(nombreDB)
    cursor = conexion.cursor()
    return conexion, cursor


def crear_tabla():
    conexion, cursor = crear_DB()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alumnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE,
            edad INTEGER,
            fecha_creacion TEXT DEFAULT (datetime('now','localtime')),
            fecha_actualizacion TEXT
        )
    """)

    conexion.commit()
    conexion.close()