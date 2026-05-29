# voice.py

import pyttsx3

# Inicializar UNA sola vez
engine = pyttsx3.init()

engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)


def hablar(texto):

    if not texto:
        return

    # Detener cualquier cosa pendiente
    engine.stop()

    engine.say(texto)
    engine.runAndWait()