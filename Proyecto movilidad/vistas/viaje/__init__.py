import tkinter as tk

from ..estilizacion import tema
from .viaje_conductor import VistaViajeConductor
from .viaje_pasajero import VistaViajePasajero


class VistaViaje(tk.Frame):
    def __init__(self, master, navegar, tipo_usuario, comando_volver_menu, controlador_viaje, usuario_actual):
        super().__init__(master, bg=tema.FONDO)
        self.pack(fill="both", expand=True)

        if tipo_usuario == "conductor":
            VistaViajeConductor(
                self,
                navegar,
                comando_volver_menu,
                controlador_viaje,
                usuario_actual,
            )
            return

        VistaViajePasajero(
            self,
            navegar,
            comando_volver_menu,
            controlador_viaje,
            usuario_actual,
        )
