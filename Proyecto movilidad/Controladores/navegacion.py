"""Controlador simple para manejar el flujo entre pantallas."""

import tkinter as tk

from Vistas.billetera import VistaBilletera
from Vistas.inicio_sesion import VistaInicioSesion
from Vistas.menu import VistaMenu
from Vistas.pantalla_inicial import VistaPantallaInicial
from Vistas.registro import VistaRegistro
from Vistas.viaje import VistaViaje
from Repositorios.repositorio_billetera import RepositorioBilletera
from Repositorios.repositorio_usuario import RepositorioUsuario
from Servicios.Usuario.autenticacion import ServicioAutenticacion
from Servicios.Usuario.buscador import BuscadorUsuario
from Servicios.Usuario.registro import ServicioRegistro
from Modelos.Billetera.tarjetas import ServicioTarjeta
from Servicios.Billetera.servicio_billetera import ServicioBilletera
from Servicios.Viajes.servicio_viaje import ServicioViaje
from Controladores.controlador_iniciosesion import ControladorInicioSesion
from Controladores.controlador_registro import ControladorRegistro
from Controladores.controlador_billetera import ControladorBilletera
from Controladores.controlador_viaje import (
    ControladorViajeConductor,
    ControladorViajePasajero,
)
from abstracciones import NavegadorAbstracto, RutaNavegacion

class Navegacion:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Movilidad")
        self.ventana.geometry("1000x720")
        self.ventana.minsize(760, 620)
        self.ventana.attributes("-fullscreen", True)
        self.usuario_actual = None
        self.repositorio_usuario = RepositorioUsuario()
        self.repositorio_billetera = RepositorioBilletera()
        self.buscador_usuario = BuscadorUsuario(self.repositorio_usuario)
        self.servicio_autenticacion = ServicioAutenticacion(
            self.repositorio_usuario,
            self.buscador_usuario,
        )
        self.servicio_registro = ServicioRegistro(
            self.repositorio_usuario,
            self.buscador_usuario,
        )
        self.servicio_tarjeta = ServicioTarjeta(self.repositorio_billetera)
        self.servicio_billetera = ServicioBilletera(
            self.repositorio_billetera,
            self.servicio_tarjeta,
        )
        self.servicio_viaje = ServicioViaje(
            servicio_billetera=self.servicio_billetera,
        )

        self.controlador_inicio_sesion = ControladorInicioSesion(
            self.servicio_autenticacion,
        )
        self.controlador_registro = ControladorRegistro(
            self.servicio_registro
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
        self.navegador = NavegadorRutas(self)

    def iniciar(self):
        self.navegar("pantalla_inicial")
        self.ventana.mainloop()

    def navegar(self, destino):
        self.navegador.navegar(destino)

    def establecer_usuario_actual(self, usuario):
        self.servicio_billetera.obtener_billetera(usuario)
        self.usuario_actual = usuario
        return self.usuario_actual

    def obtener_usuario_actual(self):
        return self.usuario_actual

    def obtener_tipo_usuario(self):
        if self.usuario_actual is None:
            return "pasajero"

        return getattr(self.usuario_actual, "tipo_usuario", "pasajero")

class RutaPantallaInicial(RutaNavegacion):
    destino = "pantalla_inicial"

    def ejecutar(self):
        self.mostrar(VistaPantallaInicial, "Movilidad")


class RutaInicioSesion(RutaNavegacion):
    destino = "inicio_sesion"

    def ejecutar(self):
        self.limpiar_pantalla()
        self.navegacion.ventana.title("Inicio de sesion")
        VistaInicioSesion(
            self.navegacion.ventana,
            self.navegacion.navegar,
            self.navegacion.controlador_inicio_sesion,
            self.inicio_sesion_exitoso,
        )

    def inicio_sesion_exitoso(self, usuario):
        self.navegacion.establecer_usuario_actual(usuario)
        self.navegacion.navegar("menu")


class RutaRegistro(RutaNavegacion):
    destino = "registro"

    def ejecutar(self):
        self.limpiar_pantalla()
        self.navegacion.ventana.title("Registro")
        VistaRegistro(
            self.navegacion.ventana,
            self.navegacion.navegar,
            self.navegacion.controlador_registro,
            self.registro_exitoso,
        )

    def registro_exitoso(self, usuario):
        self.navegacion.establecer_usuario_actual(usuario)
        self.navegacion.navegar("menu")


class RutaMenu(RutaNavegacion):
    destino = "menu"

    def ejecutar(self):
        self.mostrar(VistaMenu, "Menu principal")


class RutaBilletera(RutaNavegacion):
    destino = "billetera"

    def ejecutar(self):
        self.limpiar_pantalla()
        self.navegacion.ventana.title("Billetera virtual")
        vista = VistaBilletera(
            self.navegacion.ventana,
            self.navegacion.navegar,
        )
        self.navegacion.controlador_billetera.conectar_vista(
            vista,
            self.navegacion.obtener_usuario_actual(),
        )


class RutaViaje(RutaNavegacion):
    destino = "viaje"

    def ejecutar(self):
        self.limpiar_pantalla()
        self.navegacion.ventana.title("Viaje")
        VistaViaje(
            self.navegacion.ventana,
            self.navegacion.navegar,
            self.navegacion.obtener_tipo_usuario(),
            lambda: self.navegacion.navegar("menu"),
            self.navegacion.controlador_viaje_pasajero,
            self.navegacion.controlador_viaje_conductor,
            self.navegacion.obtener_usuario_actual(),
        )


class RutaSalir(RutaNavegacion):
    destino = "salir"

    def ejecutar(self):
        self.navegacion.ventana.destroy()


class NavegadorRutas(NavegadorAbstracto):
    def __init__(self, navegacion):
        self.rutas = {
            ruta.destino: ruta(navegacion)
            for ruta in RutaNavegacion.rutas_registradas
        }

    def navegar(self, destino):
        ruta = self.rutas.get(destino)
        if ruta is not None:
            ruta.ejecutar()


