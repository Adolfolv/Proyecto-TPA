from Validaciones.perfil import ValidacionesPerfil


class ServicioPerfil:
    """Caso de uso para consultar y actualizar datos editables del perfil."""

    CAMPOS_EDITABLES = ("nombre", "apellido", "correo", "telefono")

    def __init__(self, repositorio_usuario, buscador_usuario_por_correo):
        self.repositorio_usuario = repositorio_usuario
        self.validaciones_perfil = ValidacionesPerfil(buscador_usuario_por_correo)

    def obtener_perfil(self, usuario):
        if usuario is None:
            raise ValueError("No hay usuario activo.")

        return self._datos_perfil(usuario)

    def actualizar_perfil(self, usuario, datos):
        if usuario is None:
            raise ValueError("No hay usuario activo.")

        datos_actualizados = {
            campo: str(datos.get(campo, "")).strip()
            for campo in self.CAMPOS_EDITABLES
        }
        self.validaciones_perfil.validar(usuario, datos_actualizados)

        for campo, valor in datos_actualizados.items():
            setattr(usuario, campo, valor)

        imagen = str(datos.get("imagen", self._imagen_perfil(usuario)) or "").strip()
        usuario.imagen = imagen

        usuario_actualizado = self.repositorio_usuario.actualizar(usuario)
        if usuario_actualizado is None:
            raise ValueError("No se encontró el usuario para actualizar.")
        return self._datos_perfil(usuario_actualizado)

    def _datos_perfil(self, usuario):
        return {
            "nombre": getattr(usuario, "nombre", ""),
            "apellido": getattr(usuario, "apellido", ""),
            "correo": getattr(usuario, "correo", ""),
            "telefono": getattr(usuario, "telefono", ""),
            "tipo_usuario": getattr(usuario, "tipo_usuario", "usuario"),
            "imagen": self._imagen_perfil(usuario),
        }

    @staticmethod
    def _imagen_perfil(usuario):
        return getattr(usuario, "imagen", "") or getattr(usuario, "selfie", "")
