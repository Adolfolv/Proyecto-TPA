import json
import urllib.request

from Modelos.Viaje.modelo_viajes import PuntoRelativo


URL_OSRM = "http://router.project-osrm.org/route/v1/driving"
TIMEOUT_OSRM = 4

# Limites geograficos usados para convertir entre el mapa relativo de la
# aplicacion y coordenadas reales de Osorno.
OSORNO_LAT_NORTE = -40.5480
OSORNO_LAT_SUR = -40.6050
OSORNO_LNG_OESTE = -73.1650
OSORNO_LNG_ESTE = -73.0850


def punto_relativo_desde_coordenada(latitud: float, longitud: float) -> PuntoRelativo:
    """Convierte una coordenada real a un punto normalizado entre 0 y 1."""

    x = (longitud - OSORNO_LNG_OESTE) / (OSORNO_LNG_ESTE - OSORNO_LNG_OESTE)
    y = (latitud - OSORNO_LAT_NORTE) / (OSORNO_LAT_SUR - OSORNO_LAT_NORTE)
    return (
        min(1.0, max(0.0, round(x, 5))),
        min(1.0, max(0.0, round(y, 5))),
    )


class Trayectoria:
    """Proveedor de rutas entre puntos relativos del mapa de Osorno."""

    def coordenada_real(self, punto):
        """Convierte un punto relativo normalizado a latitud/longitud real."""

        x = min(1.0, max(0.0, punto[0]))
        y = min(1.0, max(0.0, punto[1]))
        latitud = OSORNO_LAT_NORTE + y * (OSORNO_LAT_SUR - OSORNO_LAT_NORTE)
        longitud = OSORNO_LNG_OESTE + x * (OSORNO_LNG_ESTE - OSORNO_LNG_OESTE)
        return latitud, longitud

    def limpiar_puntos(self, puntos, umbral=0.001):
        """Reduce puntos casi repetidos para que la animacion sea estable."""

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
        """Calcula una ruta por OSRM."""

        return self._calcular_trayectoria_osrm(inicio, destino)

    def _calcular_trayectoria_osrm(self, inicio, destino):
        latitud_inicio, longitud_inicio = self.coordenada_real(inicio)
        latitud_destino, longitud_destino = self.coordenada_real(destino)
        url = (
            f"{URL_OSRM}/{longitud_inicio},{latitud_inicio};"
            f"{longitud_destino},{latitud_destino}"
            "?overview=full&geometries=geojson&steps=false"
        )

        with urllib.request.urlopen(url, timeout=TIMEOUT_OSRM) as respuesta:  # noqa: S310
            datos = json.loads(respuesta.read())

        coordenadas = datos["routes"][0]["geometry"]["coordinates"]
        puntos = [
            punto_relativo_desde_coordenada(latitud, longitud)
            for longitud, latitud in coordenadas
        ]
        return self.limpiar_puntos(puntos)
