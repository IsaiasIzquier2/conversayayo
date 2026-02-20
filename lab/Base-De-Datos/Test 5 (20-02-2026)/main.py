#
#   Base de datos, que recuerda un evento y tienes que llamarlo para funcionar.
#


from mensajes import guardar_mensaje
from recordatorios import guardar_recordatorio, obtener_proximo_evento
from ia import responder
from datetime import datetime


def activar_conversacion():
    print("\nConversayayo activado. Di 'adiós' para terminar.\n")

    while True:
        mensaje = input("Tú: ")

        if mensaje.lower() == "adiós":
            print("Conversayayo desactivado.\n")
            break

        guardar_mensaje("usuario", mensaje)

        # Consultar eventos
        if "tengo algo pronto" in mensaje.lower():
            evento = obtener_proximo_evento()

            if evento:
                texto, fecha_evento = evento
                fecha_obj = datetime.strptime(fecha_evento, "%Y-%m-%d %H:%M:%S")
                fecha_formateada = fecha_obj.strftime("%d-%m-%Y %H:%M")
                respuesta = f"Tienes pendiente: '{texto}' el {fecha_formateada}"
            else:
                respuesta = "No tienes ningún evento próximo."

            print("Asistente:", respuesta)
            guardar_mensaje("ia", respuesta)
            continue

        # Guardar recordatorio
        if "recuérdalo" in mensaje.lower():
            print("¿Qué fecha y hora tiene el evento? (YYYY-MM-DD HH:MM)")
            fecha_input = input("Fecha: ")

            try:
                fecha_obj = datetime.strptime(fecha_input, "%Y-%m-%d %H:%M")
                fecha_evento = fecha_obj.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                print("Formato incorrecto.")
                continue

            print(f"¿Confirmas guardar para {fecha_evento}? (si/no)")
            confirmacion = input("Confirmar: ")

            if confirmacion.lower() == "si":
                guardar_recordatorio(mensaje, fecha_evento)
                respuesta = "Recordatorio guardado."
            else:
                respuesta = "Cancelado."

            print("Asistente:", respuesta)
            guardar_mensaje("ia", respuesta)
            continue

        # Respuesta IA simulada
        respuesta = responder(mensaje)
        print("Asistente:", respuesta)
        guardar_mensaje("ia", respuesta)


def main():
    print("Sistema iniciado. Esperando palabra de activación...\n")

    while True:
        entrada = input(">> ")

        if entrada.lower() == "salir":
            break

        if entrada.lower() == "conversayayo":
            activar_conversacion()


if __name__ == "__main__":
    main()