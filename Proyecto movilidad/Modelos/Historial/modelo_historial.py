from dataclasses import dataclass


@dataclass(frozen=True)
class RegistroHistorialViaje:
    """Copia inmutable de un viaje que ya termino."""

    id_viaje: str
    id_pasajero: str
    id_conductor: str
    pasajero: str
    conductor: str
    origen: str
    destino: str
    fecha_inicio: str
    fecha_finalizacion: str
    modalidad: str
    tipo_viaje: str
    vehiculo: str
    precio: float
    pago_conductor: float
    distancia: float
    duracion: float
    cantidad_pasajeros: int = 1
    volumen: float | None = None
    peso: float | None = None
    tipo_material: str | None = None


@dataclass(frozen=True)
class ActividadDiaria:
    fecha: str
    cantidad: int
    variacion: int


@dataclass(frozen=True)
class ResumenHistorial:
    viajes: tuple[RegistroHistorialViaje, ...]
    actividad: tuple[ActividadDiaria, ...]
    total_ultimos_7_dias: int
    tendencia_porcentual: float
