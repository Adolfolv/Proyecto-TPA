"""Casos de uso de suscripciones para pasajero, separados por responsabilidad."""

from datetime import datetime, timedelta

from Modelos.Suscripcion.modelos_suscripcion import (
    ESTADO_ACTIVA,
    ESTADO_CANCELADA,
    ESTADO_PAUSADA,
    VIAJE_ASIGNADO,
    VIAJE_CANCELADO,
    VIAJE_EN_CURSO,
    VIAJE_FINALIZADO,
    VIAJE_PROGRAMADO,
    ResumenSuscripcion,
)
from Validaciones.suscripcion import (
    ESTADOS_VIAJE_ACTIVO,
    ESTADOS_VIAJE_PENDIENTE,
)


class ServicioAltaSuscripcionPasajero:
    """Previsualiza y crea suscripciones nuevas."""

    def __init__(self, repositorio, viajes, pagos, validador, horarios,
                 politica_pasajero, fabrica, crear_unidad_trabajo, reloj):
        self.repositorio = repositorio
        self.viajes = viajes
        self.pagos = pagos
        self.validador = validador
        self.horarios = horarios
        self.politica_pasajero = politica_pasajero
        self.fabrica = fabrica
        self.crear_unidad_trabajo = crear_unidad_trabajo
        self.reloj = reloj

    def previsualizar(self, usuario, origen, destino, fecha_inicio, fecha_fin,
                     dias_semana, hora, cantidad):
        ahora = self.reloj()
        inicio, fin, dias, horario, pasajeros = self.validador.validar(
            usuario, origen, destino, fecha_inicio, fecha_fin, dias_semana, hora,
            cantidad, ahora=ahora,
        )
        fechas = self.horarios.generar_fechas(inicio, fin, dias, horario, ahora)
        if not fechas:
            raise ValueError("El periodo elegido no contiene horarios futuros para esos dias.")
        existentes = tuple(
            viaje for viaje in self.repositorio.listar_viajes(id_pasajero=usuario.id_usuario)
            if viaje.estado in ESTADOS_VIAJE_ACTIVO
        )
        self.politica_pasajero.validar_alta(ahora, tuple(fechas), existentes)
        self.validador.validar_dias_con_horarios_futuros(fechas, dias)
        precio = self.fabrica.calculadora.calcular_precio_por_viaje(origen, destino, pasajeros)
        return ResumenSuscripcion(
            origen=origen,
            destino=destino,
            fecha_inicio=inicio.isoformat(),
            fecha_fin=fin.isoformat(),
            dias_semana=dias,
            hora=horario.strftime("%H:%M"),
            cantidad_pasajeros=pasajeros,
            fechas_viaje=tuple(fecha.isoformat(timespec="minutes") for fecha in fechas),
            precio_por_viaje=precio,
            precio_total=precio * len(fechas),
        )

    def confirmar(self, usuario, origen, destino, fecha_inicio, fecha_fin,
                  dias_semana, hora, cantidad, conductor=None):
        if conductor is None:
            raise ValueError("Selecciona un conductor antes de crear la suscripcion.")
        resumen = self.previsualizar(
            usuario, origen, destino, fecha_inicio, fecha_fin, dias_semana, hora, cantidad,
        )
        suscripcion, viajes = self.fabrica.crear_desde_resumen(usuario, resumen, conductor)
        self.pagos.cobrar_suscripcion(usuario, resumen.precio_total)
        try:
            with self.crear_unidad_trabajo() as unidad:
                unidad.repositorio.agregar_sin_guardar(suscripcion, viajes)
                unidad.confirmar()
        except OSError:
            self.pagos.reembolsar_suscripcion(usuario, resumen.precio_total)
            raise
        return suscripcion

    def buscar_conductores(self, cantidad_pasajeros, origen, destino):
        return self.viajes.buscar_vehiculos(cantidad_pasajeros, origen, destino)

    def obtener_lugares_disponibles(self):
        return self.viajes.comun.obtener_lugares_disponibles()


