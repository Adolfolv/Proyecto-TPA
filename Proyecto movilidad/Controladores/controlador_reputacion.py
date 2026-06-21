from dataclasses import dataclass, field


@dataclass
class ResultadoReputacion:
    datos: dict = field(default_factory=dict)
    error: str = ""

    @property
    def exitoso(self):
        return self.error == ""


class ControladorReputacion:
    """Adapta las acciones de la vista sin capturar excepciones."""

    def __init__(self, servicio_reputacion):
        self.servicio_reputacion = servicio_reputacion

    def listar_conductores(self):
        return self.servicio_reputacion.listar_conductores()

    def cargar_reputacion(self, conductor):
        datos, error = self.servicio_reputacion.obtener_reputacion(conductor)
        return ResultadoReputacion(datos, error)

    def agregar_opinion(self, conductor, usuario, estrellas, comentario):
        datos, error = self.servicio_reputacion.agregar_opinion(
            conductor,
            usuario,
            estrellas,
            comentario,
        )
        return ResultadoReputacion(datos, error)
