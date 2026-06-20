"""Construccion de dependencias de la aplicacion,."""

from Controladores.controlador_billetera import (
    ControladorMovimientosBilletera,
    ControladorResumenBilletera,
    ControladorTarjetas,
)
from Controladores.controlador_admin import ControladorAdmin
from Controladores.controlador_ayuda import ControladorAyuda
from Controladores.controlador_iniciosesion import ControladorInicioSesion
from Controladores.controlador_perfil import ControladorPerfil
from Controladores.controlador_registro import ControladorRegistro
from Controladores.controlador_suscripcion import ControladorSuscripcion
from Controladores.controlador_viaje import (
    ControladorViajeConductor,
    ControladorViajePasajero,
)
from Repositorios.repositorio_billetera import RepositorioBilletera
from Repositorios.repositorio_suscripcion import RepositorioSuscripcion
from Repositorios.repositorio_usuario import RepositorioUsuario
from Servicios.Billetera.operaciones_billetera import (
    OperacionPago,
    OperacionMovimientoTarjeta,
)
from Servicios.Billetera.fabrica_billetera import FabricaBilletera
from Servicios.Billetera.fabrica_tarjeta import FabricaTarjeta
from Servicios.Billetera.servicio_billetera import ServicioBilletera
from Servicios.Billetera.servicio_tarjetas import ServicioTarjeta
from Servicios.Admin.servicio_admin import ServicioAdmin
from Servicios.Ayuda.cliente_gemini import ClienteGemini
from Servicios.Ayuda.contenido_ayuda import ContenidoAyuda
from Servicios.Ayuda.servicio_ayuda import ServicioAyuda
from Servicios.Usuario.autenticacion import ServicioAutenticacion
from Servicios.Usuario.buscador import (
    BuscadorTarjeta,
    BuscadorUsuario,
    BuscadorUsuarioPorCorreo,
)
from Servicios.Usuario.fabrica_usuario import FabricaUsuario
from Servicios.Usuario.perfil import ServicioPerfil
from Servicios.Usuario.registro import ServicioRegistro
from Servicios.Suscripciones.servicio_suscripcion import ServicioSuscripcion
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
        self.repositorio_suscripcion = RepositorioSuscripcion()

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
        self.servicio_perfil = ServicioPerfil(
            self.repositorio_usuario,
            self.buscador_usuario_por_correo,
        )
        # Servicio exclusivo para consultas del panel administrador.
        # Comparte el mismo repositorio de usuarios para no duplicar datos
        # ni alterar el flujo actual de registro, login, billetera o viaje.
        self.servicio_admin = ServicioAdmin(
            self.repositorio_usuario,
        )
        self.contenido_ayuda = ContenidoAyuda()
        self.cliente_gemini = ClienteGemini()
        self.servicio_ayuda = ServicioAyuda(self.contenido_ayuda, self.cliente_gemini)
        
        self.servicio_tarjeta = ServicioTarjeta(
            self.repositorio_billetera,
            self.buscador_tarjeta,
            fabrica_tarjeta=self.fabrica_tarjeta,
        )
        # Patron Strategy/Command: cada clave selecciona una operacion concreta de billetera.
        self.operaciones_billetera = {
            "pagar": OperacionPago(
                self.repositorio_billetera,
                "Pago",
                "pagar",
            ),
            "recibir": OperacionPago(
                self.repositorio_billetera,
                "Pago recibido",
                "recibir_pago",
            ),
            "reembolsar": OperacionPago(
                self.repositorio_billetera,
                "Reembolso suscripcion",
                "recibir_pago",
            ),
            "cargar": OperacionMovimientoTarjeta(
                self.repositorio_billetera,
                self.servicio_tarjeta,
                "Carga desde tarjeta",
            ),
            "retirar": OperacionMovimientoTarjeta(
                self.repositorio_billetera,
                self.servicio_tarjeta,
                "Retiro a tarjeta",
                origen_es_billetera=True,
            ),
        }
        self.servicio_billetera = ServicioBilletera(
            self.repositorio_billetera,
            self.operaciones_billetera,
        )
        self.servicio_viaje = ServicioViaje(
            servicio_billetera=self.servicio_billetera,
        )
        self.servicio_suscripcion = ServicioSuscripcion(
            self.repositorio_suscripcion,
            self.repositorio_usuario,
            self.servicio_viaje,
        )

        # Controladores: adaptan lo que pide la vista hacia los servicios.
        self.controlador_inicio_sesion = ControladorInicioSesion(
            self.servicio_autenticacion,
        )
        self.controlador_registro = ControladorRegistro(
            self.servicio_registro,
        )
        self.controlador_perfil = ControladorPerfil(
            self.servicio_perfil,
        )
        # Controlador del panel admin: evita que la vista llame directo a
        # servicios o repositorios cuando congela/elimina cuentas.
        self.controlador_admin = ControladorAdmin(
            self.servicio_admin,
        )
        self.controlador_ayuda = ControladorAyuda(self.servicio_ayuda)
        self.controlador_resumen_billetera = ControladorResumenBilletera(
            self.servicio_billetera,
        )
        self.controlador_tarjetas = ControladorTarjetas(
            self.servicio_tarjeta,
        )
        self.controlador_movimientos_billetera = ControladorMovimientosBilletera(
            self.servicio_billetera,
        )
        self.controlador_viaje_pasajero = ControladorViajePasajero(
            self.servicio_viaje,
        )
        self.controlador_viaje_conductor = ControladorViajeConductor(
            self.servicio_viaje,
        )
        self.controlador_suscripcion = ControladorSuscripcion(
            self.servicio_suscripcion,
        )
