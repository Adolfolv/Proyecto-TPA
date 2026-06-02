from math import asin, cos, radians, sin, sqrt
from random import choice, randint, sample

from Servicios.Viajes.datos_viaje import CALLES_OSORNO, CONDUCTORES_SIMULADOS, LUGARES_OSORNO, PASAJEROS_SIMULADOS
from Servicios.Viajes.persistencia_usuario import PersistenciaUsuarioViajes
from Servicios.Viajes.trayectoria import Trayectoria
from Servicios.Validaciones.validaciones_viaje import ValidacionesViaje

#.
class ServicioViaje:
    def __init__(self, persistencia_usuario=None):
        self.viajes = []
        self.persistencia_usuario = persistencia_usuario or PersistenciaUsuarioViajes()
        self.trayectoria = Trayectoria()
        self.validaciones = ValidacionesViaje()

    # --- flujo conductor ---
    def buscar_pasajeros(self, ubicacion_inicial):
        pasajero = choice(PASAJEROS_SIMULADOS)
        datos_pasajero = self.obtener_datos_pasajero(pasajero, ubicacion_inicial)
        datos_pasajero["duracion_busqueda"] = randint(5, 10)
        return datos_pasajero

    # --- flujo pasajero ---
    def buscar_vehiculos(self, cantidad_usuarios, ubicacion_inicial, ubicacion_final):
        valido, error = self.validaciones.validar_busqueda_vehiculos(
            cantidad_usuarios,
            ubicacion_inicial,
            ubicacion_final,
        )
        if not valido:
            return {
                "ok": False,
                "error": error,
                "vehiculos": [],
            }

        return {
            "ok": True,
            "error": "",
            "vehiculos": self.obtener_vehiculos_disponibles(ubicacion_inicial),
        }

    def obtener_vehiculos_disponibles(self, ubicacion_inicial):
        vehiculos = []
        cantidad_vehiculos = min(5, len(CONDUCTORES_SIMULADOS))
        conductores = sample(CONDUCTORES_SIMULADOS, cantidad_vehiculos)
        ubicacion_pasajero = LUGARES_OSORNO[ubicacion_inicial]

        for conductor in conductores:
            punto_conductor = self.obtener_punto_conductor_random()
            distancia = round(self.calcular_km_trayectoria([ubicacion_pasajero, punto_conductor]), 2)
            vehiculos.append(self.obtener_datos_vehiculo(conductor, punto_conductor, distancia))
        return vehiculos

    def obtener_punto_conductor_random(self):
        calle = choice(CALLES_OSORNO)
        puntos_calle = calle[1]
        return choice(puntos_calle)

    def obtener_datos_vehiculo(self, conductor, punto_conductor, distancia):
        return {
            "nombre_completo": f"{conductor['nombre']} {conductor['apellido']}",
            "vehiculo": f"{conductor['marca_vehiculo']} {conductor['modelo_vehiculo']}",
            "patente": conductor["patente"],
            "imagen": conductor["imagen"],
            "precio": float(conductor["precio"]),
            "distancia": distancia,
            "tiempo": self.calcular_tiempo_por_km(distancia),
            "ubicacion_relativa": punto_conductor,
            "ubicacion_real": self.trayectoria.coordenada_real(punto_conductor),
        }

    def calcular_tiempo_por_km(self, distancia):
        if distancia <= 0:
            return 0
        return min(20, max(1, round(distancia * 4)))

    def obtener_datos_pasajero(self, pasajero, ubicacion_conductor):
        distancias = self.calcular_km_viaje(ubicacion_conductor, pasajero)
        tiempos = self.calcular_tiempos_viaje(
            distancias["km_para_llegar"],
            distancias["km_transportando"],
        )
        return {
            "nombre_completo": f"{pasajero['nombre']} {pasajero['apellido']}",
            "vehiculo": f"{pasajero['marca_vehiculo']} {pasajero['modelo_vehiculo']}",
            "trayecto": f"{pasajero['ubicacion_inicial']} -> {pasajero['ubicacion_final']}",
            "ubicacion_inicial": pasajero["ubicacion_inicial"],
            "ubicacion_final": pasajero["ubicacion_final"],
            "ubicacion_conductor": ubicacion_conductor,
            "imagen": pasajero["imagen"],
            "precio": float(pasajero["pago"]),
            "distancia": distancias["km_para_llegar"] + distancias["km_transportando"],
            "duracion": tiempos["tiempo_para_llegar"] + tiempos["tiempo_transportando"],
            **distancias,
            **tiempos,
        }

    def calcular_km_viaje(self, ubicacion_conductor, pasajero):
        ruta_llegada = self.trayectoria.calcular_trayectoria(
            LUGARES_OSORNO[ubicacion_conductor],
            LUGARES_OSORNO[pasajero["ubicacion_inicial"]],
        )
        ruta_transporte = self.trayectoria.calcular_trayectoria(
            LUGARES_OSORNO[pasajero["ubicacion_inicial"]],
            LUGARES_OSORNO[pasajero["ubicacion_final"]],
        )
        return {
            "km_para_llegar": round(self.calcular_km_trayectoria(ruta_llegada), 2),
            "km_transportando": round(self.calcular_km_trayectoria(ruta_transporte), 2),
        }

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

    def formar_trayectoria(self, ubicacion_inicial, ubicacion_final):
        inicio = LUGARES_OSORNO[ubicacion_inicial]
        destino = LUGARES_OSORNO[ubicacion_final]
        return self.formar_trayectoria_por_puntos(inicio, destino)

    def formar_trayectoria_por_puntos(self, inicio, destino):
        ruta_relativa = self.trayectoria.calcular_trayectoria(inicio, destino)
        return [self.trayectoria.coordenada_real(punto) for punto in ruta_relativa]

    # --- persistencia y pago ---
    def iniciar_viaje(self, viaje, usuario):
        self.viajes.append(viaje)
        return self.persistencia_usuario.guardar_viaje(usuario, viaje)
