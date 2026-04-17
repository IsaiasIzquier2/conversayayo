from datetime import datetime


# ==========================
# OBTENER HORA ACTUAL
# ==========================

def obtener_hora_actual():
    """
    Devuelve la hora actual en formato HH:MM
    """
    ahora = datetime.now()
    return ahora.strftime("%H:%M")


# ==========================
# OBTENER FECHA ACTUAL
# ==========================

def obtener_fecha_actual():
    """
    Devuelve la fecha actual en formato DD-MM-YYYY
    """
    ahora = datetime.now()
    return ahora.strftime("%d-%m-%Y")


# ==========================
# FORMATEAR FECHA PARA MOSTRAR
# ==========================

def formatear_fecha(fecha_texto):
    """
    Convierte una fecha de base de datos
    YYYY-MM-DD HH:MM
    a formato legible
    DD-MM-YYYY HH:MM
    """

    try:
        fecha_obj = datetime.strptime(fecha_texto, "%Y-%m-%d %H:%M")
        return fecha_obj.strftime("%d-%m-%Y %H:%M")
    except:
        return fecha_texto


# ==========================
# OBTENER TIMESTAMP ACTUAL
# ==========================

def timestamp():
    """
    Devuelve timestamp actual para registros
    """

    ahora = datetime.now()

    return ahora.strftime("%Y-%m-%d %H:%M:%S")