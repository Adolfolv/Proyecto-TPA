import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile


def cargar_json(archivo):
    try:
        with open(archivo, "r", encoding="utf-8") as archivo_json:
            return json.load(archivo_json)
    except FileNotFoundError:
        return {}


def guardar_json(archivo, datos):
    destino = Path(archivo)
    destino.parent.mkdir(parents=True, exist_ok=True)
    temporal = None
    try:
        with NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=destino.parent,
            delete=False,
        ) as archivo_temporal:
            temporal = Path(archivo_temporal.name)
            json.dump(datos, archivo_temporal, indent=4, ensure_ascii=False)
            archivo_temporal.flush()
            os.fsync(archivo_temporal.fileno())
        os.replace(temporal, destino)
    except Exception:
        if temporal is not None:
            temporal.unlink(missing_ok=True)
        raise
