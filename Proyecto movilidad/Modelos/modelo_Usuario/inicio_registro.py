from modelo_Usuario.generador_de_usuario import GeneradorID
from Billetera.datos_billetera import Billetera
from Validaciones.validaciones import (
    ValidadorContrasenaUsuario,
    ValidadorCorreo,
    ValidadorCorreoUnico,
    ValidadorEdad,
    ValidadorTelefono,
    ValidadorUsuarioEncontrado,
)

class ServicioRegistro:

    def __init__(self, servicio_usuario):
        self.servicio_usuario = servicio_usuario

        self.validador_correo = ValidadorCorreo()
        self.validador_correo_unico = ValidadorCorreoUnico(servicio_usuario)
        self.validador_edad = ValidadorEdad()
        self.validador_telefono = ValidadorTelefono()

    def registrar_usuario(self, usuario):

        if not self.validador_correo.validar(usuario.correo):
            raise ValueError("Correo invalido.")

        if not self.validador_edad.validar(usuario.edad):
            raise ValueError("Edad invalida.")

        if not self.validador_telefono.validar(usuario.telefono):
            raise ValueError("Telefono invalido.")

        if not self.validador_correo_unico.validar(usuario.correo):
            raise ValueError(
                "El correo ya se encuentra registrado."
            )

        if usuario.id_usuario is None:
            usuario.id_usuario = GeneradorID.generar("USR")

        if usuario.billetera is None:
            usuario.billetera = Billetera()

        return self.servicio_usuario.agregar(usuario)


class ServicioAutenticacion:

    def __init__(self, servicio_usuario):
        self.servicio_usuario = servicio_usuario
        self.validador_usuario_encontrado = ValidadorUsuarioEncontrado()
        self.validador_contrasena_usuario = ValidadorContrasenaUsuario()

    def iniciar_sesion(
        self,
        correo,
        contrasena,
    ):
        usuario = (
            self.servicio_usuario
            .buscar_por_correo(correo)
        )

        if not self.validador_usuario_encontrado.validar(usuario):
            return None

        if not self.validador_contrasena_usuario.validar((usuario, contrasena)):
            return None

        return usuario
