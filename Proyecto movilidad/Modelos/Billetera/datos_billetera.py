from dataclasses import dataclass, field
# Archivo para manejar los datos relacionados con la billetera del usuario, incluyendo las clases para representar,
@dataclass
class Tarjetas:
    titular: str
    numero_tarjeta: str
    vencimiento: str
    cvv: str
    saldo: int
    
@dataclass
class Transaccion:
    id_transaccion: str
    tipo: str
    monto: int
    fecha: str

@dataclass
class Billetera:
    saldo: int = 0
    tarjetas: list[Tarjetas] = field(default_factory=list)
    transacciones: list[Transaccion] = field(default_factory=list)


@dataclass
class SolicitudOperacionBilletera:
    usuario: object
    monto: int
    numero_tarjeta: str = None

#.
