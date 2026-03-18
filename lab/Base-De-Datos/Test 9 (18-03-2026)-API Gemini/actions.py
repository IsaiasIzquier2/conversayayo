from datetime import datetime
from memory import guardar_evento, obtener_eventos
from utils import formatear_fecha
from ai import preguntar_ia
import re


# ==========================
# EXTRAER FECHA DEL TEXTO
# ==========================
def extraer_fecha(texto):
    """
    Busca fechas en formato:
    YYYY-MM-DD HH:MM
    """
    patron = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}"
    match = re.search(patron, texto)
    return match.group() if match else None


# ==========================
# EJECUTAR ACCIONES
# ==========================
def ejecutar_accion(intent, texto):

    if intent == "guardar_recordatorio":

        fecha = extraer_fecha(texto)

        # Si NO hay fecha en el texto → preguntar
        if not fecha:
            fecha = input("Fecha evento (YYYY-MM-DD HH:MM): ")

        guardar_evento(texto, fecha)

        print("Asistente: Perfecto, ya lo he guardado ")


    elif intent == "consultar_eventos":

        eventos = obtener_eventos()

        if not eventos:
            print("Asistente: No tienes nada pendiente.")

        else:
            print("Asistente: Esto es lo que tienes apuntado:\n")

            for texto_evento, fecha in eventos:

                fecha_bonita = formatear_fecha(fecha)

                print(f" {texto_evento}")
                print(f"    {fecha_bonita}")
                print()


    elif intent == "hora":

        ahora = datetime.now()

        print("Asistente: Son las", ahora.strftime("%H:%M"))


    else:

        respuesta = preguntar_ia(texto)

        print("Asistente:", respuesta)