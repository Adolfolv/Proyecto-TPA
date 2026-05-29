
from modelo_Usuario.usuario_datos import Usuario

class GeneradorID:

    contador = 0
    @classmethod
    def generar(cls, prefijo="ID"):
        cls.contador += 1
        return f"{prefijo}{cls.contador:04}"
    