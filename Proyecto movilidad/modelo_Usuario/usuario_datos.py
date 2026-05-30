from dataclasses import dataclass, field
from Billetera.datos_billetera import Billetera

#clases para representar a los usuarios, tanto pasajeros como conductores, con sus respectivos atributos y métodos.
#LA IDEA DE USAR DATACLASSES ES PARA SIMPLIFICAR LA CREACION DE OBJETOS Y SU CONVERSION A JSON, 
# PERO HAY QUE TENER CUIDADO CON LOS ATRIBUTOS QUE SON OBJETOS ANIDADOS, COMO LA BILLETERA, TARJETAS Y TRANSACCIONES, 
# YA QUE HAY QUE MANEJAR SU CONVERSION A JSON DE MANERA ESPECIAL EN EL SERVICIOUSUARIO. 
#MAS QUE NADA ERA PARA USAR ASDICT DE DATACLASSES PARA CONVERTIR LOS OBJETOS A DICCIONARIOS MUCHO MAS FACIL
@dataclass
class Auto:
    marca: str
    modelo: str
    año: int
    patente: str

@dataclass
class Usuario:
    id_usuario: str
    nombre: str
    correo: str
    edad: int
    telefono: str
    contraseña: str
    billetera: Billetera = field(default=None, init=False)

    def __post_init__(self):
        if self.billetera is None:
            self.billetera = Billetera()

@dataclass
class Pasajero(Usuario):
    direccion: str
    tipo_usuario: str = field(default="pasajero", init=False)

@dataclass
class Conductor(Usuario):
    licencia_conducir: str
    auto: Auto
    tipo_usuario: str = field(default="conductor", init=False)

"""""""""""
usuario1 = Pasajero(
    id_usuario=1,
    nombre="Juan Pérez",
    correo="juan.perez@example.com",
    edad=30,
    telefono="123456789",
    contraseña="contraseña123",
    direccion="Calle Falsa 123"
)

print(asdict(usuario1))
"""""""""


