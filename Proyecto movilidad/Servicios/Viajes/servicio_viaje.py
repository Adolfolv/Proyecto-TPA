from math import asin, cos, radians, sin, sqrt
from random import choice, randint

from Servicios.Viajes.datos_viaje import LUGARES_OSORNO, PASAJEROS_SIMULADOS
from Servicios.Viajes.persistencia_usuario import PersistenciaUsuarioViajes
from Servicios.Viajes.trayectoria import Trayectoria

#.
class ServicioViaje:
    def __init__(self, persistencia_usuario=None):
        self.viajes = []
        self.persistencia_usuario = persistencia_usuario or PersistenciaUsuarioViajes()
        self.trayectoria = Trayectoria()

    def buscar_pasajeros(
        self,
        ubicacion_inicial,
    ):
        pasajero = choice(PASAJEROS_SIMULADOS)
        datos_pasajero = self.obtener_datos_pasajero(pasajero, ubicacion_inicial)
        datos_pasajero["duracion_busqueda"] = randint(5, 10)
        return datos_pasajero

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
                "tiempo_transportando": 20,
            }
        if km_transportando <= 0:
            return {
                "tiempo_para_llegar": 20,
                "tiempo_transportando": 0,
            }

        tiempo_para_llegar = round(20 * (km_para_llegar / distancia_total))
        tiempo_para_llegar = min(19, max(1, tiempo_para_llegar))
        tiempo_transportando = 20 - tiempo_para_llegar
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
        ruta_relativa = self.trayectoria.calcular_trayectoria(inicio, destino)
        return [self.trayectoria.coordenada_real(punto) for punto in ruta_relativa]

#Esta funcion recibe los datos del pasajero y el viaje, con unos datos se va a encargar de animar el viaje, 
#y con otros datos se va a encargar de guardar el viaje en el historial del usuario
    def iniciar_viaje(self, viaje, usuario):
        self.viajes.append(viaje)
        return self.persistencia_usuario.guardar_viaje(usuario, viaje)
