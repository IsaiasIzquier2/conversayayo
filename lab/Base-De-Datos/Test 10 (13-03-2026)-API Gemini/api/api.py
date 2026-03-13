from fastapi import FastAPI
from .ai import preguntar_ia

app = FastAPI()


@app.get("/")
def inicio():
    return {"mensaje": "API Conversayayo funcionando"}


@app.post("/chat")
def chat(data: dict):

    mensaje = data.get("mensaje")

    respuesta = preguntar_ia(mensaje)

    return {"respuesta": respuesta}