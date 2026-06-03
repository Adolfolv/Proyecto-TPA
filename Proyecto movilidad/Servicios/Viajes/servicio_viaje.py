from random import Random

<<<<<<< HEAD
from Servicios.Viajes.datos_viaje import LUGARES_OSORNO
from Servicios.Viajes.servicio_viaje_conductor import ServicioViajeConductor
from Servicios.Viajes.servicio_viaje_pasajero import ServicioViajePasajero
from Servicios.Viajes.servicios_compartidos import ServicioPagoViaje, ServicioViajeComun
=======
from Modelos.Viaje.modelo_viajes import (
    PasajeroEncontrado,
    PasajeroSimulado,
    ResultadoBusquedaVehiculos,
    ResultadoViaje,
    RutasViaje,
    VehiculoDisponible,
    Viaje,
)
from Servicios.Viajes.datos_viaje import (
    CALLES_OSORNO,
    CONDUCTORES_SIMULADOS,
    LUGARES_OSORNO,
    PASAJEROS_SIMULADOS,
)
from Servicios.Viajes.trayectoria import Trayectoria
from Validaciones.validaciones_viaje import ValidacionesViaje
>>>>>>> f1f87bdc14be7cf8c2d6afd1c39f8a1dc16ac266


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
    ):
        randomizador = randomizador or Random()
        self.comun = ServicioViajeComun(trayectoria)
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
<<<<<<< HEAD
=======


class ServicioViajeComun:
    """Operaciones compartidas: rutas, tiempos y distancias."""

    def __init__(self, trayectoria=None):
        self.viajes = []
        self.trayectoria = trayectoria or Trayectoria()

    def obtener_punto_lugar(self, nombre_lugar):
        return LUGARES_OSORNO[nombre_lugar]

    def calcular_tiempo_por_km(self, distancia):
        if distancia <= 0:
            return 0
        return min(20, max(1, round(distancia * 4)))

    def calcular_km_trayectoria(self, ruta_relativa):
        if len(ruta_relativa) < 2:
            return 0

        distancia = 0
        for inicio, destino in zip(ruta_relativa, ruta_relativa[1:]):
            distancia += self.calcular_km_entre_coordenadas(
                self.trayectoria.coordenada_real(inicio),
                self.trayectoria.coordenada_real(destino),
            )
        return distancia

    def calcular_km_entre_coordenadas(self, inicio, destino):
        latitud_inicio, longitud_inicio = inicio
        latitud_destino, longitud_destino = destino
        radio_tierra = 6371
        diferencia_latitud = radians(latitud_destino - latitud_inicio)
        diferencia_longitud = radians(longitud_destino - longitud_inicio)
        a = (
            sin(diferencia_latitud / 2) ** 2
            + cos(radians(latitud_inicio))
            * cos(radians(latitud_destino))
            * sin(diferencia_longitud / 2) ** 2
        )
        return 2 * radio_tierra * asin(sqrt(a))

    def calcular_tiempos_viaje(self, km_para_llegar, km_transportando):
        distancia_total = km_para_llegar + km_transportando
        if distancia_total <= 0:
            return {
                "tiempo_para_llegar": 0,
                "tiempo_transportando": 0,
            }
        if km_para_llegar <= 0:
            return {
                "tiempo_para_llegar": 0,
                "tiempo_transportando": self.calcular_tiempo_por_km(km_transportando),
            }
        if km_transportando <= 0:
            return {
                "tiempo_para_llegar": self.calcular_tiempo_por_km(km_para_llegar),
                "tiempo_transportando": 0,
            }

        duracion_total = self.calcular_tiempo_por_km(distancia_total)
        if duracion_total <= 1:
            return {
                "tiempo_para_llegar": 1,
                "tiempo_transportando": 0,
            }

        tiempo_para_llegar = round(duracion_total * (km_para_llegar / distancia_total))
        tiempo_para_llegar = min(duracion_total - 1, max(1, tiempo_para_llegar))
        tiempo_transportando = duracion_total - tiempo_para_llegar
        return {
            "tiempo_para_llegar": tiempo_para_llegar,
            "tiempo_transportando": tiempo_transportando,
        }

    def formar_trayectoria(self, ubicacion_inicial, ubicacion_final):
        inicio = self.obtener_punto_lugar(ubicacion_inicial)
        destino = self.obtener_punto_lugar(ubicacion_final)
        return self.formar_trayectoria_por_puntos(inicio, destino)

    def formar_trayectoria_por_puntos(self, inicio, destino):
        ruta_relativa = self.trayectoria.calcular_trayectoria(inicio, destino)
        return [self.trayectoria.coordenada_real(punto) for punto in ruta_relativa]

    def iniciar_viaje(self, viaje, usuario):
        self.viajes.append(viaje)
        return viaje

    def nombre_usuario(self, usuario):
        if usuario is None:
            return ""
        return f"{getattr(usuario, 'nombre', '')} {getattr(usuario, 'apellido', '')}".strip()


