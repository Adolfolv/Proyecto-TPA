from random import Random

from Modelos.Viaje.modelo_viajes import ResultadoBusquedaVehiculos, ResultadoViaje, RutasViaje
from Servicios.Viajes.datos_viaje import CALLES_OSORNO, CONDUCTORES_SIMULADOS
from Servicios.Viajes.servicios_compartidos import ServicioPagoViaje
from Validaciones.validaciones_viaje import ValidacionesViaje


class ServicioViajePasajero:
    """Caso de uso donde un pasajero busca, elige y paga un vehiculo."""

    def __init__(
        self,
        servicio_comun,
        validaciones=None,
        randomizador=None,
        servicio_pagos=None,
    ):
        self.comun = servicio_comun
        self.validaciones = validaciones or ValidacionesViaje()
        self.randomizador = randomizador or Random()
        self.servicio_pagos = servicio_pagos or ServicioPagoViaje()
        self.error_busqueda_vehiculos = ""
        self.vehiculos_encontrados = []

    def buscar_vehiculos(self, cantidad_usuarios, ubicacion_inicial, ubicacion_final):
        valido, error = self.validaciones.validar_busqueda_vehiculos(
            cantidad_usuarios,
            ubicacion_inicial,
            ubicacion_final,
        )
        self.error_busqueda_vehiculos = error
        self.vehiculos_encontrados = []

        if not valido:
            return ResultadoBusquedaVehiculos(False, error=error)

        vehiculos = tuple(self.obtener_vehiculos_disponibles(ubicacion_inicial))
        ruta_busqueda = self.formar_ruta_busqueda(ubicacion_inicial, ubicacion_final)

        self.vehiculos_encontrados = list(vehiculos)
        return ResultadoBusquedaVehiculos(
            True,
            vehiculos=vehiculos,
            ruta_busqueda=ruta_busqueda,
        )

    def obtener_error_busqueda_vehiculos(self):
        return self.error_busqueda_vehiculos

    def obtener_vehiculos_encontrados(self):
        return self.vehiculos_encontrados

    def formar_ruta_busqueda(self, ubicacion_inicial, ubicacion_final):
        return self.comun.formar_trayectoria(ubicacion_inicial, ubicacion_final)

    def formar_rutas_inicio_viaje(self, vehiculo, ubicacion_inicial, ubicacion_final):
        ruta_llegada = self.comun.formar_trayectoria_por_puntos(
            vehiculo.ubicacion_relativa,
            self.comun.obtener_punto_lugar(ubicacion_inicial),
        )
        ruta_viaje = self.comun.formar_trayectoria(ubicacion_inicial, ubicacion_final)
        return RutasViaje(llegada=ruta_llegada, viaje=ruta_viaje)

    def confirmar_viaje(self, usuario, vehiculo, ubicacion_inicial, ubicacion_final):
        rutas_viaje = self.formar_rutas_inicio_viaje(
            vehiculo,
            ubicacion_inicial,
            ubicacion_final,
        )
        self.servicio_pagos.cobrar_pasajero(usuario, vehiculo.precio)
        viaje = self.comun.fabrica.crear_viaje_pasajero(vehiculo, usuario)
        self.comun.iniciar_viaje(viaje, usuario)
        return ResultadoViaje(True, rutas_viaje=rutas_viaje, viaje=viaje)

    def obtener_vehiculos_disponibles(self, ubicacion_inicial):
        vehiculos = []
        cantidad_vehiculos = min(5, len(CONDUCTORES_SIMULADOS))
        conductores = self.randomizador.sample(CONDUCTORES_SIMULADOS, cantidad_vehiculos)
        ubicacion_pasajero = self.comun.obtener_punto_lugar(ubicacion_inicial)

        for conductor in conductores:
            punto_conductor = self.obtener_punto_conductor_random()
            distancia = round(
                self.comun.calcular_km_trayectoria([ubicacion_pasajero, punto_conductor]),
                2,
            )
            vehiculos.append(
                self.comun.fabrica.crear_vehiculo_disponible(
                    conductor,
                    punto_conductor,
                    distancia,
                )
            )
        return vehiculos

    def obtener_punto_conductor_random(self):
        calle = self.randomizador.choice(CALLES_OSORNO)
        return self.randomizador.choice(calle.puntos)
