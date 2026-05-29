from dataclasses import dataclass

@dataclass
class solicitud_viaje:
    condutor: str
    pasajeros:str
    origen: str
    destino: str
    fecha_hora: str
    
@dataclass
class viaje:
    estado: str
    

