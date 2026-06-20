from dataclasses import asdict
from pathlib import Path

from Modelos.Suscripcion.modelos_suscripcion import SuscripcionViaje, ViajeProgramado
from Repositorios.repositorio_json import cargar_json, guardar_json


class RepositorioSuscripcion:
    """Persiste suscripciones y sus viajes generados en un unico documento JSON."""

    def __init__(self, archivo=None):
        self.archivo = archivo or Path(__file__).resolve().parents[1] / "suscripciones.json"
        self.suscripciones = []
        self.viajes_programados = []
        self.cargado = False

    def cargar(self):
        datos = cargar_json(self.archivo)
        if not isinstance(datos, dict):
            datos = {}

        self.suscripciones = [
            SuscripcionViaje(
                **{
                    **item,
                    "dias_semana": tuple(item.get("dias_semana", ())),
                }
            )
            for item in datos.get("suscripciones", [])
        ]
        self.viajes_programados = [
            ViajeProgramado(**item)
            for item in datos.get("viajes_programados", [])
        ]
        self.cargado = True
        return self.suscripciones, self.viajes_programados

    def guardar(self):
        guardar_json(
            self.archivo,
            {
                "suscripciones": [asdict(item) for item in self.suscripciones],
                "viajes_programados": [asdict(item) for item in self.viajes_programados],
            },
        )

    def _asegurar_cargado(self):
        if not self.cargado:
            self.cargar()

    def agregar(self, suscripcion, viajes_programados):
        self._asegurar_cargado()
        self.suscripciones.append(suscripcion)
        self.viajes_programados.extend(viajes_programados)
        self.guardar()
        return suscripcion

    def listar_suscripciones(self, id_pasajero=None):
        self._asegurar_cargado()
        if id_pasajero is None:
            return list(self.suscripciones)
        return [
            item for item in self.suscripciones
            if str(item.id_pasajero) == str(id_pasajero)
        ]

    def listar_viajes(self, id_pasajero=None, id_suscripcion=None):
        self._asegurar_cargado()
        viajes = self.viajes_programados
        if id_pasajero is not None:
            viajes = [item for item in viajes if str(item.id_pasajero) == str(id_pasajero)]
        if id_suscripcion is not None:
            viajes = [item for item in viajes if item.id_suscripcion == id_suscripcion]
        return list(viajes)

    def obtener_suscripcion(self, id_suscripcion):
        self._asegurar_cargado()
        return next(
            (item for item in self.suscripciones if item.id_suscripcion == id_suscripcion),
            None,
        )

    def guardar_cambios(self):
        self._asegurar_cargado()
        self.guardar()

