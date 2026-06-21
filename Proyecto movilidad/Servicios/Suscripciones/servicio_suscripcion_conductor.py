"""Casos de uso de suscripciones disponibles para el conductor."""

from datetime import datetime

from Modelos.Suscripcion.modelos_suscripcion import ESTADO_ACTIVA, ESTADO_CANCELADA, VIAJE_ASIGNADO, VIAJE_CANCELADO, VIAJE_EN_CURSO, VIAJE_FINALIZADO, VIAJE_PROGRAMADO
from Servicios.Suscripciones.puertos import FabricaUnidadTrabajo, PasarelaPagosSuscripcion, RepositorioSuscripciones, SelectorOfertas
from Validaciones.suscripcion import ESTADOS_VIAJE_ACTIVO, ESTADOS_VIAJE_PENDIENTE


class ServicioSuscripcionConductor:
    """SRP por actor: ofertas, agenda y ejecución del conductor."""

    COMISION_PLATAFORMA = 0.20

    def __init__(self, repositorio: RepositorioSuscripciones, catalogo, selector: SelectorOfertas, fabrica, pagos: PasarelaPagosSuscripcion, politica_horarios, politica_conductor, crear_unidad_trabajo: FabricaUnidadTrabajo, reloj):
        self.repositorio = repositorio
        self.catalogo = catalogo
        self.selector = selector
        self.fabrica = fabrica
        self.pagos = pagos
        self.politica_horarios = politica_horarios
        self.politica_conductor = politica_conductor
        self.crear_unidad_trabajo = crear_unidad_trabajo
        self.reloj = reloj

    # --- Ofertas y agenda -------------------------------------------------
    def buscar_ofertas_conductor(self, conductor):
        self.politica_conductor.validar_conductor(conductor)
        existentes = {suscripcion.id_suscripcion for suscripcion in self.repositorio.listar_suscripciones()}
        disponibles = {identificador: datos for identificador, datos in self.catalogo.items() if identificador not in existentes and datos["cantidad_pasajeros"] <= int(conductor.auto.cantidad_asientos)}
        return [self.fabrica.crear_oferta_simulada(identificador, disponibles[identificador], conductor)[0] for identificador in self.selector.seleccionar_ids(disponibles)]

    def listar_disponibles_conductor(self, conductor):
        self.politica_conductor.validar_conductor(conductor)
        disponibles = []
        for suscripcion in self.repositorio.listar_suscripciones():
            viajes = self.repositorio.listar_viajes(id_suscripcion=suscripcion.id_suscripcion)
            if suscripcion.estado == ESTADO_ACTIVA and not suscripcion.id_conductor and int(conductor.auto.cantidad_asientos) >= suscripcion.cantidad_pasajeros and any(viaje.estado in (VIAJE_PROGRAMADO, VIAJE_ASIGNADO) for viaje in viajes):
                disponibles.append(suscripcion)
        return sorted(disponibles, key=lambda item: (item.fecha_inicio, item.hora))

    def listar_actuales_conductor(self, conductor):
        self.politica_conductor.validar_conductor(conductor)
        return sorted(self.repositorio.listar_suscripciones_conductor(conductor.id_usuario, (ESTADO_ACTIVA,)), key=lambda item: (item.fecha_inicio, item.hora))

    def obtener_agenda_conductor(self, conductor):
        suscripciones = self.listar_actuales_conductor(conductor)
        ids = {suscripcion.id_suscripcion for suscripcion in suscripciones}
        viajes = sorted((viaje for viaje in self.repositorio.listar_viajes_conductor(conductor.id_usuario) if viaje.id_suscripcion in ids), key=lambda viaje: viaje.fecha_hora)
        return suscripciones, viajes

    def agregar_suscripcion_conductor(self, conductor, id_suscripcion):
        suscripcion = self.repositorio.obtener_suscripcion(id_suscripcion)
        viajes_simulados = None
        if suscripcion is None and id_suscripcion in self.catalogo:
            suscripcion, viajes_simulados = self.fabrica.crear_oferta_simulada(id_suscripcion, self.catalogo[id_suscripcion], conductor)
        if suscripcion is not None and str(suscripcion.id_conductor) == str(conductor.id_usuario):
            return suscripcion
        nuevos = viajes_simulados or [viaje for viaje in self.repositorio.listar_viajes(id_suscripcion=id_suscripcion) if viaje.estado in (VIAJE_PROGRAMADO, VIAJE_ASIGNADO)]
        existentes = tuple(self.repositorio.listar_viajes_conductor(conductor.id_usuario, ESTADOS_VIAJE_ACTIVO))
        fechas = tuple(datetime.fromisoformat(viaje.fecha_hora) for viaje in nuevos)
        self.politica_conductor.validar_aceptacion(conductor, suscripcion, fechas, existentes)
        nombre = f"{conductor.nombre} {conductor.apellido}"
        vehiculo = f"{conductor.auto.marca} {conductor.auto.modelo} ({conductor.auto.patente})"
        with self.crear_unidad_trabajo() as unidad:
            suscripcion.id_conductor, suscripcion.conductor, suscripcion.vehiculo = str(conductor.id_usuario), nombre, vehiculo
            for viaje in nuevos:
                viaje.id_conductor, viaje.conductor, viaje.vehiculo, viaje.estado = str(conductor.id_usuario), nombre, vehiculo, VIAJE_ASIGNADO
            if viajes_simulados is not None:
                unidad.repositorio.agregar_sin_guardar(suscripcion, nuevos)
            unidad.confirmar()
        return suscripcion

    def listar_viajes_suscripcion_conductor(self, conductor, id_suscripcion):
        suscripcion = self.repositorio.obtener_suscripcion(id_suscripcion)
        self.politica_conductor.validar_pertenencia(conductor, suscripcion)
        self.politica_conductor.validar_capacidad(conductor, suscripcion.cantidad_pasajeros)
        return sorted(self.repositorio.listar_viajes(id_suscripcion=id_suscripcion), key=lambda item: item.fecha_hora)

    def cancelar_suscripcion_conductor(self, conductor, id_suscripcion):
        suscripcion = self.repositorio.obtener_suscripcion(id_suscripcion)
        self.politica_conductor.validar_pertenencia(conductor, suscripcion)
        if suscripcion.estado != ESTADO_ACTIVA:
            raise ValueError("La suscripcion ya no se puede cancelar.")
        viajes = self.repositorio.listar_viajes(id_suscripcion=id_suscripcion)
        if any(viaje.estado == VIAJE_EN_CURSO for viaje in viajes):
            raise ValueError("No puedes cancelar una suscripcion con un viaje en curso.")
        with self.crear_unidad_trabajo() as unidad:
            suscripcion.estado = ESTADO_CANCELADA
            for viaje in viajes:
                if viaje.estado in (VIAJE_PROGRAMADO, VIAJE_ASIGNADO):
                    viaje.estado, viaje.error = VIAJE_CANCELADO, "Suscripcion cancelada por el conductor."
            unidad.confirmar()
        return suscripcion

    # --- Ejecución de viajes ---------------------------------------------
    def confirmar_pasajero_abordo_conductor(self, conductor, id_viaje):
        self.politica_conductor.validar_conductor(conductor)
        pendientes = self.repositorio.listar_viajes_conductor(conductor.id_usuario, ESTADOS_VIAJE_PENDIENTE)
        viaje = self.politica_horarios.proximo(pendientes)
        if viaje is None or viaje.id_viaje_programado != id_viaje:
            raise ValueError("Solo puedes iniciar el proximo viaje de tu agenda.")
        ahora = self.reloj()
        if ahora < datetime.fromisoformat(viaje.fecha_hora):
            raise ValueError("Aun no llega la hora de abordar al pasajero.")
        with self.crear_unidad_trabajo() as unidad:
            viaje.estado, viaje.inicio_confirmado_en = VIAJE_EN_CURSO, ahora.isoformat(timespec="seconds")
            unidad.confirmar()
        return viaje

    def finalizar_viaje_conductor(self, conductor, id_viaje):
        self.politica_conductor.validar_conductor(conductor)
        viaje = self._obtener_viaje(id_viaje)
        if viaje.estado not in (VIAJE_PROGRAMADO, VIAJE_ASIGNADO, VIAJE_EN_CURSO):
            raise ValueError("Este viaje ya no se puede finalizar.")
        suscripcion = self.repositorio.obtener_suscripcion(viaje.id_suscripcion)
        if suscripcion is None or suscripcion.estado != ESTADO_ACTIVA:
            raise ValueError("La suscripcion ya no esta activa.")
        self.politica_conductor.validar_capacidad(conductor, viaje.cantidad_pasajeros)
        if viaje.id_conductor and str(viaje.id_conductor) != str(conductor.id_usuario):
            raise ValueError("El viaje fue gestionado por otro conductor.")
        if viaje.pago_conductor_estado == "PAGADO":
            return viaje
        if viaje.pago_conductor_estado == "PROCESANDO":
            raise ValueError("La liquidacion esta en revision; no se volvera a pagar automaticamente.")

        # Saga: persistir PROCESANDO antes del abono evita pagos duplicados.
        viaje.id_conductor = str(conductor.id_usuario)
        viaje.conductor = f"{conductor.nombre} {conductor.apellido}"
        viaje.vehiculo = f"{conductor.auto.marca} {conductor.auto.modelo} ({conductor.auto.patente})"
        viaje.pago_conductor = viaje.pago_conductor or round(viaje.precio * (1 - self.COMISION_PLATAFORMA))
        viaje.pago_conductor_estado = "PROCESANDO"
        self.repositorio.guardar_cambios()
        try:
            self.pagos.abonar_conductor_suscripcion(conductor, viaje.pago_conductor)
        except (ValueError, OSError):
            viaje.pago_conductor_estado = "PENDIENTE"
            self.repositorio.guardar_cambios()
            raise
        viaje.pago_conductor_estado, viaje.estado = "PAGADO", VIAJE_FINALIZADO
        suscripcion.monto_consumido = round(suscripcion.monto_consumido + viaje.precio, 2)
        self.repositorio.guardar_cambios()
        return viaje

    def cancelar_viaje_conductor(self, conductor, id_viaje):
        self.politica_conductor.validar_conductor(conductor)
        viaje = self._obtener_viaje(id_viaje)
        proximo = self.politica_horarios.proximo(self.repositorio.listar_viajes_conductor(conductor.id_usuario, ESTADOS_VIAJE_PENDIENTE))
        if proximo is None or proximo.id_viaje_programado != id_viaje:
            raise ValueError("Solo puedes cancelar el proximo viaje de tu agenda.")
        if viaje.pago_conductor_estado in ("PROCESANDO", "PAGADO"):
            raise ValueError("No se puede cancelar un viaje cuya liquidacion ya comenzo.")
        if viaje.id_conductor and str(viaje.id_conductor) != str(conductor.id_usuario):
            raise ValueError("El viaje fue gestionado por otro conductor.")
        with self.crear_unidad_trabajo() as unidad:
            viaje.id_conductor = str(conductor.id_usuario)
            viaje.conductor = f"{conductor.nombre} {conductor.apellido}"
            viaje.vehiculo = f"{conductor.auto.marca} {conductor.auto.modelo} ({conductor.auto.patente})"
            viaje.estado, viaje.error = VIAJE_CANCELADO, "Cancelado por el conductor. Sin liquidacion."
            unidad.confirmar()
        return viaje

    def _obtener_viaje(self, id_viaje):
        viaje = self.repositorio.obtener_viaje(id_viaje)
        if viaje is None:
            raise ValueError("No se encontro el viaje programado.")
        return viaje
