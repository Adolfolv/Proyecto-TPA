import json
import urllib.request

from Servicios.Viajes.datos_viaje import (
    OSORNO_LAT_NORTE,
    OSORNO_LAT_SUR,
    OSORNO_LNG_ESTE,
    OSORNO_LNG_OESTE,
)
#.
URL_OSRM = "http://router.project-osrm.org/route/v1/driving"
TIMEOUT_OSRM = 4


class Trayectoria:
    def coordenada_real(self, punto):
        x = min(1.0, max(0.0, punto[0]))
        y = min(1.0, max(0.0, punto[1]))
        latitud = OSORNO_LAT_NORTE + y * (OSORNO_LAT_SUR - OSORNO_LAT_NORTE)
        longitud = OSORNO_LNG_OESTE + x * (OSORNO_LNG_ESTE - OSORNO_LNG_OESTE)
        return latitud, longitud

    def punto_relativo_desde_coordenada(self, latitud, longitud):
        x = (longitud - OSORNO_LNG_OESTE) / (OSORNO_LNG_ESTE - OSORNO_LNG_OESTE)
        y = (latitud - OSORNO_LAT_NORTE) / (OSORNO_LAT_SUR - OSORNO_LAT_NORTE)
        return (
            min(1.0, max(0.0, round(x, 5))),
            min(1.0, max(0.0, round(y, 5))),
        )

    def limpiar_puntos(self, puntos, umbral=0.001):
        limpios = []
        for punto in puntos:
            if not limpios:
                limpios.append(punto)
                continue

            ultimo_punto = limpios[-1]

            distancia_x = ultimo_punto[0] - punto[0]
            distancia_y = ultimo_punto[1] - punto[1]
            
            if (distancia_x * distancia_x + distancia_y * distancia_y) ** 0.5 > umbral:
                limpios.append(punto)
        return limpios

    def calcular_trayectoria(self, inicio, destino):
        latitud_inicio, longitud_inicio = self.coordenada_real(inicio)
        latitud_destino, longitud_destino = self.coordenada_real(destino)
        url = (
            f"{URL_OSRM}/{longitud_inicio},{latitud_inicio};{longitud_destino},{latitud_destino}"
            "?overview=full&geometries=geojson&steps=false"
        )

        with urllib.request.urlopen(url, timeout=TIMEOUT_OSRM) as respuesta:  # noqa: S310
            datos = json.loads(respuesta.read())

        coordenadas = datos["routes"][0]["geometry"]["coordinates"]
        puntos = [
            self.punto_relativo_desde_coordenada(latitud, longitud)
            for longitud, latitud in coordenadas
        ]
        return self.limpiar_puntos(puntos)
