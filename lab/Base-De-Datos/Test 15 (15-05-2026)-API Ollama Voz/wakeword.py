import speech_recognition as sr
from tts import hablar

recognizer = sr.Recognizer()


def escuchar_wakeword():

    print("\n(Esperando 'conversayayo'...)")

    while True:

        try:

            with sr.Microphone() as source:

                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)

            texto = recognizer.recognize_google(audio, language="es-ES").lower()

            print(f"(Detectado: {texto})")

            if "conversa yayo" or "conversar yayo" or "conversa ya yo" or "conversar ya yo" or "con berta yayo" in texto:
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