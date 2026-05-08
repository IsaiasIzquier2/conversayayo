from intent_detector import detectar_intencion
from actions import ejecutar_accion
from speech import escuchar_usuario


def iniciar_conversacion():

    while True:

        texto = escuchar_usuario()

        if not texto:
            continue

        if texto.lower() == "adios":

            print("Asistente: Hasta luego 😊")

            break

        intent = detectar_intencion(texto)

        ejecutar_accion(intent, texto)