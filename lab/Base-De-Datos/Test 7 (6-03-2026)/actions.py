from datetime import datetime
from memory import guardar_evento, obtener_eventos
from utils import formatear_fecha


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
            print("Asistente: Esto es lo que tienes apuntado:\n")

            for texto_evento, fecha in eventos:

                fecha_bonita = formatear_fecha(fecha)

                print(f"📌 {texto_evento}")
                print(f"   🕒 {fecha_bonita}")
                print()


    elif intent == "hora":

        ahora = datetime.now()

        print("Asistente: Son las", ahora.strftime("%H:%M"))


    else:

        print("Asistente: Estoy aquí contigo 😊")