import unicodedata


def quitar_tildes(texto):
    """
    Convierte:
    recuérdalo → recuerdalo
    """
    texto = unicodedata.normalize('NFD', texto)
    texto = texto.encode('ascii', 'ignore').decode('utf-8')
    return texto


def detectar_intencion(texto):

    texto = texto.lower()
    texto = quitar_tildes(texto)

    if "recuerd" in texto or "avisa" in texto or "apunta" in texto:
        return "guardar_recordatorio"

    if "tengo algo" in texto or "que tengo" in texto:
        return "consultar_eventos"

    if "hora" in texto:
        return "hora"

    return "charla"