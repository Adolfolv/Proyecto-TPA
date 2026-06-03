
#archivo para manejar la lectura y escritura de datos en formato JSON, con métodos genéricos para cargar y guardar listas de objetos de cualquier clase.


import json


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
        json.dump(
            datos,
            f,
            indent=4,
            ensure_ascii=False,
        )