class ConsultaSuscripcionPasajero:
    """Realiza consultas de suscripciones y viajes del pasajero."""

    def __init__(self, repositorio):
        self.repositorio = repositorio

    def listar_suscripciones(self, usuario):
        return self.repositorio.listar_suscripciones(usuario.id_usuario)

    def listar_viajes(self, usuario, limite=None):
        viajes = sorted(
            self.repositorio.listar_viajes(id_pasajero=usuario.id_usuario),
            key=lambda item: item.fecha_hora,
        )
        return viajes[:limite] if limite else viajes


class ServicioViajesSuscripcionPasajero:
    """Gestiona el ciclo de vida de los viajes del pasajero."""

    def __init__(self, repositorio, horarios, crear_unidad_trabajo, reloj):
        self.repositorio = repositorio
        self.horarios = horarios
        self.crear_unidad_trabajo = crear_unidad_trabajo
        self.reloj = reloj

    def confirmar_inicio(self, usuario, id_viaje):
        viaje = next((item for item in self.repositorio.listar_viajes(
            id_pasajero=usuario.id_usuario
        ) if item.id_viaje_programado == id_viaje), None)
        if viaje is None:
            raise ValueError("No se encontro el viaje programado.")
        if viaje.estado not in (VIAJE_PROGRAMADO, VIAJE_ASIGNADO):
            raise ValueError("Este viaje ya no esta pendiente de confirmacion.")
        ahora, horario = self.reloj(), datetime.fromisoformat(viaje.fecha_hora)
        if ahora < horario - timedelta(minutes=5):
            raise ValueError("Podras confirmar el inicio desde 5 minutos antes.")
        if ahora > horario + self.horarios.MARGEN_ATRASO:
            raise ValueError("El plazo para confirmar este viaje ya vencio.")
        suscripcion = self.repositorio.obtener_suscripcion(viaje.id_suscripcion)
        if suscripcion is None or suscripcion.estado != ESTADO_ACTIVA:
            raise ValueError("La suscripcion debe estar activa para iniciar el viaje.")
        with self.crear_unidad_trabajo() as unidad:
            viaje.pasajero_confirmo_en = ahora.isoformat(timespec="seconds")
            viaje.inicio_confirmado_en = ahora.isoformat(timespec="seconds")
            viaje.estado = VIAJE_EN_CURSO
            unidad.confirmar()
        return viaje

    def completar_viaje_pasajero(self, usuario, id_viaje):
        viaje = next((item for item in self.repositorio.listar_viajes(
            id_pasajero=usuario.id_usuario
        ) if item.id_viaje_programado == id_viaje), None)
        if viaje is None or viaje.estado != VIAJE_EN_CURSO:
            raise ValueError("Solo se puede completar un viaje en curso.")
        with self.crear_unidad_trabajo() as unidad:
            viaje.estado = VIAJE_FINALIZADO
            suscripcion = self.repositorio.obtener_suscripcion(viaje.id_suscripcion)
            if suscripcion is not None:
                suscripcion.monto_consumido = round(
                    suscripcion.monto_consumido + viaje.precio, 2
                )
            unidad.confirmar()
        return viaje

    def cancelar_viaje(self, usuario, id_viaje):
        cancelables = [
            item for item in self.repositorio.listar_viajes(id_pasajero=usuario.id_usuario)
            if item.estado in ESTADOS_VIAJE_PENDIENTE
        ]
        viaje = next(
            (item for item in cancelables if item.id_viaje_programado == id_viaje), None
        )
        if viaje is None:
            raise ValueError("No se encontro el viaje programado.")
        if self.horarios.proximo(cancelables) is not viaje:
            raise ValueError("Solo se puede cancelar el proximo viaje programado.")
        with self.crear_unidad_trabajo() as unidad:
            viaje.estado = VIAJE_CANCELADO
            viaje.error = "Cancelado por el pasajero. El saldo se liquida al cancelar la suscripcion."
            unidad.confirmar()
        return viaje


