"""Casos de uso de suscripciones para conductor, separados por responsabilidad."""

from random import Random

from Modelos.Suscripcion.modelos_suscripcion import (
    ESTADO_ACTIVA,
    ESTADO_CANCELADA,
    VIAJE_ASIGNADO,
    VIAJE_CANCELADO,
    VIAJE_EN_CURSO,
    VIAJE_FINALIZADO,
    VIAJE_PROGRAMADO,
)
from Validaciones.suscripcion import (
    ESTADOS_VIAJE_PENDIENTE,
)


class ServicioOfertasSuscripcionConductor:
    """Busca y filtra suscripciones disponibles para un conductor."""

    MINIMO_OFERTAS_SELECCION = 3
    MAXIMO_OFERTAS_SELECCION = 5

    def __init__(self, repositorio, catalogo, fabrica):
        self.repositorio = repositorio
        self.catalogo = catalogo
        self.fabrica = fabrica
        self._randomizador = Random()

    def buscar_ofertas_conductor(self, conductor):
        existentes = {
            suscripcion.id_suscripcion
            for suscripcion in self.repositorio.listar_suscripciones()
        }
        disponibles = {
            identificador: datos
            for identificador, datos in self.catalogo.items()
            if identificador not in existentes
            and datos["cantidad_pasajeros"] <= int(conductor.auto.cantidad_asientos)
        }
        cantidad = min(
            len(disponibles),
            self._randomizador.randint(
                self.MINIMO_OFERTAS_SELECCION,
                self.MAXIMO_OFERTAS_SELECCION,
            ),
        )
        ids = self._randomizador.sample(tuple(disponibles), cantidad) if disponibles else []
        return [
            self.fabrica.crear_oferta_simulada(
                identificador, disponibles[identificador], conductor
            )[0]
            for identificador in ids
        ]

    def listar_disponibles_conductor(self, conductor):
        disponibles = []
        for suscripcion in self.repositorio.listar_suscripciones():
            viajes = self.repositorio.listar_viajes(
                id_suscripcion=suscripcion.id_suscripcion
            )
            if (
                suscripcion.estado == ESTADO_ACTIVA
                and not suscripcion.id_conductor
                and int(conductor.auto.cantidad_asientos) >= suscripcion.cantidad_pasajeros
                and any(v.estado in (VIAJE_PROGRAMADO, VIAJE_ASIGNADO) for v in viajes)
            ):
                disponibles.append(suscripcion)
        return sorted(disponibles, key=lambda item: (item.fecha_inicio, item.hora))


class ServicioAgendaSuscripcionConductor:
    """Consulta la agenda y los viajes asignados al conductor."""

    def __init__(self, repositorio):
        self.repositorio = repositorio

    def listar_actuales_conductor(self, conductor):
        return sorted(
            self.repositorio.listar_suscripciones_conductor(
                conductor.id_usuario, (ESTADO_ACTIVA,)
            ),
            key=lambda item: (item.fecha_inicio, item.hora),
        )

    def obtener_agenda_conductor(self, conductor):
        suscripciones = self.listar_actuales_conductor(conductor)
        ids = {suscripcion.id_suscripcion for suscripcion in suscripciones}
        viajes = sorted(
            (
                viaje
                for viaje in self.repositorio.listar_viajes_conductor(
                    conductor.id_usuario
                )
                if viaje.id_suscripcion in ids
            ),
            key=lambda viaje: viaje.fecha_hora,
        )
        return suscripciones, viajes

    def listar_viajes_suscripcion_conductor(self, conductor, id_suscripcion):
        return sorted(
            self.repositorio.listar_viajes(id_suscripcion=id_suscripcion),
            key=lambda item: item.fecha_hora,
        )


