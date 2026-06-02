"""Controlador simple para manejar el flujo entre pantallas."""

import tkinter as tk
from abc import ABC, abstractmethod

from vistas.billetera import VistaBilletera
from vistas.inicio_sesion import VistaInicioSesion
from vistas.menu import VistaMenu
from vistas.pantalla_inicial import VistaPantallaInicial
from vistas.registro import VistaRegistro
from vistas.viaje import VistaViaje
from Servicios.Usuario.autenticacion import ServicioAutenticacion
from Servicios.Usuario.registro import ServicioRegistro
from Servicios.Usuario.servicio_usuario import ServicioUsuario
from Servicios.Billetera.servicio_billetera import ServicioBilletera
from Servicios.Viajes.servicio_viaje import ServicioViaje
from Controladores.controlador_iniciosesion import ControladorInicioSesion
from Controladores.controlador_registro import ControladorRegistro
from Controladores.controlador_billetera import ControladorBilletera
from Controladores.controlador_viaje import ControladorViaje

class Navegacion:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Movilidad")
        self.ventana.geometry("1000x720")
        self.ventana.minsize(760, 620)
        self.ventana.attributes("-fullscreen", True)
        self.servicio_usuario = ServicioUsuario()
        self.servicio_registro = ServicioRegistro(self.servicio_usuario)
        self.servicio_autenticacion = ServicioAutenticacion(self.servicio_usuario)
        self.servicio_billetera = ServicioBilletera(self.servicio_usuario)
        self.servicio_viaje = ServicioViaje()
        self.usuario_actual = None

        self.controlador_inicio_sesion = ControladorInicioSesion(
            self.servicio_autenticacion,
        )
        self.controlador_registro = ControladorRegistro(
            self.servicio_registro
        )
        self.controlador_billetera = ControladorBilletera(
            self.servicio_billetera,
        )
        self.controlador_viaje = ControladorViaje(
            self.servicio_viaje,
            self.servicio_billetera,
        )
        self.navegador = NavegadorRutas(self)

    def iniciar(self):
        self.navegar("pantalla_inicial")
        self.ventana.mainloop()

    def limpiar_pantalla(self):
        for widget in self.ventana.winfo_children():
            widget.destroy()
    def navegar(self, destino):
        self.navegador.navegar(destino)

    def obtener_tipo_usuario(self):
        usuario = self.obtener_usuario_actual()

        if usuario is None:
            return "pasajero"

        return getattr(usuario, "tipo_usuario", "pasajero")

    def obtener_usuario_actual(self):
        if self.usuario_actual is not None:
            return self.usuario_actual

        usuarios = self.servicio_usuario.listar_usuarios()
        self.usuario_actual = usuarios[0] if usuarios else None
        return self.usuario_actual


class NavegadorAbstracto(ABC):
    @abstractmethod
    def navegar(self, destino):
        pass


class RutaNavegacion(ABC):
    rutas_registradas = []
    destino = ""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.destino:
            RutaNavegacion.rutas_registradas.append(cls)

    def __init__(self, navegacion):
        self.navegacion = navegacion

    def mostrar(self, vista, titulo):
        self.navegacion.limpiar_pantalla()
        self.navegacion.ventana.title(titulo)
        vista(self.navegacion.ventana, self.navegacion.navegar)

    @abstractmethod
    def ejecutar(self):
        pass


class RutaPantallaInicial(RutaNavegacion):
    destino = "pantalla_inicial"

    def ejecutar(self):
        self.mostrar(VistaPantallaInicial, "Movilidad")


class RutaInicioSesion(RutaNavegacion):
    destino = "inicio_sesion"

    def ejecutar(self):
        self.navegacion.limpiar_pantalla()
        self.navegacion.ventana.title("Inicio de sesion")
        VistaInicioSesion(
            self.navegacion.ventana,
            self.navegacion.navegar,
            self.navegacion.controlador_inicio_sesion,
            self.inicio_sesion_exitoso,
        )

    def inicio_sesion_exitoso(self, usuario):
        self.navegacion.usuario_actual = usuario
        self.navegacion.navegar("menu")


class RutaRegistro(RutaNavegacion):
    destino = "registro"

    def ejecutar(self):
        self.navegacion.limpiar_pantalla()
        self.navegacion.ventana.title("Registro")
        VistaRegistro(
            self.navegacion.ventana,
            self.navegacion.navegar,
            self.navegacion.controlador_registro,
            self.registro_exitoso,
        )

    def registro_exitoso(self, usuario):
        self.navegacion.usuario_actual = usuario
        self.navegacion.navegar("menu")


class RutaMenu(RutaNavegacion):
    destino = "menu"

    def ejecutar(self):
        self.mostrar(VistaMenu, "Menu principal")


class RutaBilletera(RutaNavegacion):
    destino = "billetera"

    def ejecutar(self):
        self.navegacion.limpiar_pantalla()
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
        self.navegacion.limpiar_pantalla()
        self.navegacion.ventana.title("Viaje")
        VistaViaje(
            self.navegacion.ventana,
            self.navegacion.navegar,
            self.navegacion.obtener_tipo_usuario(),
            lambda: self.navegacion.navegar("menu"),
            self.navegacion.controlador_viaje,
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


