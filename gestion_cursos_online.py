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
        self.estudiantes = []  # carnets de estudiantes
        self.evaluacion = []

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

    def registrar_est(self, carnet):
        nombre=input("Ingrese su nombre: ")
        correo=input("Ingrese su correo: ")
        while True:
            telefono=input("Ingrese su teléfono: ")
            if len(telefono)==8:
                break
            else:
                print("Numero de teléfono no válido")

        if carnet not in self.estudiantes_registrados:
            estudiante = Estudiante(nombre, correo, telefono, carnet)
            self.estudiantes_registrados[carnet]=estudiante
            print(f"El estudiante {nombre} registrado con su carnet {carnet} correctamente ✔️\n")

        else:
            print("Este carnet ya registrado con su estudiante")

    def mostrar_cursos(self, carnet):
        obj_estudiante = self.estudiantes_registrados[carnet]

        if not obj_estudiante.cursos_inscritos:
            print("El estudiante no tiene cursos asignados.\n")

        else:
            for i, (codigo, datos) in enumerate(obj_estudiante.cursos_inscritos.items(), start=1):
                print(f"{i}.<{codigo}> - {datos['Nombre']}")
            print("")

    def asignar_curso(self, carnet, curso):
        if curso:
            obj_estudiante=self.estudiantes_registrados[carnet] # REGISTRA LOS ESTUDIOS CON LA LLAVE PRIMARIA DE CARNETS
            curso.estudiantes.append(carnet)
            obj_estudiante.cursos_inscritos[curso.codigo_curso]={
                "Nombre": curso.nombre_curso,
                "Nota": 0,
            }
            print(f"Curso {curso.nombre_curso} asignado correctamente\n")
        else:
            print("No existen cursos registrados")

    def mostrar_tareas_y_evaluaciones(self, carnet, cursos_admin):
        estudiante = self.estudiantes_registrados.get(carnet)
        if not estudiante:
            print("Estudiante no registrado.")
            return

        if not estudiante.cursos_inscritos:
            print("No tienes cursos asignados aún.\n")
            return

        for codigo, datos in estudiante.cursos_inscritos.items():
            curso = next((c for c in cursos_admin if c.codigo_curso == codigo), None)
            if curso:
                print(f"\n📘 {curso.nombre_curso} ({codigo})")
                if not curso.evaluacion:
                    print("   No hay evaluaciones registradas.")
                else:
                    for ev in curso.evaluacion:
                        print("   -", ev.mostrar_info())

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

    def registrar_instructor(self, codigo):
        nombre = input("Nombre: ")
        correo = input("Correo: ")
        while True:
            telefono = input("Ingrese su teléfono: ")
            if len(telefono) == 8:
                break
        profesion = input("Profesión: ")

        if codigo not in self.instructores_registrados:
            instructor = Instructor(nombre, correo, telefono, codigo, profesion)
            self.instructores_registrados[codigo] = instructor
            print(f"Instructor {nombre} registrado con éxito\n")
        else:
            print(f"Ya existe un instructor registrado con el código {codigo}\n.")

    def obtener_instructor(self, codigo):
        if codigo in self.instructores_registrados:
            return self.instructores_registrados[codigo]
        else:
            return None

    def crear_evaluacion(self, curso):
        print("Seleccione tipo de evaluación:")
        print("1. Examen")
        print("2. Tarea")
        opcion = input("Ingrese opción: ")

        nombre = input("Ingrese el nombre de la evaluación: ")

        if opcion == "1":
            duracion = input("Duración del examen (minutos): ")
            evaluacion = Examen(nombre, duracion)
        elif opcion == "2":
            fecha_entrega = input("Fecha de entrega (dd/mm/aaaa): ")
            evaluacion = Tarea(nombre, fecha_entrega)
        else:
            print("Opción no válida")
            return

        curso.evaluacion.append(evaluacion) # Guarda la evaluacion en la lista de curso
        print(f"{evaluacion.nombre} agregado al curso {curso.nombre_curso}\n")

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

        if codigo_curso not in self._cursos_creados:
            curso = Curso(nombre, codigo_curso)
            self._cursos_creados.append(curso)
            print(f"Curso: {nombre} creado con exito\n")
        else:
            print(f"El curso con código {codigo_curso} ya existe\n")

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

    def reporte_general(self, obj_estudiantes):
        print("\n--- Reporte General de cursos ---")
        if not self._cursos_creados:
            print("No hay cursos creados")
            return
        for curso in self._cursos_creados:
            if not curso.estudiantes:
                print(f"{curso.nombre_curso} ({curso.codigo_curso}): Sin estudiantes inscritos.\n")
                continue
            total_notas = 0
            cantidad = 0

            for carnet in curso.estudiantes:
                if carnet in obj_estudiantes.estudiantes_registrados:
                    estudinte = obj_estudiantes.estudiantes_registrados[carnet]
                    if curso.codigo_curso in estudinte.cursos_inscritos:
                        total_notas += estudinte.cursos_inscritos[curso.codigo_curso]["Nota"]
                        cantidad += 1
            if cantidad > 0:
                promedio = total_notas / cantidad
                print(f"{curso.nombre_curso} ({curso.codigo_curso}) | Promedio general: {promedio:.2f}\n")
            else:
                print(f"{curso.nombre_curso} ({curso.codigo_curso}): No hay notas registradas.\n")

    def reporte_bajo_estudiantes(self, obj_estudiantes, limite=60):
            if not self._cursos_creados:
                print("No hay cursos creados")
                return
            for curso in self._cursos_creados:
                if not curso.estudiantes:
                    print(f"{curso.nombre_curso}({curso.codigo_curso}): Sin estudiantes inscritos.\n")
                    continue
                print(f"\nCurso: {curso.nombre_curso}({curso.codigo_curso})")
            for carnet in curso.estudiantes:
                if carnet in obj_estudiantes.estudiantes_registrados:
                    estudiante = obj_estudiantes.estudiantes_registrados[carnet]
                    if curso.codigo_curso in estudiante.cursos_inscritos:
                        nota = estudiante.cursos_inscritos[curso.codigo_curso]["nota"]
                        if nota > limite:
                            print(f"{estudiante._carnet}-{estudiante.nombre}-Nota: {nota:.2f}")

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
                    print("--\nPortal del ADMIN 🤑🤑--\n")
                    print("1. Crear curso")
                    print("2. Asignar curso a instructor")
                    print("3. Reporte de notas")
                    print("4. Reporte de notas de estudiantes")
                    print("5. Salir")

                    opcion2 = input("\nSeleccione lo que desee: ")

                    match opcion2:
                        case "1":
                            admin.crear_curso()
                        case "2":
                            admin.asignar_curso_a_instructor(obj_instructor.instructores_registrados)
                        case "3":
                            print("Reporte de promedio de notas")
                            admin.reporte_general(obj_estudiantes)
                        case "4":
                            print("Reporte de notas bajas de estudiantes")
                            admin.reporte_bajo_estudiantes(obj_estudiantes)
                        case "5":
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
                        print("\n--- Registro de Instructor ---")
                        codigo = input("Código de Instructor: ")

                        if codigo not in obj_estudiantes.estudiantes_registrados:
                            obj_instructor.registrar_instructor(codigo)
                        else:
                            print("El código de instructor no debe ser igual a un carnet de estudiante\n")

                    case "2":
                        codigo_instructor = input("Ingrese su código de instructor: ")
                        instructor = obj_instructor.obtener_instructor(codigo_instructor)

                        if instructor:
                            while True:
                                print(f"\nBienvenido {instructor.nombre} 👋")
                                print("1. Añadir evaluación a su curso")
                                print("2. Añadir notas")
                                print("3. Salir")

                                option4 = input("\nSeleccione una opción: ")

                                match option4:
                                    case "1":
                                        if instructor._cursos_impartidos:
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
                                        else:
                                            print("NO tiene cursos asignados")

                                    case "2":
                                        if instructor._cursos_impartidos:
                                            print("__Cursos__\n")
                                            for curso in instructor._cursos_impartidos:
                                                print(curso.mostrar_datos_curso())
                                            print("")

                                            codigo_curso_algo = input("Ingrese el código del curso en el que desea añadir notas: ")

                                            asignatura = None
                                            for curso in instructor._cursos_impartidos:
                                                if curso.codigo_curso == codigo_curso_algo:
                                                    asignatura = curso
                                                    break

                                            if asignatura:
                                                if not asignatura.estudiantes:
                                                    print("Este curso no tiene estudiantes inscritos aún.")
                                                else:
                                                    print(f"Estudiantes inscritos en {asignatura.nombre_curso}:")
                                                    for carnet in asignatura.estudiantes:
                                                        print(f" - {carnet}")

                                                    carnet_est = input("Ingrese el carnet del estudiante: ")
                                                    if carnet_est in obj_estudiantes.estudiantes_registrados:
                                                        estudiante = obj_estudiantes.estudiantes_registrados[carnet_est]
                                                        if codigo_curso_algo in estudiante.cursos_inscritos:
                                                            nota = float(input("Ingrese la nota: "))
                                                            estudiante.cursos_inscritos[codigo_curso_algo]["Nota"] = nota
                                                            print(
                                                                f"✅ Nota {nota} asignada a {estudiante.nombre} en {asignatura.nombre_curso}\n")
                                                        else:
                                                            print("El estudiante no está inscrito en este curso.")
                                                    else:
                                                        print("El carnet ingresado no está registrado.")
                                            else:
                                                print("Este curso no existe o no está asignado a usted.")

                                        else:
                                            print("Usted no tiene cursos asignados\n")
                                    case "3":
                                        print("Saliendo del portal de instructores...")
                                        break
                        else:
                            print("Código de profesor incorrecto ✖️")

                    case "3":
                        print("Saliendo...\n")
                        break

        case "3":
            while True:
                print("--\nPortal Estudiante 📗🎓--\n")
                print("1. Registrarse")
                print("2. Acceder al portal")
                print("3. Salir")

                opcion5 = input("\nSeleccione lo que desee: ")

                match opcion5:
                    case "1":
                        print("\n--- Registro de Estudiane ---")
                        carnet=input("Ingrese su carnet: ")#validacion de existencia
                        if carnet not in obj_instructor.instructores_registrados:
                            obj_estudiantes.registrar_est(carnet)
                        else:
                            print("El carnet no debe ser igual a un código de instructor\n")

                    case "2":
                        if not obj_estudiantes.estudiantes_registrados:
                            print(f"No existen estudiantes registrados\n")

                        else:
                            carnet_validacion = input("Ingrese su código de estudiante: ")

                            if carnet_validacion in obj_estudiantes.estudiantes_registrados:
                                while True:
                                    print(f"\nBienvenido {obj_estudiantes.estudiantes_registrados[carnet_validacion].nombre}\n")
                                    print("1. Inscribirse a un curso")
                                    print("2. Ver cursos inscritos")  # opcion que muestra solo el curso sin mostrar la nota (para estudiantes que no deseen ver sus notas)
                                    print("3. Ver tareas")
                                    print("4. Ver notas por curso")
                                    print("5. Salir")

                                    opcion6 = input("\nSeleccione una opción: ")
                                    match opcion6:
                                        case "1":
                                            if admin._cursos_creados:
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
                                            else:
                                                print("No existen cursos registrados")

                                        case "2":
                                            print("Mostrar cursos")
                                            obj_estudiantes.mostrar_cursos(carnet_validacion)

                                        case "3":
                                            obj_estudiantes.mostrar_tareas_y_evaluaciones(carnet_validacion, admin._cursos_creados)

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
