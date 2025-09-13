class Usuario:  # Clase base para Instructor y Estudiante
    def __init__(self, nombre, correo, telefono):
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    def mostrar_datos(self):
        pass

class Curso:
    def __init__(self, nombre_curso, codigo_curso, evaluacion, tarea):
        self.nombre_curso = nombre_curso
        self._codigo_curso = codigo_curso
        self.instructor = None
        self.estudiantes = []  # almacenar ids o referencias a estudiantes
        self.tarea = tarea
        self.evaluacion = evaluacion


    @property
    def codigo_curso(self):
        return self._codigo_curso

    def asignar_instructor(self, instructor):
        self._instructor = instructor

    def inscribir_estudiante(self, estudiante):
        self.estudiantes.append(estudiante)

    def mostrar_datos(self):
        return f"Curso: {self.nombre_curso} | Código: {self._codigo_curso} | Instructor: {self._instructor.nombre if self._instructor else 'Sin asignar'}"

class Estudiante(Usuario):
    def __init__(self, nombre, correo, telefono, carnet):
        super().__init__(nombre, correo, telefono)
        self._carnet = carnet
        self.cursos_inscritos =[]

    def inscribirse(self, curso):
        self.cursos_inscritos.append(curso)
        curso.inscribir_estudiante(self)

    def mostrar_datos(self):
        if self.cursos_inscritos:
            nombres_cursos = []
            for curso in self.cursos_inscritos:
                nombres_cursos.append(curso.nombre_curso)
            cursos = ", ".join(nombres_cursos)
        else:
            cursos = "Ninguno"

        return f"Estudiante | Carnet: {self._carnet} | {super().mostrar_datos()} | Cursos: {cursos}"


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

class Administrador(Usuario):
    def __init__(self):
        super().__init__("Admin", None, 11110000)
        self._codigo_ingreso = "администратор007"
        self._cursos_creados = []


    @property
    def codigo_ingreso(self):
        return self._codigo_ingreso

    def crear_curso(self, nombre_curso, codigo_curso, evaluacion=None, tarea=None):
        curso = Curso(nombre_curso, codigo_curso, evaluacion, tarea)
        self._cursos_creados.append(curso)
        #return curso

    def asignar_curso_a_instructor(self, curso, instructor):
        instructor.asignar_curso(curso)

class Evaluacion:
    def __init__(self, nombre, punteo):
        self.nombre = nombre
        self._punteo = punteo
        self._calificaciones = {}

    @property
    def punteo(self):
        return self._punteo

    @property
    def calificaciones(self):
        return self._calificaciones

    def registrar_calificacion(self, estudiante, nota):
        self._calificaciones[estudiante._carnet] = nota

    def ver_calificaciones(self):
        if self._calificaciones:
            for carnet, nota in self._calificaciones.items():
                print(f"Carnet: {carnet} | Nota: {nota}")
        else:
            print("No hay calificaciones registradas.")

class Examen(Evaluacion):
    def __init__(self, nombre, ponderacion, duracion):
        super().__init__(nombre, ponderacion)
        self._duracion = duracion

    @property
    def duracion(self):
        return self._duracion

    def mostrar_info(self):
        return f"Examen: {self.nombre} | Ponderación: {self._punteo}% | Duración: {self._duracion} min"

class Tarea(Evaluacion):
    def __init__(self, nombre, ponderacion, fecha_entrega):
        super().__init__(nombre, ponderacion)
        self._fecha_entrega = fecha_entrega

    @property
    def fecha_entrega(self):
        return self._fecha_entrega

    def mostrar_info(self):
        return f"Tarea: {self.nombre} | Ponderación: {self._punteo}% | Fecha de entrega: {self._fecha_entrega}"

admin=Administrador()

estudiantes=["Juanito", "Samuel"]
instructores_registrados = {}



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
                    print("3. Salir")

                    opcion2 = input("\nSeleccione lo que desee: ")

                    match opcion2:
                        case "1":
                            nombre = input("Nombre de curso: ")
                            codigo_curso = input("Codigo de curso: ")
                            admin.crear_curso(nombre, codigo_curso)
                        case "2":
                           if not admin._cursos_creados:
                               print("No se ha creado el curso.")
                           if not instructores_registrados:
                               print("No se ha registrado ningun instructor")

                           codigo_curso = input("Codigo de curso: ")
                           codigo_instructor = input("Codigo de instructor: ")


                           if codigo_curso in instructores_registrados:
                               instructor = instructores_registrados[codigo_instructor]

                               curso_ADM = None
                               for i in admin._cursos_creados:
                                   if i.codigo == codigo_curso:
                                       curso_ADM = i
                                       break
                               if curso_ADM:
                                   instructor.asignar_curso(curso_ADM)
                                   print(f"Curso: {codigo_curso} asignado a Instructor: {instructor.nombre}")
                               else:
                                   print("El curso no existe")
                           else:
                               print("No se ha encontrado instructor")
                        case "3":
                            print("Saliendo del portal admin....")
                            break
            else:
                print("Código incorrecto ✖️")

        case "2":
            while True:
                print("--Portal Instructor 👨‍🏫👩‍🏫--\n")
                print("1. Registrar usuario")
                print("2. Acceder al portal")
                print("3. Salir")

                opcion3 = input("\nInicie sesión: ")

                match opcion3:
                    case "1":
                        print("Aquí se va a registrar usted")

                    case "2":
                        profesor = input("Ingrese su código de profesor: ")

                        if profesor in profesores:
                            while True:
                                print(f"Bienvenido {profesor}\n")
                                print("1. Añadir evaluación a su curso")
                                print("2. Añadir tarea a su curso")
                                print("3. Añadir notas")
                                print("4. Salir")

                                option4 = input("\nSeleccione una opción: ")

                                match option4:
                                    case "1":
                                        print("Añadir evaluación")
                                    case "2":
                                        print("Añadir una tarea")
                                    case "3":
                                        print("Añadir notas")
                                    case "4":
                                        print("Saliendo del portal de instructores...")
                                        break
                        else:
                            print("Código de profesor incorrecto ✖️")
                    case "3":
                        print("Saliendo ...")
                        break

        case "3":
            while True:
                print("--Portal Estudiante 📗🎓--\n")
                print("1. Registrarse")
                print("2. Acceder al portal")
                print("3. Salir")

                opcion5 = input("\nSeleccione lo que desee: ")

                match opcion5:
                    case "1":
                        print("Aquí se va a registrar el estudiante")

                    case "2":
                        estudiante = input("Ingrese su código de estudiante: ")

                        if estudiante in estudiantes:
                            while True:
                                print(f"Bienvenido {estudiante}\n")
                                print("1. Inscribirse a un curso")
                                print("2. Ver cursos inscritos")
                                print("3. Ver tareas")
                                print("4. Ver notas")
                                print("5. Salir")

                                opcion6 = input("\nSeleccione una opción: ")
                                match opcion6:
                                    case "1":
                                        print("Inscribirse a un curso")
                                    case "2":
                                        print("Mostrar cursos")
                                    case "3":
                                        print("Mostrar tareas")
                                    case "4":
                                        print("Mostrar notas")
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