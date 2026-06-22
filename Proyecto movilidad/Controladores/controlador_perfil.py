from Modelos.resultado import ResultadoOperacion


class ControladorPerfil:
    """Adapta los datos del usuario para la vista de perfil."""

    def __init__(self, servicio_perfil):
        self.servicio_perfil = servicio_perfil

    def obtener_perfil(self, usuario):
        try:
            return ResultadoOperacion(datos=self.servicio_perfil.obtener_perfil(usuario))
        except ValueError as error:
            return ResultadoOperacion(error=str(error))

    def actualizar_perfil(self, usuario, nombre, apellido, correo, telefono):
        try:
            return ResultadoOperacion(
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
            return ResultadoOperacion(error=str(error))
