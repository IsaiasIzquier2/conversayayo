from database import crear_DB


# -----------------------
# VALIDACIONES
# -----------------------

def validar_nombre(nombre):
    return bool(nombre.strip())


def validar_edad(edad):
    return edad >= 0


def alumno_existe(nombre):
    conexion, cursor = crear_DB()
    cursor.execute(
        "SELECT 1 FROM alumnos WHERE nombre = ?",
        (nombre,)
    )
    resultado = cursor.fetchone()
    conexion.close()
    return resultado is not None


# -----------------------
# OPERACIONES CRUD
# -----------------------

def insertar_alumno(nombre, edad):
    conexion, cursor = crear_DB()
    cursor.execute(
        "INSERT INTO alumnos (nombre, edad) VALUES (?, ?)",
        (nombre, edad)
    )
    conexion.commit()
    conexion.close()


def eliminar_alumno(nombre):
    conexion, cursor = crear_DB()
    cursor.execute(
        "DELETE FROM alumnos WHERE nombre = ?",
        (nombre,)
    )
    conexion.commit()
    conexion.close()


def actualizar_alumno(nombre, nueva_edad):
    conexion, cursor = crear_DB()
    cursor.execute(
        "UPDATE alumnos SET edad = ? WHERE nombre = ?",
        (nueva_edad, nombre)
    )
    conexion.commit()
    conexion.close()


def mostrar_alumnos():
    conexion, cursor = crear_DB()
    cursor.execute("SELECT * FROM alumnos")
    resultados = cursor.fetchall()
    conexion.close()
    return resultados