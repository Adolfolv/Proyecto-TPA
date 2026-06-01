OSORNO_LAT_NORTE = -40.5480
OSORNO_LAT_SUR = -40.6050
OSORNO_LNG_OESTE = -73.1650
OSORNO_LNG_ESTE = -73.0850

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


def _punto_relativo_desde_coordenada(latitud: float, longitud: float) -> tuple[float, float]:
    x = (longitud - OSORNO_LNG_OESTE) / (OSORNO_LNG_ESTE - OSORNO_LNG_OESTE)
    y = (latitud - OSORNO_LAT_NORTE) / (OSORNO_LAT_SUR - OSORNO_LAT_NORTE)
    return (
        min(1.0, max(0.0, round(x, 5))),
        min(1.0, max(0.0, round(y, 5))),
    )


LUGARES_OSORNO = {
    nombre: _punto_relativo_desde_coordenada(latitud, longitud)
    for nombre, (latitud, longitud) in COORDENADAS_REALES_OSORNO.items()
}

CALLES_OSORNO = (
    (
        "Av. Republica - eje centro oriente",
        (
            _punto_relativo_desde_coordenada(-40.57450, -73.13630),
            _punto_relativo_desde_coordenada(-40.57397, -73.13572),
            _punto_relativo_desde_coordenada(-40.57408, -73.13048),
            _punto_relativo_desde_coordenada(-40.57296, -73.12880),
            _punto_relativo_desde_coordenada(-40.57293, -73.12563),
            _punto_relativo_desde_coordenada(-40.57380, -73.11800),
            _punto_relativo_desde_coordenada(-40.57500, -73.103889),
        ),
        8,
    ),
    (
        "Juan Mackenna - Manuel Rodriguez",
        (
            _punto_relativo_desde_coordenada(-40.57296, -73.12880),
            _punto_relativo_desde_coordenada(-40.57920, -73.13020),
            _punto_relativo_desde_coordenada(-40.58333, -73.13167),
            _punto_relativo_desde_coordenada(-40.58794, -73.12787),
        ),
        7,
    ),
    (
        "Los Carrera - acceso sur centro",
        (
            _punto_relativo_desde_coordenada(-40.57408, -73.13048),
            _punto_relativo_desde_coordenada(-40.57920, -73.13020),
            _punto_relativo_desde_coordenada(-40.58333, -73.13167),
        ),
        6,
    ),
    (
        "Rene Soriano - Chuyaca - ULagos",
        (
            _punto_relativo_desde_coordenada(-40.57500, -73.103889),
            _punto_relativo_desde_coordenada(-40.57980, -73.10100),
            _punto_relativo_desde_coordenada(-40.58420, -73.09500),
            _punto_relativo_desde_coordenada(-40.587167, -73.089164),
        ),
        8,
    ),
    (
        "Ruta 5 Sur - enlace oriente",
        (
            _punto_relativo_desde_coordenada(-40.56000, -73.10650),
            _punto_relativo_desde_coordenada(-40.57500, -73.103889),
            _punto_relativo_desde_coordenada(-40.58420, -73.09500),
            _punto_relativo_desde_coordenada(-40.59600, -73.09200),
        ),
        9,
    ),
    (
        "Rahue Centro",
        (
            _punto_relativo_desde_coordenada(-40.57539, -73.14577),
            _punto_relativo_desde_coordenada(-40.57520, -73.14420),
        ),
        6,
    ),
    (
        "Costanera centro",
        (
            _punto_relativo_desde_coordenada(-40.57520, -73.14420),
            _punto_relativo_desde_coordenada(-40.57450, -73.13630),
            _punto_relativo_desde_coordenada(-40.57397, -73.13572),
        ),
        5,
    ),
    (
        "Calle Burchard - acceso directo Hospital",
        (
            _punto_relativo_desde_coordenada(-40.57293, -73.12563),
            _punto_relativo_desde_coordenada(-40.57600, -73.12580),
            _punto_relativo_desde_coordenada(-40.57900, -73.12640),
            _punto_relativo_desde_coordenada(-40.58300, -73.12700),
            _punto_relativo_desde_coordenada(-40.58794, -73.12787),
        ),
        6,
    ),
    (
        "Av. Errazuriz - eje sur transversal",
        (
            _punto_relativo_desde_coordenada(-40.58333, -73.13167),
            _punto_relativo_desde_coordenada(-40.58300, -73.12700),
            _punto_relativo_desde_coordenada(-40.58200, -73.12000),
            _punto_relativo_desde_coordenada(-40.58100, -73.10500),
            _punto_relativo_desde_coordenada(-40.57980, -73.10100),
        ),
        7,
    ),
    (
        "Calle Arturo Prat - eje norte sur oriente",
        (
            _punto_relativo_desde_coordenada(-40.57380, -73.11800),
            _punto_relativo_desde_coordenada(-40.57600, -73.11780),
            _punto_relativo_desde_coordenada(-40.57900, -73.11600),
            _punto_relativo_desde_coordenada(-40.58100, -73.10500),
        ),
        6,
    ),
)