class ServicioPagoViaje:
    """Reglas de pago propias del flujo de viajes."""

    def __init__(self, servicio_billetera=None):
        self.servicio_billetera = servicio_billetera

    def cobrar_pasajero(self, usuario, monto):
        if self.servicio_billetera is None:
            raise ValueError("No se pudo realizar el pago del viaje.")

        if getattr(usuario, "tipo_usuario", "") != "pasajero":
            raise ValueError("No se pudo realizar el pago del viaje.")

        self.servicio_billetera.pagar(usuario, monto)
        return True

    def abonar_conductor(self, usuario, monto):
        if self.servicio_billetera is None:
            raise ValueError("No se pudo abonar el pago al conductor.")

        if getattr(usuario, "tipo_usuario", "") != "conductor":
            raise ValueError("No se pudo abonar el pago al conductor.")

        self.servicio_billetera.recibir_pago(usuario, monto)
        return True


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
        viaje = self.crear_viaje(vehiculo, usuario)
        self.comun.iniciar_viaje(viaje, usuario)
        return ResultadoViaje(True, rutas_viaje=rutas_viaje, viaje=viaje)

    def crear_viaje(self, vehiculo, usuario):
        return Viaje(
            pasajero=self.comun.nombre_usuario(usuario),
            conductor=vehiculo.nombre_completo,
            vehiculo=vehiculo.vehiculo,
            precio=float(vehiculo.precio),
            distancia=float(vehiculo.distancia),
            duracion=float(vehiculo.tiempo),
        )

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
            vehiculos.append(self.obtener_datos_vehiculo(conductor, punto_conductor, distancia))
        return vehiculos

    def obtener_punto_conductor_random(self):
        calle = self.randomizador.choice(CALLES_OSORNO)
        return self.randomizador.choice(calle.puntos)

    def obtener_datos_vehiculo(self, conductor, punto_conductor, distancia):
        return VehiculoDisponible(
            nombre_completo=f"{conductor.nombre} {conductor.apellido}",
            vehiculo=f"{conductor.marca_vehiculo} {conductor.modelo_vehiculo}",
            patente=conductor.patente,
            imagen=conductor.imagen,
            precio=float(conductor.precio),
            distancia=distancia,
            tiempo=self.comun.calcular_tiempo_por_km(distancia),
            ubicacion_relativa=punto_conductor,
            ubicacion_real=self.comun.trayectoria.coordenada_real(punto_conductor),
        )


class ServicioViajeConductor:
    """Caso de uso donde un conductor busca y acepta un pasajero."""

    def __init__(self, servicio_comun, randomizador=None, servicio_pagos=None):
        self.comun = servicio_comun
        self.randomizador = randomizador or Random()
        self.servicio_pagos = servicio_pagos or ServicioPagoViaje()

    def buscar_pasajeros(self, ubicacion_inicial):
        pasajero = self.randomizador.choice(PASAJEROS_SIMULADOS)
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
        return PasajeroEncontrado(
            nombre_completo=f"{pasajero.nombre} {pasajero.apellido}",
            vehiculo=f"{pasajero.marca_vehiculo} {pasajero.modelo_vehiculo}",
            trayecto=f"{pasajero.ubicacion_inicial} -> {pasajero.ubicacion_final}",
            ubicacion_inicial=pasajero.ubicacion_inicial,
            ubicacion_final=pasajero.ubicacion_final,
            ubicacion_conductor=ubicacion_conductor,
            imagen=pasajero.imagen,
            precio=float(pasajero.pago),
            distancia=distancias["km_para_llegar"] + distancias["km_transportando"],
            duracion=tiempos["tiempo_para_llegar"] + tiempos["tiempo_transportando"],
            km_para_llegar=distancias["km_para_llegar"],
            km_transportando=distancias["km_transportando"],
            tiempo_para_llegar=tiempos["tiempo_para_llegar"],
            tiempo_transportando=tiempos["tiempo_transportando"],
            duracion_busqueda=duracion_busqueda,
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
        viaje = self.crear_viaje(pasajero, conductor)
        self.servicio_pagos.abonar_conductor(conductor, viaje.precio)
        self.comun.iniciar_viaje(viaje, conductor)
        return ResultadoViaje(True, rutas_viaje=rutas_viaje, viaje=viaje)

    def crear_viaje(self, pasajero, conductor):
        return Viaje(
            pasajero=pasajero.nombre_completo,
            conductor=self.comun.nombre_usuario(conductor),
            vehiculo=pasajero.vehiculo,
            precio=float(pasajero.precio),
            distancia=float(pasajero.distancia),
            duracion=float(pasajero.duracion),
        )

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
>>>>>>> f1f87bdc14be7cf8c2d6afd1c39f8a1dc16ac266
