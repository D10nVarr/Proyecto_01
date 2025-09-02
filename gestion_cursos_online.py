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
        return f"Carnet: {self.carnet} | Nombre: {self.nombre} | Correo: {self.correo} telefono: {self.telefono}"

class instructor(Usuario):
    def __init__(self,nombre,correo,telefono,codigo,profesion):
        super().__init__(nombre,correo,telefono)
        self.__codigo = codigo
        self.profesion = profesion
        self.estudiantes = {}

    def ver_codigo(self):
        return self.__codigo

    def mostrar_datos(self):
        return f"Instructor-Nombre: {self.nombre} | Profesion: {self.profesion} | Correo: {self.correo} | telefono: {self.telefono}"

class Administrador(Usuario):
    def __init__(self,nombre,correo):
        super().__init__(nombre,correo)

    def crear_curso(self,curso,tipo):
        pass
