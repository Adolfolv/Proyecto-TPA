from dataclasses import dataclass, field
from typing import Optional

from Modelos.Billetera.datos_billetera import Billetera

#clases para representar a los usuarios, tanto pasajeros como conductores, con sus respectivos atributos y métodos.
#LA IDEA DE USAR DATACLASSES ES PARA SIMPLIFICAR LA CREACION DE OBJETOS Y SU CONVERSION A JSON, 
# PERO HAY QUE TENER CUIDADO CON LOS ATRIBUTOS QUE SON OBJETOS ANIDADOS, COMO LA BILLETERA, TARJETAS Y TRANSACCIONES, 
# YA QUE HAY QUE MANEJAR SU CONVERSION A JSON DE MANERA ESPECIAL EN EL SERVICIOUSUARIO. 
#MAS QUE NADA ERA PARA USAR ASDICT DE DATACLASSES PARA CONVERTIR LOS OBJETOS A DICCIONARIOS MUCHO MAS FACIL.
@dataclass
class Auto:
    marca: str
    modelo: str
    ano: int
    patente: str
    cantidad_asientos: int
    peso_equipaje: float

@dataclass
class Usuario:
    id_usuario: str
    nombre: str
    apellido: str
    correo: str
    edad: int
    telefono: str
    contrasena: str
    # Estado administrado desde el panel admin. Es kw_only para no romper
    # los constructores de Pasajero/Conductor, que agregan campos propios.
    cuenta_congelada: bool = field(default=False, kw_only=True)
    billetera: Optional[Billetera] = field(default=None, init=False)

@dataclass
class Pasajero(Usuario):
    direccion: str
    tipo_usuario: str = field(default="pasajero", init=False)

@dataclass
class Conductor(Usuario):
    tipo_licencia: str
    licencia_conducir: str
    selfie: str
    auto: Auto
    tipo_usuario: str = field(default="conductor", init=False)

#modelo administrador
@dataclass
class Administrador(Usuario):
    tipo_usuario: str = field(default="administrador", init=False)

"""""""""""
usuario1 = Pasajero(
    id_usuario=1,
    nombre="Juan Pérez",
    correo="juan.perez@example.com",
    edad=30,
    telefono="123456789",
    contrasena="contraseña123",
    direccion="Calle Falsa 123"
)

print(asdict(usuario1))
"""""""""


