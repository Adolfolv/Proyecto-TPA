from dataclasses import dataclass


# Alias simples para que las firmas de viaje comuniquen si una ruta usa puntos
# relativos del mapa interno o coordenadas reales para TkinterMapView.
PuntoRelativo = tuple[float, float]
CoordenadaReal = tuple[float, float]
RutaReal = list[CoordenadaReal]


@dataclass(frozen=True)
class CalleOsorno:
    """Tramo simulado usado para ubicar conductores alrededor de Osorno."""

    nombre: str
    puntos: tuple[PuntoRelativo, ...]


@dataclass(frozen=True)
class ConductorSimulado:
    """Datos base de un conductor disponible para el flujo de pasajero."""

    nombre: str
    apellido: str
    imagen: str
    marca_vehiculo: str
    modelo_vehiculo: str
    patente: str
    precio: float


@dataclass(frozen=True)
class PasajeroSimulado:
    """Datos base de un pasajero disponible para el flujo de conductor."""

    nombre: str
    apellido: str
    imagen: str
    marca_vehiculo: str
    modelo_vehiculo: str
    pago: float
    ubicacion_inicial: str
    ubicacion_final: str


@dataclass(frozen=True)
class VehiculoDisponible:
    """Resultado tipado que el pasajero puede seleccionar para viajar."""

    nombre_completo: str
    vehiculo: str
    patente: str
    imagen: str
    precio: float
    distancia: float
    tiempo: int
    ubicacion_relativa: PuntoRelativo
    ubicacion_real: CoordenadaReal


@dataclass(frozen=True)
class PasajeroEncontrado:
    """Resultado tipado que el conductor puede aceptar para iniciar viaje."""

    nombre_completo: str
    vehiculo: str
    trayecto: str
    ubicacion_inicial: str
    ubicacion_final: str
    ubicacion_conductor: str
    imagen: str
    precio: float
    distancia: float
    duracion: int
    km_para_llegar: float
    km_transportando: float
    tiempo_para_llegar: int
    tiempo_transportando: int
    duracion_busqueda: int


@dataclass(frozen=True)
class RutasViaje:
    """Rutas reales que la vista necesita para animar llegada y traslado."""

    llegada: RutaReal
    viaje: RutaReal


@dataclass(frozen=True)
class ResultadoBusquedaVehiculos:
    """Respuesta del caso de uso de busqueda del pasajero."""

    exitoso: bool
    error: str = ""
    vehiculos: tuple[VehiculoDisponible, ...] = ()
    ruta_busqueda: RutaReal | None = None


@dataclass(frozen=True)
class ResultadoBusquedaPasajero:
    """Respuesta del caso de uso de busqueda del conductor."""

    exitoso: bool
    error: str = ""
    pasajero: PasajeroEncontrado | None = None
    ruta_pasajero: RutaReal | None = None


@dataclass
class Viaje:
    """Registro de un viaje creado durante el flujo actual."""

    pasajero: str
    conductor: str
    vehiculo: str
    precio: float
    distancia: float
    duracion: float


@dataclass(frozen=True)
class ResultadoViaje:
    """Respuesta tipada de un caso de uso que inicia o confirma un viaje."""

    exitoso: bool
    error: str = ""
    rutas_viaje: RutasViaje | None = None
    viaje: Viaje | None = None

