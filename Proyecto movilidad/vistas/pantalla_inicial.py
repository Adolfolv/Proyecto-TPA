"""Pantalla inicial visual sin navegacion."""

import tkinter as tk

from estilizacion import tema
from estilizacion.widgets import Moldes


class VistaPantallaInicial(tk.Frame):
    def __init__(self):
        ventana = tk.Tk()
        ventana.title("Movilidad")
        ventana.geometry("720x520")
        ventana.minsize(620, 460)
        ventana.attributes("-fullscreen", True)

        self.moldes = Moldes()

        super().__init__(ventana, bg=tema.FONDO)
        self.pack(fill="both", expand=True)
        self.crear_widgets()

    def crear_widgets(self):
        panel_central = self.moldes.crear_frame(self, tema.PANEL, tema.BORDE, 1, 28, 24, relx=0.5, rely=0.5, ancla="center", ancho=560, alto=430)

        barra_superior = self.moldes.crear_frame(panel_central, tema.PANEL, llenar="x")
        self.moldes.crear_boton(barra_superior, "Tema", lado="left", margen_x=4)
        self.moldes.crear_boton(barra_superior, "Salir", lado="right", margen_x=4)
        self.moldes.crear_label(panel_central, "Bienvenido a Movilidad", tema.FUENTE_TITULO, tema.TEXTO, tema.PANEL, margen_y=(34, 10))
        self.moldes.crear_label(panel_central, "Gestiona tus viajes, tu perfil y tu billetera desde una sola pantalla.", tema.FUENTE_TEXTO, tema.TEXTO_SUAVE, tema.PANEL, 430, "center", margen_y=(0, 22))
        self.moldes.crear_label(panel_central, "Accesos disponibles", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL, margen_y=(0, 8))
        self.moldes.crear_boton(panel_central, "Registrarse", True, 28, margen_y=6)
        self.moldes.crear_boton(panel_central, "Iniciar Sesion", False, 28, margen_y=6)
        self.moldes.crear_boton(panel_central, "Ayuda", False, 28, margen_y=6)
        self.moldes.crear_label(panel_central, "Selecciona una opcion para continuar.", tema.FUENTE_TEXTO, tema.TEXTO_SUAVE, tema.PANEL, 430, "center", lado="bottom", margen_y=(10, 2))

    def ejecutar(self):
        self.master.mainloop()


if __name__ == "__main__":
    VistaPantallaInicial().ejecutar()
