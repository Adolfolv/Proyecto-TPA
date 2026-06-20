from Modelos.Viaje.modelo_viajes import (
    CalleOsorno,
    ConductorSimulado,
    PasajeroSimulado,
)
from Servicios.Viajes.trayectoria import (
    OSORNO_LAT_NORTE,
    OSORNO_LAT_SUR,
    OSORNO_LNG_ESTE,
    OSORNO_LNG_OESTE,
    punto_relativo_desde_coordenada,
)


COORDENADAS_REALES_OSORNO = {
    "Plaza de Armas Osorno": (-40.57397, -73.13572),
    "Terminal de Buses Osorno": (-40.57293, -73.12563),
    "Hospital Base San Jose": (-40.58794, -73.12787),
    "Universidad de Los Lagos": (-40.587167, -73.089164),
    "Portal Osorno": (-40.57408, -73.13048),
    "Parque Chuyaca": (-40.575000, -73.103889),
    "Mercado Municipal Osorno": (-40.57296, -73.12880),
    "Estadio Ruben Marcos Peralta": (-40.58333, -73.13167),
    "Casino Marina del Sol Osorno": (-40.57539, -73.14577),
}

IMAGENES_LUGARES_OSORNO = {
    "Plaza de Armas Osorno": "plazadearmas.png",
    "Terminal de Buses Osorno": "terminal.png",
    "Hospital Base San Jose": "hospital base.png",
    "Universidad de Los Lagos": "ulagos.png",
    "Portal Osorno": "portalosorno.png",
    "Parque Chuyaca": "parquechuyaca.png",
    "Mercado Municipal Osorno": "mercadomunicipalosorno.png",
    "Estadio Ruben Marcos Peralta": "estadiorubenmarcos.png",
    "Casino Marina del Sol Osorno": "casino.png",
}

LUGARES_OSORNO = {
    nombre: punto_relativo_desde_coordenada(latitud, longitud)
    for nombre, (latitud, longitud) in COORDENADAS_REALES_OSORNO.items()
}

# Calles usadas solo para sembrar puntos plausibles de conductores simulados.
CALLES_OSORNO = (
    CalleOsorno(
        "Av. Republica - eje centro oriente",
        (
            punto_relativo_desde_coordenada(-40.57450, -73.13630),
            punto_relativo_desde_coordenada(-40.57397, -73.13572),
            punto_relativo_desde_coordenada(-40.57408, -73.13048),
            punto_relativo_desde_coordenada(-40.57296, -73.12880),
            punto_relativo_desde_coordenada(-40.57293, -73.12563),
            punto_relativo_desde_coordenada(-40.57380, -73.11800),
            punto_relativo_desde_coordenada(-40.57500, -73.103889),
        ),
    ),
    CalleOsorno(
        "Juan Mackenna - Manuel Rodriguez",
        (
            punto_relativo_desde_coordenada(-40.57296, -73.12880),
            punto_relativo_desde_coordenada(-40.57920, -73.13020),
            punto_relativo_desde_coordenada(-40.58333, -73.13167),
            punto_relativo_desde_coordenada(-40.58794, -73.12787),
        ),
    ),
    CalleOsorno(
        "Los Carrera - acceso sur centro",
        (
            punto_relativo_desde_coordenada(-40.57408, -73.13048),
            punto_relativo_desde_coordenada(-40.57920, -73.13020),
            punto_relativo_desde_coordenada(-40.58333, -73.13167),
        ),
    ),
    CalleOsorno(
        "Rene Soriano - Chuyaca - ULagos",
        (
            punto_relativo_desde_coordenada(-40.57500, -73.103889),
            punto_relativo_desde_coordenada(-40.57980, -73.10100),
            punto_relativo_desde_coordenada(-40.58420, -73.09500),
            punto_relativo_desde_coordenada(-40.587167, -73.089164),
        ),
    ),
    CalleOsorno(
        "Ruta 5 Sur - enlace oriente",
        (
            punto_relativo_desde_coordenada(-40.56000, -73.10650),
            punto_relativo_desde_coordenada(-40.57500, -73.103889),
            punto_relativo_desde_coordenada(-40.58420, -73.09500),
            punto_relativo_desde_coordenada(-40.59600, -73.09200),
        ),
    ),
    CalleOsorno(
        "Rahue Centro",
        (
            punto_relativo_desde_coordenada(-40.57539, -73.14577),
            punto_relativo_desde_coordenada(-40.57520, -73.14420),
        ),
    ),
    CalleOsorno(
        "Costanera centro",
        (
            punto_relativo_desde_coordenada(-40.57520, -73.14420),
            punto_relativo_desde_coordenada(-40.57450, -73.13630),
            punto_relativo_desde_coordenada(-40.57397, -73.13572),
        ),
    ),
    CalleOsorno(
        "Calle Burchard - acceso directo Hospital",
        (
            punto_relativo_desde_coordenada(-40.57293, -73.12563),
            punto_relativo_desde_coordenada(-40.57600, -73.12580),
            punto_relativo_desde_coordenada(-40.57900, -73.12640),
            punto_relativo_desde_coordenada(-40.58300, -73.12700),
            punto_relativo_desde_coordenada(-40.58794, -73.12787),
        ),
    ),
    CalleOsorno(
        "Av. Errazuriz - eje sur transversal",
        (
            punto_relativo_desde_coordenada(-40.58333, -73.13167),
            punto_relativo_desde_coordenada(-40.58300, -73.12700),
            punto_relativo_desde_coordenada(-40.58200, -73.12000),
            punto_relativo_desde_coordenada(-40.58100, -73.10500),
            punto_relativo_desde_coordenada(-40.57980, -73.10100),
        ),
    ),
    CalleOsorno(
        "Calle Arturo Prat - eje norte sur oriente",
        (
            punto_relativo_desde_coordenada(-40.57380, -73.11800),
            punto_relativo_desde_coordenada(-40.57600, -73.11780),
            punto_relativo_desde_coordenada(-40.57900, -73.11600),
            punto_relativo_desde_coordenada(-40.58100, -73.10500),
        ),
    ),
)

