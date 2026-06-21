import tkinter as tk

from ..estilizacion import tema
from .conductor.vista_suscripcion_conductor import VistaSuscripcionConductor
from .pasajero.vista_suscripcion_pasajero import VistaSuscripcionPasajero


class VistaSuscripcionViaje(tk.Frame):
    """Enruta la seccion de suscripciones segun el rol autenticado."""

    def __init__(
        self,
        padre,
        navegar,
        tipo_usuario,
        controlador_pasajero,
        controlador_conductor,
        usuario_actual,
    ):
        super().__init__(padre, bg=tema.FONDO)
        self.pack(fill="both", expand=True)
        if tipo_usuario == "conductor":
            VistaSuscripcionConductor(
                self, navegar, controlador_conductor, usuario_actual
            )
            return
        VistaSuscripcionPasajero(
            self, navegar, controlador_pasajero, usuario_actual
        )


__all__ = ["VistaSuscripcionViaje"]
