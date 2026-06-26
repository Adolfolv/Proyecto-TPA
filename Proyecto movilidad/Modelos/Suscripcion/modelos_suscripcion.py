from dataclasses import dataclass


NOMBRES_DIAS = ("Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom")


ESTADO_ACTIVA = "ACTIVA"
ESTADO_CANCELADA = "CANCELADA"
ESTADO_FINALIZADA = "FINALIZADA"

VIAJE_PROGRAMADO = "PROGRAMADO"
VIAJE_ASIGNADO = "ASIGNADO"
VIAJE_BUSCANDO = "BUSCANDO_CONDUCTOR"
VIAJE_CONFIRMADO = "CONFIRMADO"
VIAJE_CANCELADO = "CANCELADO"
VIAJE_FALLIDO = "FALLIDO"
VIAJE_EN_CURSO = "EN_CURSO"
VIAJE_FINALIZADO = "FINALIZADO"


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
    monto_consumido: float = 0.0
    monto_reembolsado: float = 0.0
    cargo_cancelacion: float = 0.0
    reembolso_pendiente: float = 0.0
    reembolso_estado: str = "PENDIENTE"
    id_conductor: str = ""
    conductor: str = ""
    vehiculo: str = ""
    ubicacion_conductor: str = ""
    aceptada_en: str = ""


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
    inicio_confirmado_en: str = ""
    duracion_trayecto_segundos: int = 0
    id_conductor: str = ""
    ubicacion_conductor: str = ""
    aceptado_en: str = ""
    pasajero_confirmo_en: str = ""
    km_para_llegar: float = 0.0
    km_transportando: float = 0.0
    tiempo_para_llegar: int = 0
    tiempo_transportando: int = 0
    pago_conductor: float = 0.0
    pago_conductor_estado: str = "PENDIENTE"


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
