from abstracciones import Buscador
from Validaciones.billetera import normalizar_numero_tarjeta

#-
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

    def buscar(self, origen, numero_tarjeta):
        billetera = getattr(origen, "billetera", origen)
        numero_buscado = normalizar_numero_tarjeta(numero_tarjeta)

        for tarjeta in billetera.tarjetas:
            if normalizar_numero_tarjeta(tarjeta.numero_tarjeta) == numero_buscado:
                return tarjeta

        return None
