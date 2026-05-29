import pyttsx3

engine = pyttsx3.init()

engine.setProperty("rate", 170)

engine.say("Hola, esta es una prueba de voz.")
engine.runAndWait()