class ServicioEstadoSuscripcionPasajero:
    """Cambia el estado de una suscripción y coordina su reembolso."""

    CARGO_CANCELACION = 0.05

    def __init__(self, repositorio, pagos, politica_pasajero,
                 crear_unidad_trabajo, reloj):
        self.repositorio = repositorio
        self.pagos = pagos
        self.politica_pasajero = politica_pasajero
        self.crear_unidad_trabajo = crear_unidad_trabajo
        self.reloj = reloj

    def cambiar_estado(self, usuario, id_suscripcion, nuevo_estado):
        suscripcion = self._obtener_propia(usuario, id_suscripcion)
        if nuevo_estado == ESTADO_CANCELADA:
            self.politica_pasajero.validar_sin_viaje_inminente(
                self.repositorio.listar_viajes(id_pasajero=usuario.id_usuario),
                self.reloj(),
            )
        transiciones = {
            ESTADO_ACTIVA: {ESTADO_PAUSADA, ESTADO_CANCELADA},
            ESTADO_PAUSADA: {ESTADO_ACTIVA, ESTADO_CANCELADA},
        }
        if nuevo_estado not in transiciones.get(suscripcion.estado, set()):
            raise ValueError("Ese cambio de estado no esta permitido.")
        if nuevo_estado != ESTADO_CANCELADA:
            with self.crear_unidad_trabajo() as unidad:
                suscripcion.estado = nuevo_estado
                unidad.confirmar()
            return suscripcion
        return self._cancelar_suscripcion(usuario, suscripcion)

    def _cancelar_suscripcion(self, usuario, suscripcion):
        viajes = self.repositorio.listar_viajes(id_suscripcion=suscripcion.id_suscripcion)
        if any(viaje.estado == VIAJE_EN_CURSO for viaje in viajes):
            raise ValueError("No se puede cancelar mientras existe un viaje en curso.")
        estado_anterior = suscripcion.estado
        estados_viajes = {
            viaje.id_viaje_programado: (viaje.estado, viaje.error, viaje.reembolsado)
            for viaje in viajes
        }
        consumido = sum(v.precio for v in viajes if v.estado == VIAJE_FINALIZADO)
        monto_consumido = max(suscripcion.monto_consumido, consumido)
        saldo = max(0, suscripcion.precio_total - monto_consumido)
        cargo = round(saldo * self.CARGO_CANCELACION, 2)
        reembolso = round(max(0, saldo - cargo), 2)

        if reembolso and not suscripcion.monto_reembolsado:
            with self.crear_unidad_trabajo() as unidad:
                self._marcar_cancelada(suscripcion, viajes, monto_consumido)
                suscripcion.cargo_cancelacion = cargo
                suscripcion.reembolso_pendiente = reembolso
                suscripcion.reembolso_estado = "PROCESANDO"
                unidad.confirmar()
            try:
                self.pagos.reembolsar_suscripcion(usuario, reembolso)
            except (ValueError, OSError):
                with self.crear_unidad_trabajo() as unidad:
                    suscripcion.estado = estado_anterior
                    suscripcion.reembolso_estado = "PENDIENTE"
                    suscripcion.reembolso_pendiente = 0.0
                    for viaje in viajes:
                        viaje.estado, viaje.error, viaje.reembolsado = estados_viajes[
                            viaje.id_viaje_programado
                        ]
                    unidad.confirmar()
                raise
            with self.crear_unidad_trabajo() as unidad:
                suscripcion.monto_reembolsado = reembolso
                suscripcion.reembolso_pendiente = 0.0
                suscripcion.reembolso_estado = "PAGADO"
                unidad.confirmar()
        else:
            with self.crear_unidad_trabajo() as unidad:
                self._marcar_cancelada(suscripcion, viajes, monto_consumido)
                if not reembolso:
                    suscripcion.reembolso_estado = "SIN_SALDO"
                unidad.confirmar()
        return suscripcion

    @staticmethod
    def _marcar_cancelada(suscripcion, viajes, monto_consumido):
        suscripcion.estado = ESTADO_CANCELADA
        suscripcion.monto_consumido = monto_consumido
        for viaje in viajes:
            if viaje.estado in (VIAJE_PROGRAMADO, VIAJE_ASIGNADO):
                viaje.estado = VIAJE_CANCELADO
                viaje.error = "Suscripcion cancelada por el pasajero."
                viaje.reembolsado = True

    def _obtener_propia(self, usuario, id_suscripcion):
        suscripcion = self.repositorio.obtener_suscripcion(id_suscripcion)
        if suscripcion is None or str(suscripcion.id_pasajero) != str(usuario.id_usuario):
            raise ValueError("No se encontro la suscripcion.")
        return suscripcion
