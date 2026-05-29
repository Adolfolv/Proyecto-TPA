from JSON.repositorio import RepositorioJSONGenerico
from modelo_Usuario.usuario_datos import Usuario, Pasajero, Conductor, Auto
from generador_de_usuario import GeneradorID  
from Billetera.datos_billetera import Billetera, Tarjetas, Transaccion

#Esta es la unica responsable de manejar los datos de los usuarios, cargar, guardar, buscar, etc. Solo esta interactua con el repositorio JSON, el resto de la app interactua con esta clase para obtener o modificar datos de los usuarios. Es la unica que conoce la estructura del JSON y como convertirlo a objetos Usuario, Pasajero o Conductor.
#Si necesitas guardar algo llama la funcion desde aqui
class ServicioUsuario:

    def __init__(self, archivo="usuarios.json"):
        self.repo = RepositorioJSONGenerico(archivo, Usuario)
        self.usuarios = self._cargar()

    def _cargar(self):
        datos = self.repo.cargar_json()
        usuarios = []

        for u in datos:

            billetera_data = u.get("billetera", {})

            tarjetas = [
                Tarjetas(**t) for t in billetera_data.get("tarjetas", [])
            ]

            transacciones = [
                Transaccion(**tr) for tr in billetera_data.get("transacciones", [])
            ]

            billetera = Billetera(
                saldo=billetera_data.get("saldo", 0.0),
                tarjetas=tarjetas,
                transacciones=transacciones
            )

            tipo = u.get("tipo_usuario", "usuario")
            u_sin_billetera = {k: v for k, v in u.items() if k != "billetera"}

            if tipo == "conductor":

                if "auto" in u_sin_billetera and isinstance(u_sin_billetera["auto"], dict):
                    u_sin_billetera["auto"] = Auto(**u_sin_billetera["auto"])

                usuario = Conductor(**u_sin_billetera)

            elif tipo == "pasajero":
                usuario = Pasajero(**u_sin_billetera)

            else:
                usuario = Usuario(**u_sin_billetera)

            usuario.billetera = billetera

            usuarios.append(usuario)

        return usuarios
    def buscar_usuario(self, id_usuario: int):
        for u in self.usuarios:
            if u.id_usuario == id_usuario:
                return u
        return None

    def agregar_usuario(self, usuario):
        if usuario.id_usuario is None:
            usuario.id_usuario = GeneradorID.generar("USR")
        self.usuarios.append(usuario)
        self.repo.guardar_json(self.usuarios)  
        return usuario

    def listar_usuarios(self):
        return self.usuarios
    
    def guardar(self):
        self.repo.guardar_json(self.usuarios)
    
