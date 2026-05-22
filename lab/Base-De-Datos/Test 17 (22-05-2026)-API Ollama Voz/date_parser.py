import re
import requests
from datetime import datetime, timedelta


DIAS_SEMANA = {
    "lunes": 0, "martes": 1, "miércoles": 2, "miercoles": 2,
    "jueves": 3, "viernes": 4, "sábado": 5, "sabado": 5, "domingo": 6
}


def extraer_hora(texto: str):
    """Extrae hora y minuto del texto. Devuelve (hora, minuto) o None."""

    texto = texto.lower()

    patrones = [
        (r'a las (\d{1,2}):(\d{2})', lambda m: (int(m.group(1)), int(m.group(2)))),
        (r'(\d{1,2}):(\d{2})',        lambda m: (int(m.group(1)), int(m.group(2)))),
        (r'a las (\d{1,2}) y media',  lambda m: (int(m.group(1)), 30)),
        (r'a las (\d{1,2}) y cuarto', lambda m: (int(m.group(1)), 15)),
        (r'a las (\d{1,2})',          lambda m: (int(m.group(1)), 0)),
        (r'\b(\d{1,2}) en punto\b',   lambda m: (int(m.group(1)), 0)),
    ]

    for patron, extractor in patrones:
        match = re.search(patron, texto)
        if match:
            hora, minuto = extractor(match)
            if "tarde" in texto or "noche" in texto:
                if hora < 12:
                    hora += 12
            return hora, minuto

    return None


def calcular_fecha(texto: str):
    """
    Intenta calcular la fecha en Python puro.
    Devuelve datetime o None si no puede.
    """

    texto_lower = texto.lower()
    hoy = datetime.now()
    fecha = None

    # Mañana
    if "mañana" in texto_lower:
        fecha = hoy + timedelta(days=1)

    # Pasado mañana
    elif "pasado mañana" in texto_lower:
        fecha = hoy + timedelta(days=2)

    # Día de la semana: "el lunes", "el próximo martes", etc.
    else:
        for nombre_dia, numero_dia in DIAS_SEMANA.items():
            if nombre_dia in texto_lower:
                dias_hasta = (numero_dia - hoy.weekday()) % 7
                if dias_hasta == 0:
                    dias_hasta = 7  # Si hoy es ese día, la próxima semana
                fecha = hoy + timedelta(days=dias_hasta)
                break

    # Fecha concreta: "el 18", "el 18 de mayo", "el 3 de junio"
    if fecha is None:
        meses = {
            "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
            "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
            "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
        }

        # Con mes: "el 18 de mayo"
        match = re.search(r'\b(\d{1,2}) de (\w+)', texto_lower)
        if match:
            dia = int(match.group(1))
            mes_nombre = match.group(2)
            mes = meses.get(mes_nombre)
            if mes:
                año = hoy.year
                candidata = datetime(año, mes, dia)
                if candidata < hoy:
                    candidata = datetime(año + 1, mes, dia)
                fecha = candidata

        # Solo día: "el 18"
        if fecha is None:
            match = re.search(r'\bel (\d{1,2})\b', texto_lower)
            if match:
                dia = int(match.group(1))
                mes = hoy.month
                año = hoy.year
                try:
                    candidata = datetime(año, mes, dia)
                    if candidata.date() <= hoy.date():
                        # Pasar al mes siguiente
                        mes = mes + 1 if mes < 12 else 1
                        año = año if mes > 1 else año + 1
                        candidata = datetime(año, mes, dia)
                    fecha = candidata
                except ValueError:
                    pass

    return fecha


def parsear_fecha(fecha_raw: str):

    if not fecha_raw:
        return None

    # 1. Intentar calcular la fecha en Python
    fecha = calcular_fecha(fecha_raw)

    # 2. Si no podemos, dejar a Ollama como último recurso
    if fecha is None:
        hoy = datetime.now()
        hoy_str = hoy.strftime("%Y-%m-%d %H:%M")
        dias = {
            "Monday": "lunes", "Tuesday": "martes", "Wednesday": "miércoles",
            "Thursday": "jueves", "Friday": "viernes", "Saturday": "sábado",
            "Sunday": "domingo"
        }
        dia_es = dias.get(hoy.strftime("%A"), "")

        prompt = f"""
Hoy es {dia_es} {hoy_str}.

Convierte esta expresión de fecha al formato YYYY-MM-DD HH:MM.
Devuelve SOLO el resultado, sin texto adicional.

Expresión: {fecha_raw}
"""
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "llama3", "prompt": prompt, "stream": False}
            )
            respuesta = response.json()["response"].strip()
            match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', respuesta)
            if match:
                fecha = datetime.strptime(match.group(0), "%Y-%m-%d %H:%M")
        except Exception as e:
            print("Error Ollama fecha:", e)
            return None

    if fecha is None:
        return None

    # 3. Aplicar la hora extraída sobre la fecha calculada
    hora = extraer_hora(fecha_raw)
    if hora:
        fecha = fecha.replace(hour=hora[0], minute=hora[1], second=0, microsecond=0)
    else:
        fecha = fecha.replace(second=0, microsecond=0)

    return fecha


def fecha_a_str(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M")