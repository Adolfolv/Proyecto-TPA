from abstracciones import Buscador


class BuscadorUsuario(Buscador):

    def __init__(self, repositorio_usuario):
        self.repositorio_usuario = repositorio_usuario

    def buscar(self, id_usuario):
        for usuario in self.repositorio_usuario.listar():
            if str(usuario.id_usuario) == str(id_usuario):
                return usuario

        return None


class BuscadorUsuarioPorCorreo(Buscador):
    def __init__(self, repositorio_usuario):
            self.repositorio_usuario = repositorio_usuario

    def buscar(self, correo):
        correo_normalizado = correo.strip().lower()

        for usuario in self.repositorio_usuario.listar():
            if usuario.correo.strip().lower() == correo_normalizado:
                return usuario

        return None
    
class BuscadorTarjeta(Buscador):

    def buscar(self, usuario, numero_tarjeta):
        for tarjeta in usuario.billetera.tarjetas:
            if tarjeta.numero_tarjeta == numero_tarjeta:
                return tarjeta

        return None

