class Usuario:  # Clase base para Instructor y Estudiante
    def __init__(self, nombre, correo, telefono):
        self._nombre = nombre
        self._correo = correo
        self._telefono = telefono

    def mostrar_datos(self):
        pass

    @property
    def nombre(self):
        return self._nombre

    @property
    def correo(self):
        return self._correo

    @property
    def telefono(self):
        return self._telefono


class Curso:
    def __init__(self, nombre_curso, codigo_curso):
        self._nombre_curso = nombre_curso
        self._codigo_curso = codigo_curso
        self.instructor = None
        self.estudiantes = []  # almacenar ids o referencias a estudiantes

    @property
    def nombre_curso(self):
        return self._nombre_curso

    @property
    def codigo_curso(self):
        return self._codigo_curso

    def asignar_instructor(self, instructor):
        self._instructor = instructor

    def inscribir_estudiante(self, estudiante):
        self.estudiantes.append(estudiante)

    def mostrar_datos(self):
        return f"Curso: {self._nombre_curso} | Código: {self._codigo_curso} | Instructor: {self._instructor.nombre if self._instructor else 'Sin asignar'}"


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
        self._cursos_impartidos = set()

    @property
    def codigo(self):
        return self._codigo

    def asignar_curso(self, curso):
        self._cursos_impartidos.add(curso)
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