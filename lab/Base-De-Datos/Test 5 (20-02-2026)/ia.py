def responder(mensaje):
    mensaje = mensaje.lower()

    if "hora" in mensaje:
        from datetime import datetime
        return f"Son las {datetime.now().strftime('%H:%M')}"

    if "hola" in mensaje:
        return "Hola 😊 ¿En qué puedo ayudarte?"

    return "Estoy aquí contigo."