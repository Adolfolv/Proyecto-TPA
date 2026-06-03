from random import Random

from Servicios.Viajes.datos_viaje import LUGARES_OSORNO
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
        persistencia_usuario=None,
        trayectoria=None,
        randomizador=None,
        servicio_billetera=None,
    ):
        randomizador = randomizador or Random()
        self.comun = ServicioViajeComun(persistencia_usuario, trayectoria)
        self.pagos = ServicioPagoViaje(servicio_billetera)
        self.pasajero = ServicioViajePasajero(
            self.comun,
            randomizador=randomizador,
            servicio_pagos=self.pagos,
        )
        self.conductor = ServicioViajeConductor(
            self.comun,
            randomizador=randomizador,
            servicio_pagos=self.pagos,
        )

    @property
    def viajes(self):
        return self.comun.viajes

    def obtener_lugares_disponibles(self):
        return tuple(LUGARES_OSORNO)

    def buscar_pasajeros(self, ubicacion_inicial):
        return self.conductor.buscar_pasajeros(ubicacion_inicial)

    def buscar_vehiculos(self, cantidad_usuarios, ubicacion_inicial, ubicacion_final):
        return self.pasajero.buscar_vehiculos(
            cantidad_usuarios,
            ubicacion_inicial,
            ubicacion_final,
        )

    def obtener_error_busqueda_vehiculos(self):
        return self.pasajero.obtener_error_busqueda_vehiculos()

    def obtener_vehiculos_encontrados(self):
        return self.pasajero.obtener_vehiculos_encontrados()

    def formar_ruta_busqueda_pasajero(self, ubicacion_inicial, ubicacion_final):
        return self.pasajero.formar_ruta_busqueda(ubicacion_inicial, ubicacion_final)

    def formar_rutas_viaje_pasajero(self, vehiculo, ubicacion_inicial, ubicacion_final):
        return self.pasajero.formar_rutas_inicio_viaje(
            vehiculo,
            ubicacion_inicial,
            ubicacion_final,
        )

    def formar_rutas_viaje_conductor(self, pasajero):
        return self.conductor.formar_rutas_inicio_viaje(pasajero)

    def formar_ruta_pasajero_conductor(self, pasajero):
        return self.conductor.formar_ruta_pasajero(pasajero)

    def confirmar_viaje_pasajero(self, usuario, vehiculo, ubicacion_inicial, ubicacion_final):
        return self.pasajero.confirmar_viaje(
            usuario,
            vehiculo,
            ubicacion_inicial,
            ubicacion_final,
        )

    def iniciar_viaje_conductor(self, pasajero, conductor):
        return self.conductor.iniciar_viaje(pasajero, conductor)

    def formar_trayectoria(self, ubicacion_inicial, ubicacion_final):
        return self.comun.formar_trayectoria(ubicacion_inicial, ubicacion_final)

    def formar_trayectoria_por_puntos(self, inicio, destino):
        return self.comun.formar_trayectoria_por_puntos(inicio, destino)

    def iniciar_viaje(self, viaje, usuario):
        return self.comun.iniciar_viaje(viaje, usuario)

    def calcular_tiempo_por_km(self, distancia):
        return self.comun.calcular_tiempo_por_km(distancia)

    def calcular_km_trayectoria(self, ruta_relativa):
        return self.comun.calcular_km_trayectoria(ruta_relativa)

    def calcular_km_entre_coordenadas(self, inicio, destino):
        return self.comun.calcular_km_entre_coordenadas(inicio, destino)

    def calcular_tiempos_viaje(self, km_para_llegar, km_transportando):
        return self.comun.calcular_tiempos_viaje(km_para_llegar, km_transportando)
