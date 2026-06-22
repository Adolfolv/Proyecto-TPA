from Modelos.resultado import ResultadoOperacion


class ControladorReputacion:
    """Adapta las acciones y transforma errores para la vista."""

    def __init__(self, servicio_reputacion):
        self.servicio_reputacion = servicio_reputacion

    def listar_conductores(self):
        return self.servicio_reputacion.listar_conductores()

    def cargar_reputacion(self, conductor):
        try:
            datos = self.servicio_reputacion.obtener_reputacion(conductor)
            return ResultadoOperacion(datos=datos)
        except ValueError as error:
            return ResultadoOperacion(error=str(error))

    def agregar_opinion(self, conductor, usuario, estrellas, comentario):
        try:
            datos = self.servicio_reputacion.agregar_opinion(
                conductor,
                usuario,
                estrellas,
                comentario,
            )
            return ResultadoOperacion(datos=datos)
        except ValueError as error:
            return ResultadoOperacion(error=str(error))
