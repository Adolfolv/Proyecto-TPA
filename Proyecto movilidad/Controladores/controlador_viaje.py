from Modelos.Viaje.modelo_viajes import Viaje


class ControladorViaje:

    def __init__(self, servicio_viaje, servicio_billetera=None):
        self.servicio_viaje = servicio_viaje
        self.servicio_billetera = servicio_billetera

    def buscar_pasajeros(
        self,
        ubicacion_inicial,
    ):
        return self.servicio_viaje.buscar_pasajeros(
            ubicacion_inicial,
        )

    def buscar_vehiculos(self, cantidad_usuarios, ubicacion_inicial, ubicacion_final):
        return self.servicio_viaje.buscar_vehiculos(
            cantidad_usuarios,
            ubicacion_inicial,
            ubicacion_final,
        )

    def formar_trayectoria(self, ubicacion_inicial, ubicacion_final):
        return self.servicio_viaje.formar_trayectoria(
            ubicacion_inicial,
            ubicacion_final,
        )

    def formar_trayectoria_por_puntos(self, punto_inicial, punto_final):
        return self.servicio_viaje.formar_trayectoria_por_puntos(
            punto_inicial,
            punto_final,
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
        self.servicio_viaje.iniciar_viaje(viaje, usuario)
        self.pagar_conductor(usuario, viaje.precio)
        return viaje

    def pagar_conductor(self, usuario, monto):
        if self.servicio_billetera is None:
            return False

        if getattr(usuario, "tipo_usuario", "") != "conductor":
            return False

        self.servicio_billetera.recibir_pago(usuario, monto)
        return True
