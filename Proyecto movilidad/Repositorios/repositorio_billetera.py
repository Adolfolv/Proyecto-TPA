from pathlib import Path
from dataclasses import asdict

from Modelos.Billetera.datos_billetera import Billetera
from Repositorios.repositorio_json import cargar_json, guardar_json
from Servicios.Billetera.fabrica_billetera import FabricaBilletera


class RepositorioBilletera:

    def __init__(self, archivo=None, fabrica=None):
        archivo = (
            archivo
            or Path(__file__).resolve().parents[1] / "billeteras.json"
        )
        self.archivo = archivo
        self.fabrica = fabrica or FabricaBilletera()
        self.billeteras = {}
        self.cargado = False

    def cargar(self):
        self.billeteras = {
            str(datos["id_usuario"]): self.fabrica.crear_desde_dict(datos)
            for datos in cargar_json(self.archivo)
            if datos.get("id_usuario") is not None
        }
        self.cargado = True
        return self.billeteras

    def guardar(self):
        datos = [
            self.billetera_a_json(id_usuario, billetera)
            for id_usuario, billetera in self.billeteras.items()
        ]
        guardar_json(self.archivo, datos)
        self.cargado = True

    def obtener(self, usuario):
        billetera = self.obtener_por_usuario(usuario.id_usuario)
        usuario.billetera = billetera
        return billetera

    def obtener_por_usuario(self, id_usuario):
        if not self.cargado:
            self.cargar()

        id_usuario = str(id_usuario)
        billetera = self.billeteras.get(id_usuario)

        if billetera is None:
            billetera = Billetera()
            self.billeteras[id_usuario] = billetera
            self.guardar()

        return billetera

    def guardar_usuario(self, usuario):
        billetera = usuario.billetera or self.obtener_por_usuario(usuario.id_usuario)
        self.guardar_por_usuario(usuario.id_usuario, billetera)

    def guardar_por_usuario(self, id_usuario, billetera):
        if not self.cargado:
            self.cargar()

        self.billeteras[str(id_usuario)] = billetera
        self.guardar()

    def billetera_a_json(self, id_usuario, billetera):
        datos = asdict(billetera)
        for tarjeta in datos["tarjetas"]:
            tarjeta.pop("cvv", None)

        datos["id_usuario"] = str(id_usuario)
        return datos
    #.
