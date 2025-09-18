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
        while True:
            try:
                nombre = input("Ingrese su nombre: ")
                if nombre is None:
                    print("Error: entrada vacía. Intente de nuevo.\n")
                    continue
                nombre = nombre.strip()
                if nombre == "":
                    print("No puede ingresar un valor vacío, intente nuevamente.\n")
                    continue
            except Exception as e:
                print(f"Error inesperado: {e}\n")
            else:
                break

        while True:
            try:
                correo = input("Ingrese su correo: ")
                if correo is None:
                    print("Error: entrada vacía. Intente de nuevo.\n")
                    continue
                correo = correo.strip()
                if correo == "":
                    print("No puede ingresar un valor vacío, intente nuevamente.\n")
                    continue
            except Exception as e:
                print(f"Error inesperado: {e}\n")
            else:
                break
        while True:
            telefono=input("Ingrese su teléfono: ")
            if len(telefono)==8:
                break
            else:
                print("Numero de teléfono no válido, debe contener 8 dígitos\n")

        if carnet not in self.estudiantes_registrados:
            estudiante = Estudiante(nombre, correo, telefono, carnet)
            self.estudiantes_registrados[carnet] = estudiante
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
                tareas = [ev for ev in curso.evaluacion if isinstance(ev, Tarea)]
                if not tareas:
                    print("   No hay tareas registradas.")
                else:
                    for ev in tareas:
                        print("   -", ev.mostrar_info())

    def mostrar_notas(self, carnet, cursos_admin):
        obj_estudiante = self.estudiantes_registrados.get(carnet)
        if not obj_estudiante:
            print("Estudiante no registrado.")
            return

        if not obj_estudiante.cursos_inscritos:
            print(f"El estudiante {carnet} no tiene cursos asignados.\n")
            return

        print(f"Notas por curso del estudiante {obj_estudiante._carnet}:\n")

        for codigo, datos in obj_estudiante.cursos_inscritos.items():
            curso = next((c for c in cursos_admin if c.codigo_curso == codigo), None)
            if not curso:
                continue

            print(f"➡️ {datos['Nombre']} ({codigo}):")
            if not curso.evaluacion:
                print("   No hay evaluaciones registradas.")
                print("   Nota final: 0\n")
                continue

            total = 0
            for ev in curso.evaluacion:
                punteo = ev.obtener_punteo(obj_estudiante._carnet)
                tipo = "Examen" if isinstance(ev, Examen) else "Tarea"
                print(f"   - {tipo}: {ev.nombre} -> {punteo}")
                total += punteo

            print(f"   Nota final: {total}\n")

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
        while True:
            try:
                nombre = input("Nombre: ")
                if nombre is None:
                    print("Error: entrada vacía. Intente de nuevo.\n")
                    continue
                nombre = nombre.strip()
                if nombre == "":
                    print("No puede ingresar un valor vacío, intente nuevamente.\n")
                    continue
            except Exception as e:
                print(f"Error inesperado: {e}\n")
            else:
                break

        while True:
            try:
                correo = input("Correo: ")
                if correo is None:
                    print("Error: entrada vacía. Intente de nuevo.\n")
                    continue
                correo = correo.strip()
                if correo == "":
                    print("No puede ingresar un valor vacío, intente nuevamente.\n")
                    continue
            except Exception as e:
                print(f"Error inesperado: {e}\n")
            else:
                break

        while True:
            telefono = input("Ingrese su teléfono: ")
            if len(telefono) == 8:
                break
            else:
                print("Numero de teléfono no válido, debe contener 8 dígitos\n")

        while True:
            try:
                profesion = input("Profesión: ")
                if profesion is None:
                    print("Error: entrada vacía. Intente de nuevo.\n")
                    continue
                profesion = profesion.strip()
                if profesion == "":
                    print("No puede ingresar un valor vacío, intente nuevamente.\n")
                    continue
            except Exception as e:
                print(f"Error inesperado: {e}\n")
            else:
                break

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

        while True:
            try:
                opcion = input("Ingrese opción: ")
                if opcion is None:
                    print("Error: entrada vacía. Intente de nuevo.\n")
                    continue
                opcion = opcion.strip()
                if opcion not in ("1", "2"):
                    print("Opción no válida\n")
                    continue
            except Exception as e:
                print(f"Error inesperado: {e}\n")
            else:
                break

        while True:
            try:
                nombre = input("Ingrese el nombre de la evaluación: ")
                if nombre is None:
                    print("Error: entrada vacía. Intente de nuevo.\n")
                    continue
                nombre = nombre.strip()
                if nombre == "":
                    print("No puede ingresar un valor vacío, intente nuevamente.\n")
                    continue
            except Exception as e:
                print(f"Error inesperado: {e}\n")
            else:
                break

        if opcion == "1":
            while True:
                try:
                    dur = input("Duración del examen (minutos): ")
                    if dur is None:
                        print("Error: entrada vacía. Intente de nuevo.\n")
                        continue
                    dur = dur.strip()
                    if dur == "":
                        print("No puede dejar este campo vacío.\n")
                        continue
                    duracion = int(dur)
                    if duracion <= 0:
                        print("La duración debe ser un entero positivo.\n")
                        continue
                except ValueError:
                    print("Ingrese un número entero válido para la duración.\n")
                except TypeError:
                    print("Tipo de dato inválido para duración.\n")
                except Exception as e:
                    print(f"Error inesperado: {e}\n")
                else:
                    break
            evaluacion = Examen(nombre, duracion)

        else:
            while True:
                try:
                    fecha_entrega = input("Fecha de entrega (dd/mm/aaaa): ")
                    if fecha_entrega is None:
                        print("Error: entrada vacía. Intente de nuevo.\n")
                        continue
                    fecha_entrega = fecha_entrega.strip()
                    if fecha_entrega == "":
                        print("No puede dejar este campo vacío.\n")
                        continue
                except Exception as e:
                    print(f"Error inesperado: {e}")
                else:
                    break
            evaluacion = Tarea(nombre, fecha_entrega)

        curso.evaluacion.append(evaluacion)
        print(f"{evaluacion.nombre} agregado al curso {curso.nombre_curso}\n")

    def anadir_punteo_evaluacion(self, asignatura, registro_estudiantes):
        if not asignatura:
            print("Este curso no existe o no está asignado a usted.")
            return

        if not asignatura.estudiantes:
            print("Este curso no tiene estudiantes inscritos aún.")
            return

        if not asignatura.evaluacion:
            print("Este curso no tiene evaluaciones registradas.")
            return

        print(f"Evaluaciones del curso {asignatura.nombre_curso}:")
        for i, ev in enumerate(asignatura.evaluacion, start=1):
            print(f"{i}. {ev.mostrar_info()}")
        print("")

        while True:
            try:
                idx = int(input("Seleccione la evaluación por número: "))
                if 1 <= idx <= len(asignatura.evaluacion):
                    break
                else:
                    print("Número fuera de rango.")
            except ValueError:
                print("Ingrese un número válido.")
            except TypeError:
                print("Tipo de dato inválido.")
            except Exception as e:
                print(f"Error inesperado: {e}")

        evaluacion = asignatura.evaluacion[idx - 1]

        print(f"Estudiantes inscritos en {asignatura.nombre_curso}:")
        for carnet in asignatura.estudiantes:
            print(f" - {carnet}")

        while True:
            try:
                carnet_est = input("Ingrese el carnet del estudiante: ")
                if carnet_est is None:
                    print("Error: entrada vacía. Intente de nuevo.")
                    continue
                carnet_est = carnet_est.strip()
                if carnet_est == "":
                    print("No puede ingresar un valor vacío, intente nuevamente.")
                    continue
            except Exception as e:
                print(f"Error inesperado: {e}")
            else:
                break

        if carnet_est not in registro_estudiantes.estudiantes_registrados:
            print("El carnet ingresado no está registrado.")
            return

        estudiante = registro_estudiantes.estudiantes_registrados[carnet_est]

        if asignatura.codigo_curso not in estudiante.cursos_inscritos:
            print("El estudiante no está inscrito en este curso.")
            return

        while True:
            try:
                nota_str = input("Ingrese el punteo: ")
                if nota_str is None:
                    print("Error: entrada vacía. Intente de nuevo.")
                    continue
                nota_str = nota_str.strip()
                if nota_str == "":
                    print("No puede dejar la nota vacía.")
                    continue
                nota = float(nota_str)
                if 0 <= nota <= 100:
                    break
                else:
                    print("El punteo debe estar entre 0 y 100.")
            except ValueError:
                print("Ingrese un número válido para el punteo.")
            except TypeError:
                print("Tipo de dato inválido para el punteo.")
            except Exception as e:
                print(f"Error inesperado: {e}")

        evaluacion.asignar_punteo(carnet_est, nota)

        total = 0
        for ev in asignatura.evaluacion:
            total += ev.obtener_punteo(carnet_est)

        estudiante.cursos_inscritos[asignatura.codigo_curso]["Nota"] = total
        print(f"Punteo {nota} registrado en '{evaluacion.nombre}'. Nota final actual: {total:.2f}\n")

