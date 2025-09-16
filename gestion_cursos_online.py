class Usuario:  # Clase base para Instructor y Estudiante
    def __init__(self, nombre, correo, telefono):
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    def mostrar_datos(self):
        pass

class Curso:
    def __init__(self, nombre_curso, codigo_curso):
        self.nombre_curso = nombre_curso
        self.__codigo_curso = codigo_curso
        self.instructor = None
        self.estudiantes = [] # almacenar carnets de estudiantes para su posterior búsqueda
        self.tarea = [] #almacena objetos de tareas
        self.evaluacion = [] #almacena objetos de evaluaciones

    @property
    def codigo_curso(self):
        return self.__codigo_curso

    @codigo_curso.setter
    def codigo_curso(self, new_codigo_curso):
        self.__codigo_curso = new_codigo_curso

    def asignar_instructor(self, instructor):
        self.instructor = instructor

    def mostrar_datos_curso(self):
        return f"Curso: {self.nombre_curso} | Código: {self.codigo_curso} | Instructor: {self.instructor.nombre if self.instructor else 'Sin asignar'}"

class Estudiante(Usuario):
    def __init__(self, nombre, correo, telefono, carnet):
        super().__init__(nombre, correo, telefono)
        self._carnet = carnet
        self.cursos_inscritos ={} #almacena los cursos como objeto, junto con una nota asignada por el instructor

    def mostrar_datos(self):
        if self.cursos_inscritos:
            nombres_cursos = []
            for curso in self.cursos_inscritos:
                nombres_cursos.append(curso.nombre_curso)
            cursos = ", ".join(nombres_cursos)
        else:
            cursos = "Ninguno"

        return f"Estudiante | Carnet: {self._carnet} | {super().mostrar_datos()} | Cursos: {cursos}"

class RegistroEstudiante:
    def __init__(self):
        self.estudiantes_registrados={}#almacena todos los objetos de estudiantes

    def registrar_est(self):
        carnet=input("Ingrese su carnet: ")#validacion de existencia
        nombre=input("Ingrese su nombre: ")
        correo=input("Ingrese su correo: ")
        telefono=input("Ingrese su telefono: ")

        estudiante = Estudiante(nombre, correo, telefono, carnet)
        self.estudiantes_registrados[carnet]=estudiante
        print(f"El estudiante {nombre} registrado con su carnet {carnet} correctamente\n")

    def mostrar_cursos(self, carnet):
        obj_estudiante = self.estudiantes_registrados[carnet]

        if not obj_estudiante.cursos_inscritos:
            print("El estudiante no tiene cursos asignados.")

        else:
            for i, (codigo, datos) in enumerate(obj_estudiante.cursos_inscritos.items(), start=1):
                print(f"{i}.<{codigo}> - {datos['Nombre']}")
            print("")

    def asignar_curso(self, carnet, curso):
        obj_estudiante=self.estudiantes_registrados[carnet] # REGISTRA LOS ESTUDIOS CON LA LLAVE PRIMARIA DE CARNETS
        curso.estudiantes.append(carnet)
        obj_estudiante.cursos_inscritos[curso.codigo_curso]={
            "Nombre": curso.nombre_curso,
            "Nota": 0,
        }
        print(f"Curso {curso.nombre_curso} asignado correctamente\n")

    def mostrar_notas(self, carnet):
        obj_estudiante = self.estudiantes_registrados[carnet]
        if not obj_estudiante.cursos_inscritos:
            print(f"El estudiante {obj_estudiante._carnet} no tiene cursos asignados.\n")
        else:
            print(f"Notas de cursos del estudiante {obj_estudiante._carnet}:\n")

            for codigo, datos in obj_estudiante.cursos_inscritos.items():
                print(f" ➡️ {datos['Nombre']} ({codigo}): {datos['Nota']}")
            print("")

class Instructor(Usuario):
    def __init__(self, nombre, correo, telefono, codigo, profesion):
        super().__init__(nombre, correo, telefono)
        self._codigo = codigo
        self._profesion = profesion
        self._cursos_impartidos = []

    @property
    def codigo(self):
        return self._codigo

    def asignar_curso(self, curso):
        self._cursos_impartidos.append(curso)
        curso.asignar_instructor(self)

    def mostrar_datos(self):
        if self._cursos_impartidos:
            nombres_cursos = []
            for curso in self._cursos_impartidos:
                nombres_cursos.append(curso.nombre_curso)
            cursos = ", ".join(nombres_cursos)
        else:
            cursos = "Ninguno"
        return f"Instructor | Código: {self._codigo} | Profesión: {self._profesion} | {super().mostrar_datos()} | Cursos: {cursos}"

