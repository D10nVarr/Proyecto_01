class Usuario: #para guardar al instructor y al estudiante
    def __init__(self, nombre, correo, telefono):
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    def mostrar_datos(self):
        pass

class Estudiante(Usuario):
    def __init__(self, nombre, correo, telefono, carnet):
        super().__init__(nombre, correo, telefono)
        self.carnet = carnet
        self.curso = {}

    def mostrar_datos(self):
        return f"Carnet: {self.carnet} | Nombre: {self.nombre} | Correo: {self.correo} | Telefono: {self.telefono}"

class Instructor(Usuario):
    def __init__(self,nombre,correo,telefono,codigo,profesion):
        super().__init__(nombre,correo,telefono)
        self.__codigo = codigo
        self.profesion = profesion
        self.estudiantes = {}

    def ver_codigo(self):
        return self.__codigo

    def crear_curso(self):
        pass


    def mostrar_datos(self):
        return f"Instructor-Nombre: {self.nombre} | Profesion: {self.profesion} | Correo: {self.correo} | Telefono: {self.telefono}"


class Curso:
    def __init__(self, nombre_curso, codigo_curso, instructor):
        self.nombre_curso = nombre_curso
        self.codigo_curso = codigo_curso
        self.instructor = instructor

    def mostrar_datos(self):
        return (f"Curso: {self.nombre_curso},"
                f"\nCódigo de curso: {self.codigo_curso}"
                f"\n{self.instructor.mostrar_datos()}")

