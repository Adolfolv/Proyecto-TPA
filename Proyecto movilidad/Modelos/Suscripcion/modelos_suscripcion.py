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
    cantidad_viajes: int = 0
    precio_por_viaje: float = 0.0
    precio_total: float = 0.0
    pagada_anticipadamente: bool = False


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
    reembolsado: bool = False
    pagado_anticipadamente: bool = False


@dataclass(frozen=True)
class ResumenSuscripcion:
    origen: str
    destino: str
    fecha_inicio: str
    fecha_fin: str
    dias_semana: tuple[int, ...]
    hora: str
    cantidad_pasajeros: int
    fechas_viaje: tuple[str, ...]
    precio_por_viaje: float
    precio_total: float

    @property
    def cantidad_viajes(self):
        return len(self.fechas_viaje)
