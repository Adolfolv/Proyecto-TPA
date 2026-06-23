from datetime import datetime, timedelta

from Modelos.Historial.modelo_historial import (
    ActividadDiaria,
    RegistroHistorialViaje,
    ResumenHistorial,
)


class FabricaHistorial:
    """Adapta los dos modelos operativos al mismo modelo historico."""

    def __init__(self, reloj=None):
        self.reloj = reloj or datetime.now

    def desde_viaje_normal(self, viaje):
        return RegistroHistorialViaje(
            id_viaje=viaje.id_viaje,
            id_pasajero=viaje.id_pasajero,
            id_conductor=viaje.id_conductor,
            pasajero=viaje.pasajero,
            conductor=viaje.conductor,
            origen=viaje.origen,
            destino=viaje.destino,
            fecha_inicio=viaje.fecha_inicio,
            fecha_finalizacion=self.reloj().isoformat(timespec="seconds"),
            modalidad="VIAJE NORMAL",
            tipo_viaje=viaje.tipo.upper(),
            vehiculo=viaje.vehiculo,
            precio=float(viaje.precio),
            pago_conductor=float(viaje.precio),
            distancia=float(viaje.distancia),
            duracion=float(viaje.duracion),
            cantidad_pasajeros=int(viaje.cantidad_pasajeros),
            volumen=viaje.volumen,
            peso=viaje.peso,
            tipo_material=viaje.tipo_material,
        )

    def desde_suscripcion(self, suscripcion, viaje):
        return RegistroHistorialViaje(
            id_viaje=viaje.id_viaje_programado,
            id_pasajero=str(viaje.id_pasajero),
            id_conductor=str(viaje.id_conductor),
            pasajero="",
            conductor=viaje.conductor,
            origen=viaje.origen,
            destino=viaje.destino,
            fecha_inicio=viaje.inicio_confirmado_en or viaje.fecha_hora,
            fecha_finalizacion=self.reloj().isoformat(timespec="seconds"),
            modalidad="SUSCRIPCION",
            tipo_viaje="NORMAL",
            vehiculo=viaje.vehiculo or suscripcion.vehiculo,
            precio=float(viaje.precio),
            pago_conductor=float(viaje.pago_conductor),
            distancia=float(viaje.km_para_llegar + viaje.km_transportando),
            duracion=float(viaje.duracion_trayecto_segundos),
            cantidad_pasajeros=int(viaje.cantidad_pasajeros),
        )


class ServicioHistorial:
    def __init__(self, repositorio, fabrica, reloj=None):
        self.repositorio = repositorio
        self.fabrica = fabrica
        self.reloj = reloj or datetime.now

    def registrar_viaje_normal(self, viaje):
        registro = self.fabrica.desde_viaje_normal(viaje)
        return self._guardar_registro(registro)

    def registrar_viaje_suscripcion(self, suscripcion, viaje):
        registro = self.fabrica.desde_suscripcion(suscripcion, viaje)
        return self._guardar_registro(registro)

    def _guardar_registro(self, registro):
        existente = self.repositorio.obtener_por_viaje(registro.id_viaje)
        if existente is None:
            return self.repositorio.agregar(registro)
        if not self._debe_actualizar(existente, registro):
            return existente
        actualizado = self.repositorio.actualizar(registro)
        if actualizado is None:
            raise ValueError("No se encontro el viaje en el historial.")
        return actualizado

    @staticmethod
    def _debe_actualizar(existente, nuevo):
        return (
            nuevo.pago_conductor > existente.pago_conductor
            or (not existente.id_conductor and nuevo.id_conductor)
            or (not existente.conductor and nuevo.conductor)
        )

    def consultar(self, usuario):
        viajes = sorted(
            self.repositorio.listar_por_usuario(usuario.id_usuario),
            key=lambda item: item.fecha_finalizacion,
            reverse=True,
        )
        actividad, total, tendencia = self._calcular_actividad(viajes)
        return ResumenHistorial(tuple(viajes), actividad, total, tendencia)

    def _calcular_actividad(self, viajes):
        hoy = self.reloj().date()
        cantidades = {
            hoy - timedelta(days=indice): 0
            for indice in range(14)
        }
        for viaje in viajes:
            fecha = datetime.fromisoformat(viaje.fecha_finalizacion).date()
            if fecha in cantidades:
                cantidades[fecha] += 1

        dias_actuales = [hoy - timedelta(days=indice) for indice in range(6, -1, -1)]
        dia_anterior = hoy - timedelta(days=7)
        anterior = cantidades[dia_anterior]
        actividad = []
        for fecha in dias_actuales:
            cantidad = cantidades[fecha]
            actividad.append(
                ActividadDiaria(fecha.isoformat(), cantidad, cantidad - anterior)
            )
            anterior = cantidad

        total_actual = sum(cantidades[hoy - timedelta(days=i)] for i in range(7))
        total_anterior = sum(cantidades[hoy - timedelta(days=i)] for i in range(7, 14))
        if total_anterior:
            tendencia = ((total_actual - total_anterior) / total_anterior) * 100
        else:
            tendencia = 100.0 if total_actual else 0.0
        return tuple(actividad), total_actual, round(tendencia, 1)