class RegistroInstructor:
    def __init__(self):
        self.instructores_registrados = {}

    def registrar_instructor(self):
        print("\n--- Registro de Instructor ---")
        codigo = input("Código de Instructor: ")
        nombre = input("Nombre: ")
        correo = input("Correo: ")
        telefono = input("Teléfono: ")
        profesion = input("Profesión: ")

        instructor = Instructor(nombre, correo, telefono, codigo, profesion)
        self.instructores_registrados[codigo] = instructor
        print(f"Instructor {nombre} registrado con éxito\n")

    def obtener_instructor(self, codigo):
        if codigo in self.instructores_registrados:
            return self.instructores_registrados[codigo]
        else:
            return None

    def crear_evaluacion(self, curso): #objeto de curso, que se necesita ingresar para luego verificar si esta dentro de sus cursos impartidos (a realizar) en el menú
    # agregar evaluacion al objeto del curso
        evaluacion=input("Ingrese el nombre de la evaluacion: ")
        obj_evaluacion=Evaluacion(evaluacion)
        curso.evaluacion.append(obj_evaluacion)



class Administrador(Usuario):
    def __init__(self):
        super().__init__("Admin", None, 11110000)
        self._codigo_ingreso = "администратор007"
        self._cursos_creados = []

    @property
    def codigo_ingreso(self):
        return self._codigo_ingreso

    def crear_curso(self):
        nombre = input("Nombre de curso: ")
        codigo_curso = input("Codigo de curso: ")
        curso = Curso(nombre, codigo_curso)
        self._cursos_creados.append(curso)
        print(f"Curso: {nombre} creado con exito")

    def asignar_curso_a_instructor(self, instructores_registrados):
        if not self._cursos_creados:
            print("No hay cursos registrados")
            return
        if not instructores_registrados:
            print("No hay instructores registrados")
            return
        codigo_curso = input("Codigo de curso: ")
        codigo_instructor = input("Codigo de instructor: ")

        Curso_ADM = None
        for curso in self._cursos_creados:
            if curso.codigo_curso == codigo_curso:
                Curso_ADM = curso
                break

        if Curso_ADM and codigo_instructor in instructores_registrados:
            instructor = instructores_registrados[codigo_instructor]
            instructor.asignar_curso(Curso_ADM)
            print(f"Curso: {Curso_ADM.nombre_curso} asignado a instructor: {instructor.nombre}")
        else:
            print("No hay cursos registrados")

class Evaluacion:
    def __init__(self, nombre):
        self.nombre = nombre

    def mostrar_evaluacion(self):
        print(f"Evaluación: {self.nombre}")

class Examen(Evaluacion):
    def __init__(self, nombre, duracion):
        super().__init__(nombre)
        self._duracion = duracion

    @property
    def duracion(self):
        return self._duracion

    def mostrar_info(self):
        return f"Examen: {self.nombre} | Duración: {self._duracion} min"

class Tarea(Evaluacion):
    def __init__(self, nombre, fecha_entrega):
        super().__init__(nombre)
        self._fecha_entrega = fecha_entrega

    @property
    def fecha_entrega(self):
        return self._fecha_entrega

    def mostrar_info(self):
        return f"Tarea: {self.nombre} | Fecha de entrega: {self._fecha_entrega}"

admin=Administrador()

obj_estudiantes=RegistroEstudiante()
#instructores_registrados = {}#pendiente de la parte de instructores
obj_instructor = RegistroInstructor()

