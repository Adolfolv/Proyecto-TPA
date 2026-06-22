from dataclasses import asdict

from JSON.rutas import ARCHIVO_OPINIONES
from Modelos.Reputacion.opinion import Opinion
from JSON.Repositorios.repositorio_json import cargar_json, guardar_json


class RepositorioReputacion:
    def __init__(self, archivo=None):
        self.archivo = archivo or ARCHIVO_OPINIONES

    def _escribir_opiniones(self, opiniones):
        guardar_json(
            self.archivo,
            {
                "opiniones": [
                    asdict(opinion)
                    for opinion in opiniones
                ]
            },
        )

    def _leer_opiniones(self):
        documento = cargar_json(self.archivo)
        if not isinstance(documento, dict):
            raise ValueError("El archivo de opiniones debe contener un objeto.")

        return [
            Opinion(**datos)
            for datos in documento.get("opiniones", [])
        ]

    def listar(self):
        return self._leer_opiniones()

    def listar_por_conductor(self, id_conductor):
        id_conductor = str(id_conductor)
        return [
            opinion
            for opinion in self.listar()
            if opinion.id_conductor == id_conductor
        ]

    def buscar_del_pasajero(self, id_conductor, id_pasajero):
        return next(
            (
                opinion
                for opinion in self.listar_por_conductor(id_conductor)
                if opinion.id_pasajero == str(id_pasajero)
            ),
            None,
        )

    def agregar(self, opinion):
        opiniones = self.listar()
        opiniones.append(opinion)
        self._escribir_opiniones(opiniones)
        return opinion
