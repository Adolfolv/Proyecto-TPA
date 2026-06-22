"""Servicios compartidos que no corresponden a validación."""

from datetime import date, datetime

from Modelos.Suscripcion.modelos_suscripcion import (
    ESTADO_ACTIVA,
    ESTADO_CANCELADA,
    ESTADO_FINALIZADA,
    VIAJE_CANCELADO,
    VIAJE_FALLIDO,
    VIAJE_FINALIZADO,
)
from Validaciones.suscripcion import ESTADOS_VIAJE_PENDIENTE, PoliticaHorariosSuscripcion


class LimpiadorSuscripcionesFinalizadas:
    """Descarta suscripciones cerradas cuando ya no quedan pagos pendientes."""

    def limpiar(self, suscripciones, viajes_programados):
        protegidas = {
            suscripcion.id_suscripcion
            for suscripcion in suscripciones
            if suscripcion.reembolso_estado == "PROCESANDO"
        }

        viajes_por_suscripcion = {}
        for viaje in viajes_programados:
            viajes_por_suscripcion.setdefault(viaje.id_suscripcion, []).append(viaje)

        eliminables = {
            suscripcion.id_suscripcion
            for suscripcion in suscripciones
            if suscripcion.estado in (ESTADO_CANCELADA, ESTADO_FINALIZADA)
            and suscripcion.id_suscripcion not in protegidas
            and all(
                self._viaje_financieramente_cerrado(viaje)
                for viaje in viajes_por_suscripcion.get(
                    suscripcion.id_suscripcion,
                    (),
                )
            )
        }

        suscripciones_vigentes = [
            suscripcion
            for suscripcion in suscripciones
            if suscripcion.id_suscripcion not in eliminables
        ]
        viajes_vigentes = [
            viaje
            for viaje in viajes_programados
            if viaje.id_suscripcion not in eliminables
            and not (
                viaje.id_suscripcion not in protegidas
                and self._viaje_financieramente_cerrado(viaje)
            )
        ]
        return suscripciones_vigentes, viajes_vigentes

    @staticmethod
    def _viaje_financieramente_cerrado(viaje):
        if viaje.estado in (VIAJE_CANCELADO, VIAJE_FALLIDO):
            return True
        return (
            viaje.estado == VIAJE_FINALIZADO
            and viaje.pago_conductor_estado == "PAGADO"
        )


class ProcesadorSuscripcionesPendientes:
    """Actualiza viajes caducados y suscripciones vencidas."""

    def __init__(self, repositorio, crear_unidad_trabajo, reloj):
        self.repositorio = repositorio
        self.crear_unidad_trabajo = crear_unidad_trabajo
        self.reloj = reloj

    def procesar(self, ahora=None):
        ahora = ahora or self.reloj()
        cambios = False
        with self.crear_unidad_trabajo() as unidad:
            for viaje in self.repositorio.listar_viajes():
                horario = datetime.fromisoformat(viaje.fecha_hora)
                if viaje.estado not in ESTADOS_VIAJE_PENDIENTE or horario > ahora:
                    continue
                suscripcion = self.repositorio.obtener_suscripcion(viaje.id_suscripcion)
                if suscripcion is None or suscripcion.estado == ESTADO_CANCELADA:
                    viaje.estado = VIAJE_CANCELADO
                    viaje.error = "La suscripcion ya no esta disponible."
                    cambios = True
                elif (
                    suscripcion.estado != "PAUSADA"
                    and ahora - horario > PoliticaHorariosSuscripcion.MARGEN_ATRASO
                ):
                    viaje.estado = VIAJE_FALLIDO
                    viaje.error = "El horario vencio mientras la aplicacion estaba cerrada."
                    cambios = True
            cambios = self._finalizar_suscripciones_vencidas(ahora.date()) or cambios
            if cambios:
                unidad.confirmar()

    def _finalizar_suscripciones_vencidas(self, fecha_actual):
        cambios = False
        for suscripcion in self.repositorio.listar_suscripciones():
            if (
                suscripcion.estado == ESTADO_ACTIVA
                and date.fromisoformat(suscripcion.fecha_fin) < fecha_actual
            ):
                suscripcion.estado = ESTADO_FINALIZADA
                cambios = True
        return cambios


class ServicioPagosSuscripcion:
    """Delega operaciones monetarias a la pasarela de pagos."""

    def __init__(self, pasarela):
        self.pasarela = pasarela

    def cobrar_suscripcion(self, usuario, monto):
        return self.pasarela.cobrar_suscripcion(usuario, monto)

    def reembolsar_suscripcion(self, usuario, monto):
        return self.pasarela.reembolsar_suscripcion(usuario, monto)

    def abonar_conductor(self, conductor, monto):
        return self.pasarela.abonar_conductor_suscripcion(conductor, monto)
