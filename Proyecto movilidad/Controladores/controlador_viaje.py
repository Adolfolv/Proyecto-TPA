from Modelos.Viaje.modelo_viajes import Viaje


class ControladorViaje:

    def __init__(self, servicio_viaje):
        self.servicio_viaje = servicio_viaje

    def buscar_pasajeros(
        self,
        ubicacion_inicial,
    ):
        return self.servicio_viaje.buscar_pasajeros(
            ubicacion_inicial,
        )

    def formar_trayectoria(self, ubicacion_inicial, ubicacion_final):
        return self.servicio_viaje.formar_trayectoria(
            ubicacion_inicial,
            ubicacion_final,
        )

    def iniciar_viaje(self, ubicacion_inicial, datos_pasajero, usuario):
        conductor = f"{usuario.nombre} {usuario.apellido}"
        viaje = Viaje(
            pasajero=datos_pasajero["nombre_completo"],
            conductor=conductor,
            vehiculo=datos_pasajero["vehiculo"],
            precio=float(datos_pasajero["precio"]),
            distancia=float(datos_pasajero["distancia"]),
            duracion=float(datos_pasajero["duracion"]),
        )
        return self.servicio_viaje.iniciar_viaje(viaje, usuario)