PUENTES_OSORNO = (
    (
        "Puente San Pedro",
        _punto_relativo_desde_coordenada(-40.57520, -73.14420),
        _punto_relativo_desde_coordenada(-40.57450, -73.13630),
    ),
)

CONDUCTORES_SIMULADOS = (
    {"nombre": "Martin Rojas", "imagen": "hombre1.png"},
    {"nombre": "Matias Soto", "imagen": "hombre2.png"},
    {"nombre": "Diego Perez", "imagen": "hombre3.png"},
    {"nombre": "Felipe Munoz", "imagen": "hombre4.png"},
    {"nombre": "Sebastian Vidal", "imagen": "hombre5.png"},
    {"nombre": "Cristobal Arias", "imagen": "hombre6.png"},
    {"nombre": "Nicolas Munoz", "imagen": "hombre7.png"},
    {"nombre": "Benjamin Torres", "imagen": "hombre8.png"},
    {"nombre": "Pablo Lagos", "imagen": "hombre9.png"},
    {"nombre": "Agustin Cardenas", "imagen": "hombre10.png"},
)

USUARIOS_SOLICITANTES_SIMULADOS = (
    {"nombre": "Nicolas Vera", "imagen": "hombre11.png"},
    {"nombre": "Felipe Castro", "imagen": "hombre12.png"},
    {"nombre": "Benjamin Silva", "imagen": "hombre13.png"},
    {"nombre": "Tomas Paredes", "imagen": "hombre14.png"},
    {"nombre": "Agustin Navarro", "imagen": "hombre15.png"},
    {"nombre": "Martin Fuentes", "imagen": "hombre16.png"},
    {"nombre": "Antonia Reyes", "imagen": "mujer1.png"},
    {"nombre": "Catalina Morales", "imagen": "mujer2.png"},
    {"nombre": "Isidora Fuentes", "imagen": "mujer3.png"},
    {"nombre": "Martina Alvarez", "imagen": "mujer4.png"},
)

PASAJEROS_SIMULADOS = (
    {
        "nombre": "Nicolas",
        "apellido": "Vera",
        "imagen": "hombre11.png",
        "marca_vehiculo": "Toyota",
        "modelo_vehiculo": "Corolla",
        "pago": 4200,
        "ubicacion_inicial": "Plaza de Armas Osorno",
        "ubicacion_final": "Hospital Base San Jose",
    },
    {
        "nombre": "Felipe",
        "apellido": "Castro",
        "imagen": "hombre12.png",
        "marca_vehiculo": "Hyundai",
        "modelo_vehiculo": "Accent",
        "pago": 3900,
        "ubicacion_inicial": "Terminal de Buses Osorno",
        "ubicacion_final": "Universidad de Los Lagos",
    },
    {
        "nombre": "Benjamin",
        "apellido": "Silva",
        "imagen": "hombre13.png",
        "marca_vehiculo": "Chevrolet",
        "modelo_vehiculo": "Sail",
        "pago": 3600,
        "ubicacion_inicial": "Portal Osorno",
        "ubicacion_final": "Parque Chuyaca",
    },
    {
        "nombre": "Tomas",
        "apellido": "Paredes",
        "imagen": "hombre14.png",
        "marca_vehiculo": "Kia",
        "modelo_vehiculo": "Rio",
        "pago": 4500,
        "ubicacion_inicial": "Mercado Municipal Osorno",
        "ubicacion_final": "Casino Marina del Sol Osorno",
    },
    {
        "nombre": "Antonia",
        "apellido": "Reyes",
        "imagen": "mujer1.png",
        "marca_vehiculo": "Suzuki",
        "modelo_vehiculo": "Swift",
        "pago": 4100,
        "ubicacion_inicial": "Estadio Ruben Marcos Peralta",
        "ubicacion_final": "Plaza de Armas Osorno",
    },
)
