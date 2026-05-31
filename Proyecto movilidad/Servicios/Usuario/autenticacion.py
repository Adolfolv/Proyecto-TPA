from Validaciones.inicio_sesion import (
    ValidadorContrasenaUsuario,
    ValidadorUsuarioEncontrado,
)


class ServicioAutenticacion:

    def __init__(self, servicio_usuario):
        self.servicio_usuario = servicio_usuario
        self.validador_usuario_encontrado = ValidadorUsuarioEncontrado()
        self.validador_contrasena_usuario = ValidadorContrasenaUsuario()

    def iniciar_sesion(self, correo, contrasena):
        usuario = self.servicio_usuario.buscar_por_correo(correo)

        if not self.validador_usuario_encontrado.validar(usuario):
            return None

        if not self.validador_contrasena_usuario.validar((usuario, contrasena)):
            return None

        return usuario
