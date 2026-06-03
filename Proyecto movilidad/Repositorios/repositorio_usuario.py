from pathlib import Path
from dataclasses import asdict

from Modelos.Usuario.usuario_datos import Auto, Conductor, Pasajero, Usuario
from Repositorios.repositorio_json import cargar_json, guardar_json
from Servicios.Usuario.generador_id import GeneradorID


class RepositorioUsuario:

    def __init__(self, archivo=None):
        archivo = (
            archivo
            or Path(__file__).resolve().parents[1] / "usuarios.json"
        )
        self.archivo = archivo
        self.usuarios = []

    def cargar(self):
        self.usuarios = [
            self.crear_usuario(datos)
            for datos in cargar_json(self.archivo)
        ]
        GeneradorID.sincronizar_desde_usuarios(self.usuarios)
        return self.usuarios

    def guardar(self):
        guardar_json(
            self.archivo,
            [
                self.usuario_a_json(usuario)
                for usuario in self.usuarios
            ]
        )

    def agregar(self, usuario):
        self.cargar()
        self.usuarios.append(usuario)
        self.guardar()
        return usuario

    def listar(self):
        if not self.usuarios:
            self.cargar()

        return self.usuarios

    def crear_usuario(self, datos):
        tipo = datos.get("tipo_usuario", "usuario")
        datos_usuario = {
            clave: valor
            for clave, valor in datos.items()
            if clave not in ("billetera", "tipo_usuario")
        }
        datos_usuario.setdefault("apellido", "")

        if tipo == "conductor":
            auto = datos_usuario.get("auto")

            if isinstance(auto, dict):
                datos_usuario["auto"] = Auto(**auto)

            datos_usuario.setdefault("selfie", "")
            usuario = Conductor(**datos_usuario)
        elif tipo == "pasajero":
            usuario = Pasajero(**datos_usuario)
        else:
            usuario = Usuario(**datos_usuario)

        return usuario

    def usuario_a_json(self, usuario):
        datos = asdict(usuario)
        datos.pop("billetera", None)
        datos["tipo_usuario"] = getattr(usuario, "tipo_usuario", "usuario")
        return datos
