"""Construccion de dependencias de la aplicacion."""

from Controladores.controlador_billetera import ControladorBilletera
from Controladores.controlador_iniciosesion import ControladorInicioSesion
from Controladores.controlador_registro import ControladorRegistro
from Controladores.controlador_viaje import (
    ControladorViajeConductor,
    ControladorViajePasajero,
)
from Repositorios.repositorio_billetera import RepositorioBilletera
from Repositorios.repositorio_usuario import RepositorioUsuario
from Servicios.Billetera.operaciones_billetera import (
    OperacionCargaTarjeta,
    OperacionPago,
    OperacionPagoRecibido,
    OperacionRetiroTarjeta,
)
from Servicios.Billetera.fabrica_billetera import FabricaBilletera
from Servicios.Billetera.fabrica_tarjeta import FabricaTarjeta
from Servicios.Billetera.servicio_billetera import ServicioBilletera
from Servicios.Billetera.servicio_tarjetas import ServicioTarjeta
from Servicios.Usuario.autenticacion import ServicioAutenticacion
from Servicios.Usuario.buscador import (
    BuscadorTarjeta,
    BuscadorUsuario,
    BuscadorUsuarioPorCorreo,
)
from Servicios.Usuario.fabrica_usuario import FabricaUsuario
from Servicios.Usuario.registro import ServicioRegistro
from Servicios.Viajes.servicio_viaje import ServicioViaje


class DependenciasAplicacion:
    """Crea y conecta repositorios, servicios y controladores."""

    def __init__(self):
        # Punto de composicion: aqui se decide que implementaciones concretas
        # usa la aplicacion. Si cambia JSON por otra persistencia, se toca aqui.
        self.fabrica_usuario = FabricaUsuario()
        self.fabrica_billetera = FabricaBilletera()
        self.fabrica_tarjeta = FabricaTarjeta()
        self.repositorio_usuario = RepositorioUsuario(fabrica=self.fabrica_usuario)
        self.repositorio_billetera = RepositorioBilletera(
            fabrica=self.fabrica_billetera
        )

        # Buscadores compartidos por servicios de usuario y billetera.
        self.buscador_usuario = BuscadorUsuario(self.repositorio_usuario)
        self.buscador_usuario_por_correo = BuscadorUsuarioPorCorreo(
            self.repositorio_usuario
        )
        self.buscador_tarjeta = BuscadorTarjeta()

        # Servicios: contienen la logica de negocio y dependen de repositorios.
        self.servicio_autenticacion = ServicioAutenticacion(
            self.repositorio_usuario,
            self.buscador_usuario,
        )
        self.servicio_registro = ServicioRegistro(
            self.repositorio_usuario,
            self.buscador_usuario_por_correo,
            self.fabrica_usuario,
        )
        self.servicio_tarjeta = ServicioTarjeta(
            self.repositorio_billetera,
            self.buscador_tarjeta,
            fabrica_tarjeta=self.fabrica_tarjeta,
        )
        self.operaciones_billetera = {
            "pagar": OperacionPago(self.repositorio_billetera),
            "recibir": OperacionPagoRecibido(self.repositorio_billetera),
            "cargar": OperacionCargaTarjeta(
                self.repositorio_billetera,
                self.servicio_tarjeta,
            ),
            "retirar": OperacionRetiroTarjeta(
                self.repositorio_billetera,
                self.servicio_tarjeta,
            ),
        }
        self.servicio_billetera = ServicioBilletera(
            self.repositorio_billetera,
            self.operaciones_billetera,
        )
        self.servicio_viaje = ServicioViaje(
            servicio_billetera=self.servicio_billetera,
        )

        # Controladores: adaptan lo que pide la vista hacia los servicios.
        self.controlador_inicio_sesion = ControladorInicioSesion(
            self.servicio_autenticacion,
        )
        self.controlador_registro = ControladorRegistro(
            self.servicio_registro,
        )
        self.controlador_billetera = ControladorBilletera(
            self.servicio_billetera,
            self.servicio_tarjeta,
        )
        self.controlador_viaje_pasajero = ControladorViajePasajero(
            self.servicio_viaje,
        )
        self.controlador_viaje_conductor = ControladorViajeConductor(
            self.servicio_viaje,
        )
