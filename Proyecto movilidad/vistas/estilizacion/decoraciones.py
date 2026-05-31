"""Decoraciones visuales reutilizables."""

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
