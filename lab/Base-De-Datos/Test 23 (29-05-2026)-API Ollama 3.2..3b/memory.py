from database import conectar
from datetime import datetime


def guardar_evento(texto, fecha):

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        """
        INSERT INTO eventos (texto, fecha_evento)
        VALUES (?, ?)
        """,
        (texto, fecha)
    )

    conexion.commit()
    conexion.close()


def obtener_eventos():

    conexion = conectar()
    cursor = conexion.cursor()

    # Usamos la hora local de Python en lugar de datetime('now') de SQLite
    # para evitar problemas con UTC vs hora española
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M")

    cursor.execute(
        """
        SELECT texto, fecha_evento
        FROM eventos
        WHERE fecha_evento >= ?
        ORDER BY fecha_evento
        """,
        (ahora,)
    )

    datos = cursor.fetchall()

    conexion.close()

    return datos


def borrar_evento_por_fecha(fecha):

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        """
        DELETE FROM eventos
        WHERE fecha_evento LIKE ?
        """,
        (fecha + "%",)
    )

    conexion.commit()
    conexion.close()


def limpiar_eventos_pasados():
    """
    Elimina de la base de datos todos los eventos cuya fecha ya pasó.
    Se puede llamar al arrancar el programa.
    """

    conexion = conectar()
    cursor = conexion.cursor()

    ahora = datetime.now().strftime("%Y-%m-%d %H:%M")

    cursor.execute(
        """
        DELETE FROM eventos
        WHERE fecha_evento < ?
        """,
        (ahora,)
    )

    eliminados = cursor.rowcount

    conexion.commit()
    conexion.close()

    if eliminados > 0:
        print(f"[INFO] Se eliminaron {eliminados} evento(s) pasado(s).")