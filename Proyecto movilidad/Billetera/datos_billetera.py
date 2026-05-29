from dataclasses import dataclass, field

@dataclass
class Tarjetas:
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
    saldo: float = 0.0
    tarjetas: list[Tarjetas] = field(default_factory=list)
    transacciones: list[Transaccion] = field(default_factory=list)

