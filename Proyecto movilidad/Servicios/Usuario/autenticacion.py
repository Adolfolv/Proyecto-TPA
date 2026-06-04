from Validaciones.inicio_sesion import (
    ValidadorContrasenaUsuario,
    ValidadorUsuarioEncontrado,
)
from Servicios.Usuario.buscador import BuscadorUsuario, BuscadorUsuarioPorCorreo

#_
class ServicioAutenticacion:

    def __init__(self, repositorio_usuario, buscador_usuario=None):
        self.repositorio_usuario = repositorio_usuario
        self.buscador_usuario = buscador_usuario or BuscadorUsuario(repositorio_usuario)
        self.validador_usuario_encontrado = ValidadorUsuarioEncontrado()
        self.validador_contrasena_usuario = ValidadorContrasenaUsuario()
        self.buscador_usuario_por_correo = BuscadorUsuarioPorCorreo(repositorio_usuario)

    def iniciar_sesion(self, correo, contrasena):
        usuario = self.buscador_usuario_por_correo.buscar(correo)

        if not self.validador_usuario_encontrado.validar(usuario):
            return None

        if not self.validador_contrasena_usuario.validar((usuario, contrasena)):
            return None

        return usuario
