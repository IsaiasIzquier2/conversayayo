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

Extrae del texto el evento y la fecha/hora mencionada.

Devuelve SOLO este JSON sin ningún texto adicional:
{{"evento": "nombre del evento", "fecha_raw": "texto exacto de la fecha tal como aparece"}}

Ejemplos:
- "tengo médico el martes a las 10" → {{"evento": "médico", "fecha_raw": "el martes a las 10"}}
- "apunta dentista pasado mañana a las 5 de la tarde" → {{"evento": "dentista", "fecha_raw": "pasado mañana a las 5 de la tarde"}}
- "anota revisión el 3 de junio a las 9" → {{"evento": "revisión", "fecha_raw": "el 3 de junio a las 9"}}

Texto: {texto}
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

        inicio = respuesta.find("{")
        fin = respuesta.rfind("}") + 1

        if inicio == -1 or fin == 0:
            return None

        datos = json.loads(respuesta[inicio:fin])

        return datos

    except Exception as e:
        print("Error interpretando:", e)
        return None