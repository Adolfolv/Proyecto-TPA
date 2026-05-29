class Perfil:

    def __init__(self, servicio_usuario):
        self.servicio_usuario = servicio_usuario
        self.usuario_actual = None

    def cargar_perfil(self, id_usuario: int):
        self.usuario_actual = self.servicio_usuario.buscar_usuario(id_usuario)
        return self.usuario_actual

    def ver_perfil(self):
        return self.usuario_actual

    def actualizar_perfil(self, datos: dict):

        if not self.usuario_actual:
            return False

        if "nombre" in datos:
            self.usuario_actual.nombre = datos["nombre"]

        if "correo" in datos:
            self.usuario_actual.correo = datos["correo"]

        if "edad" in datos:
            self.usuario_actual.edad = datos["edad"]

        if "telefono" in datos:
            self.usuario_actual.telefono = datos["telefono"]

        if "contraseña" in datos:
            self.usuario_actual.contraseña = datos["contraseña"]

        self.servicio_usuario.guardar()
        return True