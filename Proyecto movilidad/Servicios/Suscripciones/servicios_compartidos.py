"""Servicios compartidos que no corresponden a validacion."""

from datetime import date, datetime

from Modelos.Suscripcion.modelos_suscripcion import (
    ESTADO_ACTIVA,
    ESTADO_CANCELADA,
    ESTADO_FINALIZADA,
    VIAJE_CANCELADO,
    VIAJE_FALLIDO,
)
from Validaciones.suscripcion import (
    ESTADOS_VIAJE_PENDIENTE,
    PoliticaHorariosSuscripcion,
)


class ProcesadorSuscripcionesPendientes:
    """Actualiza viajes caducados y suscripciones vencidas."""

    def __init__(self, repositorio, reloj):
        self.repositorio = repositorio
        self.reloj = reloj

    def procesar(self, ahora=None):
        ahora = ahora or self.reloj()
        cambios = False

        for viaje in self.repositorio.listar_viajes():
            horario = datetime.fromisoformat(viaje.fecha_hora)
            if viaje.estado not in ESTADOS_VIAJE_PENDIENTE or horario > ahora:
                continue

            suscripcion = self.repositorio.obtener_suscripcion(viaje.id_suscripcion)
            if suscripcion is None or suscripcion.estado == ESTADO_CANCELADA:
                viaje.estado = VIAJE_CANCELADO
                viaje.error = "La suscripcion ya no esta disponible."
                cambios = True
            elif ahora - horario > PoliticaHorariosSuscripcion.MARGEN_ATRASO:
                viaje.estado = VIAJE_FALLIDO
                viaje.error = "El horario vencio mientras la aplicacion estaba cerrada."
                cambios = True

        cambios = self._finalizar_suscripciones_vencidas(ahora.date()) or cambios
        if cambios:
            self.repositorio.guardar_cambios()

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
