#
#   En esta base de datos, se pueden realizar todas las acciones, solo con alumnos y su edad, y se registra el horario de la entrada y cuando se actualiza también.
#

from datetime import datetime
from database import crear_tabla
from operaciones import (
    insertar_alumno,
    eliminar_alumno,
    actualizar_alumno,
    mostrar_alumnos,
    validar_nombre,
    validar_edad,
    alumno_existe
)

crear_tabla()


def añadir():
    nombre = input("Nombre del alumno: ")

    if not validar_nombre(nombre):
        print(" El nombre no puede estar vacío.")
        return

    if alumno_existe(nombre):
        print(" Ese alumno ya existe.")
        return

    try:
        edad = int(input("Edad del alumno: "))
    except ValueError:
        print(" La edad debe ser un número.")
        return

    if not validar_edad(edad):
        print(" La edad no puede ser negativa.")
        return

    insertar_alumno(nombre, edad)
    print(" Alumno añadido correctamente.")


def eliminar():
    nombre = input("Nombre del alumno a eliminar: ")

    if not alumno_existe(nombre):
        print(" Ese alumno no existe.")
        return

    confirmar = input("¿Seguro que quieres eliminarlo? (s/n): ")

    if confirmar.lower() == "s":
        eliminar_alumno(nombre)
        print(" Alumno eliminado.")


def actualizar():
    nombre = input("Nombre del alumno a actualizar: ")

    if not alumno_existe(nombre):
        print(" Ese alumno no existe.")
        return

    try:
        nueva_edad = int(input("Nueva edad: "))
    except ValueError:
        print(" La edad debe ser un número.")
        return

    if not validar_edad(nueva_edad):
        print(" Edad no válida.")
        return

    actualizar_alumno(nombre, nueva_edad)
    print(" Alumno actualizado.")


def mostrar():
    alumnos = mostrar_alumnos()

    if not alumnos:
        print("No hay alumnos registrados.")
        return

    print("\n========== LISTA DE ALUMNOS ==========\n")

    for alumno in alumnos:
        id_, nombre, edad, fecha_creacion, fecha_actualizacion = alumno

        # Formatear fecha de creación
        fecha_creacion = datetime.strptime(
            fecha_creacion,
            "%Y-%m-%d %H:%M:%S"
        ).strftime("%d-%m-%Y %H:%M")

        # Formatear fecha de actualización si existe
        if fecha_actualizacion:
            fecha_actualizacion = datetime.strptime(
                fecha_actualizacion,
                "%Y-%m-%d %H:%M:%S"
            ).strftime("%d-%m-%Y %H:%M")
        else:
            fecha_actualizacion = "Nunca"

        print("----------------------------------------")
        print(f"ID: {id_}")
        print(f"Nombre: {nombre}")
        print(f"Edad: {edad}")
        print(f"Creado: {fecha_creacion}")
        print(f"Actualizado: {fecha_actualizacion}")

    print("----------------------------------------")


# -----------------------
# MENÚ PRINCIPAL
# -----------------------

while True:
    print("\n1 - Añadir")
    print("2 - Eliminar")
    print("3 - Actualizar")
    print("4 - Mostrar")
    print("5 - Salir")

    opcion = input("Elige una opción: ")

    if opcion == "1":
        añadir()

    elif opcion == "2":
        eliminar()

    elif opcion == "3":
        actualizar()

    elif opcion == "4":
        mostrar()

    elif opcion == "5":
        print("Saliendo...")
        break

    else:
        print(" Opción no válida.")