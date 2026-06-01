from pathlib import Path

from Modelos.Viaje.modelo_viajes import CuentaViajes, Viaje
from Repositorios.repositorio_json import RepositorioJSONGenerico


class PersistenciaUsuarioViajes:

    def __init__(self, archivo=None):
        archivo = (
            archivo
            or Path(__file__).resolve().parents[2] / "viajes.json"
        )
        self.repo = RepositorioJSONGenerico(
            archivo,
            CuentaViajes,
        )
        self.cuentas = self._cargar()

    def _cargar(self):
        cuentas = []
        for datos in self.repo.cargar_json():
            viajes = [
                self._crear_viaje(viaje)
                for viaje in datos.get("viajes", [])
            ]
            cuentas.append(
                CuentaViajes(
                    id_usuario=datos.get("id_usuario", ""),
                    tipo_usuario=datos.get("tipo_usuario", ""),
                    viajes=viajes,
                )
            )
        return cuentas

    def _crear_viaje(self, datos):
        return Viaje(
            pasajero=datos.get("pasajero", datos.get("usuario", "")),
            conductor=datos.get("conductor", ""),
            vehiculo=datos.get("vehiculo", ""),
            precio=float(datos.get("precio", 0)),
            distancia=float(datos.get("distancia", 0)),
            duracion=float(datos.get("duracion", 0)),
        )

    def guardar_viaje(self, usuario, viaje):
        cuenta = self.buscar_o_crear_cuenta(usuario)
        cuenta.viajes.append(viaje)
        self.guardar()
        return viaje

    def buscar_o_crear_cuenta(self, usuario):
        id_usuario = str(getattr(usuario, "id_usuario", ""))
        tipo_usuario = getattr(usuario, "tipo_usuario", "")

        for cuenta in self.cuentas:
            if str(cuenta.id_usuario) == id_usuario:
                cuenta.tipo_usuario = tipo_usuario
                return cuenta

        cuenta = CuentaViajes(
            id_usuario=id_usuario,
            tipo_usuario=tipo_usuario,
            viajes=[],
        )
        self.cuentas.append(cuenta)
        return cuenta

    def listar_cuentas(self):
        return self.cuentas

    def guardar(self):
        self.repo.guardar_json(self.cuentas)
