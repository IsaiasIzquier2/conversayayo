import unicodedata


def limpiar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto)
    texto = texto.encode('ascii', 'ignore').decode('utf-8')
    return texto


def detectar_intencion(texto):

    texto = limpiar_texto(texto)

    # GUARDAR RECORDATORIO
    if "recuerd" in texto or "apunta" in texto or "anota" in texto:
        return "guardar_recordatorio"
    
    # BORRAR EVENTO
    if "borra" in texto or "elimina" in texto or "quita" in texto:
        return "borrar_evento"

    # CONSULTAR EVENTOS
    if (
        "que tengo" in texto
        or "tengo algo" in texto
        or "algo pronto" in texto
        or "cita" in texto
        or "agenda" in texto
        or "recordatorio" in texto
    ):
        return "consultar_eventos"

    # HORA
    if "hora" in texto:
        return "hora"

    return "charla"

