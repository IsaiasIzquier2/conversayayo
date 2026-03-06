from datetime import datetime
from memory import guardar_evento, obtener_eventos


def ejecutar_accion(intent, texto):

    if intent == "guardar_recordatorio":

        fecha = input("Fecha evento (YYYY-MM-DD HH:MM): ")

        guardar_evento(texto, fecha)

        print("Asistente: Perfecto, ya lo he guardado 😊")


    elif intent == "consultar_eventos":

        eventos = obtener_eventos()

        if not eventos:
            print("Asistente: No tienes nada pendiente.")

        else:
            print("Asistente: Esto es lo que tienes apuntado:")

            for evento in eventos:
                print(evento)


    elif intent == "hora":

        ahora = datetime.now()

        print("Asistente: Son las", ahora.strftime("%H:%M"))


    else:

        print("Asistente: Estoy aquí contigo 😊")