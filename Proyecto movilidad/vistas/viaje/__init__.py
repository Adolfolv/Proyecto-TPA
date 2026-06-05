import tkinter as tk

from ..estilizacion import tema
from .viaje_conductor import VistaViajeConductor
from .viaje_pasajero import VistaViajePasajero


class VistaViaje(tk.Frame):
    def __init__(
        self,
        padre,
        navegar,
        tipo_usuario,
        comando_volver_menu,
        controlador_pasajero,
        controlador_conductor,
        usuario_actual,
    ):
        super().__init__(padre, bg=tema.FONDO)
        self.pack(fill="both", expand=True)

        if tipo_usuario == "conductor":
            VistaViajeConductor(
                self,
                navegar,
                comando_volver_menu,
                controlador_conductor,
                usuario_actual,
            )
            return

        VistaViajePasajero(
            self,
            navegar,
            comando_volver_menu,
            controlador_pasajero,
            usuario_actual,
        )
