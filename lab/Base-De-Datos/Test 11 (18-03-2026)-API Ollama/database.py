import sqlite3


def conectar():

    conexion = sqlite3.connect("conversayayo.db")

    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        texto TEXT,
        fecha_evento TEXT,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conexion.commit()

    return conexion