class ServicioAsignacionSuscripcionConductor:
    """Acepta o cancela asignaciones completas de suscripción."""

    def __init__(self, repositorio, catalogo, fabrica):
        self.repositorio = repositorio
        self.catalogo = catalogo
        self.fabrica = fabrica

    def agregar_suscripcion_conductor(self, conductor, id_suscripcion):
        suscripcion = self.repositorio.obtener_suscripcion(id_suscripcion)
        viajes_simulados = None
        if suscripcion is None and id_suscripcion in self.catalogo:
            suscripcion, viajes_simulados = self.fabrica.crear_oferta_simulada(
                id_suscripcion, self.catalogo[id_suscripcion], conductor
            )
        if suscripcion is not None and str(suscripcion.id_conductor) == str(
            conductor.id_usuario
        ):
            return suscripcion
        nuevos = viajes_simulados or [
            viaje
            for viaje in self.repositorio.listar_viajes(id_suscripcion=id_suscripcion)
            if viaje.estado in (VIAJE_PROGRAMADO, VIAJE_ASIGNADO)
        ]
        nombre = f"{conductor.nombre} {conductor.apellido}"
        vehiculo = (
            f"{conductor.auto.marca} {conductor.auto.modelo} "
            f"({conductor.auto.patente})"
        )
        suscripcion.id_conductor = str(conductor.id_usuario)
        suscripcion.conductor = nombre
        suscripcion.vehiculo = vehiculo
        for viaje in nuevos:
            viaje.id_conductor = str(conductor.id_usuario)
            viaje.conductor = nombre
            viaje.vehiculo = vehiculo
            viaje.estado = VIAJE_ASIGNADO
        if viajes_simulados is not None:
            self.repositorio.registrar_cambios(suscripcion, nuevos)
        self.repositorio.guardar_cambios()
        return suscripcion

    def cancelar_suscripcion_conductor(self, conductor, id_suscripcion):
        suscripcion = self.repositorio.obtener_suscripcion(id_suscripcion)
        viajes = self.repositorio.listar_viajes(id_suscripcion=id_suscripcion)
        suscripcion.estado = ESTADO_CANCELADA
        for viaje in viajes:
            if viaje.estado in (VIAJE_PROGRAMADO, VIAJE_ASIGNADO):
                viaje.estado = VIAJE_CANCELADO
                viaje.error = "Suscripcion cancelada por el conductor."
        self.repositorio.guardar_cambios()
        return suscripcion


class ServicioViajesSuscripcionConductor:
    """Ejecuta, cancela y liquida viajes del conductor."""

    COMISION_PLATAFORMA = 0.20

    def __init__(self, repositorio, pagos, horarios, reloj,
                 servicio_historial=None):
        self.repositorio = repositorio
        self.pagos = pagos
        self.horarios = horarios
        self.reloj = reloj
        self.servicio_historial = servicio_historial

    def confirmar_pasajero_abordo_conductor(self, conductor, id_viaje):
        pendientes = self.repositorio.listar_viajes_conductor(
            conductor.id_usuario, ESTADOS_VIAJE_PENDIENTE
        )
        viaje = self.horarios.proximo(pendientes)
        ahora = self.reloj()
        viaje.estado = VIAJE_EN_CURSO
        viaje.inicio_confirmado_en = ahora.isoformat(timespec="seconds")
        self.repositorio.guardar_cambios()
        return viaje

    def finalizar_viaje_conductor(self, conductor, id_viaje):
        viaje = self._obtener_viaje(id_viaje)
        suscripcion = self.repositorio.obtener_suscripcion(viaje.id_suscripcion)
        if viaje.pago_conductor_estado == "PAGADO":
            return viaje

        viaje.id_conductor = str(conductor.id_usuario)
        viaje.conductor = f"{conductor.nombre} {conductor.apellido}"
        viaje.vehiculo = (
            f"{conductor.auto.marca} {conductor.auto.modelo} "
            f"({conductor.auto.patente})"
        )
        viaje.pago_conductor = viaje.pago_conductor or round(
            viaje.precio * (1 - self.COMISION_PLATAFORMA)
        )
        viaje.pago_conductor_estado = "PROCESANDO"
        self.repositorio.guardar_cambios()
        try:
            self.pagos.abonar_conductor_suscripcion(conductor, viaje.pago_conductor)
        except (ValueError, OSError):
            viaje.pago_conductor_estado = "PENDIENTE"
            self.repositorio.guardar_cambios()
            raise
        if self.servicio_historial is not None:
            self.servicio_historial.registrar_viaje_suscripcion(
                suscripcion,
                viaje,
            )
        viaje.pago_conductor_estado = "PAGADO"
        viaje.estado = VIAJE_FINALIZADO
        suscripcion.monto_consumido = round(
            suscripcion.monto_consumido + viaje.precio, 2
        )
        self.repositorio.guardar_cambios()
        return viaje

    def cancelar_viaje_conductor(self, conductor, id_viaje):
        viaje = self._obtener_viaje(id_viaje)
        viaje.id_conductor = str(conductor.id_usuario)
        viaje.conductor = f"{conductor.nombre} {conductor.apellido}"
        viaje.vehiculo = (
            f"{conductor.auto.marca} {conductor.auto.modelo} "
            f"({conductor.auto.patente})"
        )
        viaje.estado = VIAJE_CANCELADO
        viaje.error = "Cancelado por el conductor. Sin liquidacion."
        self.repositorio.guardar_cambios()
        return viaje

    def _obtener_viaje(self, id_viaje):
        return self.repositorio.obtener_viaje(id_viaje)
