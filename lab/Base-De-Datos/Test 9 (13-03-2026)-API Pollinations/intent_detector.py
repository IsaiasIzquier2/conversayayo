def detectar_intencion(texto):

    texto = texto.lower()

    if "recuerd" in texto:
        return "guardar_recordatorio"

    if "tengo algo" in texto or "que tengo" in texto:
        return "consultar_eventos"

    if "hora" in texto:
        return "hora"

    return "charla"