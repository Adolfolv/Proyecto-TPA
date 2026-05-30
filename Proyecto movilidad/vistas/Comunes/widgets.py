"""Moldes de widgets comunes para las vistas."""

import tkinter as tk
from tkinter import ttk

from Comunes import tema


class Moldes:
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

    def crear_canvas(self, padre, color, llenar=None, expandir=False, lado=None, margen_x=0, margen_y=0):
        canvas = tk.Canvas(padre, bg=color, bd=0, highlightthickness=0, yscrollincrement=24)

        if llenar or expandir or lado or margen_x or margen_y:
            canvas.pack(fill=llenar, expand=expandir, side=lado, padx=margen_x, pady=margen_y)

        return canvas

    def crear_scroll_vertical(self, padre, comando, llenar=None, expandir=False, lado=None, margen_x=0, margen_y=0):
        barra = ttk.Scrollbar(padre, orient="vertical", command=comando)

        if llenar or expandir or lado or margen_x or margen_y:
            barra.pack(fill=llenar, expand=expandir, side=lado, padx=margen_x, pady=margen_y)

        return barra
