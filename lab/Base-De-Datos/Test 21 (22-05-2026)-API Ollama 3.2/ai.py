import requests
import json
from datetime import datetime
from config import MODELO_OLLAMA

DIAS_ES = {
    "Monday": "lunes", "Tuesday": "martes", "Wednesday": "miércoles",
    "Thursday": "jueves", "Friday": "viernes", "Saturday": "sábado",
    "Sunday": "domingo"
}

MESES_ES = {
    "January": "enero", "February": "febrero", "March": "marzo",
    "April": "abril", "May": "mayo", "June": "junio",
    "July": "julio", "August": "agosto", "September": "septiembre",
    "October": "octubre", "November": "noviembre", "December": "diciembre"
}


def fecha_hoy_completa():
    hoy = datetime.now()
    dia_semana = DIAS_ES.get(hoy.strftime("%A"), "")
    dia = hoy.day
    mes = MESES_ES.get(hoy.strftime("%B"), "")
    año = hoy.year
    hora = hoy.strftime("%H:%M")
    return f"{dia_semana} {dia} de {mes} de {año}, son las {hora}"


# ==========================
# CHAT NORMAL
# ==========================
def preguntar_ia(mensaje):

    hoy = fecha_hoy_completa()

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": MODELO_OLLAMA,
                "prompt": f"""
Hoy es {hoy}.

Eres un asistente para personas mayores. Responde en 1 o 2 frases máximo. Sé claro, cercano y breve.

Usuario: {mensaje}
Asistente:
""",
                "stream": False
            }
        )

        return response.json()["response"].strip()

    except:
        return "Ahora mismo no puedo pensar bien."


# ==========================
# INTERPRETAR EVENTO (IA)
# ==========================
def interpretar_evento(texto):

    hoy = datetime.now().strftime("%Y-%m-%d %H:%M")

    prompt = f"""
Hoy es {hoy}.

Tu tarea es extraer el evento y la fecha de este texto.

Devuelve SOLO este JSON, sin explicaciones, sin texto antes ni después:
{{"evento": "nombre corto del evento", "fecha_raw": "expresión de fecha y hora tal como aparece en el texto"}}

Ejemplos:
- "el próximo lunes tengo médico a las 10" → {{"evento": "médico", "fecha_raw": "el próximo lunes a las 10"}}
- "apunta dentista pasado mañana a las 5 de la tarde" → {{"evento": "dentista", "fecha_raw": "pasado mañana a las 5 de la tarde"}}
- "tengo una cita el 3 de junio a las 9" → {{"evento": "cita", "fecha_raw": "el 3 de junio a las 9"}}
- "el lunes 25 a las 10 de la mañana tengo revisión" → {{"evento": "revisión", "fecha_raw": "el lunes 25 a las 10 de la mañana"}}

Texto: {texto}

JSON:
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": MODELO_OLLAMA,
                "prompt": prompt,
                "stream": False
            }
        )

        respuesta = response.json()["response"].strip()

        print(f"[DEBUG] Ollama respondió: {respuesta}")

        inicio = respuesta.find("{")
        fin = respuesta.rfind("}") + 1

        if inicio == -1 or fin == 0:
            print("[DEBUG] No se encontró JSON en la respuesta")
            return None

        json_str = respuesta[inicio:fin]
        datos = json.loads(json_str)

        print(f"[DEBUG] Evento: {datos.get('evento')} | Fecha raw: {datos.get('fecha_raw')}")

        return datos

    except Exception as e:
        print(f"[DEBUG] Error interpretando: {e}")
        return None