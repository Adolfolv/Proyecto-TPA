# Clase para generar IDs únicos para los usuarios, con un formato específico..
class GeneradorID:

    contador = 0

    @classmethod
    def sincronizar_desde_usuarios(cls, usuarios):
        mayor = cls.contador

        for usuario in usuarios:
            id_usuario = str(usuario.id_usuario)
            if id_usuario.startswith("USR") and id_usuario[3:].isdigit():
                mayor = max(mayor, int(id_usuario[3:]))
            elif id_usuario.isdigit():
                mayor = max(mayor, int(id_usuario))

        cls.contador = mayor

    @classmethod
    def generar(cls, prefijo="ID"):
        cls.contador += 1
        return f"{prefijo}{cls.contador:04}"
    
