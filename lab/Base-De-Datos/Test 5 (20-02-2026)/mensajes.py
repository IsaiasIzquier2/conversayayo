from db import conectar
from datetime import datetime

def guardar_mensaje(rol, contenido):
    conexion, cursor = conectar()
    cursor.execute("""
        INSERT INTO mensajes (rol, contenido)
        VALUES (?, ?)
    """, (rol, contenido))
    conexion.commit()
    conexion.close()


def mostrar_historial():
    conexion, cursor = conectar()
    cursor.execute("""
        SELECT rol, contenido, fecha_creacion
        FROM mensajes
        ORDER BY fecha_creacion ASC
    """)
    mensajes = cursor.fetchall()
    conexion.close()

    print("\n===== HISTORIAL =====\n")
    for rol, contenido, fecha in mensajes:
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
        fecha_formateada = fecha_obj.strftime("%d-%m-%Y %H:%M")
        print(f"[{fecha_formateada}] {rol.upper()}: {contenido}")