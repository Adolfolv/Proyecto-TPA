"""Pantalla inicial visual sin navegación..."""

import tkinter as tk

from .estilizacion import tema
from .estilizacion.widgets import Moldes


class VistaPantallaInicial(tk.Frame):
    def __init__(self, padre, navegar):
        self.navegar = navegar
        self.moldes = Moldes()

        super().__init__(padre, bg=tema.FONDO)
        self.pack(fill="both", expand=True)
        self.crear_widgets()

    def cambiar_tema(self):
        # FLUJO TEMA 1: Lo llama el boton "Tema" de esta pantalla.
        # Siguiente paso: tema.alternar_tema() en vistas/estilizacion/tema.py.
        tema.alternar_tema()

        # FLUJO TEMA 3: Despues del cambio, vuelve a navegacion.py para
        # reconstruir VistaPantallaInicial con las constantes nuevas.
        self.navegar("pantalla_inicial")

    def crear_widgets(self):
        panel_central = self.moldes.crear_frame(self, tema.PANEL, tema.BORDE, 1, 28, 24, relx=0.5, rely=0.5, ancla="center", ancho=560, alto=430)

        barra_superior = self.moldes.crear_frame(panel_central, tema.PANEL, llenar="x")
        self.moldes.crear_boton(barra_superior, tema.texto_boton(), comando=self.cambiar_tema, lado="left", margen_x=4)
        self.moldes.crear_boton(barra_superior, "Salir", comando=lambda: self.navegar("salir"), lado="right", margen_x=4)
        self.moldes.crear_label(panel_central, "Bienvenido a Movilidad", tema.FUENTE_TITULO, tema.TEXTO, tema.PANEL, margen_y=(34, 10))
        self.moldes.crear_label(panel_central, "Gestiona tus viajes, tu perfil y tu billetera desde una sola pantalla.", tema.FUENTE_TEXTO, tema.TEXTO_SUAVE, tema.PANEL, 430, "center", margen_y=(0, 22))
        self.moldes.crear_label(panel_central, "Accesos disponibles", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL, margen_y=(0, 8))
        self.moldes.crear_boton(panel_central, "Registrarse", True, 28, lambda: self.navegar("registro"), margen_y=6)
        self.moldes.crear_boton(panel_central, "Iniciar sesión", False, 28, lambda: self.navegar("inicio_sesion"), margen_y=6)
        self.moldes.crear_boton(panel_central, "Ayuda", False, 28, margen_y=6)
        self.moldes.crear_label(panel_central, "Selecciona una opción para continuar.", tema.FUENTE_TEXTO, tema.TEXTO_SUAVE, tema.PANEL, 430, "center", lado="bottom", margen_y=(10, 2))
