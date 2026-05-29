from fastapi import FastAPI
import requests
from config import MODELO_OLLAMA

app = FastAPI()


@app.get("/")
def inicio():
    return {"mensaje": "API Conversayayo funcionando con Ollama"}


@app.post("/chat")
def chat(data: dict):

    mensaje = data.get("mensaje")

    prompt = f"""
Eres Conversayayo, un asistente para personas mayores.

Reglas IMPORTANTES:
- Responde SIEMPRE en 1 o 2 frases máximo
- Sé claro, cercano y breve
- No des explicaciones largas
- No hagas listas
- No hagas preguntas innecesarias
- Usa un tono amable y sencillo

Usuario: {mensaje}
Asistente:
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

        respuesta = response.json()["response"]

        return {"respuesta": respuesta.strip()}

    except Exception as e:

        print("ERROR:", e)

        return {"respuesta": "Ahora mismo estoy un poco lento 😅"}