from modelo_Usuario.generador_de_usuario import GeneradorID
from Billetera.datos_billetera import Billetera


class ServicioRegistro:
    """
    Responsable del registro de usuarios.
    """

    def __init__(self, servicio_usuario):
        self.servicio_usuario = (servicio_usuario)

    def registrar_usuario(self, usuario):
        usuario_existente = (self.servicio_usuario.buscar_por_correo(usuario.correo)
        )

        if usuario_existente is not None:
            raise ValueError(
                "El correo ya se encuentra registrado."
            )

        if usuario.id_usuario is None:
            usuario.id_usuario = (GeneradorID.generar("USR"))

        if (getattr(usuario, "billetera", None)
            is None
        ):
            usuario.billetera = (
                Billetera()
            )

        return (
            self.servicio_usuario
            .agregar(usuario)
        )


class ServicioAutenticacion:

    def __init__(self, servicio_usuario):
        self.servicio_usuario = servicio_usuario

    def iniciar_sesion(
        self,
        correo,
        contrasena,
    ):
        usuario = (
            self.servicio_usuario
            .buscar_por_correo(correo)
        )

        if usuario is None:
            return None

        if usuario.contraseña != contrasena:
            return None

        return usuario