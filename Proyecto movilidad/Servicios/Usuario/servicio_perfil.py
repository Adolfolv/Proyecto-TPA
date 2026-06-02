from Validaciones.perfil import ValidadorPerfilCargado
from Validaciones.registro import ValidadorCorreo, ValidadorEdad, ValidadorTelefono
#.

class ServicioPerfil:

    def __init__(self, servicio_usuario):
        self.servicio_usuario = servicio_usuario
        self.validador_perfil_cargado = ValidadorPerfilCargado()
        self.validador_correo = ValidadorCorreo()
        self.validador_edad = ValidadorEdad()
        self.validador_telefono = ValidadorTelefono()

    def cargar_perfil(self, id_usuario: int):
        usuario = self.servicio_usuario.buscar_usuario(id_usuario)
        return self.servicio_usuario.establecer_usuario_actual(usuario)

    def ver_perfil(self):
        return self.servicio_usuario.obtener_usuario_actual(False)

    def actualizar_perfil(self, datos: dict):
        usuario_actual = self.ver_perfil()

        if not self.validador_perfil_cargado.validar(usuario_actual):
            return False

        if "nombre" in datos:
            usuario_actual.nombre = datos["nombre"]

        if "correo" in datos:
            if not self.validador_correo.validar(datos["correo"]):
                return False

            usuario_actual.correo = datos["correo"]

        if "edad" in datos:
            if not self.validador_edad.validar(datos["edad"]):
                return False

            usuario_actual.edad = datos["edad"]

        if "telefono" in datos:
            if not self.validador_telefono.validar(datos["telefono"]):
                return False

            usuario_actual.telefono = datos["telefono"]

        if "contrasena" in datos:
            usuario_actual.contrasena = datos["contrasena"]

        self.servicio_usuario.guardar()
        return True
