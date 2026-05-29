
from JSON import Json_utilidades
from modelo_Usuario.usuario_datos import Usuario

class GeneradorID:

    contador = 0
    @classmethod
    def generar(cls, prefijo="ID"):
        cls.contador += 1
        return f"{prefijo}{cls.contador:04}"
    
class agregar_usuario:

    def __init__(self, archivo="usuarios.json"):
        self.archivo = archivo

    def agregar(self, usuario):

        datos = Json_utilidades.cargar_json(self.archivo)
        usuarios = [
            Usuario(**u)
            for u in datos
        ]
        usuarios.append(usuario)
        Json_utilidades.guardar_json(self.archivo, usuarios)