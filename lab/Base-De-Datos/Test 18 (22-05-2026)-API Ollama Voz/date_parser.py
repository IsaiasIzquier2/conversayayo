import re
import requests
from datetime import datetime, timedelta


DIAS_SEMANA = {
    "lunes": 0, "martes": 1, "miércoles": 2, "miercoles": 2,
    "jueves": 3, "viernes": 4, "sábado": 5, "sabado": 5, "domingo": 6
}


def extraer_hora(texto: str):

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

    texto_lower = texto.lower()
    hoy = datetime.now()
    fecha = None

    # Mañana / pasado mañana
    if "pasado mañana" in texto_lower:
        fecha = hoy + timedelta(days=2)
    elif "mañana" in texto_lower:
        fecha = hoy + timedelta(days=1)

    # Fecha con día de la semana Y número: "lunes 25", "el lunes 25 de mayo"
    # Si viene el número concreto del día, nos fiamos del número
    if fecha is None:
        meses = {
            "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
            "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
            "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
        }

        # Con día, mes y año: "25 de mayo de 2026"
        match = re.search(r'\b(\d{1,2}) de (\w+) de (\d{4})', texto_lower)
        if match:
            dia = int(match.group(1))
            mes = meses.get(match.group(2))
            año = int(match.group(3))
            if mes:
                try:
                    fecha = datetime(año, mes, dia)
                except ValueError:
                    pass

        # Con día y mes: "el 25 de mayo"
        if fecha is None:
            match = re.search(r'\b(\d{1,2}) de (\w+)', texto_lower)
            if match:
                dia = int(match.group(1))
                mes = meses.get(match.group(2))
                if mes:
                    año = hoy.year
                    try:
                        candidata = datetime(año, mes, dia)
                        if candidata.date() < hoy.date():
                            candidata = datetime(año + 1, mes, dia)
                        fecha = candidata
                    except ValueError:
                        pass

        # Solo número de día: "el 25", "el lunes 25"
        if fecha is None:
            match = re.search(r'\b(\d{1,2})\b', texto_lower)
            if match:
                dia = int(match.group(1))
                if 1 <= dia <= 31:
                    mes = hoy.month
                    año = hoy.year
                    try:
                        candidata = datetime(año, mes, dia)
                        if candidata.date() < hoy.date():
                            mes = mes + 1 if mes < 12 else 1
                            año = año if mes > 1 else año + 1
                            candidata = datetime(año, mes, dia)
                        fecha = candidata
                    except ValueError:
                        pass

    # Solo día de la semana sin número: "el lunes", "el martes que viene"
    if fecha is None:
        for nombre_dia, numero_dia in DIAS_SEMANA.items():
            if nombre_dia in texto_lower:
                dias_hasta = (numero_dia - hoy.weekday()) % 7
                if dias_hasta == 0:
                    dias_hasta = 7
                fecha = hoy + timedelta(days=dias_hasta)
                break

    return fecha


def parsear_fecha(fecha_raw: str):

    if not fecha_raw:
        return None

    fecha = calcular_fecha(fecha_raw)

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

    hora = extraer_hora(fecha_raw)
    if hora:
        fecha = fecha.replace(hour=hora[0], minute=hora[1], second=0, microsecond=0)
    else:
        fecha = fecha.replace(second=0, microsecond=0)

    return fecha


def fecha_a_str(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M")