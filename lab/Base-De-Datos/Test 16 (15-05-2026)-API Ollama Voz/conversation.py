import speech_recognition as sr
from intent_detector import detectar_intencion
from actions import ejecutar_accion
from tts import hablar
from config import VOZ_ACTIVA

recognizer = sr.Recognizer()


def escuchar_usuario_conversacion():

    if not VOZ_ACTIVA:
        texto = input("Tú: ").strip()
        return texto if texto else "__silencio__"

    try:

        with sr.Microphone() as source:

            print("\n🎤 Escuchando...")

            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)

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