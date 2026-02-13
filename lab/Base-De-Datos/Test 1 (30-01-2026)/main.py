from database import crear_tabla
from operaciones import insertar_alumnos, mostrar_alumnos, eliminar_alumnos, actualizar_alumnos

crear_tabla()



def alumnos_añadir():
    alumnos = []
    
    numAlumnos = int(input("Cuantos alumnos quieres añadir: "))

    contador = 0


    while contador < numAlumnos:

        alumnos.append(        
    (
        input("Añade el nombre del nuevo alumno: "),
        int(input("Añade la edad del nuevo alumno: "))
    )
)

        contador += 1

    insertar_alumnos(alumnos)

def alumnos_eliminar():
    numAlumnos = int(input("Cuantos alumnos quieres eliminar: "))

    contador = 0

    nombres = []

    while contador < numAlumnos:

        nombres.append(input("Añade el nombre del Alumno que quieres eliminar: "))

        contador += 1

    eliminar_alumnos(nombres)

def alumnos_actualizar():
    numAlumnos = int(input("Cuantos alumnos quieres actualizar: "))

    contador = 0

    

    while contador < numAlumnos:

        alumnoACT = input("Añade el nombre del Alumno que quieres actualizar: ")

        edadACT = int(input("A que edad lo quieres actualizar: "))

        contador += 1

    actualizar_alumnos(edadACT, alumnoACT)





while True:
    accion = input("Que accion deseas realizar, añadir, eliminar, actualizar, mostrar o salir: ")

    if accion == "añadir":
        alumnos_añadir()

    elif accion == "eliminar":
        alumnos_eliminar()

    elif accion == "actualizar":
        alumnos_actualizar()

    elif accion == "mostrar":
        for alumno in mostrar_alumnos():
            print(alumno)

    elif accion == "salir":
        
        
        break

    
