from intent_detector import detectar_intencion
from actions import ejecutar_accion


def iniciar_conversacion():

    while True:

        texto = input("Tú: ")

        if texto.lower() == "adios":
            print("Asistente: Hasta luego 😊")
            break

        intent = detectar_intencion(texto)

        ejecutar_accion(intent, texto)