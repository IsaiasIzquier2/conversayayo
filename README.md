# Conversayayo
[Presentación Conversayayo](https://canva.link/w2surtm6mjc28la)

Conversayayo es un asistente de voz pensado para acompañar a personas de avanzada edad y ayudar a reducir la soledad no deseada. La idea es que cualquier persona mayor pueda conversar con este asistente, sin tocar ninguna pantalla ni teclado, solo con la voz.

---

## Como funciona

El asistente escucha de forma continua hasta que detecta la palabra clave "Conversayayo". En ese momento se activa, responde y empieza a conversar. Incluye gestion de recordatorios y citas, memoria conversacional, y limpieza automatica de eventos pasados cada medianoche.

El modelo de lenguaje corre localmente mediante Ollama, lo que significa que las respuestas no dependen de ninguna API externa de pago.

---

## Funcionalidades

- Activacion por palabra clave ("Conversayayo")
- Conversacion natural en español
- Gestion de recordatorios y citas
- Memoria conversacional entre turnos
- Limpieza automatica de eventos pasados a medianoche
- Modelo de lenguaje local con Ollama, sin APIs de pago
  

---

## Tecnologias utilizadas

| Componente | Desarrollo |
|---|---|
| Reconocimiento de voz (STT) | SpeechRecognition + Google |
| Sintesis de voz (TTS) | edge-tts + pygame |
| Modelo de lenguaje (LLM) | Ollama + llama3.2:3b |
| Base de datos | SQLite |
| Lenguaje principal | Python |

---

## Estructura del proyecto

```
conversayayo/
├── lab/
│   └── Base-De-Datos/
│       └── Test 23 (version final)/
│           ├── api                 # Carpeta API
│           │   └── api.py          # Enlace con la API
│           ├── main.py             # Punto de entrada
│           ├── wakeword.py         # Deteccion de palabra clave
│           ├── speech.py           # Reconocimiento de voz
│           ├── tts.py              # Sintesis de voz
│           ├── conversation.py     # Flujo de conversacion
│           ├── ai.py               # Integracion con Ollama
│           ├── intent_detector.py  # Deteccion de intenciones
│           ├── actions.py          # Ejecucion de acciones
│           ├── memory.py           # Memoria del asistente
│           ├── database.py         # Base de datos
│           ├── date_parser.py      # Interpretacion de fechas
│           ├── config.py           # Configuracion general
│           └── utils.py            # Utilidades
├── web/                            # Interfaz web auxiliar
├── conversayayo.db                 # Base de datos principal
└── README.md
```

---

## Instalacion

### Requisitos previos

- Python 3.11+
- [Ollama](https://ollama.com/) instalado en el sistema
- (Raspberry Pi): micrófono USB y altavoz

### 1. Clonar el repositorio

```bash
git clone https://github.com/IsaiasIzquier2/conversayayo.git
cd conversayayo
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python3 -m venv ~/conversayayo-venv
source ~/conversayayo-venv/bin/activate

pip install pipwin
pipwin install pyaudio
pip install SpeechRecognition
pip install pyaudio

pip install edge-tts pygame

pip install dateparser
```

### 3. Descargar el modelo de lenguaje

```bash
ollama pull llama3.2:3b
```



## Configuracion

En `config.py` se pueden ajustar los parametros principales:

```python
VOZ_ACTIVA = False       # False para modo texto, True para modo voz
TIEMPO_FRASE = 50        # Segundos maximos para completar una frase
TIMEOUT_SILENCIO = 15    # Segundos de silencio antes de suspenderse
MODELO_OLLAMA = "llama3.2:3b"
```

---

## Uso

```bash
source ~/conversayayo-venv/bin/activate
systemctl start ollama

cd conversayayo/lab/Base-De-Datos/Test\ 23*/
python main.py
```

Con `VOZ_ACTIVA = False` el asistente funciona por terminal. Con `VOZ_ACTIVA = True` escucha por microfono y responde por altavoz. En ambos casos, di o escribe "Conversayayo" para activarlo y "adios" para cerrar la conversacion.


## Licencia

Proyecto desarrollado con fines educativos.
