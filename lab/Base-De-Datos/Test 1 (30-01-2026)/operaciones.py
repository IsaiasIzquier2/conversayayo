from database import crear_DB

def insertar_alumnos(alumnos):
    
    conexion, cursor = crear_DB()
    cursor.executemany("INSERT INTO alumnos (nombre, edad) VALUES (?, ?)", alumnos)
    conexion.commit()
    conexion.close()

def eliminar_alumnos(nombres):

    conexion, cursor = crear_DB()
    for nombre in nombres:
        cursor.execute(
            "DELETE FROM alumnos WHERE nombre = ?",
            (nombre,)
        )
    conexion.commit()
    conexion.close()

def actualizar_alumnos(edadACT, alumnoACT):
    
    conexion, cursor = crear_DB()
    cursor.execute("""
    UPDATE alumnos SET edad = ? WHERE nombre = ?
    """,(edadACT, alumnoACT))
    conexion.commit()
    conexion.close()

def mostrar_alumnos():
    conexion, cursor = crear_DB()
    cursor.execute("SELECT * FROM alumnos")
    resultados = cursor.fetchall()
    conexion.close()
    return resultados