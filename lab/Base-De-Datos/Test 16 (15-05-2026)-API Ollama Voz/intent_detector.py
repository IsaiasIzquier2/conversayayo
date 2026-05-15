import unicodedata
import re


def limpiar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto)
    texto = texto.encode('ascii', 'ignore').decode('utf-8')
    return texto


def contiene_palabra(texto, palabra):
    return bool(re.search(rf'\b{palabra}\b', texto))


def es_pregunta_consulta(texto):
    patrones = [
        "que tengo",
        "qué tengo",
        "tengo algo",
        "algo pendiente",
        "algo pronto",
        "mis citas",
        "mis recordatorios",
        "que hay",
        "que me queda",
    ]
    return any(p in texto for p in patrones)


def detectar_intencion(texto):

    texto = limpiar_texto(texto)

    # BORRAR EVENTO
    if "borra" in texto or "elimina" in texto or "quita" in texto:
        return "borrar_evento"

    # CONSULTAR — va antes que guardar para que "que tengo" no se confunda
    if es_pregunta_consulta(texto) or "agenda" in texto:
        return "consultar_eventos"

    # GUARDAR RECORDATORIO
    if (
        "recuerd" in texto
        or "apunta" in texto
        or "anota" in texto
        or "tengo" in texto
    ):
        return "guardar_recordatorio"

    # HORA
    if contiene_palabra(texto, "hora"):
        return "hora"

    return "charla"