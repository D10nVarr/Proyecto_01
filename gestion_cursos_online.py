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

    def mostrar_datos(self):
        return f"Carnet: {self.carnet} | Nombre: {self.nombre} | Correo: {self.correo} telefono: {self.telefono}"




