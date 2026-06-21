from dataclasses import dataclass


@dataclass
class Opinion:
    id_opinion: str | None
    id_conductor: str
    id_pasajero: str
    nombre_pasajero: str
    estrellas: int
    comentario: str
