from dataclasses import dataclass


@dataclass
class Ubicacion:
    origen: str
    destino: str
@dataclass
class SolicitudViaje:
    cant_pasajeros:int
    fecha_hora: str
    ubicacion: Ubicacion
@dataclass
class Viaje:
    pasajero: str
    conductor: str
    vehiculo: str
    precio: float
    distancia: float
    duracion: float


@dataclass
class CuentaViajes:
    id_usuario: str
    tipo_usuario: str
    viajes: list[Viaje]

