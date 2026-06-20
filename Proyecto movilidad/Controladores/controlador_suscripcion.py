from dataclasses import dataclass, field


@dataclass
class ResultadoSuscripcion:
    datos: object = None
    error: str = ""

    @property
    def exitoso(self):
        return not self.error


class ControladorSuscripcion:
    """Adapta los casos de uso de suscripciones para la vista Tkinter."""

    def __init__(self, servicio_suscripcion):
        self.servicio = servicio_suscripcion

    def crear(self, usuario, datos):
        return self._ejecutar(
            self.servicio.crear,
            usuario,
            datos["origen"],
            datos["destino"],
            datos["fecha_inicio"],
            datos["fecha_fin"],
            datos["dias_semana"],
            datos["hora"],
            datos["cantidad_pasajeros"],
        )

    def listar(self, usuario):
        return self._ejecutar(self.servicio.listar_suscripciones, usuario)

    def listar_viajes(self, usuario):
        return self._ejecutar(self.servicio.listar_viajes, usuario)

    def cambiar_estado(self, usuario, id_suscripcion, estado):
        return self._ejecutar(self.servicio.cambiar_estado, usuario, id_suscripcion, estado)

    def cancelar_viaje(self, usuario, id_viaje):
        return self._ejecutar(self.servicio.cancelar_viaje, usuario, id_viaje)

    def _ejecutar(self, operacion, *argumentos):
        try:
            return ResultadoSuscripcion(datos=operacion(*argumentos))
        except (ValueError, OSError) as error:
            return ResultadoSuscripcion(error=str(error))