CONDUCTORES_SIMULADOS = (
    ConductorSimulado("Martin", "Rojas", "hombre1.png", "Toyota", "Yaris", "ABCD-12", 3800),
    ConductorSimulado("Matias", "Soto", "hombre2.png", "Hyundai", "Accent", "WXYZ-98", 4200),
    ConductorSimulado("Diego", "Perez", "hombre3.png", "Chevrolet", "Sail", "JKLM-34", 3600),
    ConductorSimulado("Felipe", "Munoz", "hombre4.png", "Kia", "Rio", "PQRS-56", 4500),
    ConductorSimulado("Sebastian", "Vidal", "hombre5.png", "Suzuki", "Swift", "TUVW-78", 4100),
    ConductorSimulado("Cristobal", "Arias", "hombre6.png", "Nissan", "Versa", "EFGH-90", 4700),
    ConductorSimulado("Nicolas", "Munoz", "hombre7.png", "Renault", "Logan", "IJKL-11", 3900),
    ConductorSimulado("Benjamin", "Torres", "hombre8.png", "Mazda", "2", "MNOP-22", 4300),
    ConductorSimulado("Pablo", "Lagos", "hombre9.png", "Volkswagen", "Gol", "QRST-33", 4000),
    ConductorSimulado("Agustin", "Cardenas", "hombre10.png", "Ford", "Fiesta", "UVWX-44", 4400),
)

PASAJEROS_SIMULADOS = (
    PasajeroSimulado(
        "Nicolas",
        "Vera",
        "hombre11.png",
        "Toyota",
        "Corolla",
        4200,
        "Plaza de Armas Osorno",
        "Hospital Base San Jose",
    ),
    PasajeroSimulado(
        "Felipe",
        "Castro",
        "hombre12.png",
        "Hyundai",
        "Accent",
        3900,
        "Terminal de Buses Osorno",
        "Universidad de Los Lagos",
    ),
    PasajeroSimulado(
        "Benjamin",
        "Silva",
        "hombre13.png",
        "Chevrolet",
        "Sail",
        3600,
        "Portal Osorno",
        "Parque Chuyaca",
    ),
    PasajeroSimulado(
        "Tomas",
        "Paredes",
        "hombre14.png",
        "Kia",
        "Rio",
        4500,
        "Mercado Municipal Osorno",
        "Casino Marina del Sol Osorno",
    ),
    PasajeroSimulado(
        "Antonia",
        "Reyes",
        "mujer1.png",
        "Suzuki",
        "Swift",
        4100,
        "Estadio Ruben Marcos Peralta",
        "Plaza de Armas Osorno",
    ),
)
