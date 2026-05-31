"""Constantes compartidas por las vistas."""


# --- constantes archivo registro.py ---

TITULO_REGISTRO = "Registro"
GEOMETRIA_REGISTRO = "900x700"
TAMANO_MINIMO_REGISTRO = (760, 620)
PANTALLA_COMPLETA_REGISTRO = True

CATEGORIAS_LICENCIA = ("Categoria A1", "Categoria A2", "Categoria A3", "Categoria B")
PREFIJO_TELEFONO = "+56 9"

MARCAS_MODELOS = {
    "Chevrolet": ("Sail", "Onix", "Spark", "Tracker", "N400 Max", "Captiva", "Aveo", "Cruze"),
    "Hyundai": ("Accent", "Grand i10", "Elantra", "Tucson", "Creta", "Venue", "Santa Fe", "H-1"),
    "Kia": ("Rio", "Morning", "Cerato", "Sportage", "Soluto", "Sorento", "Carens", "Carnival"),
    "Toyota": ("Yaris", "Corolla", "RAV4", "Hilux", "Raize", "Fortuner", "Avanza", "Prius"),
    "Suzuki": ("Swift", "Baleno", "Dzire", "Vitara", "S-Presso", "Celerio", "Ertiga", "Jimny"),
    "Nissan": ("Versa", "March", "Sentra", "Kicks", "Qashqai", "X-Trail", "Navara", "Pathfinder"),
    "Peugeot": ("208", "2008", "301", "308", "3008", "Partner", "Rifter", "5008"),
    "Renault": ("Symbol", "Logan", "Sandero", "Duster", "Koleos", "Captur", "Oroch", "Kwid"),
    "Mazda": ("2", "3", "6", "CX-3", "CX-30", "CX-5", "BT-50", "CX-9"),
    "Mitsubishi": ("L200", "Outlander", "ASX", "Eclipse Cross", "Montero", "Xpander", "Mirage", "Lancer"),
    "Volkswagen": ("Gol", "Polo", "Virtus", "T-Cross", "Tiguan", "Saveiro", "Nivus", "Amarok"),
    "Ford": ("Fiesta", "Focus", "Escape", "EcoSport", "Territory", "Ranger", "Explorer", "Maverick"),
    "MG": ("MG3", "ZS", "ZX", "HS", "GT", "RX5", "Marvel R", "MG4"),
    "Changan": ("Alsvin", "CS15", "CS35", "CS55", "Uni-T", "Hunter", "Honor S", "M201"),
    "Subaru": ("Impreza", "Legacy", "XV", "Forester", "Outback", "WRX", "Evoltis", "BRZ"),
    "Citroen": ("C3", "C4", "C-Elysee", "Berlingo", "Aircross", "Spacetourer", "Jumpy", "C5"),
    "Fiat": ("Argo", "Cronos", "Mobi", "Pulse", "Strada", "Fiorino", "Uno", "500"),
    "Honda": ("City", "Civic", "Accord", "WR-V", "HR-V", "CR-V", "Pilot", "Fit"),
    "JAC": ("S2", "S3", "S4", "JS2", "JS3", "JS4", "T6", "Sunray"),
    "Jetour": ("X70", "X70 Plus", "Dashing", "X90 Plus", "X95", "T2", "X70 Coupe", "X70S"),
    "GWM": ("Haval H6", "Haval Jolion", "Poer", "Wingle", "Ora 03", "Tank 300", "Haval H9", "M4"),
    "Mercedes-Benz": ("A200", "C200", "E200", "GLA", "GLB", "GLC", "Vito", "Sprinter"),
    "Volvo": ("S60", "S90", "V40", "XC40", "XC60", "XC90", "C40", "EX30"),
}


TITULO_VIAJE = "Viaje"
GEOMETRIA_VIAJE = "1200x720"
TAMANO_MINIMO_VIAJE = (900, 620)

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
