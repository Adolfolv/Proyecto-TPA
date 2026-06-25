from abstracciones import Validador
from Servicios.Usuario.seguridad_contrasena import SeguridadContrasena


class ValidadorUsuarioEncontrado(Validador):
    def validar(self, valor):
        return valor is not None


class ValidadorContrasenaUsuario(Validador):
    def __init__(self, seguridad=None):
        self.seguridad = seguridad or SeguridadContrasena()

    def validar(self, datos):
        usuario, contrasena = datos
        return self.seguridad.verificar(contrasena, getattr(usuario, "contrasena", ""))
