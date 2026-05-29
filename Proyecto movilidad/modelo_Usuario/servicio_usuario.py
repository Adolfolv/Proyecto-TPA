from JSON.repositorio import RepositorioJSONGenerico
from modelo_Usuario.usuario_datos import Usuario, Pasajero, Conductor, Auto


class ServicioUsuario:

    def __init__(self, archivo="usuarios.json"):
        self.repo = RepositorioJSONGenerico(archivo, Usuario)
        self.usuarios = self._cargar()

    def _cargar(self):
        datos = self.repo.cargar_json()
        usuarios = []

        for u in datos:
            tipo = u.get("tipo_usuario", "usuario")
            if tipo == "conductor":
                if "auto" in u and isinstance(u["auto"], dict):
                    u["auto"] = Auto(**u["auto"])
                usuarios.append(Conductor(**u))

            elif tipo == "pasajero":
                usuarios.append(Pasajero(**u))

            else:
                usuarios.append(Usuario(**u))

        return usuarios

    def buscar_usuario(self, id_usuario: int):
        for u in self.usuarios:
            if u.id_usuario == id_usuario:
                return u
        return None

    def agregar_usuario(self, usuario):
        self.usuarios.append(usuario)
        self.repo.guardar_json(self.usuarios)  
        return usuario

    def listar_usuarios(self):
        return self.usuarios
    
    def guardar(self):
        self.repo.guardar_json(self.usuarios)
    
