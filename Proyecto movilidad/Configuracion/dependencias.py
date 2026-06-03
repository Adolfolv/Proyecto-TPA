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
from Servicios.Billetera.servicio_billetera import ServicioBilletera
from Servicios.Billetera.servicio_tarjetas import ServicioTarjeta
from Servicios.Usuario.autenticacion import ServicioAutenticacion
from Servicios.Usuario.buscador import BuscadorTarjeta, BuscadorUsuario
from Servicios.Usuario.registro import ServicioRegistro
from Servicios.Viajes.servicio_viaje import ServicioViaje


class DependenciasAplicacion:
    """Crea y conecta repositorios, servicios y controladores."""

    def __init__(self):
        # Punto de composicion: aqui se decide que implementaciones concretas
        # usa la aplicacion. Si cambia JSON por otra persistencia, se toca aqui.
        self.repositorio_usuario = RepositorioUsuario()
        self.repositorio_billetera = RepositorioBilletera()

        # Buscadores compartidos por servicios de usuario y billetera.
        self.buscador_usuario = BuscadorUsuario(self.repositorio_usuario)
        self.buscador_tarjeta = BuscadorTarjeta()

        # Servicios: contienen la logica de negocio y dependen de repositorios.
        self.servicio_autenticacion = ServicioAutenticacion(
            self.repositorio_usuario,
            self.buscador_usuario,
        )
        self.servicio_registro = ServicioRegistro(
            self.repositorio_usuario,
            self.buscador_usuario,
        )
        self.servicio_tarjeta = ServicioTarjeta(
            self.repositorio_billetera,
            self.buscador_tarjeta,
        )
        self.servicio_billetera = ServicioBilletera(
            self.repositorio_billetera,
            self.servicio_tarjeta,
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
