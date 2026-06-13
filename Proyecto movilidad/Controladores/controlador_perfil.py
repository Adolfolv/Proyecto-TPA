from dataclasses import dataclass, field


@dataclass
class ResultadoPerfil:
    datos: dict = field(default_factory=dict)
    error: str = ""

    @property
    def exitoso(self):
        return self.error == ""


class ControladorPerfil:
    """Adapta los datos del usuario para la vista de perfil."""

    def __init__(self, servicio_perfil):
        self.servicio_perfil = servicio_perfil

    def obtener_perfil(self, usuario):
        try:
            return ResultadoPerfil(datos=self.servicio_perfil.obtener_perfil(usuario))
        except ValueError as error:
            return ResultadoPerfil(error=str(error))

    def actualizar_perfil(self, usuario, nombre, apellido, correo, telefono):
        try:
            return ResultadoPerfil(
                datos=self.servicio_perfil.actualizar_perfil(
                    usuario,
                    {
                        "nombre": nombre,
                        "apellido": apellido,
                        "correo": correo,
                        "telefono": telefono,
                    },
                )
            )
        except ValueError as error:
            return ResultadoPerfil(error=str(error))
