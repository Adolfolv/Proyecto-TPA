from pathlib import Path

from JSON.repositorio import RepositorioJSONGenerico
from Modelos.modelo_Usuario.generador_de_usuario import GeneradorID
from modelo_Usuario.usuario_datos import Usuario, Pasajero, Conductor, Auto
from Modelos.Billetera.datos_billetera import Billetera, Tarjetas, Transaccion

#Esta es la unica responsable de manejar los datos de los usuarios, cargar, guardar, buscar, etc. Solo esta interactua con el repositorio JSON, 
# el resto de la app interactua con esta clase para obtener o modificar datos de los usuarios. 
# Es la unica que conoce la estructura del JSON y como convertirlo a objetos Usuario, Pasajero o Conductor.
#Si necesitas guardar algo llama la funcion desde aqui

#IMPORTANTE: ESTAS CLASE SE BASO EN LA IMPLEMENTACION DE DATACLASSES, SI SE HACE ALGUNA MODIFICACION EN LAS CLASES DE USUARIOS, BILLETERA, TARJETAS O TRANSACCIONES, 
# HAY QUE MODIFICAR ESTA CLASE PARA QUE PUEDA CARGAR Y GUARDAR LOS DATOS CORRECTAMENTE.

class ServicioUsuario:
    """
    Responsable de la persistencia de usuarios.

    - Cargar usuarios.
    - Guardar usuarios.
    - Buscar usuarios.
    - Reconstruir objetos desde JSON.
    """

    def __init__(self, archivo=None):
        archivo = (
            archivo
            or Path(__file__).resolve().parents[2] / "usuarios.json"
        )

        self.repo = RepositorioJSONGenerico(
            archivo,
            Usuario,
        )

        self.usuarios = self._cargar()

    def _cargar(self):
        usuarios = [
            self._crear_usuario(datos)
            for datos in self.repo.cargar_json()
        ]

        GeneradorID.sincronizar_desde_usuarios(
            usuarios
        )

        return usuarios

    def _crear_usuario(self, datos):
        billetera = self._crear_billetera(
            datos.get("billetera", {})
        )

        tipo = datos.get("tipo_usuario", "usuario")

        datos_usuario = {
            clave: valor
            for clave, valor in datos.items()
            if clave not in (
                "billetera",
                "tipo_usuario",
            )
        }
        datos_usuario.setdefault("apellido", "")

        if tipo == "conductor":

            auto = datos_usuario.get("auto")

            if isinstance(auto, dict):
                datos_usuario["auto"] = Auto(**auto)
            usuario = Conductor(**datos_usuario)

        elif tipo == "pasajero":
            usuario = Pasajero(**datos_usuario)

        else:
            usuario = Usuario(**datos_usuario)
        usuario.billetera = billetera
        return usuario

    def _crear_billetera(self, datos):
        tarjetas = [
            Tarjetas(**tarjeta)
            for tarjeta in datos.get(
                "tarjetas",
                [],
            )
        ]

        transacciones = [
            Transaccion(**transaccion)
            for transaccion in datos.get(
                "transacciones",
                [],
            )
        ]

        return Billetera(saldo=datos.get("saldo", 0.0),
            tarjetas=tarjetas,
            transacciones=transacciones,
        )

    def buscar_usuario(self, id_usuario):
        for usuario in self.usuarios:

            if (str(usuario.id_usuario)== str(id_usuario)):
                return usuario

        return None

    def buscar_por_correo(self, correo):
        correo_normalizado = (correo.strip().lower())
        for usuario in self.usuarios:

            if (usuario.correo.strip().lower()== correo_normalizado):
                return usuario

        return None

    def agregar(self, usuario):
        self.usuarios.append(usuario)
        self.guardar()
        return usuario

    def listar_usuarios(self):
        return self.usuarios

    def guardar(self):
        self.repo.guardar_json(
            self.usuarios
        )
    
