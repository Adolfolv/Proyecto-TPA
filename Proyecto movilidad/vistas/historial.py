import tkinter as tk

from .componentes_historial import AccionesHistorial, ConstructorHistorial, RenderizadorHistorial
from .estilizacion import tema
from .estilizacion.widgets import Moldes


class VistaHistorial(tk.Frame):
    """Ensambla los componentes de la pantalla de historial."""

    def __init__(self, padre, navegar, controlador, usuario_actual):
        super().__init__(padre, bg=tema.FONDO)
        self.pack(fill="both", expand=True)
        self.navegar = navegar
        self.controlador = controlador
        self.usuario_actual = usuario_actual
        self.moldes = Moldes()
        self.viajes = ()
        self.viajes_por_item = {}
        self.renderizador = RenderizadorHistorial(self)
        self.acciones = AccionesHistorial(self)
        ConstructorHistorial(self).crear()
        self.acciones.cargar()
