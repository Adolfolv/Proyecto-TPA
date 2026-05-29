from dataclasses import dataclass, field

@dataclass
class tarjetas:
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
class billetera:
    saldo: float
    tarjetas: list = field(default_factory=list)
    transacciones: list = field(default_factory=list)

