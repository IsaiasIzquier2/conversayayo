from wakeword import escuchar_wakeword
from conversation import iniciar_conversacion


def main():

    print("Dispositivo Conversayayo encendido.")

    while True:

        print("\n🔵 Esperando palabra clave...")

        activar = escuchar_wakeword()

        if activar:

            iniciar_conversacion()


if __name__ == "__main__":
    main()