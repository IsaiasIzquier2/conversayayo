from datetime import datetime
from memory import guardar_evento, obtener_eventos
from utils import fecha_conversacional
from ai import interpretar_evento, preguntar_ia
from tts import hablar
from date_parser import parsear_fecha, fecha_a_str


def pedir_fecha_corregida(texto_evento):
    """
    El usuario ha dicho que la fecha no es correcta.
    Le pedimos solo la fecha, manteniendo el evento que ya teníamos.
    """

    hablar("¿Qué fecha es correcta?")
    nueva_fecha_texto = input("Tú: ").strip()

    fecha_dt = parsear_fecha(nueva_fecha_texto)

    if not fecha_dt:
        hablar("No he podido entender la fecha, puedes decirla de otra forma?")
        return

    fecha_str = fecha_a_str(fecha_dt)
    fecha_legible = fecha_conversacional(fecha_str)

    hablar(f"Tienes {texto_evento} el {fecha_legible}. ¿Es correcto?")

    respuesta = input("(si/no): ").strip().lower()

    if respuesta == "si":
        guardar_evento(texto_evento, fecha_str)
        hablar("Perfecto, ya lo he guardado.")
    else:
        hablar("Vale, lo dejamos aquí.")


def ejecutar_accion(intent, texto):

    # ==========================
    # GUARDAR RECORDATORIO
    # ==========================
    if intent == "guardar_recordatorio":

        datos = interpretar_evento(texto)

        if not datos or not datos.get("fecha_raw"):
            hablar("No he entendido bien la fecha, puedes repetirlo?")
            return

        texto_evento = datos.get("evento", texto)
        fecha_raw = datos.get("fecha_raw")

        fecha_dt = parsear_fecha(fecha_raw)

        if not fecha_dt:
            hablar("No he podido entender la fecha, puedes decirla de otra forma?")
            return

        fecha_str = fecha_a_str(fecha_dt)
        fecha_legible = fecha_conversacional(fecha_str)

        hablar(f"Tienes {texto_evento} el {fecha_legible}. ¿Es correcto?")

        respuesta_usuario = input("(si/no): ").strip().lower()

        if respuesta_usuario == "si":
            guardar_evento(texto_evento, fecha_str)
            hablar("Perfecto, ya lo he guardado.")
        else:
            # Mantenemos el evento y pedimos solo la fecha
            pedir_fecha_corregida(texto_evento)

    # ==========================
    # CONSULTAR EVENTOS
    # ==========================
    elif intent == "consultar_eventos":

        eventos = obtener_eventos()

        if not eventos:
            hablar("No tienes nada pendiente.")
            return

        if len(eventos) == 1:
            texto_evento, fecha = eventos[0]
            fecha_legible = fecha_conversacional(fecha)
            hablar(f"Sí, tienes {texto_evento.lower()} el {fecha_legible}.")
            return

        hablar(f"Tienes {len(eventos)} citas programadas.")

        for texto_evento, fecha in eventos:
            fecha_legible = fecha_conversacional(fecha)
            hablar(f"El {fecha_legible} tienes {texto_evento.lower()}.")

    # ==========================
    # HORA
    # ==========================
    elif intent == "hora":

        ahora = datetime.now()
        hablar(f"Son las {ahora.strftime('%H:%M')}.")

    # ==========================
    # CHARLA NORMAL
    # ==========================
    else:

        respuesta = preguntar_ia(texto)
        hablar(respuesta)