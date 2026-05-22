import speech_recognition as sr
from config import VOZ_ACTIVA

recognizer = sr.Recognizer()


def escuchar_usuario():

    if not VOZ_ACTIVA:
        texto = input("Tú: ").strip()
        return texto

    try:

        with sr.Microphone() as source:

            print("\n🎤 Escuchando...")

            recognizer.adjust_for_ambient_noise(source)

            audio = recognizer.listen(source)

        texto = recognizer.recognize_google(audio, language="es-ES")

        print("Tú:", texto)

        return texto

    except sr.UnknownValueError:
        print("Asistente: No te entendí 😅")
        return ""

    except sr.RequestError as e:
        print("Error reconocimiento:", e)
        return ""

    except Exception as e:
        print("Error:", e)
        return ""