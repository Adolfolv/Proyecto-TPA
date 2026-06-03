class ControladorViajeBase:
    """Operaciones compartidas por los controladores del modulo de viaje."""

    def __init__(self, servicio_viaje):
        self.servicio_viaje = servicio_viaje

    def obtener_lugares_disponibles(self):
        return self.servicio_viaje.obtener_lugares_disponibles()


class ControladorViajePasajero(ControladorViajeBase):
    """Controlador del flujo donde el usuario solicita un viaje."""

    def __init__(self, servicio_viaje):
        super().__init__(servicio_viaje)
        self.error_busqueda_vehiculos = ""
        self.error_viaje = ""
        self.vehiculos_encontrados = []
        self.ruta_busqueda_pasajero = None
        self.rutas_viaje_pasajero = None
        self.resultado_viaje_pasajero = None

    def buscar_vehiculos_pasajero(self, cantidad_usuarios, ubicacion_inicial, ubicacion_final):
        self.error_busqueda_vehiculos = ""
        self.vehiculos_encontrados = []
        self.ruta_busqueda_pasajero = None

        resultado = self.servicio_viaje.buscar_vehiculos(
            cantidad_usuarios,
            ubicacion_inicial,
            ubicacion_final,
        )
        self.error_busqueda_vehiculos = resultado.error

        if not resultado.exitoso:
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
        self.error_viaje = ""
        self.rutas_viaje_pasajero = None
        self.resultado_viaje_pasajero = None

        resultado = self.servicio_viaje.confirmar_viaje_pasajero(
            usuario,
            vehiculo,
            ubicacion_inicial,
            ubicacion_final,
        )
        self.error_viaje = resultado.error

        if not resultado.exitoso:
            return False

        self.rutas_viaje_pasajero = resultado.rutas_viaje
        self.resultado_viaje_pasajero = resultado
        return True

    def iniciar_viaje_pasajero_confirmado(self):
        return self.resultado_viaje_pasajero.viaje

    def obtener_rutas_viaje_pasajero(self):
        return self.rutas_viaje_pasajero

    def obtener_error_viaje(self):
        return self.error_viaje


class ControladorViajeConductor(ControladorViajeBase):
    """Controlador del flujo donde el conductor acepta un viaje."""

    def __init__(self, servicio_viaje):
        super().__init__(servicio_viaje)
        self.error_viaje = ""
        self.rutas_viaje_conductor = None
        self.resultado_viaje_conductor = None

    def buscar_pasajero_conductor(self, ubicacion_inicial):
        return self.servicio_viaje.buscar_pasajeros(ubicacion_inicial)

    def formar_ruta_pasajero_conductor(self, pasajero):
        return self.servicio_viaje.formar_ruta_pasajero_conductor(pasajero)

    def iniciar_viaje_conductor(self, pasajero, conductor):
        self.error_viaje = ""
        self.rutas_viaje_conductor = None
        self.resultado_viaje_conductor = None

        resultado = self.servicio_viaje.iniciar_viaje_conductor(pasajero, conductor)
        self.error_viaje = resultado.error
        self.rutas_viaje_conductor = resultado.rutas_viaje
        self.resultado_viaje_conductor = resultado
        return resultado.viaje

    def obtener_rutas_viaje_conductor(self):
        return self.rutas_viaje_conductor

    def obtener_error_viaje(self):
        return self.error_viaje
