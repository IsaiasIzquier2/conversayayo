import speech_recognition as sr
import threading
from intent_detector import detectar_intencion
from actions import ejecutar_accion
from tts import hablar
from config import VOZ_ACTIVA

recognizer = sr.Recognizer()

TIMEOUT_SILENCIO = 15  # segundos sin hablar para suspenderse


def escuchar_usuario_conversacion():

    if not VOZ_ACTIVA:

        # Timeout por terminal usando threading
        resultado = [None]

        def leer_input():
            resultado[0] = input("Tú: ").strip()

        hilo = threading.Thread(target=leer_input)
        hilo.daemon = True
        hilo.start()
        hilo.join(timeout=TIMEOUT_SILENCIO)

        if hilo.is_alive():
            return "__silencio__"

        return resultado[0] if resultado[0] else "__silencio__"

    try:

        with sr.Microphone() as source:

            print("\n🎤 Escuchando...")

            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=TIMEOUT_SILENCIO, phrase_time_limit=10)

        texto = recognizer.recognize_google(audio, language="es-ES")

        print("Tú:", texto)

        return texto

    except sr.WaitTimeoutError:
        return "__silencio__"

    except sr.UnknownValueError:
        print("Asistente: No te entendí")
        return ""

    except sr.RequestError as e:
        print("Error reconocimiento:", e)
        return ""

    except Exception as e:
        print("Error:", e)
        return ""


def iniciar_conversacion():

    hablar("Sí, dime.")

    while True:

        texto = escuchar_usuario_conversacion()

        if texto == "__silencio__":
            hablar("Cuando me necesites, llámame.")
            break

        if not texto:
            continue

        texto_lower = texto.lower()

        if "adios" in texto_lower and "conversayayo" in texto_lower:
            hablar("Hasta luego.")
            break

        if texto_lower == "adios":
            hablar("Hasta luego.")
            break

        intent = detectar_intencion(texto)
        ejecutar_accion(intent, texto)