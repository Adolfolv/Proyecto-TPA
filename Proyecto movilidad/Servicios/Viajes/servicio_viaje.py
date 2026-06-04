from Servicios.Viajes.servicio_viaje_conductor import ServicioViajeConductor
from Servicios.Viajes.servicio_viaje_pasajero import ServicioViajePasajero
from Servicios.Viajes.servicios_compartidos import ServicioPagoViaje, ServicioViajeComun


class ServicioViaje:
    """Fachada del modulo de viajes.

    Mantiene una entrada simple para el controlador y delega la logica real en
    servicios especializados: pasajero, conductor, pagos y operaciones comunes.
    """

    def __init__(self, servicio_billetera):
        self.comun = ServicioViajeComun()
        self.pagos = ServicioPagoViaje(servicio_billetera)
        self.pasajero = ServicioViajePasajero(self.comun, self.pagos)
        self.conductor = ServicioViajeConductor(self.comun, self.pagos)

    def buscar_pasajeros(self, ubicacion_conductor):
        return self.conductor.buscar_pasajeros(ubicacion_conductor)

    def buscar_vehiculos(self, cantidad_usuarios, ubicacion_inicial, ubicacion_final):
        return self.pasajero.buscar_vehiculos(cantidad_usuarios,ubicacion_inicial,ubicacion_final)

    def confirmar_viaje_pasajero(self, usuario, vehiculo, ubicacion_inicial, ubicacion_final):
        return self.pasajero.confirmar_viaje(usuario,vehiculo,ubicacion_inicial,ubicacion_final)

    def iniciar_viaje_conductor(self, pasajero, conductor):
        return self.conductor.iniciar_viaje(pasajero, conductor)
