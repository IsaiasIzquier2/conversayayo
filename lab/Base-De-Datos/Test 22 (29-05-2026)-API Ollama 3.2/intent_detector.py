import unicodedata
import re


PALABRAS_DIA = [
    "mañana", "pasado mañana", "lunes", "martes", "miércoles", "miercoles",
    "jueves", "viernes", "sábado", "sabado", "domingo", "hoy"
]

PALABRAS_EVENTO = [
    "cita", "médico", "medico", "dentista", "farmacia", "reunion", "reunión",
    "revisión", "revision", "operación", "operacion", "consulta", "clase",
    "cumpleaños", "cumpleanos", "boda", "viaje", "quedada", "quedado"
]


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


def es_consulta_por_fecha(texto):
    """
    Detecta preguntas sobre un día concreto:
    - "mañana tengo algo que hacer"
    - "el lunes tengo algo"
    - "hoy tengo algo pendiente"
    - "qué tengo el lunes"
    - "tengo algo mañana"
    """

    tiene_dia = any(dia in texto for dia in PALABRAS_DIA)

    if not tiene_dia:
        return False

    # Patrones de consulta (más amplios)
    patrones_consulta = [
        r'tengo algo',
        r'tengo cosas',
        r'tengo que hacer',
        r'tengo plan',
        r'hay algo',
        r'que tengo',
        r'tengo pendiente',
        r'tengo programado',
        r'estoy libre',
        r'tengo hueco',
    ]

    for patron in patrones_consulta:
        if re.search(patron, texto):
            return True

    return False


def es_nuevo_evento(texto):
    """
    Detecta que el usuario está creando un evento nuevo.
    Busca que haya un evento concreto mencionado junto con una hora.
    """

    tiene_evento = any(ev in texto for ev in PALABRAS_EVENTO)
    tiene_hora = bool(re.search(r'a las \d|(\d{1,2}:\d{2})', texto))
    tiene_trigger = any(p in texto for p in [
        "recuerd", "apunta", "anota", "recuérdame", "apúntame"
    ])

    # Si tiene trigger explícito siempre es guardar
    if tiene_trigger:
        return True

    # Si tiene evento concreto Y hora, es guardar
    if tiene_evento and tiene_hora:
        return True

    return False


def detectar_intencion(texto):

    texto = limpiar_texto(texto)

    print(f"[DEBUG INTENT] '{texto}'")

    # BORRAR EVENTO
    if "borra" in texto or "elimina" in texto or "quita" in texto:
        print("[DEBUG INTENT] → borrar_evento")
        return "borrar_evento"

    # GUARDAR — tiene prioridad si hay trigger explícito o evento+hora
    if es_nuevo_evento(texto):
        print("[DEBUG INTENT] → guardar_recordatorio")
        return "guardar_recordatorio"

    # CONSULTAR POR FECHA CONCRETA
    if es_consulta_por_fecha(texto):
        print("[DEBUG INTENT] → consultar_por_fecha")
        return "consultar_por_fecha"

    # CONSULTAR GENERAL
    if es_pregunta_consulta(texto) or "agenda" in texto:
        print("[DEBUG INTENT] → consultar_eventos")
        return "consultar_eventos"

    # GUARDAR — si solo tiene "tengo" sin ser consulta
    if "tengo" in texto:
        print("[DEBUG INTENT] → guardar_recordatorio")
        return "guardar_recordatorio"

    # HORA
    if contiene_palabra(texto, "hora"):
        print("[DEBUG INTENT] → hora")
        return "hora"

    print("[DEBUG INTENT] → charla")
    return "charla"