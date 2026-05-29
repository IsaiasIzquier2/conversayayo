# Conversayayo
[Presentación Conversayayo](https://canva.link/w2surtm6mjc28la)

# Conversayayo

Conversayayo es un asistente de voz pensado para acompañar a personas de avanzada edad y ayudar a reducir la soledad no deseada. La idea es simple: que cualquier persona mayor pueda hablarle como si fuera alguien de casa, sin tocar ninguna pantalla ni teclado, solo con la voz.

Este proyecto ha sido desarrollado en grupo como trabajo intermodular de segundo año de Grado Medio.



## ¿Cómo funciona?

El asistente escucha de forma continua hasta que detecta la palabra clave *"Conversayayo"*. En ese momento se activa, responde y empieza a conversar. Todo funciona de forma completamente offline sobre una Raspberry Pi 4, sin mandar ningún dato a internet, lo que garantiza tanto la privacidad como que el dispositivo funcione siempre independientemente de la conexión.

Para el reconocimiento de voz se optó por **Vosk** con un modelo en español, ya que era la opción más ligera y estable para correr en un hardware tan limitado como la Raspberry Pi. Para la síntesis de voz se eligió **Piper**, que genera audio de calidad de forma muy eficiente. Y para el modelo de lenguaje se usó **Ollama** con `llama3.2:3b`, el modelo que mejor equilibrio dio entre calidad de respuesta y recursos consumidos tras comparar varias opciones enfocadas a bajo consumo.



## Funcionalidades

- Activación por palabra clave (*"Conversayayo"*)
- Conversación natural en español
- Gestión de recordatorios y citas
- Memoria conversacional entre turnos
- Completamente offline, sin dependencias de APIs externas
- Interfaz por voz



## Tecnologías utilizadas

| Componente | Tecnología |
|---|---|
| Reconocimiento de voz (STT) | [Vosk](https://alphacephei.com/vosk/) + modelo `vosk-model-small-es-0.42` |
| Síntesis de voz (TTS) | [Piper](https://github.com/rhasspy/piper) + voz `es_ES-mls_9972` |
| Modelo de lenguaje (LLM) | [Ollama](https://ollama.com/) + `llama3.2:3b` |
| Base de datos | SQLite |
| Hardware objetivo | Raspberry Pi 4 |
| Lenguaje principal | Python 3 |



## Estructura del proyecto

```
conversayayo/
 lab/                        # Versiones de desarrollo y pruebas
    Base-De-Datos/
        Test 16 (versión final)/
            main.py             # Punto de entrada
            wakeword.py         # Detección de palabra clave
            speech.py           # Reconocimiento de voz (Vosk)
            tts.py              # Síntesis de voz (Piper)
            conversation.py     # Flujo de conversación
            ai.py               # Integración con Ollama
            intent_detector.py  # Detección de intenciones
            actions.py          # Ejecución de acciones
            memory.py           # Memoria del asistente
            database.py         # Base de datos
            date_parser.py      # Interpretación de fechas
            config.py           # Configuración general
            utils.py            # Utilidades
 web/                        # Interfaz web auxiliar
 conversayayo.db             # Base de datos principal
 README.md
```



## Instalación

### Requisitos previos

- Raspberry Pi 4 con Raspberry Pi OS (Debian 12)
- Micrófono USB
- Altavoz con salida de audio
- Python 3.11+
- [Ollama](https://ollama.com/) instalado en el sistema

### 1. Clonar el repositorio

```bash
git clone https://github.com/IsaiasIzquier2/conversayayo.git
cd conversayayo
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python3 -m venv ~/conversayayo-venv
source ~/conversayayo-venv/bin/activate
pip install vosk sounddevice requests
```

### 3. Descargar el modelo de reconocimiento de voz

```bash
wget https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip
unzip vosk-model-small-es-0.42.zip -d ~/model_stt
```

### 4. Instalar Piper y la voz en español

```bash
# Raspberry Pi 4 (ARM64)
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_arm64.tar.gz
tar -xzf piper_arm64.tar.gz -C ~/piper --strip-components=1

# Modelo de voz
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/es/es_ES/mls_9972/low/es_ES-mls_9972-low.onnx -P ~/
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/es/es_ES/mls_9972/low/es_ES-mls_9972-low.onnx.json -P ~/
```

### 5. Descargar el modelo de lenguaje

```bash
ollama pull llama3.2:3b
```

### 6. Activar el modo de voz

En `config.py` establecer:

```python
VOZ_ACTIVA = True
```

---

## Uso

```bash
# Activar el entorno virtual
source ~/conversayayo-venv/bin/activate

# Asegurarse de que Ollama está corriendo
systemctl start ollama

# Lanzar el asistente
cd conversayayo/lab/Base-De-Datos/Test\ 16*/
python main.py
```

Una vez arrancado, di **"Conversayayo"** para activarlo. Para terminar la conversación di **"adiós"** o **"adiós Conversayayo"**.



## Licencia

Proyecto desarrollado con fines educativos.
