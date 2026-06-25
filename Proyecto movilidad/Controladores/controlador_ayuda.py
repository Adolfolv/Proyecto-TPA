from Modelos.resultado import ResultadoOperacion


class ControladorAyuda:
    """Adapta la vista de ayuda al servicio sin exponer detalles de IA."""

    def __init__(self, servicio_ayuda):
        self.servicio_ayuda = servicio_ayuda

    def pedir_solicitud(self, solicitud=None, usuario=None):
        try:
            respuesta = self.servicio_ayuda.pedir_solicitud(solicitud, usuario)
            return ResultadoOperacion(datos=respuesta)
        except Exception as error:
            return ResultadoOperacion(error=str(error))
