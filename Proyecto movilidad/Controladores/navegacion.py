"""Controlador simple para manejar el flujo entre pantallas."""

import tkinter as tk

from Vistas.billetera import VistaBilletera
from Vistas.inicio_sesion import VistaInicioSesion
from Vistas.menu import VistaMenu
from Vistas.pantalla_inicial import VistaPantallaInicial
from Vistas.registro import VistaRegistro
from Vistas.viaje import VistaViaje
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
        self.servicio_billetera = ServicioBilletera()
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
            self.servicio_usuario,
        )
        self.controlador_viaje = ControladorViaje(
            self.servicio_viaje,
        )

    def iniciar(self):
        self.mostrar_pantalla_inicial()
        self.ventana.mainloop()

    def limpiar_pantalla(self):
        for widget in self.ventana.winfo_children():
            widget.destroy()
    #redirige a la pantalla correspondiente segun el destino solicitado
    def navegar(self, destino):
        if destino == "pantalla_inicial":
            self.mostrar_pantalla_inicial()
        elif destino == "inicio_sesion":
            self.mostrar_inicio_sesion()
        elif destino == "registro":
            self.mostrar_registro()
        elif destino == "menu":
            self.mostrar_menu()
        elif destino == "billetera":
            self.mostrar_billetera()
        elif destino == "viaje":
            self.mostrar_viaje()
        elif destino == "salir":
            self.salir()

    def mostrar(self, vista, titulo):
        self.limpiar_pantalla()
        self.ventana.title(titulo)
        vista(self.ventana, self.navegar)

    def mostrar_pantalla_inicial(self):
        self.mostrar(
            VistaPantallaInicial,
            "Movilidad",
        )

    def mostrar_inicio_sesion(self):
        self.limpiar_pantalla()
        self.ventana.title("Inicio de sesion")
        VistaInicioSesion(
            self.ventana,
            self.navegar,
            self.controlador_inicio_sesion,
            self.inicio_sesion_exitoso,
        )

    def mostrar_registro(self):
        self.limpiar_pantalla()
        self.ventana.title("Registro")
        VistaRegistro(
            self.ventana,
            self.navegar,
            self.controlador_registro,
            self.registro_exitoso,
        )

    def registro_exitoso(self, usuario):
        self.usuario_actual = usuario
        self.mostrar_menu()

    def inicio_sesion_exitoso(self, usuario):
        self.usuario_actual = usuario
        self.mostrar_menu()

    def mostrar_menu(self):
        self.mostrar(
            VistaMenu,
            "Menu principal",
        )

    def mostrar_billetera(self):
        self.limpiar_pantalla()
        self.ventana.title("Billetera virtual")
        vista = VistaBilletera(
            self.ventana,
            self.navegar,
        )
        self.controlador_billetera.conectar_vista(
            vista,
            self.obtener_usuario_actual(),
        )

    def mostrar_viaje(self):
        tipo_usuario = self.obtener_tipo_usuario()
        self.limpiar_pantalla()
        self.ventana.title("Viaje")
        VistaViaje(
            self.ventana,
            self.navegar,
            tipo_usuario,
            self.volver_menu,
            self.controlador_viaje,
            self.obtener_usuario_actual(),
        )

    def volver_menu(self):
        self.mostrar_menu()

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


    def salir(self):
        self.ventana.destroy()
