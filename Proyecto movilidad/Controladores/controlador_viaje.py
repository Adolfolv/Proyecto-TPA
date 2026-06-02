from Modelos.Viaje.modelo_viajes import Viaje


class ControladorViaje:
    """Controlador MVC del apartado de viajes.

    La vista le pide casos de uso concretos; el controlador coordina servicios,
    pagos y estado preparado, pero no pinta widgets ni anima mapas.
    """

    def __init__(self, servicio_viaje, servicio_billetera=None):
        self.servicio_viaje = servicio_viaje
        self.servicio_billetera = servicio_billetera
        self.error_busqueda_vehiculos = ""
        self.error_viaje = ""
        self.vehiculos_encontrados = []
        self.ruta_busqueda_pasajero = None
        self.rutas_viaje_pasajero = None
        self.rutas_viaje_conductor = None

    def obtener_lugares_disponibles(self):
        return self.servicio_viaje.obtener_lugares_disponibles()

    def buscar_pasajeros(self, ubicacion_inicial):
        return self.servicio_viaje.buscar_pasajeros(ubicacion_inicial)

    def buscar_pasajero_conductor(self, ubicacion_inicial):
        return self.buscar_pasajeros(ubicacion_inicial)

    def buscar_vehiculos_pasajero(self, cantidad_usuarios, ubicacion_inicial, ubicacion_final):
        """Ejecuta la busqueda completa que necesita la pantalla de pasajero."""

        self.error_busqueda_vehiculos = ""
        self.vehiculos_encontrados = []
        self.ruta_busqueda_pasajero = None

        resultado = self.servicio_viaje.buscar_vehiculos(
            cantidad_usuarios,
            ubicacion_inicial,
            ubicacion_final,
        )

        if not resultado.exitoso:
            self.error_busqueda_vehiculos = resultado.error
            return False

        self.vehiculos_encontrados = list(resultado.vehiculos)
        self.ruta_busqueda_pasajero = resultado.ruta_busqueda
        return True

    def obtener_error_busqueda_vehiculos(self):
        return self.error_busqueda_vehiculos

    def obtener_vehiculos_encontrados(self):
        return self.vehiculos_encontrados

    def obtener_ruta_busqueda_pasajero(self):
        return self.ruta_busqueda_pasajero

    def confirmar_pago_pasajero(self, usuario, vehiculo, ubicacion_inicial, ubicacion_final):
        """Prepara rutas y cobra antes de permitir iniciar la animacion."""

        self.error_viaje = ""
        self.rutas_viaje_pasajero = None

        try:
            self.rutas_viaje_pasajero = self.servicio_viaje.formar_rutas_viaje_pasajero(
                vehiculo,
                ubicacion_inicial,
                ubicacion_final,
            )
            pago_realizado = self.pagar_pasajero(usuario, vehiculo.precio)
        except ValueError as error:
            self.rutas_viaje_pasajero = None
            self.error_viaje = str(error)
            return False
        except AttributeError:
            self.rutas_viaje_pasajero = None
            self.error_viaje = "No se pudo obtener la billetera del usuario."
            return False

        if not pago_realizado:
            self.rutas_viaje_pasajero = None
            self.error_viaje = "No se pudo realizar el pago del viaje."
            return False

        return True

    def iniciar_viaje_pasajero_confirmado(self, vehiculo, usuario):
        if self.rutas_viaje_pasajero is None:
            raise ValueError("No hay rutas preparadas para iniciar el viaje.")

        return self.iniciar_viaje_pasajero(vehiculo, usuario)

    def obtener_rutas_viaje_pasajero(self):
        return self.rutas_viaje_pasajero

    def obtener_rutas_viaje_conductor(self):
        return self.rutas_viaje_conductor

    def obtener_error_viaje(self):
        return self.error_viaje

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

    def formar_ruta_pasajero_conductor(self, pasajero):
        return self.formar_trayectoria(
            pasajero.ubicacion_inicial,
            pasajero.ubicacion_final,
        )

    def iniciar_viaje_conductor(self, pasajero, conductor):
        """Registra el viaje del conductor y deja rutas listas para la vista."""

        self.error_viaje = ""
        self.rutas_viaje_conductor = None

        try:
            self.rutas_viaje_conductor = self.servicio_viaje.formar_rutas_viaje_conductor(
                pasajero,
            )
            viaje = Viaje(
                pasajero=pasajero.nombre_completo,
                conductor=self.nombre_usuario(conductor),
                vehiculo=pasajero.vehiculo,
                precio=float(pasajero.precio),
                distancia=float(pasajero.distancia),
                duracion=float(pasajero.duracion),
            )
            if not self.pagar_conductor(conductor, viaje.precio):
                raise ValueError("No se pudo abonar el pago al conductor.")
            self.servicio_viaje.iniciar_viaje(viaje, conductor)
            return viaje
        except ValueError as error:
            self.error_viaje = str(error)
            self.rutas_viaje_conductor = None
            raise
        except AttributeError as error:
            self.error_viaje = "No se pudo obtener la billetera del conductor."
            self.rutas_viaje_conductor = None
            raise ValueError(self.error_viaje) from error

    def iniciar_viaje_pasajero(self, vehiculo, usuario):
        viaje = Viaje(
            pasajero=self.nombre_usuario(usuario),
            conductor=vehiculo.nombre_completo,
            vehiculo=vehiculo.vehiculo,
            precio=float(vehiculo.precio),
            distancia=float(vehiculo.distancia),
            duracion=float(vehiculo.tiempo),
        )
        self.servicio_viaje.iniciar_viaje(viaje, usuario)
        return viaje

    def nombre_usuario(self, usuario):
        if usuario is None:
            return ""
        return f"{getattr(usuario, 'nombre', '')} {getattr(usuario, 'apellido', '')}".strip()

    def pagar_conductor(self, usuario, monto):
        if self.servicio_billetera is None:
            return False

        if getattr(usuario, "tipo_usuario", "") != "conductor":
            return False

        self.servicio_billetera.recibir_pago(usuario, monto)
        return True

    def pagar_pasajero(self, usuario, monto):
        if self.servicio_billetera is None:
            return False

        if getattr(usuario, "tipo_usuario", "") != "pasajero":
            return False

        self.servicio_billetera.pagar(usuario, monto)
        return True
