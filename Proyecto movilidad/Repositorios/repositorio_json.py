
#archivo para manejar la lectura y escritura de datos en formato JSON, con métodos genéricos para cargar y guardar listas de objetos de cualquier clase.


import json
from dataclasses import asdict


def cargar_json(archivo):
    try:
        with open(
            archivo,
            "r",
            encoding="utf-8",
        ) as f:
            return json.load(f)

    except FileNotFoundError:
        return []


def guardar_json(archivo, datos):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump([asdict(dato) for dato in datos],
            f,
            indent=4,
            ensure_ascii=False,
        )

