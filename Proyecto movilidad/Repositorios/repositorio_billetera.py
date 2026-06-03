from pathlib import Path
from dataclasses import asdict

from Modelos.Billetera.datos_billetera import Billetera, Tarjetas, Transaccion
from Repositorios.repositorio_json import cargar_json, guardar_json


class RepositorioBilletera:

    def __init__(self, archivo=None):
        archivo = (
            archivo
            or Path(__file__).resolve().parents[1] / "billeteras.json"
        )
        self.archivo = archivo
        self.billeteras = {}

    def cargar(self):
        self.billeteras = {}

        for datos in cargar_json(self.archivo):
            id_usuario = datos.get("id_usuario")

            if id_usuario is not None:
                self.billeteras[str(id_usuario)] = self.crear_billetera(datos)

        return self.billeteras

    def guardar(self):
        guardar_json(
            self.archivo,
            [
                self.billetera_a_json(id_usuario, billetera)
                for id_usuario, billetera in self.billeteras.items()
            ]
        )

    def obtener(self, usuario):
        if not self.billeteras:
            self.cargar()

        id_usuario = str(usuario.id_usuario)
        billetera = self.billeteras.get(id_usuario)

        if billetera is None:
            billetera = usuario.billetera or Billetera()
            self.billeteras[id_usuario] = billetera
            self.guardar()

        usuario.billetera = billetera
        return billetera

    def guardar_usuario(self, usuario):
        self.billeteras[str(usuario.id_usuario)] = usuario.billetera
        self.guardar()

    def crear_billetera(self, datos):
        tarjetas = [
            Tarjetas(**tarjeta)
            for tarjeta in datos.get("tarjetas", [])
        ]
        transacciones = [
            Transaccion(**transaccion)
            for transaccion in datos.get("transacciones", [])
        ]
        return Billetera(
            saldo=datos.get("saldo", 0.0),
            tarjetas=tarjetas,
            transacciones=transacciones,
        )

    def billetera_a_json(self, id_usuario, billetera):
        datos = asdict(billetera)
        datos["id_usuario"] = id_usuario
        return datos
