"""Procesamiento temporal independiente de Tkinter."""

from datetime import date, datetime, timedelta

from Modelos.Suscripcion.modelos_suscripcion import ESTADO_ACTIVA, ESTADO_CANCELADA, ESTADO_FINALIZADA, ESTADO_PAUSADA, VIAJE_ASIGNADO, VIAJE_CANCELADO, VIAJE_FALLIDO, VIAJE_PROGRAMADO
from Servicios.Suscripciones.puertos import FabricaUnidadTrabajo, RepositorioSuscripciones


class ProcesadorSuscripciones:
    MARGEN_ATRASO = timedelta(minutes=15)

    def __init__(self, repositorio: RepositorioSuscripciones, crear_unidad_trabajo: FabricaUnidadTrabajo, reloj):
        self.repositorio = repositorio
        self.crear_unidad_trabajo = crear_unidad_trabajo
        self.reloj = reloj

    def procesar(self, ahora=None):
        ahora = ahora or self.reloj()
        cambios = False
        with self.crear_unidad_trabajo() as unidad:
            for viaje in self.repositorio.listar_viajes():
                if viaje.estado not in (VIAJE_PROGRAMADO, VIAJE_ASIGNADO) or datetime.fromisoformat(viaje.fecha_hora) > ahora:
                    continue
                suscripcion = self.repositorio.obtener_suscripcion(viaje.id_suscripcion)
                if suscripcion is None or suscripcion.estado == ESTADO_CANCELADA:
                    viaje.estado, viaje.error, cambios = VIAJE_CANCELADO, "La suscripcion ya no esta disponible.", True
                elif suscripcion.estado != ESTADO_PAUSADA and ahora - datetime.fromisoformat(viaje.fecha_hora) > self.MARGEN_ATRASO:
                    viaje.estado, viaje.error, cambios = VIAJE_FALLIDO, "El horario vencio mientras la aplicacion estaba cerrada.", True
            cambios = self._finalizar_suscripciones(ahora.date()) or cambios
            if cambios:
                unidad.confirmar()
            else:
                unidad.marcar_sin_cambios()
        return []

    def _finalizar_suscripciones(self, fecha_actual):
        cambios = False
        for suscripcion in self.repositorio.listar_suscripciones():
            if suscripcion.estado == ESTADO_ACTIVA and date.fromisoformat(suscripcion.fecha_fin) < fecha_actual:
                suscripcion.estado, cambios = ESTADO_FINALIZADA, True
        return cambios
