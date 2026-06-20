from Validaciones.registro import (
    ValidadorApellido,
    ValidadorCorreo,
    ValidadorNombre,
    ValidadorTelefono,
)


class ValidadorCorreoPerfil:
    def __init__(self, buscador_usuario_por_correo):
        self.buscador_usuario_por_correo = buscador_usuario_por_correo

    def validar(self, usuario, correo):
        usuario_encontrado = self.buscador_usuario_por_correo.buscar(correo)
        if usuario_encontrado is None:
            return True

        if str(usuario_encontrado.id_usuario) == str(usuario.id_usuario):
            return True

        raise ValueError("El correo ya se encuentra registrado.")


class ValidacionesPerfil:
    def __init__(self, buscador_usuario_por_correo):
        self.validador_nombre = ValidadorNombre()
        self.validador_apellido = ValidadorApellido()
        self.validador_correo = ValidadorCorreo()
        self.validador_telefono = ValidadorTelefono()
        self.validador_correo_perfil = ValidadorCorreoPerfil(
            buscador_usuario_por_correo
        )

    def validar(self, usuario, datos):
        self.validador_nombre.validar(datos["nombre"])
        self.validador_apellido.validar(datos["apellido"])
        self.validador_correo.validar(datos["correo"])
        self.validador_telefono.validar(datos["telefono"])
        self.validador_correo_perfil.validar(usuario, datos["correo"])
        return True
