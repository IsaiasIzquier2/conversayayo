import speech_recognition as sr
import re
import unicodedata

recognizer = sr.Recognizer()


def limpiar_texto(texto):

    texto = texto.lower()

    # Quitar tildes
    texto = unicodedata.normalize("NFD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")

    # Quitar espacios
    texto = re.sub(r"\s+", "", texto)

    return texto


def escuchar_wakeword():

    try:

        with sr.Microphone() as source:

            print("\n🎧 Diga 'conversayayo' para activar...")

            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            audio = recognizer.listen(
                source,
                timeout=5,          # espera máximo 5s para empezar
                phrase_time_limit=5
            )

        texto = recognizer.recognize_google(
            audio,
            language="es-ES"
        )

        print("Detectado:", texto)

        texto_limpio = limpiar_texto(texto)

        # Variantes permitidas
        if (
            "conversayayo" in texto_limpio
            or "conversaya yo" in texto_limpio
            or "conversaya" in texto_limpio
            or "Converse a Yayo" in texto_limpio
            or "conversación" in texto_limpio
            or "Converso Yayo" in texto_limpio  
            or "conversayayo" == texto_limpio
        ):

            print("🟢 Asistente activado")
            return True

        return False

    except:

        return False