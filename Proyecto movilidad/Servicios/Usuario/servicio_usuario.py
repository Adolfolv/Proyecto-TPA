from pathlib import Path
from dataclasses import asdict

from Repositorios.repositorio_json import cargar_json, guardar_json
from Servicios.Usuario.generador_id import GeneradorID
from Modelos.Usuario.usuario_datos import Usuario, Pasajero, Conductor, Auto


class ServicioUsuario:
    """
    Responsable de usuarios.

    - Cargar usuarios.
    - Guardar usuarios.
    - Buscar usuarios.
    - Reconstruir datos de usuario desde JSON.
    """

    def __init__(self, archivo=None):
        self.archivo = (
            archivo
            or Path(__file__).resolve().parents[2] / "usuarios.json"
        )

        self.usuarios = self._cargar()
        self.usuario_actual = None

    def _cargar(self):
        usuarios = [
            self._crear_usuario(datos)
            for datos in cargar_json(self.archivo)
        ]

        GeneradorID.sincronizar_desde_usuarios(
            usuarios
        )

        return usuarios

    def _crear_usuario(self, datos):
        tipo = datos.get("tipo_usuario", "usuario")

        datos_usuario = {
            clave: valor
            for clave, valor in datos.items()
            if clave not in (
                "billetera",
                "tipo_usuario",
            )
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

    def buscar_usuario(self, id_usuario):
        for usuario in self.usuarios:

            if (str(usuario.id_usuario)== str(id_usuario)):
                return usuario

        return None

    def buscar_por_correo(self, correo):
        correo_normalizado = (correo.strip().lower())
        for usuario in self.usuarios:

            if (usuario.correo.strip().lower()== correo_normalizado):
                return usuario

        return None

    def agregar(self, usuario):
        self.usuarios.append(usuario)
        self.guardar()
        return usuario

    def listar_usuarios(self):
        return self.usuarios

    def establecer_usuario_actual(self, usuario):
        self.usuario_actual = usuario
        return self.usuario_actual

    def obtener_usuario_actual(self, usar_primer_usuario=True):
        if self.usuario_actual is not None:
            return self.usuario_actual

        if not usar_primer_usuario:
            return None

        usuarios = self.listar_usuarios()
        self.usuario_actual = usuarios[0] if usuarios else None
        return self.usuario_actual

    def obtener_tipo_usuario(self):
        usuario = self.obtener_usuario_actual()

        if usuario is None:
            return "pasajero"

        return getattr(usuario, "tipo_usuario", "pasajero")

    def guardar(self):
        guardar_json(self.archivo, [asdict(usuario) for usuario in self.usuarios])
    
