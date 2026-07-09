"""Pantalla de inicio de sesion."""

import tkinter as tk

from .estilizacion import tema
from .estilizacion.decoraciones import crear_panel_mensaje
from .estilizacion.widgets import Moldes


class VistaInicioSesion(tk.Frame):
    def __init__(self, padre, navegar, controlador, al_iniciar=None):
        self.navegar = navegar
        self.controlador = controlador
        self.al_iniciar = al_iniciar
        self.moldes = Moldes()
        self.mostrar_contrasena = tk.BooleanVar(padre, value=False)


        super().__init__(padre, bg=tema.FONDO)
        self.pack(fill="both", expand=True)
        self.crear_widgets()

    def crear_widgets(self):
        panel = self.moldes.crear_frame(
            self,
            tema.PANEL,
            tema.BORDE,
            1,
            38,
            34,
            relx=0.5,
            rely=0.5,
            ancla="center",
            ancho=640,
            alto=520,
        )
        panel.grid_columnconfigure(0, weight=1)
        boton_volver = self.moldes.crear_boton(
            panel,
            "Volver",
            False,
            None,
            lambda: self.navegar("pantalla_inicial"),
        )
        boton_volver.configure(font=tema.FUENTE_BOTON, padx=12, pady=6)
        boton_volver.place(relx=1.0, x=-24, y=0, anchor="ne", width=120, height=36)

        self.moldes.crear_label(
            panel,
            "Iniciar sesión",
            tema.FUENTE_LOGIN_TITULO,
            tema.TEXTO,
            tema.PANEL,
        ).grid(row=0, column=0, sticky="w", padx=24, pady=(0, 6))
        self.moldes.crear_label(
            panel,
            "Ingresa tus datos para continuar",
            tema.FUENTE_LOGIN_TEXTO,
            tema.TEXTO_SUAVE,
            tema.PANEL,
            560,
            "left",
        ).grid(row=1, column=0, sticky="w", padx=24, pady=(0, 36))
        self.moldes.crear_label(
            panel,
            "Correo",
            tema.FUENTE_LOGIN_CAMPO,
            tema.TEXTO,
            tema.PANEL,
        ).grid(row=2, column=0, sticky="w", padx=24, pady=(0, 8))
        self.entrada_correo = self.moldes.crear_entrada(panel)
        self.entrada_correo.configure(font=tema.FUENTE_LOGIN_ENTRADA)
        self.entrada_correo.grid(row=3, column=0, sticky="ew", padx=24, pady=(0, 22), ipady=9)
        self.moldes.crear_label(
            panel,
            "Contraseña",
            tema.FUENTE_LOGIN_CAMPO,
            tema.TEXTO,
            tema.PANEL,
        ).grid(row=4, column=0, sticky="w", padx=24, pady=(0, 8))
        self.entrada_contrasena = self.moldes.crear_entrada(panel, mostrar="*")
        self.entrada_contrasena.configure(font=tema.FUENTE_LOGIN_ENTRADA)
        self.entrada_contrasena.grid(row=5, column=0, sticky="ew", padx=24, pady=(0, 18), ipady=9)
        tk.Checkbutton(
            panel,
            text="Mostrar contraseña",
            variable=self.mostrar_contrasena,
            command=self.actualizar_visibilidad_contrasena,
            bg=tema.PANEL,
            fg=tema.TEXTO,
            activebackground=tema.PANEL,
            activeforeground=tema.TEXTO,
            selectcolor=tema.PANEL,
            cursor="hand2",
            font=tema.FUENTE_LOGIN_TEXTO,
        ).grid(row=6, column=0, sticky="w", padx=24, pady=(0, 24))
        boton_inicio = self.moldes.crear_boton(
            panel,
            "Iniciar sesión",
            True,
            16,
            self.iniciar_sesion,
        )
        boton_inicio.configure(font=tema.FUENTE_LOGIN_BOTON, padx=14, pady=8)
        boton_inicio.grid(row=7, column=0, pady=(0, 12))
        area_mensaje = self.moldes.crear_frame(
            panel,
            tema.PANEL,
            fila=8,
            columna=0,
            sticky="ew",
            margen_x=14,
            margen_y=(0, 4),
        )
        self.mostrar_mensaje = crear_panel_mensaje(area_mensaje)

    def actualizar_visibilidad_contrasena(self):
        if self.entrada_contrasena is not None:
            self.entrada_contrasena.config(show="" if self.mostrar_contrasena.get() else "*")

    def iniciar_sesion(self):
        resultado = self.controlador.iniciar_sesion(
            self.entrada_correo.get(),
            self.entrada_contrasena.get(),
        )

        if resultado.error == "bloqueada":
            self.mostrar_mensaje("Esta cuenta está bloqueada.")
            return

        if not resultado.exitoso:
            self.mostrar_mensaje("Revisa este dato: correo o contraseña incorrectos.")
            return

        if self.al_iniciar is not None:
            self.al_iniciar(resultado.usuario)
