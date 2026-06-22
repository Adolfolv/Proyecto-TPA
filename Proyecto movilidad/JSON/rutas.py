from pathlib import Path


CARPETA_JSON = Path(__file__).resolve().parent
CARPETA_DATOS = CARPETA_JSON / "Datos"

ARCHIVO_USUARIOS = CARPETA_DATOS / "usuarios.json"
ARCHIVO_BILLETERAS = CARPETA_DATOS / "billeteras.json"
ARCHIVO_OPINIONES = CARPETA_DATOS / "opiniones.json"
ARCHIVO_HISTORIAL = CARPETA_DATOS / "historial_viajes.json"
ARCHIVO_SUSCRIPCIONES = CARPETA_DATOS / "suscripciones.json"
