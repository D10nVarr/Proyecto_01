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

admin=Administrador()

estudiantes=["Juanito", "Samuel"]
profesores=["Pedro", "Mateo"]

while True:
    print("----🛜 PORTAL CURSOS ONLINE 🛜----")

    print("Iniciar sesión\n")
    print("1. Administrador")
    print("2. Instructor")
    print("3. Estudiante")
    print("4. Salir")

    opcion1=input("\nSeleccione su tipo de usuario")

    match opcion1:
        case "1":
            codigo=input("Ingrese su codigo de admin: ")

            if codigo==admin.codigo_ingreso:
                while True:
                    print("--Portal del ADMIN 🤑🤑--\n")
                    print("1. Crear curso")
                    print("2. Asignar curso a instructor")
                    print("3. Salir")

                    opcion2=input("\nSeleccione lo que desee: ")

                    match opcion2:
                        case "1":
                            print("Aqui se va a crear curso")
                        case "2":
                            print("Aqui se va a asignar curso")
                        case "3":
                            break
            else:
                print("Codio incorrecto ✖️")

        case "2":
            while True:
                print("--Portal Instructor👨‍🏫👩‍🏫--\n")
                print("1. Registrar usuario")
                print("2. Acceder al portal")
                print("3. Salir")

                opcion3=input("\nInicie sesión")

                match opcion3:
                    case "1":
                        print("Aqui se va a registrar usted")

                    case "2":
                        print("Aqui usted ya esta dentro del portal")

                        profesor=input("Ingrese su código de profesor")

                        if profesor in profesores:
                            print(f"Bienvenido {profesor}")

                            print("1. Añadir evaluacion a su curso")
                            print("2. Añadir tarea a su curso")
                            print("3. Añadir notas")
                            print("4. Salir")

                            option4=input("\nSeleccione una opción: ")

                            match option4:
                                case "1":
                                    print("añadir evaluacion ")

                                case "2":
                                    print("añadir una tarea")

                                case "3":
                                    print("añadir notas")

                                case "4":
                                    print("Saliendo del portal de instructores...")
                                    break
                        else:
                            print("Codigo de profesor incorrecto✖️")
                    case "3":
                        print("Saliendo ...")
                        break

        case "3":
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
                        print(f"Bienvenido {estudiante}")

                        print("1. Inscibirse a un curso")
                        print("2. ver cursos inscritos")
                        print("3. ver tareas")
                        print("4. ver notas")
                        print("5. Salir")

                        opcion6 = input("\nSeleccione una opcion: ")
                        match opcion6:
                            case "1":
                                print("inscribirse a un curso")

                            case "2":
                                print("Mostrar cursos")

                            case "3":
                                print("Mostrar tareas")

                            case "4":
                                print("Mostrar notas")

                            case "5":
                                print("Salir")
                                break
                    else:
                        print("Codigo de estudiante incorrecto")

                case "3":
                    print(" salir")
                    break
        case "4":
            print("Saliendo.....")
            break