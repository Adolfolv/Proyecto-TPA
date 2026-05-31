from abstracciones import Validador


class ValidadorPerfilCargado(Validador):
    def validar(self, valor):
        return valor is not None
