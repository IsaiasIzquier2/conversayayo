def detectar_intencion(texto):

    texto = texto.lower()

    if "recuerdalo" in texto or "recuérdalo" in texto:
        return "guardar_recordatorio"

    if "tengo algo" in texto:
        return "consultar_eventos"

    if "hora" in texto:
        return "hora"

    return "charla"