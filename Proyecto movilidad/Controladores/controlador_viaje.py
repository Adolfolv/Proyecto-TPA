class ControladorViaje:

    def __init__(self, servicio_viaje):
        self.servicio_viaje = servicio_viaje

    def buscar_pasajeros(
        self,
        ubicacion_inicial,
        boton_buscar_pasajeros,
        selector_ubicacion,
        label_cronometro,
        frame_pasajero,
        ruta_imagenes_usuarios,
        moldes,
        tema,
        al_finalizar,
    ):
        return self.servicio_viaje.buscar_pasajeros(
            ubicacion_inicial,
            boton_buscar_pasajeros,
            selector_ubicacion,
            label_cronometro,
            frame_pasajero,
            ruta_imagenes_usuarios,
            moldes,
            tema,
            al_finalizar,
        )

    def formar_trayectoria(self, mapa, ubicacion_inicial, ubicacion_final):
        return self.servicio_viaje.formar_trayectoria(
            mapa,
            ubicacion_inicial,
            ubicacion_final,
        )

    def iniciar_viaje(self, ubicacion_inicial, datos_pasajero):
        if hasattr(self.servicio_viaje, "iniciar_viaje"):
            return self.servicio_viaje.iniciar_viaje(
                ubicacion_inicial,
                datos_pasajero,
            )
        return None
