from Servicios.Viajes.servicio_viaje_conductor import ServicioViajeConductor
from Servicios.Viajes.servicio_viaje_pasajero import ServicioViajePasajero
from Servicios.Viajes.servicios_compartidos import ServicioPagoViaje, ServicioViajeComun


class ServicioViaje:
    """Fachada del modulo de viajes.

    Mantiene una entrada simple para el controlador y delega la logica real en
    servicios especializados: pasajero, conductor, pagos y operaciones comunes.
    """

    def __init__(self, servicio_billetera, servicio_historial=None):
        self.comun = ServicioViajeComun()
        self.pagos = ServicioPagoViaje(servicio_billetera)
        self.historial = servicio_historial
        self.pasajero = ServicioViajePasajero(self.comun, self.pagos)
        self.conductor = ServicioViajeConductor(self.comun, self.pagos)

    def buscar_pasajeros(self, ubicacion_conductor):
        return self.conductor.buscar_pasajeros(ubicacion_conductor)

    def buscar_vehiculos(
        self,
        cantidad_usuarios,
        ubicacion_inicial,
        ubicacion_final,
        tipo_viaje="normal",
        volumen=None,
        peso=None,
        tipo_material=None,
    ):
        return self.pasajero.buscar_vehiculos(
            cantidad_usuarios,
            ubicacion_inicial,
            ubicacion_final,
            tipo_viaje,
            volumen,
            peso,
            tipo_material,
        )

    def confirmar_viaje_pasajero(
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
        cobrar=True,
    ):
        return self.pasajero.confirmar_viaje(
            usuario,
            vehiculo,
            ubicacion_inicial,
            ubicacion_final,
            tipo_viaje,
            volumen,
            peso,
            tipo_material,
            cantidad_pasajeros,
            cobrar=cobrar,
        )

    def cobrar_suscripcion(self, usuario, monto):
        return self.pagos.cobrar_pasajero(usuario, monto)

    def reembolsar_suscripcion(self, usuario, monto):
        return self.pagos.reembolsar_pasajero(usuario, monto)

    def abonar_conductor_suscripcion(self, conductor, monto):
        return self.pagos.abonar_conductor(conductor, monto)

    def iniciar_viaje_conductor(self, pasajero, conductor):
        return self.conductor.iniciar_viaje(pasajero, conductor)

    def finalizar_viaje(self, viaje):
        if self.historial is None:
            return viaje
        return self.historial.registrar_viaje(viaje)
