from dataclasses import asdict

from JSON.rutas import ARCHIVO_HISTORIAL
from Modelos.Historial.modelo_historial import RegistroHistorialViaje
from JSON.Repositorios.repositorio_json import cargar_json, guardar_json


class RepositorioHistorial:
    """Persistencia idempotente para viajes terminados."""

    def __init__(self, archivo=None):
        self.archivo = archivo or ARCHIVO_HISTORIAL

    def _leer_registros(self):
        datos = cargar_json(self.archivo)
        if not isinstance(datos, dict):
            raise ValueError("El archivo de historial debe contener un objeto.")
        return [
            RegistroHistorialViaje(**item)
            for item in datos.get("viajes", [])
        ]

    def _escribir_registros(self, registros):
        guardar_json(
            self.archivo,
            {"viajes": [asdict(item) for item in registros]},
        )

    def obtener_por_viaje(self, id_viaje):
        return next(
            (
                registro
                for registro in self._leer_registros()
                if registro.id_viaje == id_viaje
            ),
            None,
        )

    def agregar(self, registro):
        registros = self._leer_registros()
        registros.append(registro)
        self._escribir_registros(registros)
        return registro

    def actualizar(self, registro_actualizado):
        registros = self._leer_registros()
        for indice, registro in enumerate(registros):
            if registro.id_viaje == registro_actualizado.id_viaje:
                registros[indice] = registro_actualizado
                self._escribir_registros(registros)
                return registro_actualizado

        return None

    def listar_por_usuario(self, id_usuario):
        identificador = str(id_usuario)
        return [
            item
            for item in self._leer_registros()
            if identificador in (str(item.id_pasajero), str(item.id_conductor))
        ]
