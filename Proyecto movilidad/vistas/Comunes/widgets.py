"""Moldes de widgets comunes para las vistas."""

import tkinter as tk
from tkinter import ttk

from Comunes import tema


class Moldes:
    def configurar_selectores(self, ventana):
        estilo = ttk.Style(ventana)
        estilo.theme_use("clam")
        estilo.configure("Selector.TCombobox", fieldbackground=tema.SECUNDARIO, background=tema.SECUNDARIO, foreground=tema.TEXTO, arrowcolor=tema.TEXTO, bordercolor=tema.BORDE)
        estilo.map("Selector.TCombobox", fieldbackground=[("readonly", tema.SECUNDARIO)], foreground=[("readonly", tema.TEXTO)])
        ventana.option_add("*TCombobox*Listbox.background", tema.SECUNDARIO)
        ventana.option_add("*TCombobox*Listbox.foreground", tema.TEXTO)
        ventana.option_add("*TCombobox*Listbox.selectBackground", tema.PRIMARIO)
        ventana.option_add("*TCombobox*Listbox.selectForeground", tema.PRIMARIO_TEXTO)

    def crear_frame(
        self,
        padre,
        color,
        borde=None,
        grosor_borde=0,
        relleno_x=0,
        relleno_y=0,
        llenar=None,
        expandir=False,
        lado=None,
        margen_x=0,
        margen_y=0,
        relx=None,
        rely=None,
        ancla=None,
        ancho=None,
        alto=None,
        ancho_fijo=None,
        alto_fijo=None,
    ):
        frame = tk.Frame(
            padre,
            bg=color,
            width=ancho_fijo,
            height=alto_fijo,
            highlightbackground=borde,
            highlightthickness=grosor_borde,
            padx=relleno_x,
            pady=relleno_y,
        )

        if llenar or expandir or lado or margen_x or margen_y:
            frame.pack(fill=llenar, expand=expandir, side=lado, padx=margen_x, pady=margen_y)

        if relx is not None and rely is not None:
            frame.place(relx=relx, rely=rely, anchor=ancla, width=ancho, height=alto)

        return frame

    def crear_label(
        self,
        padre,
        texto,
        fuente,
        color,
        fondo,
        ancho_linea=None,
        justificado=None,
        llenar=None,
        expandir=False,
        lado=None,
        margen_x=0,
        margen_y=0,
    ):
        label = tk.Label(
            padre,
            text=texto,
            font=fuente,
            fg=color,
            bg=fondo,
            wraplength=ancho_linea,
            justify=justificado,
        )

        if llenar or expandir or lado or margen_x or margen_y:
            label.pack(fill=llenar, expand=expandir, side=lado, padx=margen_x, pady=margen_y)

        return label

    def crear_boton(
        self,
        padre,
        texto,
        principal=False,
        ancho=None,
        comando=None,
        llenar=None,
        expandir=False,
        lado=None,
        margen_x=0,
        margen_y=0,
    ):
        fondo = tema.SECUNDARIO
        color = tema.TEXTO

        if principal:
            fondo = tema.PRIMARIO
            color = tema.PRIMARIO_TEXTO

        boton = tk.Button(
            padre,
            text=texto,
            font=tema.FUENTE_BOTON,
            width=ancho,
            bg=fondo,
            fg=color,
            activebackground=fondo,
            activeforeground=color,
            relief="flat",
            bd=0,
            command=comando,
            padx=12,
            pady=8,
            cursor="hand2",
        )

        if llenar or expandir or lado or margen_x or margen_y:
            boton.pack(fill=llenar, expand=expandir, side=lado, padx=margen_x, pady=margen_y)

        return boton

    def crear_entrada(
        self,
        padre,
        ancho=None,
        mostrar="",
        llenar=None,
        expandir=False,
        lado=None,
        margen_x=0,
        margen_y=0,
    ):
        entrada = tk.Entry(
            padre,
            width=ancho,
            show=mostrar,
            font=tema.FUENTE_TEXTO,
            bg=tema.SECUNDARIO,
            fg=tema.TEXTO,
            insertbackground=tema.TEXTO,
            relief="flat",
            bd=0,
        )

        if llenar or expandir or lado or margen_x or margen_y:
            entrada.pack(fill=llenar, expand=expandir, side=lado, padx=margen_x, pady=margen_y, ipady=7)

        return entrada

    def crear_selector(self, padre, opciones):
        selector = ttk.Combobox(padre, values=opciones, state="readonly", font=tema.FUENTE_TEXTO, style="Selector.TCombobox")
        selector.current(0)
        return selector

    # --- DECORACIONES ---
  #lucete jorge deidad