class ControladorViajeBase:
    """Operaciones compartidas por los controladores del modulo de viaje.."""

    def __init__(self, servicio_viaje):
        self.servicio_viaje = servicio_viaje

    def obtener_lugares_disponibles(self):
        return self.servicio_viaje.comun.obtener_lugares_disponibles()

    def finalizar_viaje(self, viaje):
        return self.servicio_viaje.finalizar_viaje(viaje)


class ControladorViajePasajero(ControladorViajeBase):
    """Controlador del flujo donde el usuario solicita un viaje."""

    def buscar_vehiculos_pasajero(
        self,
        cantidad_usuarios,
        ubicacion_inicial,
        ubicacion_final,
        tipo_viaje="normal",
        volumen=None,
        peso=None,
        tipo_material=None,
    ):
        return self.servicio_viaje.buscar_vehiculos(
            cantidad_usuarios,
            ubicacion_inicial,
            ubicacion_final,
            tipo_viaje,
            volumen,
            peso,
            tipo_material,
        )

    def confirmar_pago_pasajero(
        self,
        usuario,
        vehiculo,
        ubicacion_inicial,
        ubicacion_final,
        tipo_viaje="normal",
        volumen=None,
        peso=None,
        tipo_material=None,
        cantidad_pasajeros=1,
    ):
        return self.servicio_viaje.confirmar_viaje_pasajero(
            usuario,
            vehiculo,
            ubicacion_inicial,
            ubicacion_final,
            tipo_viaje,
            volumen,
            peso,
            tipo_material,
            cantidad_pasajeros,
        )


class ControladorViajeConductor(ControladorViajeBase):
    """Controlador del flujo donde el conductor acepta un viaje."""

    def buscar_pasajero_conductor(self, ubicacion_conductor):
        return self.servicio_viaje.buscar_pasajeros(ubicacion_conductor)

    def iniciar_viaje_conductor(self, pasajero, conductor):
        return self.servicio_viaje.iniciar_viaje_conductor(pasajero, conductor)
