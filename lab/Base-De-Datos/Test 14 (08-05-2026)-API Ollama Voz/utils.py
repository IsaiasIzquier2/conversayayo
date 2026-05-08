from datetime import datetime


MESES = {
    "January": "enero",
    "February": "febrero",
    "March": "marzo",
    "April": "abril",
    "May": "mayo",
    "June": "junio",
    "July": "julio",
    "August": "agosto",
    "September": "septiembre",
    "October": "octubre",
    "November": "noviembre",
    "December": "diciembre",
}

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


def fecha_conversacional(fecha_texto):

    fecha_obj = datetime.strptime(fecha_texto, "%Y-%m-%d %H:%M")

    dia = fecha_obj.day
    mes = fecha_obj.strftime("%B")
    año = fecha_obj.year
    hora = fecha_obj.strftime("%H:%M")

    mes_es = MESES.get(mes, mes)

    return f"{dia} de {mes_es} de {año} a las {hora}"

# ==========================
# OBTENER TIMESTAMP ACTUAL
# ==========================

def timestamp():
    """
    Devuelve timestamp actual para registros
    """

    ahora = datetime.now()

    return ahora.strftime("%Y-%m-%d %H:%M:%S")