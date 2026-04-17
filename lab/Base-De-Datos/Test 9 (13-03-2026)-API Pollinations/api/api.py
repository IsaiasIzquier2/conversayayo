from fastapi import FastAPI
import requests
import urllib.parse

app = FastAPI()


@app.get("/")
def inicio():
    return {"mensaje": "API Conversayayo funcionando"}


@app.post("/chat")
def chat(data: dict):

    mensaje = data.get("mensaje")

    prompt = f"""
Eres Conversayayo, un asistente amable para personas mayores.
Habla de forma clara, cercana y sencilla.

Usuario: {mensaje}
Asistente:
"""

    try:

        prompt_encoded = urllib.parse.quote(prompt)

        url = f"https://text.pollinations.ai/{prompt_encoded}"

        response = requests.get(url)

        respuesta = response.text.strip()

        return {"respuesta": respuesta}

    except:

        return {"respuesta": "Lo siento, ahora mismo no puedo responder."}