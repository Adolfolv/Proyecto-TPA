from dataclasses import dataclass, field
# Archivo para manejar los datos relacionados con la billetera del usuario, incluyendo las clases para representar,
@dataclass
class Tarjetas:
    titular: str
    numero_tarjeta: str
    vencimiento: str
    cvv: str
    saldo: float
    
@dataclass
class Transaccion:
    id_transaccion: str
    tipo: str
    monto: float
    fecha: str

@dataclass
class Billetera:
    id_usuario: str = None
    saldo: float = 0.0
    tarjetas: list[Tarjetas] = field(default_factory=list)
    transacciones: list[Transaccion] = field(default_factory=list)

