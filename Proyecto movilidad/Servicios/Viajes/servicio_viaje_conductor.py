from random import Random

from Modelos.Viaje.modelo_viajes import (
    PasajeroSimulado,
    ResultadoBusquedaPasajero,
    ResultadoViaje,
    RutasViaje,
)
from Servicios.Viajes.datos_viaje import PASAJEROS_SIMULADOS


class ServicioViajeConductor:
    """Caso de uso donde un conductor busca y acepta un pasajero."""

    def __init__(
        self,
        servicio_comun,
        servicio_pagos,
    ):
        self.comun = servicio_comun
        self.pagos = servicio_pagos
        self.randomizador = randomizador or Random()

    def buscar_pasajeros(self, ubicacion_conductor):                                                           
        pasajeros = tuple(PASAJEROS_SIMULADOS)
        pasajero = self.randomizador.choice(pasajeros)
        duracion_busqueda = self.randomizador.randint(5, 10)
        pasajero_encontrado = self.obtener_datos_pasajero(
            pasajero,
            ubicacion_conductor,
            duracion_busqueda,
        )
        return ResultadoBusquedaPasajero(
            True,
            pasajero=pasajero_encontrado,
            ruta_pasajero=self.formar_ruta_pasajero(pasajero_encontrado),
        )

    def obtener_datos_pasajero(
        self,
        pasajero: PasajeroSimulado,
        ubicacion_conductor,
        duracion_busqueda,
    ):
        distancias = self.calcular_km_viaje(ubicacion_conductor, pasajero)
        tiempos = self.comun.calcular_tiempos_viaje(
            distancias["km_para_llegar"],
            distancias["km_transportando"],
        )
        return self.comun.fabrica.crear_pasajero_encontrado(
            pasajero,
            ubicacion_conductor,
            duracion_busqueda,
            distancias,
            tiempos,
        )

    def formar_rutas_viaje(self, pasajero):
        return RutasViaje(
            llegada=self.comun.formar_trayectoria(
                pasajero.ubicacion_conductor,
                pasajero.ubicacion_inicial,
            ),
            viaje=self.comun.formar_trayectoria(
                pasajero.ubicacion_inicial,
                pasajero.ubicacion_final,
            ),
        )

    def formar_ruta_pasajero(self, pasajero):
        return self.comun.formar_trayectoria(
            pasajero.ubicacion_inicial,
            pasajero.ubicacion_final,
        )

    def iniciar_viaje(self, pasajero, conductor):
        rutas_viaje = self.formar_rutas_viaje(pasajero)
        viaje = self.comun.fabrica.crear_viaje_conductor(pasajero, conductor)
        self.pagos.abonar_conductor(conductor, viaje.precio)
        self.comun.iniciar_viaje(viaje)
        return ResultadoViaje(True, rutas_viaje=rutas_viaje, viaje=viaje)

    def calcular_km_viaje(self, ubicacion_conductor, pasajero):
        ruta_llegada = self.comun.trayectoria.calcular_trayectoria(
            self.comun.obtener_punto_lugar(ubicacion_conductor),
            self.comun.obtener_punto_lugar(pasajero.ubicacion_inicial),
        )
        ruta_transporte = self.comun.trayectoria.calcular_trayectoria(
            self.comun.obtener_punto_lugar(pasajero.ubicacion_inicial),
            self.comun.obtener_punto_lugar(pasajero.ubicacion_final),
        )
        return {
            "km_para_llegar": round(self.comun.calcular_km_trayectoria(ruta_llegada), 2),
            "km_transportando": round(self.comun.calcular_km_trayectoria(ruta_transporte), 2),
        }
