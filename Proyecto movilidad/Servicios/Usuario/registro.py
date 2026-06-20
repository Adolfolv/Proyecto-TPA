from Modelos.Usuario.usuario_datos import Conductor
from Servicios.Usuario.generador_id import GeneradorID
from Validaciones.registro import ValidacionesUsuario, ValidacionesConductor

#.

class ServicioRegistro:

    def __init__(self, repositorio_usuario, buscador_usuario, fabrica_usuario):

        self.repositorio_usuario = repositorio_usuario
        self.fabrica_usuario = fabrica_usuario

        self.validaciones_usuario = ValidacionesUsuario(buscador_usuario)
        self.validaciones_conductor = ValidacionesConductor()

    def registrar_pasajero(self, datos, confirmar_contrasena=None):
        usuario = self.fabrica_usuario.crear_pasajero(datos)
        return self.registrar_usuario(usuario, confirmar_contrasena)

    def registrar_conductor(self, datos, confirmar_contrasena=None):
        usuario = self.fabrica_usuario.crear_conductor(datos)
        return self.registrar_usuario(usuario, confirmar_contrasena)

    def registrar_usuario(self, usuario, confirmar_contrasena=None):

        self.validaciones_usuario.validar(usuario, confirmar_contrasena)

        if isinstance(usuario, Conductor):
            self.validaciones_conductor.validar(usuario)

        if usuario.id_usuario is None:
            usuario.id_usuario = GeneradorID.generar("USR")

        # PERSISTENCIA
        return self.repositorio_usuario.agregar(usuario)