class Administrador(Usuario):
    def __init__(self):
        super().__init__("Admin", None, 11110000)
        self._codigo_ingreso = "администратор007"
        self._cursos_creados = []

    @property
    def codigo_ingreso(self):
        return self._codigo_ingreso

    def crear_curso(self):
        while True:
            try:
                nombre = input("Nombre de curso: ")
                if nombre is None:
                    print("Error: entrada vacía. Intente de nuevo.\n")
                    continue
                nombre = nombre.strip()
                if nombre == "":
                    print("No puede ingresar un valor vacío, intente nuevamente.\n")
                    continue
            except Exception as e:
                print(f"Error inesperado: {e}\n")
            else:
                break

        while True:
            try:
                codigo_curso = input("Codigo de curso: ")
                if codigo_curso is None:
                    print("Error: entrada vacía. Intente de nuevo.\n")
                    continue
                codigo_curso = codigo_curso.strip()
                if codigo_curso == "":
                    print("No puede ingresar un valor vacío, intente nuevamente.\n")
                    continue
            except Exception as e:
                print(f"Error inesperado: {e}\n")
            else:
                break

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

        while True:
            try:
                codigo_curso = input("Codigo de curso: ")
                if codigo_curso is None:
                    print("Error: entrada vacía. Intente de nuevo.\n")
                    continue
                codigo_curso = codigo_curso.strip()
                if codigo_curso == "":
                    print("No puede ingresar un valor vacío, intente nuevamente.\n")
                    continue
            except Exception as e:
                print(f"Error inesperado: {e}\n")
            else:
                break

        while True:
            try:
                codigo_instructor = input("Codigo de instructor: ")
                if codigo_instructor is None:
                    print("Error: entrada vacía. Intente de nuevo.\n")
                    continue
                codigo_instructor = codigo_instructor.strip()
                if codigo_instructor == "":
                    print("No puede ingresar un valor vacío, intente nuevamente.\n")
                    continue
            except Exception as e:
                print(f"Error inesperado: {e}\n")
            else:
                break

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
                        nota = estudiante.cursos_inscritos[curso.codigo_curso]["Nota"]
                        if nota < limite:
                            print(f"{estudiante._carnet} - {estudiante.nombre} - Nota: {nota:.2f}")

