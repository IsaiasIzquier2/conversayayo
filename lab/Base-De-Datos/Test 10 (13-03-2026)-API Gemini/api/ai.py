import google.generativeai as genai

API_KEY = "AIzaSyCLKT6rW8yIgLr2JsSsYo1QQkuh7y8KI9E"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


def preguntar_ia(mensaje):

    prompt = f"""
Eres Conversayayo, un asistente amable para personas mayores.
Habla de forma clara, cercana y sencilla.

Usuario: {mensaje}
Asistente:
"""

    try:

        response = model.generate_content(prompt)

        return response.text

    except:

        return "Ahora mismo no puedo responder."
    
if __name__ == "__main__":

    pregunta = input("Escribe tu pregunta: ")

    respuesta = preguntar_ia(pregunta)

    print("\nRespuesta de la IA:\n")
    print(respuesta)