"""Controlador simple para manejar el flujo entre pantallas."""

import tkinter as tk

from Configuracion.dependencias import DependenciasAplicacion
from vistas.billetera import VistaBilletera
from vistas.inicio_sesion import VistaInicioSesion
from vistas.menu import VistaMenu
from vistas.pantalla_inicial import VistaPantallaInicial
from vistas.registro import VistaRegistro
from vistas.viaje import VistaViaje
from abstracciones import NavegadorAbstracto, RutaNavegacion

class Navegacion:
    def __init__(self, dependencias=None):
        self.ventana = tk.Tk()
        self.ventana.title("Movilidad")
        self.ventana.geometry("1000x720")
        self.ventana.minsize(760, 620)
        self.ventana.attributes("-fullscreen", True)
        self.usuario_actual = None
        # Las dependencias concretas se crean fuera de Navegacion para que esta
        # clase se concentre en cambiar pantallas y mantener el usuario actual.
        self.dependencias = dependencias or DependenciasAplicacion()
        self.navegador = NavegadorRutas(self)

    def iniciar(self):
        self.navegar("pantalla_inicial")
        self.ventana.mainloop()

    def navegar(self, destino):
        self.navegador.navegar(destino)

    def establecer_usuario_actual(self, usuario):
        self.dependencias.servicio_billetera.obtener_billetera(usuario)
        self.usuario_actual = usuario
        return self.usuario_actual

    def obtener_usuario_actual(self):
        return self.usuario_actual

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
            self.navegacion.dependencias.controlador_inicio_sesion,
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
            self.navegacion.dependencias.controlador_registro,
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
            self.navegacion.dependencias.controlador_resumen_billetera,
            self.navegacion.dependencias.controlador_tarjetas,
            self.navegacion.dependencias.controlador_movimientos_billetera,
            self.navegacion.obtener_usuario_actual(),
        )

#1, se manda a vistaviaje(archivo init de viajes los datos necesarios
#para cumplir sus funcionalidades 
class RutaViaje(RutaNavegacion):
    destino = "viaje"

    def ejecutar(self):
        self.limpiar_pantalla()
        self.navegacion.ventana.title("Viaje")
        usuario_actual = self.navegacion.obtener_usuario_actual()
        VistaViaje(
            self.navegacion.ventana,
            self.navegacion.navegar,
            usuario_actual.tipo_usuario,
            lambda: self.navegacion.navegar("menu"),
            self.navegacion.dependencias.controlador_viaje_pasajero,
            self.navegacion.dependencias.controlador_viaje_conductor,
            usuario_actual,
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


