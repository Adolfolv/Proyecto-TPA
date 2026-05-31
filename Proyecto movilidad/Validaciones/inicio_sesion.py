from abstracciones import Validador


class ValidadorUsuarioEncontrado(Validador):
    def validar(self, valor):
        return valor is not None


class ValidadorContrasenaUsuario(Validador):
    def validar(self, datos):
        usuario, contrasena = datos
        return getattr(usuario, "contrasena", None) == contrasena
