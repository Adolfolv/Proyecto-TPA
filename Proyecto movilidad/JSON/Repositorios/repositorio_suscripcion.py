from copy import deepcopy
from dataclasses import asdict

from JSON.rutas import ARCHIVO_SUSCRIPCIONES
from Modelos.Suscripcion.modelos_suscripcion import (
    SuscripcionViaje,
    ViajeProgramado,
)
from JSON.Repositorios.repositorio_json import cargar_json, guardar_json


class RepositorioSuscripcion:
    """Persiste suscripciones y sus viajes generados en un unico documento JSON."""

    def __init__(self, archivo=None):
        self.archivo = archivo or ARCHIVO_SUSCRIPCIONES
        self.suscripciones = []
        self.viajes_programados = []
        self._cargado = False

    def _cargar(self):
        datos = cargar_json(self.archivo)
        if not isinstance(datos, dict):
            raise ValueError("El archivo de suscripciones debe contener un objeto.")

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
        self._cargado = True

    def _asegurar_cargado(self):
        if not self._cargado:
            self._cargar()

    def registrar_cambios(self, suscripcion, viajes_programados):
        """Registra cambios en memoria; Unit of Work decide cuándo persistir."""
        self._asegurar_cargado()
        self.suscripciones.append(suscripcion)
        self.viajes_programados.extend(viajes_programados)
        return suscripcion

    def crear_snapshot(self):
        """Memento interno utilizado por Unit of Work para poder deshacer."""
        self._asegurar_cargado()
        return deepcopy((self.suscripciones, self.viajes_programados))

    def restaurar_snapshot(self, snapshot):
        self.suscripciones, self.viajes_programados = deepcopy(snapshot)

    def reemplazar_datos(self, suscripciones, viajes_programados):
        self.suscripciones = list(suscripciones)
        self.viajes_programados = list(viajes_programados)

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

    def obtener_viaje(self, id_viaje):
        self._asegurar_cargado()
        return next((item for item in self.viajes_programados if item.id_viaje_programado == id_viaje), None)

    def listar_viajes_conductor(self, id_conductor, estados=None):
        self._asegurar_cargado()
        viajes = [item for item in self.viajes_programados if str(item.id_conductor) == str(id_conductor)]
        return [item for item in viajes if item.estado in estados] if estados else viajes

    def listar_suscripciones_conductor(self, id_conductor, estados=None):
        self._asegurar_cargado()
        suscripciones = [item for item in self.suscripciones if str(item.id_conductor) == str(id_conductor)]
        return [item for item in suscripciones if item.estado in estados] if estados else suscripciones

    def guardar_cambios(self):
        self._asegurar_cargado()
        guardar_json(
            self.archivo,
            {
                "suscripciones": [asdict(item) for item in self.suscripciones],
                "viajes_programados": [
                    asdict(item)
                    for item in self.viajes_programados
                ],
            },
        )
        self._cargado = True
