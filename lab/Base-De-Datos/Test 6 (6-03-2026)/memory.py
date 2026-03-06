from database import conectar


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

    cursor.execute(
        "SELECT texto, fecha_evento FROM eventos ORDER BY fecha_evento"
    )

    datos = cursor.fetchall()

    conexion.close()

    return datos