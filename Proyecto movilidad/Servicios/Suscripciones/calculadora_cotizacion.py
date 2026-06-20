class CalculadoraCotizacionSuscripcion:
    """Calcula el precio fijo de una suscripcion sin conocer su persistencia."""

    TARIFA_BASE = 1800
    TARIFA_POR_KM = 700
    RECARGO_PASAJERO = 250
    PRECIO_MINIMO = 2500

    def __init__(self, servicio_viaje_comun):
        self.servicio_viaje_comun = servicio_viaje_comun

    def calcular_precio_por_viaje(self, origen, destino, cantidad_pasajeros):
        ruta = self.servicio_viaje_comun.formar_trayectoria(origen, destino)
        distancia = sum(
            self.servicio_viaje_comun.calcular_km_entre_coordenadas(inicio, fin)
            for inicio, fin in zip(ruta, ruta[1:])
        )
        valor = (
            self.TARIFA_BASE
            + distancia * self.TARIFA_POR_KM
            + (cantidad_pasajeros - 1) * self.RECARGO_PASAJERO
        )
        return float(max(self.PRECIO_MINIMO, round(valor / 100) * 100))
