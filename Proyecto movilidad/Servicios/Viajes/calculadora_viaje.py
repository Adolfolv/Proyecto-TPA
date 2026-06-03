from math import asin, cos, radians, sin, sqrt


class CalculadoraViaje:
    """Calcula distancias y tiempos usados por los casos de uso de viaje."""

    def __init__(self, trayectoria):
        self.trayectoria = trayectoria

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
