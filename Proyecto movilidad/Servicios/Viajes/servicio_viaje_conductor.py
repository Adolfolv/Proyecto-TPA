from random import Random

from Modelos.Viaje.modelo_viajes import PasajeroSimulado, ResultadoViaje, RutasViaje
from Servicios.Viajes.datos_viaje import PASAJEROS_SIMULADOS
from Servicios.Viajes.servicios_compartidos import ServicioPagoViaje


class ServicioViajeConductor:
    """Caso de uso donde un conductor busca y acepta un pasajero."""

    def __init__(self, servicio_comun, randomizador=None, servicio_pagos=None):
        self.comun = servicio_comun
        self.randomizador = randomizador or Random()
        self.servicio_pagos = servicio_pagos or ServicioPagoViaje()

    def buscar_pasajeros(self, ubicacion_inicial):
        pasajeros = [
            pasajero
            for pasajero in PASAJEROS_SIMULADOS
            if pasajero.ubicacion_inicial == ubicacion_inicial
        ]
        if not pasajeros:
            return None

        pasajero = self.randomizador.choice(pasajeros)
        duracion_busqueda = self.randomizador.randint(5, 10)
        return self.obtener_datos_pasajero(
            pasajero,
            ubicacion_inicial,
            duracion_busqueda,
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

    def formar_rutas_inicio_viaje(self, pasajero):
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
        rutas_viaje = self.formar_rutas_inicio_viaje(pasajero)
        viaje = self.comun.fabrica.crear_viaje_conductor(pasajero, conductor)
        self.servicio_pagos.abonar_conductor(conductor, viaje.precio)
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
