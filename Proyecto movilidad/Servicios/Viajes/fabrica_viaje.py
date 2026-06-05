from Modelos.Viaje.modelo_viajes import (
    PasajeroEncontrado,
    VehiculoDisponible,
    Viaje,
)


class FabricaViaje:
    """Crea los modelos que viajan entre servicios, controladores y vistas."""

    def __init__(self, trayectoria, calculadora):
        self.trayectoria = trayectoria
        self.calculadora = calculadora

    def crear_viaje_pasajero(self, vehiculo, usuario):
        return Viaje(
            pasajero=self.nombre_usuario(usuario),
            conductor=vehiculo.nombre_completo,
            vehiculo=vehiculo.vehiculo,
            precio=float(vehiculo.precio),
            distancia=float(vehiculo.distancia),
            duracion=float(vehiculo.tiempo),
        )

    def crear_viaje_conductor(self, pasajero, conductor):
        return Viaje(
            pasajero=pasajero.nombre_completo,
            conductor=self.nombre_usuario(conductor),
            vehiculo=pasajero.vehiculo,
            precio=float(pasajero.precio),
            distancia=float(pasajero.distancia),
            duracion=float(pasajero.duracion),
        )

    def crear_vehiculo_disponible(self, conductor, punto_conductor, distancia):
        return VehiculoDisponible(
            nombre_completo=f"{conductor.nombre} {conductor.apellido}",
            vehiculo=f"{conductor.marca_vehiculo} {conductor.modelo_vehiculo}",
            patente=conductor.patente,
            imagen=conductor.imagen,
            precio=float(conductor.precio),
            distancia=distancia,
            tiempo=self.calculadora.calcular_tiempo_por_km(distancia),
            ubicacion_relativa=punto_conductor,
            ubicacion_real=self.trayectoria.coordenada_real(punto_conductor),
        )

    def crear_pasajero_encontrado(
        self,
        pasajero,
        ubicacion_conductor,
        duracion_busqueda,
        distancias,
        tiempos,
    ):
        return PasajeroEncontrado(
            nombre_completo=f"{pasajero.nombre} {pasajero.apellido}",
            vehiculo=f"{pasajero.marca_vehiculo} {pasajero.modelo_vehiculo}",
            trayecto=f"{pasajero.ubicacion_inicial} -> {pasajero.ubicacion_final}",
            ubicacion_inicial=pasajero.ubicacion_inicial,
            ubicacion_final=pasajero.ubicacion_final,
            ubicacion_conductor=ubicacion_conductor,
            imagen=pasajero.imagen,
            precio=float(pasajero.pago),
            distancia=distancias["km_para_llegar"] + distancias["km_transportando"],
            duracion=tiempos["tiempo_para_llegar"] + tiempos["tiempo_transportando"],
            km_para_llegar=distancias["km_para_llegar"],
            km_transportando=distancias["km_transportando"],
            tiempo_para_llegar=tiempos["tiempo_para_llegar"],
            tiempo_transportando=tiempos["tiempo_transportando"],
            duracion_busqueda=duracion_busqueda,
        )

    def nombre_usuario(self, usuario):
        return f"{usuario.nombre} {usuario.apellido}".strip()
