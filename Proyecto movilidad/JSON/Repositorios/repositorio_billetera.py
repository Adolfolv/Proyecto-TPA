from dataclasses import asdict

from JSON.rutas import ARCHIVO_BILLETERAS
from JSON.Repositorios.repositorio_json import cargar_json, guardar_json
from Servicios.Billetera.fabrica_billetera import FabricaBilletera


class RepositorioBilletera:
    # Patron Repository: esconde el acceso al JSON y entrega objetos Billetera.

    def __init__(self, archivo=None, fabrica=None):
        self.archivo = archivo or ARCHIVO_BILLETERAS
        # Inyeccion de dependencias: se puede reemplazar la fabrica si cambia la reconstruccion.
        self.fabrica = fabrica or FabricaBilletera()

    def _leer_billeteras(self):
        # Repository + Factory: lee JSON y usa la fabrica para volver a objetos.
        documento = cargar_json(self.archivo)
        if not isinstance(documento, dict):
            raise ValueError("El archivo de billeteras debe contener un objeto.")

        return {
            str(datos["id_usuario"]): self.fabrica.desde_dict(datos)
            for datos in documento.get("billeteras", [])
            if datos.get("id_usuario") is not None
        }

    def _escribir_billeteras(self, billeteras):
        # Repository: convierte los objetos a diccionarios y los persiste.
        datos = [
            self._a_dict(id_usuario, billetera)
            for id_usuario, billetera in billeteras.items()
        ]
        guardar_json(self.archivo, {"billeteras": datos})

    def obtener_por_usuario(self, id_usuario):
        billeteras = self._leer_billeteras()
        return billeteras.get(str(id_usuario))

    def agregar(self, id_usuario, billetera):
        billeteras = self._leer_billeteras()
        billeteras[str(id_usuario)] = billetera
        self._escribir_billeteras(billeteras)
        return billetera

    def actualizar(self, id_usuario, billetera):
        billeteras = self._leer_billeteras()
        id_usuario = str(id_usuario)
        if id_usuario not in billeteras:
            return None

        billeteras[id_usuario] = billetera
        self._escribir_billeteras(billeteras)
        return billetera

    def _a_dict(self, id_usuario, billetera):
        datos = asdict(billetera)
        for tarjeta in datos["tarjetas"]:
            tarjeta.pop("cvv", None)

        datos["id_usuario"] = str(id_usuario)
        return datos
