#
#   Prototipo de CHATGPT
#


import sqlite3
from datetime import datetime


# ==========================
# BASE DE DATOS
# ==========================

def crear_db():
    conexion = sqlite3.connect("asistente.db")
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mensajes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rol TEXT CHECK(rol IN ('usuario','ia')),
        contenido TEXT NOT NULL,
        fecha_creacion TEXT DEFAULT (datetime('now','localtime'))
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recordatorios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        texto_original TEXT NOT NULL,
        fecha_evento TEXT NOT NULL,
        confirmado INTEGER DEFAULT 0,
        fecha_creacion TEXT DEFAULT (datetime('now','localtime'))
    )
    """)

    conexion.commit()
    return conexion, cursor


# ==========================
# GUARDAR MENSAJES
# ==========================

def guardar_mensaje(rol, contenido):
    conexion, cursor = crear_db()
    cursor.execute("""
        INSERT INTO mensajes (rol, contenido)
        VALUES (?, ?)
    """, (rol, contenido))
    conexion.commit()
    conexion.close()


# ==========================
# GUARDAR RECORDATORIO
# ==========================

def guardar_recordatorio(texto, fecha_evento):
    conexion, cursor = crear_db()
    cursor.execute("""
        INSERT INTO recordatorios (texto_original, fecha_evento, confirmado)
        VALUES (?, ?, 1)
    """, (texto, fecha_evento))
    conexion.commit()
    conexion.close()


# ==========================
# CONSULTAR PRÓXIMO EVENTO
# ==========================

def obtener_proximo_evento():
    conexion, cursor = crear_db()
    cursor.execute("""
        SELECT texto_original, fecha_evento
        FROM recordatorios
        WHERE fecha_evento >= datetime('now')
        AND confirmado = 1
        ORDER BY fecha_evento ASC
        LIMIT 1
    """)
    resultado = cursor.fetchone()
    conexion.close()
    return resultado


# ==========================
# MOSTRAR HISTORIAL
# ==========================

def mostrar_historial():
    conexion, cursor = crear_db()
    cursor.execute("""
        SELECT rol, contenido, fecha_creacion
        FROM mensajes
        ORDER BY fecha_creacion ASC
    """)
    mensajes = cursor.fetchall()
    conexion.close()

    print("\n===== HISTORIAL =====\n")
    for rol, contenido, fecha in mensajes:
        fecha_formateada = datetime.strptime(
            fecha, "%Y-%m-%d %H:%M:%S"
        ).strftime("%d-%m-%Y %H:%M")

        print(f"[{fecha_formateada}] {rol.upper()}: {contenido}")
    print()


# ==========================
# PROGRAMA PRINCIPAL
# ==========================

def main():
    print("Asistente iniciado. Escribe 'salir' para terminar.\n")

    while True:
        mensaje = input("Tú: ")

        if mensaje.lower() == "salir":
            break

        guardar_mensaje("usuario", mensaje)

        # Caso 1: consulta de próximos eventos
        if "tengo algo pronto" in mensaje.lower():
            evento = obtener_proximo_evento()

            if evento:
                texto, fecha_evento = evento
                fecha_formateada = datetime.strptime(
                    fecha_evento, "%Y-%m-%d %H:%M:%S"
                ).strftime("%d-%m-%Y %H:%M")

                respuesta = f"Tienes pendiente: '{texto}' el {fecha_formateada}"
            else:
                respuesta = "No tienes ningún evento próximo."

            print("Asistente:", respuesta)
            guardar_mensaje("ia", respuesta)
            continue

        # Caso 2: detectar palabra clave
        if "recuérdalo" in mensaje.lower():
            print("Asistente: ¿Qué fecha y hora tiene el evento? (Formato: YYYY-MM-DD HH:MM)")
            fecha_input = input("Fecha: ")

            try:
                fecha_obj = datetime.strptime(fecha_input, "%Y-%m-%d %H:%M")
                fecha_evento = fecha_obj.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                print("Formato incorrecto. No se guardó el recordatorio.")
                continue

            print(f"Asistente: ¿Confirmas que quieres guardar este recordatorio para {fecha_evento}? (si/no)")
            confirmacion = input("Confirmar: ")

            if confirmacion.lower() == "si":
                guardar_recordatorio(mensaje, fecha_evento)
                respuesta = "Recordatorio guardado correctamente."
            else:
                respuesta = "Recordatorio cancelado."

            print("Asistente:", respuesta)
            guardar_mensaje("ia", respuesta)
            continue

        # Caso normal (respuesta simulada)
        respuesta = "Estoy aquí contigo 😊"
        print("Asistente:", respuesta)
        guardar_mensaje("ia", respuesta)


if __name__ == "__main__":
    main()