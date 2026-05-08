import requests
import json


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

    prompt = f"""
Extrae la información del evento.

Reglas:
- El campo "evento" debe ser solo el evento, sin frases como "tengo".
- Ejemplos válidos: "cita médica", "dentista", "reunión".
- No uses verbos.

Devuelve SOLO JSON:

{{
  "evento": "...",
  "fecha": "YYYY-MM-DD HH:MM"
}}

Usuario: {texto}
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

        # Intentar convertir a JSON
        datos = json.loads(respuesta)

        return datos

    except Exception as e:
        print("Error interpretando:", e)
        return None


# ==========================
# CONFIRMAR EVENTO (IA)
# ==========================
def confirmar_evento_ia(evento, fecha):

    prompt = f"""
Genera una frase corta confirmando un evento.

Ejemplo:
"Tienes una cita médica el 24/06/2026 a las 10:30, ¿es correcto?"

Evento: {evento}
Fecha: {fecha}
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

        return response.json()["response"].strip()

    except:
        return f"Tienes '{evento}' el {fecha}, ¿es correcto?"