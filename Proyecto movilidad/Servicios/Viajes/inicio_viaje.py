from abc import ABC, abstractmethod

from Modelos.Viaje.modelo_viajes import ResultadoViaje, RutasViaje


class InicioViaje(ABC):
    """Define el flujo extensible para iniciar un tipo de viaje."""

    captura_errores_pago = False

    def __init__(self, servicio_comun, servicio_pagos):
        self.comun = servicio_comun
        self.servicio_pagos = servicio_pagos

    def iniciar(self, datos):
        rutas_viaje = self.formar_rutas(datos)
        viaje = self.crear_viaje(datos)

        try:
            self.procesar_pago(datos, viaje)
        except ValueError as error:
            if not self.captura_errores_pago:
                raise
            return ResultadoViaje(False, error=str(error))

        self.comun.iniciar_viaje(viaje)
        return ResultadoViaje(True, rutas_viaje=rutas_viaje, viaje=viaje)

    @abstractmethod
    def formar_rutas(self, datos):
        raise NotImplementedError

    @abstractmethod
    def crear_viaje(self, datos):
        raise NotImplementedError

    @abstractmethod
    def procesar_pago(self, datos, viaje):
        raise NotImplementedError


class InicioViajePasajero(InicioViaje):
    captura_errores_pago = True

    def formar_rutas(self, datos):
        ruta_llegada = self.comun.formar_trayectoria_por_puntos(
            datos.vehiculo.ubicacion_relativa,
            self.comun.obtener_punto_lugar(datos.ubicacion_inicial),
        )
        ruta_viaje = self.comun.formar_trayectoria(
            datos.ubicacion_inicial,
            datos.ubicacion_final,
        )
        return RutasViaje(llegada=ruta_llegada, viaje=ruta_viaje)

    def crear_viaje(self, datos):
        return self.comun.fabrica.crear_viaje_pasajero(datos.vehiculo, datos.usuario)

    def procesar_pago(self, datos, viaje):
        self.servicio_pagos.cobrar_pasajero(datos.usuario, viaje.precio)


class InicioViajeConductor(InicioViaje):
    def formar_rutas(self, datos):
        pasajero = datos.pasajero
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

    def crear_viaje(self, datos):
        return self.comun.fabrica.crear_viaje_conductor(
            datos.pasajero,
            datos.conductor,
        )

    def procesar_pago(self, datos, viaje):
        self.servicio_pagos.abonar_conductor(datos.conductor, viaje.precio)
