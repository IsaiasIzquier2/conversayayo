import time
import unicodedata
import re

from intent_detector import detectar_intencion
from actions import ejecutar_accion
from speech import escuchar_usuario


TIEMPO_MAXIMO_SILENCIO = 20


def limpiar_texto(texto):

    texto = texto.lower()

    texto = unicodedata.normalize("NFD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")

    texto = re.sub(r"\s+", "", texto)

    return texto


def iniciar_conversacion():

    print("\n🟢 Modo conversación activado.")
    print("Di 'adios conversayayo' para salir.\n")

    ultimo_tiempo = time.time()

    while True:

        # Si pasan 20 segundos sin hablar
        if time.time() - ultimo_tiempo > TIEMPO_MAXIMO_SILENCIO:

            print("\n⏳ Tiempo de inactividad. Volviendo al modo espera.")
            break

        texto = escuchar_usuario()

        if not texto:
            continue

        ultimo_tiempo = time.time()

        texto_limpio = limpiar_texto(texto)

        # Variantes de salida
        if (
            "adiosconversayayo" in texto_limpio
            or "adiosconversaya yo" in texto_limpio
            or "adiosconversaya" in texto_limpio
        ):

            print("Asistente: Hasta luego 😊")
            break

        intent = detectar_intencion(texto)

        ejecutar_accion(intent, texto)