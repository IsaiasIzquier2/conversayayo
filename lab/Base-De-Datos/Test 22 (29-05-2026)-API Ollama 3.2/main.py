from wakeword import escuchar_wakeword
from conversation import iniciar_conversacion


def main():

    print("Dispositivo Conversayayo encendido.")

    while True:

        activar = escuchar_wakeword()

        if activar:
            iniciar_conversacion()


if __name__ == "__main__":
    main()