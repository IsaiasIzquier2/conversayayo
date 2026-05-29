from datetime import datetime
from memory import guardar_evento, obtener_eventos
from utils import fecha_conversacional
from ai import interpretar_evento, preguntar_ia
from tts import hablar
from date_parser import parsear_fecha, fecha_a_str, calcular_fecha
from config import VOZ_ACTIVA
import speech_recognition as sr

recognizer = sr.Recognizer()


def escuchar_confirmacion() -> str:
    """
    Escucha una confirmación (si/no) por voz o teclado según config.
    Devuelve 'si', 'no', o 'desconocido'.
    """

    if not VOZ_ACTIVA:
        respuesta = input("(si/no): ").strip().lower()
        if "si" in respuesta or "sí" in respuesta:
            return "si"
        if "no" in respuesta:
            return "no"
        return "desconocido"

    try:
        with sr.Microphone() as source:
            print("🎤 (si / no)...")
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=4)

        texto = recognizer.recognize_google(audio, language="es-ES").lower()
        print(f"(Confirmación detectada: {texto})")

        if "sí" in texto or "si" in texto or "correcto" in texto or "exacto" in texto or "afirmativo" in texto:
            return "si"
        if "no" in texto or "incorrecto" in texto or "mal" in texto:
            return "no"

        return "desconocido"

    except sr.WaitTimeoutError:
        return "desconocido"
    except sr.UnknownValueError:
        return "desconocido"
    except Exception as e:
        print(f"Error escuchando confirmación: {e}")
        return "desconocido"


def escuchar_texto_libre() -> str:
    """
    Escucha texto libre por voz o teclado según config.
    """

    if not VOZ_ACTIVA:
        return input("Tú: ").strip()

    try:
        with sr.Microphone() as source:
            print("🎤 Escuchando...")
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)

        texto = recognizer.recognize_google(audio, language="es-ES")
        print(f"Tú: {texto}")
        return texto

    except Exception:
        return ""


def pedir_fecha_corregida(texto_evento):

    hablar("¿Qué fecha es correcta?")
    nueva_fecha_texto = escuchar_texto_libre()

    if not nueva_fecha_texto:
        hablar("No te he escuchado, lo dejamos aquí.")
        return

    fecha_dt = parsear_fecha(nueva_fecha_texto)

    if not fecha_dt:
        hablar("No he podido entender la fecha, puedes decirla de otra forma?")
        return

    fecha_str = fecha_a_str(fecha_dt)
    fecha_legible = fecha_conversacional(fecha_str)

    hablar(f"Tienes {texto_evento} el {fecha_legible}. ¿Es correcto?")

    respuesta = escuchar_confirmacion()

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

        respuesta = escuchar_confirmacion()

        if respuesta == "si":
            guardar_evento(texto_evento, fecha_str)
            hablar("Perfecto, ya lo he guardado.")
        elif respuesta == "no":
            pedir_fecha_corregida(texto_evento)
        else:
            hablar("No te he entendido, lo dejamos aquí.")

    # ==========================
    # CONSULTAR POR FECHA
    # ==========================
    elif intent == "consultar_por_fecha":

        fecha_dt = calcular_fecha(texto)

        if not fecha_dt:
            hablar("No he entendido qué día quieres consultar.")
            return

        fecha_buscada = fecha_dt.date()
        eventos = obtener_eventos()

        eventos_del_dia = [
            (ev, f) for ev, f in eventos
            if datetime.strptime(f, "%Y-%m-%d %H:%M").date() == fecha_buscada
        ]

        if not eventos_del_dia:
            fecha_str = fecha_dt.strftime("%Y-%m-%d") + " 00:00"
            fecha_legible = fecha_conversacional(fecha_str)
            hablar(f"No tienes nada el {fecha_legible}.")
            return

        if len(eventos_del_dia) == 1:
            texto_evento, fecha = eventos_del_dia[0]
            fecha_legible = fecha_conversacional(fecha)
            hablar(f"Sí, tienes {texto_evento.lower()} el {fecha_legible}.")
            return

        hablar(f"Tienes {len(eventos_del_dia)} cosas ese día.")
        for texto_evento, fecha in eventos_del_dia:
            hora = datetime.strptime(fecha, "%Y-%m-%d %H:%M").strftime("%H:%M")
            hablar(f"{texto_evento} a las {hora}.")

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