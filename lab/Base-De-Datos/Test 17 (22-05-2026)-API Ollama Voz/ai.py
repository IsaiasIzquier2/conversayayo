import requests
import json
from datetime import datetime


# ==========================
# CHAT NORMAL
# ==========================
def preguntar_ia(mensaje):

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": f"""
Responde en 1 o 2 frases máximo. Sé claro y breve.

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
                "model": "llama3",
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