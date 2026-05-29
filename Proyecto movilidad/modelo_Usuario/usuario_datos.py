from dataclasses import dataclass, asdict

@dataclass
class Auto:
    marca: str
    modelo: str
    año: int
    patente: str

@dataclass
class Usuario:
    id_usuario: int
    nombre: str
    correo: str
    edad: int
    telefono: str
    contraseña: str

@dataclass
class Pasajero(Usuario):
    direccion: str

@dataclass
class Conductor(Usuario):
    licencia_conducir: str
    auto: Auto

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


