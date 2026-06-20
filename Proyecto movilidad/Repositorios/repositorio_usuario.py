from pathlib import Path
from dataclasses import asdict

from Repositorios.repositorio_json import cargar_json, guardar_json
from Servicios.Usuario.fabrica_usuario import FabricaUsuario
from Servicios.Usuario.generador_id import GeneradorID


class RepositorioUsuario:

    def __init__(self, archivo=None, fabrica=None):
        archivo = (
            archivo
            or Path(__file__).resolve().parents[1] / "usuarios.json"
        )
        self.archivo = archivo
        self.fabrica = fabrica or FabricaUsuario()
        self.usuarios = []

    def cargar(self):
        self.usuarios = [
            self.fabrica.crear_desde_dict(datos)
            for datos in cargar_json(self.archivo)
        ]
        GeneradorID.sincronizar_desde_usuarios(self.usuarios)
        return self.usuarios

    def guardar(self):
        guardar_json(
            self.archivo,
            [
                self.usuario_a_json(usuario)
                for usuario in self.usuarios
            ]
        )

    def agregar(self, usuario):
        self.cargar()
        self.usuarios.append(usuario)
        self.guardar()
        return usuario

    def listar(self):
        #PATRÓN DE DISEÑO: lazy initialization
        #Leer el disco duro (el archivo JSON) es una operación 
        # costosa para el procesador. El patrón de Inicialización Perezosa retrasa 
        # esta acción pesada hasta el último momento posible, es decir, hasta que 
        # alguien realmente necesite ver la lista. Si 'self.usuarios' ya tiene datos, 
        # se salta la lectura y devuelve la memoria caché (RAM), optimizando el sistema.
        if not self.usuarios:
            self.cargar()

        return self.usuarios

    def usuario_a_json(self, usuario):
        datos = asdict(usuario)
        datos.pop("billetera", None)
        datos["tipo_usuario"] = getattr(usuario, "tipo_usuario", "usuario")
        return datos
#.
