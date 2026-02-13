from database import conectar_bd

def insertar_alumnos(alumnos):
    
    conexion, cursor = conectar_bd()
    cursor.executemany("INSERT INTO alumnos (nombre, edad) VALUES (?, ?)", alumnos)
    conexion.commit()
    conexion.close()

def mostrar_alumnos():
    conexion, cursor = conectar_bd()
    cursor.execute("SELECT * FROM alumnos")
    resultados = cursor.fetchall()
    conexion.close()
    return resultados
