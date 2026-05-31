"""Controlador simple para manejar el flujo entre pantallas."""

import tkinter as tk

from Vistas.billetera import VistaBilletera
from Vistas.inicio_sesion import VistaInicioSesion
from Vistas.menu import VistaMenu
from Vistas.pantalla_inicial import VistaPantallaInicial
from Vistas.registro import VistaRegistro


class Navegacion:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Movilidad")
        self.ventana.geometry("1000x720")
        self.ventana.minsize(760, 620)
        self.ventana.attributes("-fullscreen", True)

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
        self.mostrar(
            VistaInicioSesion,
            "Inicio de sesion",
        )

    def mostrar_registro(self):
        self.mostrar(
            VistaRegistro,
            "Registro",
        )

    def mostrar_menu(self):
        self.mostrar(
            VistaMenu,
            "Menu principal",
        )

    def mostrar_billetera(self):
        self.mostrar(
            VistaBilletera,
            "Billetera virtual",
        )

    def salir(self):
        self.ventana.destroy()
