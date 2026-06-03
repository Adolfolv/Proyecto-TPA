from Validaciones.perfil import ValidadorPerfilCargado
from Validaciones.registro import ValidadorCorreo, ValidadorEdad, ValidadorTelefono


class ServicioPerfil:

    def __init__(self, buscador_usuario, repositorio_usuario):
        self.buscador_usuario = buscador_usuario
        self.repositorio_usuario = repositorio_usuario
        self.usuario_actual = None
        self.validador_perfil_cargado = ValidadorPerfilCargado()
        self.validador_correo = ValidadorCorreo()
        self.validador_edad = ValidadorEdad()
        self.validador_telefono = ValidadorTelefono()

    def cargar_perfil(self, id_usuario: int):
        self.usuario_actual = self.buscador_usuario.buscar_usuario(id_usuario)
        return self.usuario_actual

    def ver_perfil(self):
        return self.usuario_actual

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

        self.repositorio_usuario.guardar()
        return True
