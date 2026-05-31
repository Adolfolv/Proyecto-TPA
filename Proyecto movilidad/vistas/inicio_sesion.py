"""Pantalla de inicio de sesion visual sin navegacion real."""

import tkinter as tk

from .estilizacion import tema
from .estilizacion.widgets import Moldes


class VistaInicioSesion(tk.Frame):
    def __init__(self, master, navegar):
        self.navegar = navegar
        self.moldes = Moldes()
        self.mostrar_contrasena = tk.BooleanVar(master=master, value=False)
        self.entrada_contrasena = None
        self.mensaje = tk.StringVar(master=master, value="")

        super().__init__(master, bg=tema.FONDO)
        self.pack(fill="both", expand=True)
        self.crear_widgets()

    def crear_widgets(self):
        panel = self.moldes.crear_frame(self, tema.PANEL, tema.BORDE, 1, 38, 34, relx=0.5, rely=0.5, ancla="center", ancho=640, alto=500)
        panel.grid_columnconfigure(0, weight=1)
        boton_volver = self.moldes.crear_boton(panel, "Volver", False, None, lambda: self.navegar("pantalla_inicial"))
        boton_volver.configure(font=tema.FUENTE_BOTON, padx=12, pady=6)
        boton_volver.place(relx=1.0, x=-24, y=0, anchor="ne", width=120, height=36)

        self.moldes.crear_label(panel, "Iniciar sesion", tema.FUENTE_LOGIN_TITULO, tema.TEXTO, tema.PANEL).grid(row=0, column=0, sticky="w", padx=24, pady=(0, 6))
        self.moldes.crear_label(panel, "Ingresa tus datos para continuar", tema.FUENTE_LOGIN_TEXTO, tema.TEXTO_SUAVE, tema.PANEL, 560, "left").grid(row=1, column=0, sticky="w", padx=24, pady=(0, 36))
        self.moldes.crear_label(panel, "Correo", tema.FUENTE_LOGIN_CAMPO, tema.TEXTO, tema.PANEL).grid(row=2, column=0, sticky="w", padx=24, pady=(0, 8))
        entrada_correo = self.moldes.crear_entrada(panel)
        entrada_correo.configure(font=tema.FUENTE_LOGIN_ENTRADA)
        entrada_correo.grid(row=3, column=0, sticky="ew", padx=24, pady=(0, 22), ipady=9)
        self.moldes.crear_label(panel, "Contrasena", tema.FUENTE_LOGIN_CAMPO, tema.TEXTO, tema.PANEL).grid(row=4, column=0, sticky="w", padx=24, pady=(0, 8))
        self.entrada_contrasena = self.moldes.crear_entrada(panel, mostrar="*")
        self.entrada_contrasena.configure(font=tema.FUENTE_LOGIN_ENTRADA)
        self.entrada_contrasena.grid(row=5, column=0, sticky="ew", padx=24, pady=(0, 18), ipady=9)
        tk.Checkbutton(panel, text="Mostrar contrasena", variable=self.mostrar_contrasena, command=self.actualizar_visibilidad_contrasena, bg=tema.PANEL, fg=tema.TEXTO, activebackground=tema.PANEL, activeforeground=tema.TEXTO, selectcolor=tema.PANEL, cursor="hand2", font=tema.FUENTE_LOGIN_TEXTO).grid(row=6, column=0, sticky="w", padx=24, pady=(0, 24))
        boton_inicio = self.moldes.crear_boton(panel, "Iniciar sesion", True, 16, lambda: self.navegar("menu"))
        boton_inicio.configure(font=tema.FUENTE_LOGIN_BOTON, padx=14, pady=8)
        boton_inicio.grid(row=7, column=0, pady=(0, 14))
        self.moldes.crear_label(panel, "", tema.FUENTE_LOGIN_TEXTO, tema.TEXTO_SUAVE, tema.PANEL, 460, "center").grid(row=8, column=0, pady=(0, 4))

    def actualizar_visibilidad_contrasena(self):
        if self.entrada_contrasena is not None:
            self.entrada_contrasena.config(show="" if self.mostrar_contrasena.get() else "*")
