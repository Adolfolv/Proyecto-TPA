class ControladorViajeBase:
    """Operaciones compartidas por los controladores del modulo de viaje.."""

    def __init__(self, servicio_viaje):
        self.servicio_viaje = servicio_viaje

    def obtener_lugares_disponibles(self):
        return self.servicio_viaje.comun.obtener_lugares_disponibles()


class ControladorViajePasajero(ControladorViajeBase):
    """Controlador del flujo donde el usuario solicita un viaje."""

    def buscar_vehiculos_pasajero(self, cantidad_usuarios, ubicacion_inicial, ubicacion_final):
        return self.servicio_viaje.buscar_vehiculos(
            cantidad_usuarios,
            ubicacion_inicial,
            ubicacion_final,
        )

    def confirmar_pago_pasajero(self, usuario, vehiculo, ubicacion_inicial, ubicacion_final):
        return self.servicio_viaje.confirmar_viaje_pasajero(
            usuario,
            vehiculo,
            ubicacion_inicial,
            ubicacion_final,
        )


class ControladorViajeConductor(ControladorViajeBase):
    """Controlador del flujo donde el conductor acepta un viaje."""

    def buscar_pasajero_conductor(self, ubicacion_conductor):
        return self.servicio_viaje.buscar_pasajeros(ubicacion_conductor)

    def iniciar_viaje_conductor(self, pasajero, conductor):
        return self.servicio_viaje.iniciar_viaje_conductor(pasajero, conductor)
