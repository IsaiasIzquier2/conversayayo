from db import conectar
from datetime import datetime


def guardar_recordatorio(texto, fecha_evento):
    conexion, cursor = conectar()
    cursor.execute("""
        INSERT INTO recordatorios (texto_original, fecha_evento, confirmado)
        VALUES (?, ?, 1)
    """, (texto, fecha_evento))
    conexion.commit()
    conexion.close()


def obtener_proximo_evento():
    conexion, cursor = conectar()
    cursor.execute("""
        SELECT texto_original, fecha_evento
        FROM recordatorios
        WHERE fecha_evento >= datetime('now')
        AND confirmado = 1
        ORDER BY fecha_evento ASC
        LIMIT 1
    """)
    resultado = cursor.fetchone()
    conexion.close()
    return resultado