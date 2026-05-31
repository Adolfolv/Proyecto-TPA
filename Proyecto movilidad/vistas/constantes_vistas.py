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


# --- constantes archivo viaje.py ---

TITULO_VIAJE = "Viaje"
GEOMETRIA_VIAJE = "1200x720"
TAMANO_MINIMO_VIAJE = (900, 620)

LUGARES_OSORNO = (
    "Plaza de Armas Osorno",
    "Terminal de Buses Osorno",
    "Hospital Base San Jose",
    "Universidad de Los Lagos",
    "Portal Osorno",
    "Parque Chuyaca",
    "Mercado Municipal Osorno",
    "Estadio Ruben Marcos Peralta",
    "Casino Marina del Sol Osorno",
)

COORDENADAS_OSORNO = {
    "Plaza de Armas Osorno": (-40.5736242, -73.1358144),
    "Terminal de Buses Osorno": (-40.5729093, -73.1258629),
    "Hospital Base San Jose": (-40.5878547, -73.1288600),
    "Universidad de Los Lagos": (-40.5793089, -73.1323055),
    "Portal Osorno": (-40.5741404, -73.1305151),
    "Parque Chuyaca": (-40.5750802, -73.1029830),
    "Mercado Municipal Osorno": (-40.5729830, -73.1287142),
    "Estadio Ruben Marcos Peralta": (-40.5832579, -73.1315144),
    "Casino Marina del Sol Osorno": (-40.5754457, -73.1455984),
}

CONDUCTORES_DEMO = (
    ("Camila R.", "Toyota Yaris", "$3.800", "4 min"),
    ("Ignacio P.", "Hyundai Accent", "$4.100", "6 min"),
    ("Valentina M.", "Kia Rio", "$3.650", "7 min"),
    ("Tomas A.", "Chevrolet Onix", "$4.450", "9 min"),
    ("Fernanda S.", "Nissan Versa", "$4.000", "10 min"),
)
