"""Decoraciones visuales reutilizables.."""

import tkinter as tk

from . import tema


# --- DECORACION REGISTRO ---
def crear_panel_mensaje_registro(padre, compacto=False):
    alto = 42 if compacto else 58
    fuente = ("Arial", 9, "bold") if compacto else tema.FUENTE_BOTON
    wrap = 430 if compacto else 720

    contenedor = tk.Frame(
        padre,
        bg=tema.PANEL_SUAVE,
        highlightbackground=tema.BORDE,
        highlightthickness=1,
        height=alto,
    )
    etiqueta = tk.Label(
        contenedor,
        text="",
        font=fuente,
        fg=tema.TEXTO,
        bg=tema.PANEL_SUAVE,
        wraplength=wrap,
        justify="left",
    )
    etiqueta.pack(fill="both", expand=True, padx=12, pady=8)

    margen_y = (6, 0) if compacto else (10, 0)

    def mostrar(texto, exito=False):
        fondo = tema.EXITO_FONDO if exito else tema.ERROR_FONDO
        borde = tema.EXITO if exito else tema.ERROR

        contenedor.configure(bg=fondo, highlightbackground=borde)
        etiqueta.configure(text=texto, bg=fondo, fg=tema.TEXTO)

        if not contenedor.winfo_manager():
            contenedor.pack(fill="x", padx=10, pady=margen_y)

    return mostrar


def crear_panel_confirmacion_admin(padre, fila=0):
    contenedor = tk.Frame(
        padre,
        bg=tema.ERROR_FONDO,
        highlightbackground=tema.ERROR,
        highlightthickness=1,
        height=58,
    )
    contenedor.grid_columnconfigure(0, weight=1)

    etiqueta = tk.Label(
        contenedor,
        text="",
        font=tema.FUENTE_BOTON,
        fg=tema.TEXTO,
        bg=tema.ERROR_FONDO,
        wraplength=720,
        justify="left",
    )
    etiqueta.grid(row=0, column=0, sticky="ew", padx=12, pady=8)

    acciones = tk.Frame(contenedor, bg=tema.ERROR_FONDO)
    acciones.grid(row=0, column=1, sticky="e", padx=(0, 10), pady=8)

    def ocultar():
        if contenedor.winfo_manager():
            contenedor.grid_remove()

    def mostrar(texto, comando_confirmar):
        etiqueta.configure(text=texto)

        for widget in acciones.winfo_children():
            widget.destroy()

        tk.Button(
            acciones,
            text="Confirmar",
            font=tema.FUENTE_BOTON,
            bg=tema.ERROR,
            fg=tema.PRIMARIO_TEXTO,
            activebackground=tema.ERROR,
            activeforeground=tema.PRIMARIO_TEXTO,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=12,
            pady=8,
            command=lambda: (ocultar(), comando_confirmar()),
        ).pack(side="left", padx=(0, 8))
        tk.Button(
            acciones,
            text="Cancelar",
            font=tema.FUENTE_BOTON,
            bg=tema.SECUNDARIO,
            fg=tema.TEXTO,
            activebackground=tema.SECUNDARIO,
            activeforeground=tema.TEXTO,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=12,
            pady=8,
            command=ocultar,
        ).pack(side="left")

        if not contenedor.winfo_manager():
            contenedor.grid(row=fila, column=0, sticky="ew", pady=(8, 0))

    return mostrar


# --- DECORACION MENU ---
def crear_decoracion_menu_viaje(padre, comando=None, metodo=None, margen_x=0, margen_y=0, **ubicacion):
    canvas = tk.Canvas(padre, bg=tema.PANEL, bd=0, highlightthickness=0, cursor="hand2")

    def dibujar(evento=None):
        canvas.delete("all")
        ancho = max(canvas.winfo_width(), 1)
        alto = max(canvas.winfo_height(), 1)
        centro_x = ancho / 2
        centro_y = alto / 2
        radio = min(ancho, alto, 260) / 2
        canvas.create_oval(centro_x - radio * 1.55, centro_y - radio * 1.55, centro_x + radio * 1.55, centro_y + radio * 1.55, outline=tema.BORDE, width=1)
        canvas.create_oval(centro_x - radio * 1.18, centro_y - radio * 1.18, centro_x + radio * 1.18, centro_y + radio * 1.18, outline=tema.PRIMARIO, width=2)
        canvas.create_line(centro_x - radio * 1.7, centro_y - radio * 0.25, centro_x - radio * 1.2, centro_y - radio * 0.75, centro_x - radio * 0.6, centro_y - radio * 0.55, smooth=True, fill=tema.BORDE, width=2)
        canvas.create_line(centro_x + radio * 1.7, centro_y + radio * 0.25, centro_x + radio * 1.2, centro_y + radio * 0.75, centro_x + radio * 0.6, centro_y + radio * 0.55, smooth=True, fill=tema.BORDE, width=2)
        canvas.create_oval(centro_x - radio, centro_y - radio, centro_x + radio, centro_y + radio, fill=tema.PRIMARIO, outline=tema.PRIMARIO_TEXTO, width=3, tags="boton_viaje")
        canvas.create_text(centro_x, centro_y, text="Iniciar\nviaje", fill=tema.PRIMARIO_TEXTO, font=("Arial", 18, "bold"), justify="center", tags="boton_viaje")

    canvas.bind("<Configure>", dibujar)
    if comando is not None:
        canvas.tag_bind("boton_viaje", "<Button-1>", lambda evento: comando())
    if metodo == "grid":
        canvas.grid(padx=margen_x, pady=margen_y, **ubicacion)
    elif metodo == "pack":
        canvas.pack(padx=margen_x, pady=margen_y, **ubicacion)
    elif metodo == "place":
        canvas.place(**ubicacion)
    return canvas


# --- DECORACION ADMIN ---
def crear_logo_admin(padre, tipo, color, fondo):
    canvas = tk.Canvas(padre, width=150, height=120, bg=fondo, bd=0, highlightthickness=0)
    canvas.create_oval(42, 12, 108, 78, fill=color, outline="")
    canvas.create_arc(26, 54, 124, 138, start=0, extent=180, style="pieslice", fill=color, outline="")

    if tipo == "pasajero":
        canvas.create_line(47, 91, 103, 91, fill=tema.ADMIN_ACENTO_TEXTO, width=5, capstyle="round")
        canvas.create_oval(34, 82, 52, 100, fill=tema.ADMIN_ACENTO_TEXTO, outline="")
        canvas.create_oval(98, 82, 116, 100, fill=tema.ADMIN_ACENTO_TEXTO, outline="")
    elif tipo == "conductor":
        canvas.create_rectangle(38, 83, 112, 100, fill=tema.ADMIN_ACENTO_TEXTO, outline="")
        canvas.create_rectangle(50, 70, 100, 86, fill=tema.ADMIN_ACENTO_TEXTO, outline="")
        canvas.create_oval(43, 94, 59, 110, fill=fondo, outline="")
        canvas.create_oval(91, 94, 107, 110, fill=fondo, outline="")
    else:
        canvas.create_rectangle(61, 75, 89, 108, fill=tema.ADMIN_ACENTO_TEXTO, outline="")
        canvas.create_oval(56, 64, 94, 102, outline=tema.ADMIN_ACENTO_TEXTO, width=6)
        canvas.create_text(75, 91, text="A", fill=color, font=("Arial", 20, "bold"))

    return canvas
