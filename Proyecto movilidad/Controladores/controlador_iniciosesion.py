class ControladorInicioSesion:

    def __init__(self, servicio_autenticacion):
        self.servicio_autenticacion = servicio_autenticacion

    def iniciar_sesion(self, correo, contrasena):
        return self.servicio_autenticacion.iniciar_sesion(
            correo,
            contrasena,
        )
