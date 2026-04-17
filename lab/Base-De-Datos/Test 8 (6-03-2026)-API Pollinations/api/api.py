from fastapi import FastAPI
import requests

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

    url = "https://text.pollinations.ai/"

    try:

        response = requests.post(
            url,
            json={"prompt": prompt}
        )

        respuesta = response.text.strip()

        return {"respuesta": respuesta}

    except:

        return {"respuesta": "Lo siento, ahora mismo no puedo responder."}