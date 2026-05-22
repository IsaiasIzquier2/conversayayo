import speech_recognition as sr
from tts import hablar
from config import VOZ_ACTIVA

recognizer = sr.Recognizer()

VARIANTES_WAKEWORD = [
    "conversayayo",
    "conversa yayo",
    "conversa ya yo",
    "converse yayo",
    "converse ya yo",
    "conversa llayo",
    "yayo",
    "ya yo",
]


def detectar_wakeword(texto: str) -> bool:
    texto = texto.lower().strip()
    return any(variante in texto for variante in VARIANTES_WAKEWORD)


def escuchar_wakeword():

    if not VOZ_ACTIVA:
        texto = input("\n(Escribe 'conversayayo' para empezar): ")
        return detectar_wakeword(texto)

    print("\n(Esperando 'conversayayo'...)")

    while True:

        try:

            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)

            texto = recognizer.recognize_google(audio, language="es-ES").lower()
            print(f"(Detectado: {texto})")

            if detectar_wakeword(texto):
                return True

        except sr.WaitTimeoutError:
            continue

        except sr.UnknownValueError:
            continue

        except sr.RequestError as e:
            print("Error reconocimiento:", e)
            continue

        except Exception as e:
            print("Error:", e)
            continue