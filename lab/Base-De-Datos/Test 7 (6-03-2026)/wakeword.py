def escuchar_wakeword():

    texto = input("\n(Esperando 'conversayayo'): ").lower()

    if "conversayayo" in texto:
        print("Asistente: Sí, dime 😊")
        return True

    return False