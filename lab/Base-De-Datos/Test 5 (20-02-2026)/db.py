import sqlite3

def conectar():
    conexion = sqlite3.connect("asistente.db")
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mensajes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rol TEXT CHECK(rol IN ('usuario','ia')),
        contenido TEXT NOT NULL,
        fecha_creacion TEXT DEFAULT (datetime('now','localtime'))
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recordatorios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        texto_original TEXT NOT NULL,
        fecha_evento TEXT NOT NULL,
        confirmado INTEGER DEFAULT 0,
        fecha_creacion TEXT DEFAULT (datetime('now','localtime'))
    )
    """)

    conexion.commit()
    return conexion, cursor