from random import Random

from Servicios.Viajes.datos_viaje import LUGARES_OSORNO
from Servicios.Viajes.inicio_viaje import InicioViajeConductor, InicioViajePasajero
from Servicios.Viajes.servicio_viaje_conductor import ServicioViajeConductor
from Servicios.Viajes.servicio_viaje_pasajero import ServicioViajePasajero
from Servicios.Viajes.servicios_compartidos import ServicioPagoViaje, ServicioViajeComun


class ServicioViaje:
    """Fachada del modulo de viajes.

    Mantiene una entrada simple para el controlador y delega la logica real en
    servicios especializados: pasajero, conductor, pagos y operaciones comunes.
    """

    def __init__(
        self,
        trayectoria=None,
        randomizador=None,
        servicio_billetera=None,
        inicio_viaje_pasajero=None,
        inicio_viaje_conductor=None,
    ):
        randomizador = randomizador or Random()
        self.comun = ServicioViajeComun(trayectoria=trayectoria)
        self.pagos = ServicioPagoViaje(servicio_billetera)
        self.inicio_viaje_pasajero = inicio_viaje_pasajero or InicioViajePasajero(
            self.comun,
            self.pagos,
        )
        self.inicio_viaje_conductor = inicio_viaje_conductor or InicioViajeConductor(
            self.comun,
            self.pagos,
        )
        self.pasajero = ServicioViajePasajero(
            self.comun,
            randomizador=randomizador,
            inicio_viaje=self.inicio_viaje_pasajero,
        )
        self.conductor = ServicioViajeConductor(
            self.comun,
            randomizador=randomizador,
            inicio_viaje=self.inicio_viaje_conductor,
        )

    def obtener_lugares_disponibles(self):
        return tuple(LUGARES_OSORNO)

    def buscar_pasajeros(self, ubicacion_conductor):
        return self.conductor.buscar_pasajeros(ubicacion_conductor)

    def buscar_vehiculos(self, cantidad_usuarios, ubicacion_inicial, ubicacion_final):
        return self.pasajero.buscar_vehiculos(
            cantidad_usuarios,
            ubicacion_inicial,
            ubicacion_final,
        )

    def confirmar_viaje_pasajero(self, usuario, vehiculo, ubicacion_inicial, ubicacion_final):
        return self.pasajero.confirmar_viaje(
            usuario,
            vehiculo,
            ubicacion_inicial,
            ubicacion_final,
        )

    def iniciar_viaje_conductor(self, pasajero, conductor):
        return self.conductor.iniciar_viaje(pasajero, conductor)
