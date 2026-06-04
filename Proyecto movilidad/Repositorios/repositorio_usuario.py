from pathlib import Path
from dataclasses import asdict

from Modelos.Usuario.usuario_datos import Auto, Conductor, Pasajero, Usuario
from Repositorios.repositorio_json import cargar_json, guardar_json
from Servicios.Usuario.fabrica_usuario import FabricaUsuario
from Servicios.Usuario.generador_id import GeneradorID

class RepositorioUsuario:

    def __init__(self, archivo=None, fabrica=None, convertidor=None):
        archivo = (
            archivo
            or Path(__file__).resolve().parents[1] / "usuarios.json"
        )
        self.archivo = archivo
        self.fabrica = fabrica or FabricaUsuario()
        self.convertidor = convertidor or ConvertidorUsuario()
        self.usuarios = []
        self.cargado = False

    def cargar(self):
        self.usuarios = [
            self.convertidor.desde_json(datos)
            for datos in cargar_json(self.archivo)
        ]
        GeneradorID.sincronizar_desde_usuarios(self.usuarios)
        self.cargado = True
        return self.usuarios

    def guardar(self):
        guardar_json(
            self.archivo,
            [
                self.convertidor.a_json(usuario)
                for usuario in self.usuarios
            ]
        )
        self.cargado = True

    def agregar(self, usuario):
        if not self.cargado:
            self.cargar()

        self.usuarios.append(usuario)
        self.guardar()
        return usuario

    def listar(self):
        if not self.cargado:
            self.cargar()

        return self.usuarios
class ConvertidorUsuario:

    def desde_json(self, datos):
        tipo = datos.get("tipo_usuario", "usuario")
        datos_usuario = {
            clave: valor
            for clave, valor in datos.items()
            if clave not in ("billetera", "tipo_usuario")
        }

        if tipo == "conductor":
            datos_usuario["auto"] = Auto(**datos_usuario["auto"])
            return Conductor(**datos_usuario)

        if tipo == "pasajero":
            return Pasajero(**datos_usuario)

        return Usuario(**datos_usuario)

    def a_json(self, usuario):
        datos = asdict(usuario)
        datos.pop("billetera", None)
        datos["tipo_usuario"] = getattr(usuario, "tipo_usuario", "usuario")
        return datos