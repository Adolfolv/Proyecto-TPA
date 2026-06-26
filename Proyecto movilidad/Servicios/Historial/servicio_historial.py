from datetime import datetime, timedelta

from Modelos.Historial.modelo_historial import RegistroHistorialViaje


class RegistradorHistorial:
    def __init__(self, repositorio, reloj=None):
        self.repositorio = repositorio
        self.reloj = reloj or datetime.now

    def registrar_viaje(self, viaje):
        registro = RegistroHistorialViaje(
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
        existente = self.repositorio.obtener_por_viaje(registro.id_viaje)
        if existente is None:
            return self.repositorio.agregar(registro)
        if (
            registro.pago_conductor > existente.pago_conductor
            or (not existente.id_conductor and registro.id_conductor)
            or (not existente.conductor and registro.conductor)
        ):
            return self.repositorio.actualizar(registro)
        return existente

    def registrar_viaje_suscripcion(self, suscripcion, viaje):
        registro = RegistroHistorialViaje(
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
        existente = self.repositorio.obtener_por_viaje(registro.id_viaje)
        if existente is None:
            return self.repositorio.agregar(registro)
        if (
            registro.pago_conductor > existente.pago_conductor
            or (not existente.id_conductor and registro.id_conductor)
            or (not existente.conductor and registro.conductor)
        ):
            return self.repositorio.actualizar(registro)
        return existente


class ServicioHistorial:
    def __init__(self, repositorio, repositorio_billetera=None, reloj=None):
        self.repositorio = repositorio
        self.repositorio_billetera = repositorio_billetera
        self.reloj = reloj or datetime.now

    def consultar(self, usuario):
        viajes = sorted(
            self.repositorio.listar_por_usuario(usuario.id_usuario),
            key=lambda item: item.fecha_finalizacion,
            reverse=True,
        )
        billetera = None
        if self.repositorio_billetera is not None:
            billetera = self.repositorio_billetera.obtener_por_usuario(
                usuario.id_usuario
            )
        transacciones = tuple(reversed(billetera.transacciones)) if billetera else ()

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
            actividad.append({
                "fecha": fecha.isoformat(),
                "cantidad": cantidad,
                "variacion": cantidad - anterior,
            })
            anterior = cantidad

        total_actual = sum(cantidades[hoy - timedelta(days=i)] for i in range(7))
        total_anterior = sum(cantidades[hoy - timedelta(days=i)] for i in range(7, 14))
        if total_anterior:
            tendencia = ((total_actual - total_anterior) / total_anterior) * 100
        else:
            tendencia = 100.0 if total_actual else 0.0

        return {
            "viajes": tuple(viajes),
            "actividad": tuple(actividad),
            "total_ultimos_7_dias": total_actual,
            "tendencia_porcentual": round(tendencia, 1),
            "transacciones": transacciones,
        }
