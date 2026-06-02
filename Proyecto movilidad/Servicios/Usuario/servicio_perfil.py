from Validaciones.perfil import ValidadorPerfilCargado
from Validaciones.registro import ValidadorCorreo, ValidadorEdad, ValidadorTelefono
#.

class ServicioPerfil:

    def __init__(self, servicio_usuario):
        self.servicio_usuario = servicio_usuario
        self.usuario_actual = None
        self.validador_perfil_cargado = ValidadorPerfilCargado()
        self.validador_correo = ValidadorCorreo()
        self.validador_edad = ValidadorEdad()
        self.validador_telefono = ValidadorTelefono()

    def cargar_perfil(self, id_usuario: int):
        self.usuario_actual = self.servicio_usuario.buscar_usuario(id_usuario)
        return self.usuario_actual

    def ver_perfil(self):
        return self.usuario_actual

    def actualizar_perfil(self, datos: dict):

        if not self.validador_perfil_cargado.validar(self.usuario_actual):
            return False

        if "nombre" in datos:
            self.usuario_actual.nombre = datos["nombre"]

        if "correo" in datos:
            if not self.validador_correo.validar(datos["correo"]):
                return False

            self.usuario_actual.correo = datos["correo"]

        if "edad" in datos:
            if not self.validador_edad.validar(datos["edad"]):
                return False

            self.usuario_actual.edad = datos["edad"]

        if "telefono" in datos:
            if not self.validador_telefono.validar(datos["telefono"]):
                return False

            self.usuario_actual.telefono = datos["telefono"]

        if "contrasena" in datos:
            self.usuario_actual.contrasena = datos["contrasena"]

        self.servicio_usuario.guardar()
        return True
