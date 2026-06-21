"""Catálogo simulado utilizado por la estrategia de ofertas del conductor."""

RUTAS = (
    ("Plaza de Armas Osorno", "Hospital Base San Jose"), ("Terminal de Buses Osorno", "Universidad de Los Lagos"),
    ("Portal Osorno", "Parque Chuyaca"), ("Mercado Municipal Osorno", "Hospital Base San Jose"),
    ("Casino Marina del Sol Osorno", "Terminal de Buses Osorno"), ("Estadio Ruben Marcos Peralta", "Plaza de Armas Osorno"),
    ("Universidad de Los Lagos", "Portal Osorno"), ("Parque Chuyaca", "Mercado Municipal Osorno"),
    ("Hospital Base San Jose", "Casino Marina del Sol Osorno"), ("Plaza de Armas Osorno", "Universidad de Los Lagos"),
    ("Terminal de Buses Osorno", "Portal Osorno"), ("Portal Osorno", "Estadio Ruben Marcos Peralta"),
    ("Mercado Municipal Osorno", "Parque Chuyaca"), ("Casino Marina del Sol Osorno", "Hospital Base San Jose"),
    ("Estadio Ruben Marcos Peralta", "Terminal de Buses Osorno"), ("Universidad de Los Lagos", "Plaza de Armas Osorno"),
    ("Parque Chuyaca", "Casino Marina del Sol Osorno"), ("Hospital Base San Jose", "Portal Osorno"),
    ("Plaza de Armas Osorno", "Mercado Municipal Osorno"), ("Terminal de Buses Osorno", "Parque Chuyaca"),
)

OFERTAS_SIMULADAS = {
    f"oferta_simulada_{indice:02d}": {
        "origen": origen, "destino": destino,
        "dias_semana": ((indice - 1) % 7, indice % 7),
        "hora": f"{7 + ((indice * 2) % 13):02d}:{(indice % 4) * 15:02d}",
        "cantidad_pasajeros": 1 + (indice % 3),
        "distancia_conductor": round(0.8 + (indice % 6) * 0.45, 2),
    }
    for indice, (origen, destino) in enumerate(RUTAS, start=1)
}
