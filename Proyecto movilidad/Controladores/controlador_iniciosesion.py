from dataclasses import dataclass


@dataclass
class ResultadoInicioSesion:
    usuario: object = None
    error: str = ""

    @property
    def exitoso(self):
        return self.usuario is not None and self.error == ""


class ControladorInicioSesion:

    def __init__(self, servicio_autenticacion):
        self.servicio_autenticacion = servicio_autenticacion

    def iniciar_sesion(self, correo, contrasena):
        usuario = self.servicio_autenticacion.iniciar_sesion(
            correo,
            contrasena,
        )

        # El controlador traduce el fallo del servicio a un resultado que la
        # vista puede mostrar sin conocer detalles internos de autenticacion.
        if usuario is None:
            return ResultadoInicioSesion(
                error=getattr(
                    self.servicio_autenticacion,
                    "ultimo_error",
                    "credenciales",
                )
            )

        return ResultadoInicioSesion(usuario=usuario)
