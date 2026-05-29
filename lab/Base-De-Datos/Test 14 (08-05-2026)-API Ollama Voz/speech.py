import speech_recognition as sr

recognizer = sr.Recognizer()


def escuchar_usuario():

    try:

        with sr.Microphone() as source:

            print("\n🎤 Escuchando...")

            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            audio = recognizer.listen(
                source,
                timeout=None,        # no corta por esperar
                phrase_time_limit=10  # permite hablar hasta 10 segundos
            )

        texto = recognizer.recognize_google(
            audio,
            language="es-ES"
        )

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