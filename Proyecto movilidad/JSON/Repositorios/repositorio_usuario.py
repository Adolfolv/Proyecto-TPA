from dataclasses import asdict

from JSON.rutas import ARCHIVO_USUARIOS
from Modelos.Usuario.usuario_datos import (
    Administrador,
    Auto,
    Conductor,
    Pasajero,
    Usuario,
)
from JSON.Repositorios.repositorio_json import cargar_json, guardar_json


class RepositorioUsuario:

    def __init__(self, archivo=None, convertidor=None):
        self.archivo = archivo or ARCHIVO_USUARIOS
        self.convertidor = convertidor or ConvertidorUsuario()

    def _escribir_usuarios(self, usuarios):
        guardar_json(
            self.archivo,
            {
                "usuarios": [
                    self.convertidor.a_dict(usuario)
                    for usuario in usuarios
                ]
            },
        )

    def _leer_usuarios(self):
        documento = cargar_json(self.archivo)
        if not isinstance(documento, dict):
            raise ValueError("El archivo de usuarios debe contener un objeto.")

        return [
            self.convertidor.desde_dict(datos)
            for datos in documento.get("usuarios", [])
        ]

    def agregar(self, usuario):
        usuarios = self.listar()
        usuarios.append(usuario)
        self._escribir_usuarios(usuarios)
        return usuario

    def listar(self):
        return self._leer_usuarios()

    def actualizar(self, usuario_actualizado):
        usuarios = self.listar()
        for indice, usuario in enumerate(usuarios):
            if str(usuario.id_usuario) == str(usuario_actualizado.id_usuario):
                usuarios[indice] = usuario_actualizado
                self._escribir_usuarios(usuarios)
                return usuario_actualizado

        return None

    def eliminar_por_id(self, id_usuario):
        # Elimina el usuario del repositorio y vuelve a guardar usuarios.json.
        # La validacion de permisos queda en ServicioAdmin.
        usuarios = self.listar()
        usuarios_restantes = [
            usuario
            for usuario in usuarios
            if str(usuario.id_usuario) != str(id_usuario)
        ]

        if len(usuarios_restantes) == len(usuarios):
            return False

        self._escribir_usuarios(usuarios_restantes)
        return True


class ConvertidorUsuario:

    def desde_dict(self, datos):
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

        # Permite reconstruir usuarios administradores desde usuarios.json.
        # Esta conversion es necesaria para que el login pueda distinguirlos
        # y redirigirlos luego al panel de administracion.
        if tipo == "administrador":
            return Administrador(**datos_usuario)

        return Usuario(**datos_usuario)

    def a_dict(self, usuario):
        datos = asdict(usuario)
        datos.pop("billetera", None)
        datos["tipo_usuario"] = getattr(usuario, "tipo_usuario", "usuario")
        return datos
