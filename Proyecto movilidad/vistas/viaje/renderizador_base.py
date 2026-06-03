class RenderizadorViajeBase:
    """Operaciones comunes para pintar datos en las vistas de viaje."""

    def __init__(self, vista):
        # Se guarda la vista para reutilizar widgets ya creados sin volver a construirlos.
        self.vista = vista

    def dibujar_trayecto_en_mapa(self, ruta):
        # Dibuja una ruta ya calculada por el servicio/controlador.
        if self.vista.mapa_viaje is None:
            return
        self.vista.mapa_viaje.dibujar_trayectoria(ruta)

    def limpiar_trayectorias_mapa(self):
        # Limpia solo las lineas de ruta, no los marcadores del mapa.
        if self.vista.mapa_viaje is None:
            return
        self.vista.mapa_viaje.limpiar_trayectorias()