while True:
    print("----🛜 PORTAL CURSOS ONLINE 🛜----")

    print("Iniciar sesión\n")
    print("1. Administrador")
    print("2. Instructor")
    print("3. Estudiante")
    print("4. Salir")

    opcion1 = input("\nSeleccione su tipo de usuario: ")

    match opcion1:
        case "1":
            codigo = input("Ingrese su código de admin: ")

            if codigo == admin.codigo_ingreso:
                while True:
                    print("--Portal del ADMIN 🤑🤑--\n")
                    print("1. Crear curso")
                    print("2. Asignar curso a instructor")
                    print("3. Reporte de notas")
                    print("4. Salir")

                    opcion2 = input("\nSeleccione lo que desee: ")

                    match opcion2:
                        case "1":
                            admin.crear_curso()
                        case "2":
                            admin.asignar_curso_a_instructor(obj_instructor.instructores_registrados)
                        case "3":
                            print("Reporte de promedio de notas")
                        case "4":
                            print("Saliendo del portal admin....")
                            break
                        case _:
                            print("Opcion no valida")
            else:
                print("Código incorrecto ✖️")

        case "2":
            while True:
                print("\n--Portal Instructor 👨‍🏫👩‍🏫--\n")
                print("1. Registrar usuario")
                print("2. Acceder al portal")
                print("3. Salir")

                opcion3 = input("\nInicie sesión: ")

                match opcion3:
                    case "1":
                        obj_instructor.registrar_instructor()

                    case "2":
                        codigo_instructor = input("Ingrese su código de instructor: ")
                        instructor = obj_instructor.obtener_instructor(codigo_instructor)

                        if instructor:
                            while True:
                                print(f"\nBienvenido {instructor.nombre} 👋")
                                print("1. Añadir evaluación a su curso")
                                print("2. Añadir notas")
                                print("3. Añadir reportes")
                                print("4. Salir")

                                option4 = input("\nSeleccione una opción: ")

                                match option4:
                                    case "1":
                                        print("__Cursos impartidos__\n")
                                        for curso in instructor._cursos_impartidos:
                                            print(curso.mostrar_datos_curso())
                                        print("")

                                        codigo_curso_algo=input("Ingrese el código del curso al que desea asignarle un examen: ")

                                        asignatura = None
                                        for curso in admin._cursos_creados:
                                            if curso.codigo_curso == codigo_curso_algo:
                                                asignatura = curso
                                                break

                                        if asignatura:
                                            obj_instructor.crear_evaluacion(asignatura)

                                        else:
                                            print("Este curso no existe")
                                    case "2":
                                        print("Añadir notas")
                                    case "3":
                                        print("Añadir reportes")
                                    case "4":
                                        print("Saliendo del portal de instructores...")
                                        break
                        else:
                            print("Código de profesor incorrecto ✖️")

                    case "3":
                        print("Saliendo...\n")
                        break

        case "3":
            while True:
                print("--Portal Estudiante 📗🎓--\n")
                print("1. Registrarse")
                print("2. Acceder al portal")
                print("3. Mostrar reporte por curso")
                print("4. Salir")

                opcion5 = input("\nSeleccione lo que desee: ")

                match opcion5:
                    case "1":
                        obj_estudiantes.registrar_est()

                    case "2":
                        carnet_validacion = input("Ingrese su código de estudiante: ")

                        if carnet_validacion in obj_estudiantes.estudiantes_registrados:
                            while True:
                                print(
                                    f"\nBienvenido {obj_estudiantes.estudiantes_registrados[carnet_validacion].nombre}\n")
                                print("1. Inscribirse a un curso")
                                print("2. Ver cursos inscritos")  # opcion que muestra solo el curso sin mostrar la nota (para estudiantes que no deseen ver sus notas)
                                print("3. Ver tareas")
                                print("4. Ver notas por curso")
                                print("5. Salir")

                                opcion6 = input("\nSeleccione una opción: ")
                                match opcion6:
                                    case "1":
                                        print("Asignación de cursos\n")

                                        print("__Cursos disponibles__\n")
                                        for curso in admin._cursos_creados:
                                            print(curso.mostrar_datos_curso())

                                        print("")

                                        codigo_curso_buscador = input("Ingrese el código del curso al que se desee asignar: ")
                                        asignatura = None
                                        for curso in admin._cursos_creados:
                                            if curso.codigo_curso == codigo_curso_buscador:
                                                asignatura = curso
                                                break

                                        if asignatura:
                                            obj_estudiantes.asignar_curso(carnet_validacion, asignatura)

                                        else:
                                            print("Este curso no existe")

                                    case "2":
                                        print("Mostrar cursos")
                                        obj_estudiantes.mostrar_cursos(carnet_validacion)

                                    case "3":
                                        print("Mostrar tareas")
                                        # pendiente por sistema de tareas

                                    case "4":
                                        print("Mostrar notas")
                                        obj_estudiantes.mostrar_notas(carnet_validacion)

                                    case "5":
                                        print("Saliendo del portal de estudiantes...")
                                        break
                        else:
                            print("Código de estudiante incorrecto")

                    case "3":
                        print("Salir del portal de estudiantes...")
                        break

        case "4":
            print("Saliendo.....")
            break