class Evaluacion:
    def __init__(self, nombre):
        self.nombre = nombre
        self._punteos = {}

    def mostrar_info(self):
        pass

    def asignar_punteo(self, carnet, nota):
        self._punteos[carnet] = nota

    def obtener_punteo(self, carnet):
        return self._punteos.get(carnet, 0)

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
            codigo = input("Ingrese su código de admin (администратор007): ")


            if codigo == admin.codigo_ingreso:
                while True:
                    print("\n--Portal del ADMIN 🤑🤑--\n")
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
                            print("Error: Opción no válida, intente de nuevo.\n")
            else:
                print("Código incorrecto ✖️\n")

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
                        while True:
                            try:
                                codigo = input("Código de Instructor: ")
                                if codigo is None:
                                    print("Error: entrada vacía. Intente de nuevo.\n")
                                    continue
                                codigo = codigo.strip()
                                if codigo == "":
                                    print("No puede ingresar un valor vacío, intente nuevamente.\n")
                                    continue
                            except Exception as e:
                                print(f"Error inesperado: {e}\n")
                            else:
                                break

                        if codigo not in obj_estudiantes.estudiantes_registrados:
                            obj_instructor.registrar_instructor(codigo)
                        else:
                            print("El código de instructor no debe ser igual a un carnet de estudiante\n")

                    case "2":
                        while True:
                            try:
                                codigo_instructor = input("Ingrese su código de instructor: ")
                                if codigo_instructor is None:
                                    print("Error: entrada vacía. Intente de nuevo.")
                                    continue
                                codigo_instructor = codigo_instructor.strip()
                                if codigo_instructor == "":
                                    print("No puede ingresar un valor vacío, intente nuevamente.")
                                    continue
                            except Exception as e:
                                print(f"Error inesperado: {e}")
                            else:
                                break
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

                                            while True:
                                                try:
                                                    codigo_curso_algo = input(
                                                        "Ingrese el código del curso al que desea asignarle un examen: ")
                                                    if codigo_curso_algo is None:
                                                        print("Error: entrada vacía. Intente de nuevo.\n")
                                                        continue
                                                    codigo_curso_algo = codigo_curso_algo.strip()
                                                    if codigo_curso_algo == "":
                                                        print("No puede ingresar un valor vacío, intente nuevamente.\n")
                                                        continue
                                                except Exception as e:
                                                    print(f"Error inesperado: {e}\n")
                                                else:
                                                    break

                                            asignatura = None
                                            for curso in admin._cursos_creados:
                                                if curso.codigo_curso == codigo_curso_algo:
                                                    asignatura = curso
                                                    break

                                            if asignatura:
                                                obj_instructor.crear_evaluacion(asignatura)

                                            else:
                                                print("Este curso no existe\n")
                                        else:
                                            print("NO tiene cursos asignados\n")

                                    case "2":
                                        if instructor._cursos_impartidos:
                                            print("__Cursos impartidos__\n")
                                            for curso in instructor._cursos_impartidos:
                                                print(curso.mostrar_datos_curso())
                                            print("")

                                            while True:
                                                try:
                                                    codigo_curso_algo = input(
                                                        "Ingrese el código del curso en el que desea añadir punteos: ")
                                                    if codigo_curso_algo is None:
                                                        print("Error: entrada vacía. Intente de nuevo.\n")
                                                        continue
                                                    codigo_curso_algo = codigo_curso_algo.strip()
                                                    if codigo_curso_algo == "":
                                                        print("No puede ingresar un valor vacío, intente nuevamente.\n")
                                                        continue
                                                except Exception as e:
                                                    print(f"Error inesperado: {e}\n")
                                                else:
                                                    break

                                            asignatura = None
                                            for curso in instructor._cursos_impartidos:
                                                if curso.codigo_curso == codigo_curso_algo:
                                                    asignatura = curso
                                                    break

                                            if asignatura:
                                                obj_instructor.anadir_punteo_evaluacion(asignatura, obj_estudiantes)
                                            else:
                                                print("Este curso no existe o no está asignado a usted.\n")
                                        else:
                                            print("NO tiene cursos asignados\n")

                                    case "3":
                                        print("Saliendo del portal de instructores...\n")
                                        break

                                    case _:
                                        print("Error: Opción no válida, intente de nuevo.\n")
                        else:
                            print("Código de profesor incorrecto ✖️")

                    case "3":
                        print("Saliendo...\n")
                        break

                    case _:
                        print("Error: Opción no válida, intente de nuevo.\n")

        case "3":
            while True:
                print("\n--Portal Estudiante 📗🎓--\n")
                print("1. Registrarse")
                print("2. Acceder al portal")
                print("3. Salir")

                opcion5 = input("\nSeleccione lo que desee: ")

                match opcion5:
                    case "1":
                        print("\n--- Registro de Estudiante ---\n")
                        while True:
                            try:
                                carnet = input("Ingrese su carnet: ")
                                if carnet is None:
                                    print("Error: entrada vacía. Intente de nuevo.\n")
                                    continue
                                carnet = carnet.strip()
                                if carnet == "":
                                    print("No puede ingresar un valor vacío, intente nuevamente.\n")
                                    continue
                            except Exception as e:
                                print(f"Error inesperado: {e}")
                            else:
                                break

                        if carnet not in obj_instructor.instructores_registrados:
                            obj_estudiantes.registrar_est(carnet)
                        else:
                            print("El carnet no debe ser igual a un código de instructor\n")

                    case "2":
                        if not obj_estudiantes.estudiantes_registrados:
                            print(f"No existen estudiantes registrados\n")

                        else:
                            while True:
                                try:
                                    carnet_validacion = input("Ingrese su código de estudiante: ")
                                    if carnet_validacion is None:
                                        print("Error: entrada vacía. Intente de nuevo.\n")
                                        continue
                                    carnet_validacion = carnet_validacion.strip()
                                    if carnet_validacion == "":
                                        print("No puede ingresar un valor vacío, intente nuevamente.\n")
                                        continue
                                except Exception as e:
                                    print(f"Error inesperado: {e}\n")
                                else:
                                    break

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

                                                while True:
                                                    try:
                                                        codigo_curso_buscador = input(
                                                            "Ingrese el código del curso al que se desee asignar: ")
                                                        if codigo_curso_buscador is None:
                                                            print("Error: entrada vacía. Intente de nuevo.\n")
                                                            continue
                                                        codigo_curso_buscador = codigo_curso_buscador.strip()
                                                        if codigo_curso_buscador == "":
                                                            print(
                                                                "No puede ingresar un valor vacío, intente nuevamente.\n")
                                                            continue
                                                    except Exception as e:
                                                        print(f"Error inesperado: {e}\n")
                                                    else:
                                                        break

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
                                            obj_estudiantes.mostrar_notas(carnet_validacion, admin._cursos_creados)

                                        case "5":
                                            print("Saliendo del portal de estudiantes...")
                                            break

                                        case _:
                                            print("Error: Opción no válida, intente de nuevo.\n")
                            else:
                                print("Código de estudiante incorrecto")

                    case "3":
                        print("Salir del portal de estudiantes...")
                        break

                    case _:
                        print("Error: Opción no válida, intente de nuevo.\n")

        case "4":
            print("Saliendo.....")
            break

        case _:
            print("Error: Opción no válida, intente de nuevo.\n")