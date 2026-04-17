from datetime import datetime
from memory import guardar_evento, obtener_eventos
from utils import formatear_fecha
from ai import interpretar_evento, confirmar_evento_ia


def ejecutar_accion(intent, texto):

    # ==========================
    # GUARDAR RECORDATORIO (INTELIGENTE)
    # ==========================
    if intent == "guardar_recordatorio":

        datos = interpretar_evento(texto)

        if not datos or "fecha" not in datos:
            print("Asistente: No he entendido bien la fecha 😅")
            return

        texto_evento = datos.get("evento", texto)
        fecha = datos.get("fecha")

        # Confirmación con IA (respuesta natural)
        confirmacion = confirmar_evento_ia(texto_evento, fecha)
        print("Asistente:", confirmacion)

        respuesta_usuario = input("¿Es correcto? (si/no): ").lower()

        if respuesta_usuario == "si":
            guardar_evento(texto_evento, fecha)
            print("Asistente: Perfecto, ya lo he guardado 😊")
        else:
            print("Asistente: Vale, dime de nuevo la cita 😊")


    # ==========================
    # CONSULTAR EVENTOS
    # ==========================
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


    # ==========================
    # HORA
    # ==========================
    elif intent == "hora":

        ahora = datetime.now()
        print("Asistente: Son las", ahora.strftime("%H:%M"))


    # ==========================
    # CHARLA NORMAL
    # ==========================
    else:

        from ai import preguntar_ia

        respuesta = preguntar_ia(texto)

        print("Asistente:", respuesta)