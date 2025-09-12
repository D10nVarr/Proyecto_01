class Usuario: #para guardar al instructor y al estudiante
    def __init__(self, nombre, correo, telefono):
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    def mostrar_datos(self):
        pass

class Curso:
    def __init__(self, nombre_curso, codigo_curso):
        self.nombre_curso = nombre_curso
        self.codigo_curso = codigo_curso

class Estudiante(Usuario):
    def __init__(self, nombre, correo, telefono, carnet):
        super().__init__(nombre, correo, telefono)
        self.carnet = carnet
        self.curso = {}

    def mostrar_datos(self):
        return f"Carnet: {self.carnet} | Nombre: {self.nombre} | Correo: {self.correo} | Telefono: {self.telefono}"

class Instructor(Usuario):
    def __init__(self,nombre,correo,telefono,codigo,profesion, curso):
        super().__init__(nombre,correo,telefono)
        self.__codigo = codigo
        self.profesion = profesion
        self.estudiantes = {}
        self.curso = curso

    def ver_codigo(self):
        return self.__codigo

    def crear_curso(self):
        pass

    def mostrar_datos(self):
        return f"Instructor: {self.nombre} | Código: {self.__codigo} | Profesion: {self.profesion} | Correo: {self.correo} | Telefono: {self.telefono} | Curso: {self.curso.nombre_curso}  {self.curso.codigo_curso}"

curso = Curso("Mate","CR-001")
profe = Instructor("Diego", "diego@profe.com", "31232566", "777","Ingeniero",curso)

print(profe.mostrar_datos())

