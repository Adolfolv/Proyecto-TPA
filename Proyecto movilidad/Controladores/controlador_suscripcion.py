"""Controladores MVC de las suscripciones de pasajero y conductor."""


class ControladorSuscripcionBase:
    def __init__(self, servicio_suscripcion):
        self.servicio = servicio_suscripcion

    def obtener_lugares_disponibles(self):
        return self.servicio.obtener_lugares_disponibles()

    @staticmethod
    def ejecutar(operacion, *argumentos):
        try:
            return operacion(*argumentos), ""
        except (ValueError, OSError) as error:
            return None, str(error)


class ControladorSuscripcionPasajero(ControladorSuscripcionBase):
    """Expone las operaciones que puede realizar el pasajero."""

    def previsualizar(self, pasajero, datos):
        return self.ejecutar(self.servicio.previsualizar, pasajero, datos["origen"], datos["destino"], datos["fecha_inicio"], datos["fecha_fin"], datos["dias_semana"], datos["hora"], datos["cantidad_pasajeros"])

    def buscar_conductores(self, cantidad_pasajeros, origen, destino):
        return self.servicio.buscar_conductores(cantidad_pasajeros, origen, destino)

    def confirmar(self, pasajero, datos):
        return self.ejecutar(self.servicio.confirmar, pasajero, datos["origen"], datos["destino"], datos["fecha_inicio"], datos["fecha_fin"], datos["dias_semana"], datos["hora"], datos["cantidad_pasajeros"], datos.get("conductor"))

    def consultar(self, pasajero):
        return self.ejecutar(lambda: (tuple(self.servicio.listar_suscripciones(pasajero)), tuple(self.servicio.listar_viajes(pasajero))))

    def cancelar_suscripcion(self, pasajero, id_suscripcion):
        return self.ejecutar(self.servicio.cancelar_suscripcion_pasajero, pasajero, id_suscripcion)

    def cancelar_viaje(self, pasajero, id_viaje):
        return self.ejecutar(self.servicio.cancelar_viaje, pasajero, id_viaje)

    def confirmar_inicio(self, pasajero, id_viaje):
        return self.ejecutar(self.servicio.confirmar_inicio, pasajero, id_viaje)

    def completar_viaje(self, pasajero, id_viaje):
        return self.ejecutar(self.servicio.completar_viaje_pasajero, pasajero, id_viaje)


class ControladorSuscripcionConductor(ControladorSuscripcionBase):
    """Expone las operaciones que puede realizar el conductor."""

    def buscar_ofertas(self, conductor):
        return self.ejecutar(self.servicio.buscar_ofertas_conductor, conductor)

    def consultar(self, conductor):
        return self.ejecutar(self.servicio.obtener_agenda_conductor, conductor)

    def agregar_suscripcion(self, conductor, id_suscripcion):
        return self.ejecutar(self.servicio.agregar_suscripcion_conductor, conductor, id_suscripcion)

    def cancelar_suscripcion(self, conductor, id_suscripcion):
        return self.ejecutar(self.servicio.cancelar_suscripcion_conductor, conductor, id_suscripcion)

    def confirmar_pasajero_abordo(self, conductor, id_viaje):
        return self.ejecutar(self.servicio.confirmar_pasajero_abordo_conductor, conductor, id_viaje)

    def finalizar_viaje(self, conductor, id_viaje):
        return self.ejecutar(self.servicio.finalizar_viaje_conductor, conductor, id_viaje)

    def cancelar_viaje(self, conductor, id_viaje):
        return self.ejecutar(self.servicio.cancelar_viaje_conductor, conductor, id_viaje)
