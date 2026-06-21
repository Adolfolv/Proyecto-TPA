from dataclasses import asdict
from pathlib import Path

from Modelos.Reputacion.opinion import Opinion
from Repositorios.repositorio_json import cargar_json, guardar_json


class RepositorioReputacion:
    def __init__(self, archivo=None):
        self.archivo = archivo or Path(__file__).resolve().parents[1] / "opiniones.json"
        self.opiniones = None

    def listar(self):
        if self.opiniones is None:
            self.opiniones = [Opinion(**datos) for datos in cargar_json(self.archivo)]
        return self.opiniones

    def listar_por_conductor(self, id_conductor):
        return [opinion for opinion in self.listar() if opinion.id_conductor == str(id_conductor)]

    def buscar_del_pasajero(self, id_conductor, id_pasajero):
        return next(
            (opinion for opinion in self.listar_por_conductor(id_conductor) if opinion.id_pasajero == str(id_pasajero)),
            None,
        )

    def agregar(self, opinion):
        opinion.id_opinion = self.siguiente_id()
        self.listar().append(opinion)
        guardar_json(self.archivo, [asdict(item) for item in self.opiniones])
        return opinion

    def siguiente_id(self):
        numeros = [int(opinion.id_opinion[3:]) for opinion in self.listar()]
        return f"OPI{max(numeros, default=0) + 1:04d}"
