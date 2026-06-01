from Modelos.Viaje.modelo_viajes import Viaje


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

    def iniciar_viaje(self, ubicacion_inicial, datos_pasajero, usuario, contexto_animacion):
        conductor = f"{usuario.nombre} {usuario.apellido}"
        viaje = Viaje(
            pasajero=datos_pasajero["nombre_completo"],
            conductor=conductor,
            vehiculo=datos_pasajero["vehiculo"],
            precio=float(datos_pasajero["precio"]),
            distancia=float(datos_pasajero["distancia"]),
            duracion=float(datos_pasajero["duracion"]),
        )
        return self.servicio_viaje.iniciar_viaje(viaje, usuario, contexto_animacion)
