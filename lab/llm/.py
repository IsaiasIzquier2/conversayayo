import requests
import urllib.parse

def llm(prompt: str) -> str:
    # Codificar correctamente el texto (MUY IMPORTANTE)
    prompt_encoded = urllib.parse.quote_plus(prompt)

    url = f"https://text.pollinations.ai/{prompt_encoded}"

    response = requests.get(url, timeout=30)

    # Debug básico por si falla
    if response.status_code != 200:
        return f"ERROR {response.status_code}: {response.text}"

    return response.text.strip()


def main():
    print("LLM Pollinations (escribe 'salir' para terminar)\n")

    while True:
        user_input = input("Tú: ")

        if user_input.lower() == "salir":
            break

        prompt = (
            "Eres un asistente útil. "
            "Responde en español y de forma clara. "
            f"Pregunta: {user_input}"
        )

        respuesta = llm(prompt)
        print("\nIA:", respuesta, "\n")


if __name__ == "__main__":
    main()