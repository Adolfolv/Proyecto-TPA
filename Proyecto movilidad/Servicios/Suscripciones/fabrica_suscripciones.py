"""Factory de entidades del agregado de suscripciones."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import uuid4

from Modelos.Suscripcion.modelos_suscripcion import VIAJE_ASIGNADO, SuscripcionViaje, ViajeProgramado


@dataclass(frozen=True)
class ConductorParaOferta:
    """Información necesaria para construir viajes de una oferta simulada."""

    nombre_completo: str
    vehiculo: str
    patente: str
    precio: float
    distancia: float
    tiempo: int


class FabricaSuscripciones:
    """Factory: construye modelos; no valida, persiste ni mueve dinero."""

    def __init__(self, servicio_viaje_comun, calculadora, politica_horarios, reloj, comision_plataforma=0.20):
        self.comun = servicio_viaje_comun
        self.calculadora = calculadora
        self.politica_horarios = politica_horarios
        self.reloj = reloj
        self.comision_plataforma = comision_plataforma

    def crear_desde_resumen(self, pasajero, resumen, conductor):
        suscripcion = SuscripcionViaje(id_suscripcion=uuid4().hex, id_pasajero=str(pasajero.id_usuario), origen=resumen.origen, destino=resumen.destino, fecha_inicio=resumen.fecha_inicio, fecha_fin=resumen.fecha_fin, dias_semana=resumen.dias_semana, hora=resumen.hora, cantidad_pasajeros=resumen.cantidad_pasajeros, creada_en=self.reloj().isoformat(timespec="seconds"), cantidad_viajes=resumen.cantidad_viajes, precio_por_viaje=resumen.precio_por_viaje, precio_total=resumen.precio_total, pagada_anticipadamente=True, conductor=conductor.nombre_completo, vehiculo=f"{conductor.vehiculo} ({conductor.patente})")
        return suscripcion, self.crear_viajes(suscripcion, resumen.fechas_viaje, conductor)

    def crear_viajes(self, suscripcion, fechas_viaje, conductor):
        ruta = self.comun.formar_trayectoria(suscripcion.origen, suscripcion.destino)
        distancia = round(sum(self.comun.calcular_km_entre_coordenadas(inicio, fin) for inicio, fin in zip(ruta, ruta[1:])), 2)
        tiempos = self.comun.calcular_tiempos_viaje(conductor.distancia, distancia)
        return [ViajeProgramado(id_viaje_programado=uuid4().hex, id_suscripcion=suscripcion.id_suscripcion, id_pasajero=suscripcion.id_pasajero, origen=suscripcion.origen, destino=suscripcion.destino, cantidad_pasajeros=suscripcion.cantidad_pasajeros, fecha_hora=fecha_hora, estado=VIAJE_ASIGNADO, precio=suscripcion.precio_por_viaje, pagado_anticipadamente=suscripcion.pagada_anticipadamente, conductor=conductor.nombre_completo, vehiculo=f"{conductor.vehiculo} ({conductor.patente})", km_para_llegar=conductor.distancia, km_transportando=distancia, tiempo_para_llegar=conductor.tiempo, tiempo_transportando=tiempos["tiempo_transportando"], duracion_trayecto_segundos=max(1, tiempos["tiempo_transportando"]), pago_conductor=round(suscripcion.precio_por_viaje * (1 - self.comision_plataforma))) for fecha_hora in fechas_viaje]

    def crear_oferta_simulada(self, id_oferta, datos, conductor):
        ahora = self.reloj()
        inicio = ahora.date() + timedelta(days=1)
        fin = inicio + timedelta(days=28)
        horario = datetime.strptime(datos["hora"], "%H:%M").time()
        fechas = self.politica_horarios.generar_fechas(inicio, fin, datos["dias_semana"], horario, ahora)
        precio = self.calculadora.calcular_precio_por_viaje(datos["origen"], datos["destino"], datos["cantidad_pasajeros"])
        suscripcion = SuscripcionViaje(id_suscripcion=id_oferta, id_pasajero=f"pasajero_{id_oferta}", origen=datos["origen"], destino=datos["destino"], fecha_inicio=inicio.isoformat(), fecha_fin=fin.isoformat(), dias_semana=tuple(datos["dias_semana"]), hora=datos["hora"], cantidad_pasajeros=datos["cantidad_pasajeros"], creada_en=ahora.isoformat(timespec="seconds"), cantidad_viajes=len(fechas), precio_por_viaje=precio, precio_total=precio * len(fechas), pagada_anticipadamente=True)
        oferta_conductor = ConductorParaOferta(nombre_completo=f"{conductor.nombre} {conductor.apellido}", vehiculo=f"{conductor.auto.marca} {conductor.auto.modelo}", patente=conductor.auto.patente, precio=precio, distancia=datos["distancia_conductor"], tiempo=max(1, round(datos["distancia_conductor"] * 2)))
        viajes = self.crear_viajes(suscripcion, tuple(fecha.isoformat(timespec="minutes") for fecha in fechas), oferta_conductor)
        if viajes:
            viajes[0].fecha_hora = (ahora + timedelta(minutes=1)).replace(microsecond=0).isoformat(timespec="seconds")
        return suscripcion, viajes
