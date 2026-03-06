import requests


def preguntar_ia(mensaje):

    url = "http://127.0.0.1:8000/chat"

    data = {
        "mensaje": mensaje
    }

    try:

        response = requests.post(url, json=data)

        respuesta = response.json()["respuesta"]

        return respuesta

    except:

        return "Ahora mismo no puedo pensar bien."