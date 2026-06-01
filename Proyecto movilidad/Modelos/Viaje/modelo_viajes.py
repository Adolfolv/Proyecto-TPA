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
    usuario: str
    conductor: str
    vehiculo: str
    precio: float
    distancia: float
    duracion: float
    solicitud: SolicitudViaje
    

