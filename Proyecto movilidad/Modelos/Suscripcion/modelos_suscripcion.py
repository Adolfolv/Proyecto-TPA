from dataclasses import dataclass


ESTADO_ACTIVA = "ACTIVA"
ESTADO_PAUSADA = "PAUSADA"
ESTADO_CANCELADA = "CANCELADA"
ESTADO_FINALIZADA = "FINALIZADA"

VIAJE_PROGRAMADO = "PROGRAMADO"
VIAJE_BUSCANDO = "BUSCANDO_CONDUCTOR"
VIAJE_CONFIRMADO = "CONFIRMADO"
VIAJE_CANCELADO = "CANCELADO"
VIAJE_FALLIDO = "FALLIDO"


@dataclass
class SuscripcionViaje:
    id_suscripcion: str
    id_pasajero: str
    origen: str
    destino: str
    fecha_inicio: str
    fecha_fin: str
    dias_semana: tuple[int, ...]
    hora: str
    cantidad_pasajeros: int
    estado: str = ESTADO_ACTIVA
    creada_en: str = ""


@dataclass
class ViajeProgramado:
    id_viaje_programado: str
    id_suscripcion: str
    id_pasajero: str
    origen: str
    destino: str
    cantidad_pasajeros: int
    fecha_hora: str
    estado: str = VIAJE_PROGRAMADO
    conductor: str = ""
    vehiculo: str = ""
    precio: float = 0.0
    error: str = ""

