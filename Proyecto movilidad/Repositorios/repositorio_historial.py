from dataclasses import asdict
from pathlib import Path

from Modelos.Historial.modelo_historial import RegistroHistorialViaje
from Repositorios.repositorio_json import cargar_json, guardar_json


class RepositorioHistorial:
    """Persistencia idempotente para viajes terminados."""

    def __init__(self, archivo=None):
        self.archivo = archivo or Path(__file__).resolve().parents[1] / "historial_viajes.json"
        self.registros = None

    def _asegurar_cargado(self):
        if self.registros is not None:
            return
        datos = cargar_json(self.archivo)
        if not isinstance(datos, dict):
            datos = {}
        self.registros = [
            RegistroHistorialViaje(**item)
            for item in datos.get("viajes", [])
        ]

    def guardar_si_no_existe(self, registro):
        self._asegurar_cargado()
        existente = next(
            (item for item in self.registros if item.id_viaje == registro.id_viaje),
            None,
        )
        if existente is not None:
            debe_actualizar = (
                registro.pago_conductor > existente.pago_conductor
                or (not existente.id_conductor and registro.id_conductor)
                or (not existente.conductor and registro.conductor)
            )
            if not debe_actualizar:
                return existente
            indice = self.registros.index(existente)
            self.registros[indice] = registro
        else:
            self.registros.append(registro)
        guardar_json(
            self.archivo,
            {"viajes": [asdict(item) for item in self.registros]},
        )
        return registro

    def listar_por_usuario(self, id_usuario):
        self._asegurar_cargado()
        identificador = str(id_usuario)
        return [
            item
            for item in self.registros
            if identificador in (str(item.id_pasajero), str(item.id_conductor))
        ]
