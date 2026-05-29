import json
from dataclasses import asdict


class RepositorioJSONGenerico:

    def __init__(self, archivo, clase):
        self.archivo = archivo
        self.clase = clase

    # -------------------------
    # CARGAR (devuelve dicts)
    # -------------------------
    def cargar_json(self):
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    # -------------------------
    # GUARDAR (recibe objetos)
    # -------------------------
    def guardar_json(self, lista_objetos):
        datos = [asdict(obj) for obj in lista_objetos]

        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

