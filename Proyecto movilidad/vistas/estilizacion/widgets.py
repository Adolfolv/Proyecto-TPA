"""Moldes de widgets comunes para las vistas..."""

import tkinter as tk
from tkinter import ttk

from . import tema


class Moldes:
    def configurar_selectores(self, ventana):
        estilo = ttk.Style(ventana)
        estilo.theme_use("clam")
        estilo.configure(
            "Selector.TCombobox",
            fieldbackground=tema.SECUNDARIO,
            background=tema.SECUNDARIO,
            foreground=tema.TEXTO,
            arrowcolor=tema.TEXTO,
            bordercolor=tema.BORDE,
            lightcolor=tema.BORDE,
            darkcolor=tema.BORDE,
            selectbackground=tema.SECUNDARIO,
            selectforeground=tema.TEXTO,
        )
        estilo.map(
            "Selector.TCombobox",
            fieldbackground=[
                ("disabled", tema.SECUNDARIO),
                ("readonly", tema.SECUNDARIO),
                ("active", tema.SECUNDARIO),
                ("focus", tema.SECUNDARIO),
            ],
            background=[
                ("disabled", tema.SECUNDARIO),
                ("readonly", tema.SECUNDARIO),
                ("active", tema.SECUNDARIO),
                ("focus", tema.SECUNDARIO),
            ],
            foreground=[
                ("disabled", tema.TEXTO_SUAVE),
                ("readonly", tema.TEXTO),
                ("active", tema.TEXTO),
                ("focus", tema.TEXTO),
            ],
            arrowcolor=[
                ("disabled", tema.TEXTO_SUAVE),
                ("readonly", tema.TEXTO),
                ("active", tema.TEXTO),
                ("focus", tema.TEXTO),
            ],
        )
        ventana.option_add("*TCombobox*Listbox.background", tema.SECUNDARIO)
        ventana.option_add("*TCombobox*Listbox.foreground", tema.TEXTO)
        ventana.option_add("*TCombobox*Listbox.selectBackground", tema.PRIMARIO)
        ventana.option_add("*TCombobox*Listbox.selectForeground", tema.PRIMARIO_TEXTO)

    def ubicar(self, widget, metodo=None, fila=None, columna=None, columnas=1, margen_x=None, margen_y=None, **opciones):
        if metodo == "grid":
            if fila is not None:
                opciones["row"] = fila
            if columna is not None:
                opciones["column"] = columna
            if columnas != 1:
                opciones["columnspan"] = columnas
            if margen_x is not None:
                opciones["padx"] = margen_x
            if margen_y is not None:
                opciones["pady"] = margen_y
            widget.grid(**opciones)
        elif metodo == "pack":
            if margen_x is not None:
                opciones["padx"] = margen_x
            if margen_y is not None:
                opciones["pady"] = margen_y
            widget.pack(**opciones)
        elif metodo == "place":
            widget.place(**opciones)
        return widget

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
        fila=None,
        columna=None,
        columnas=1,
        sticky="nsew",
        columnas_peso=None,
        filas_peso=None,
        metodo=None,
        **ubicacion,
    ):
        panel = tk.Frame(
            padre,
            bg=color,
            width=ancho_fijo,
            height=alto_fijo,
            highlightbackground=borde,
            highlightthickness=grosor_borde,
            padx=relleno_x,
            pady=relleno_y,
        )

        if metodo is None and fila is None and relx is None and (llenar or expandir or lado or margen_x or margen_y):
            panel.pack(fill=llenar, expand=expandir, side=lado, padx=margen_x, pady=margen_y)

        if relx is not None and rely is not None:
            panel.place(relx=relx, rely=rely, anchor=ancla, width=ancho, height=alto)

        if fila is not None and columna is not None:
            panel.grid(row=fila, column=columna, columnspan=columnas, sticky=sticky, padx=margen_x, pady=margen_y)

        if metodo is not None:
            self.ubicar(panel, metodo, margen_x=margen_x, margen_y=margen_y, **ubicacion)

        for indice, peso in (columnas_peso or ()):
            panel.grid_columnconfigure(indice, weight=peso)

        for indice, peso in (filas_peso or ()):
            panel.grid_rowconfigure(indice, weight=peso)

        return panel

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
        metodo=None,
        **ubicacion,
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

        if metodo is None and (llenar or expandir or lado or margen_x or margen_y):
            label.pack(fill=llenar, expand=expandir, side=lado, padx=margen_x, pady=margen_y)

        if metodo is not None:
            self.ubicar(label, metodo, margen_x=margen_x, margen_y=margen_y, **ubicacion)

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
        metodo=None,
        **ubicacion,
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

        if metodo is None and (llenar or expandir or lado or margen_x or margen_y):
            boton.pack(fill=llenar, expand=expandir, side=lado, padx=margen_x, pady=margen_y)

        if metodo is not None:
            self.ubicar(boton, metodo, margen_x=margen_x, margen_y=margen_y, **ubicacion)

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
        metodo=None,
        **ubicacion,
    ):
        entrada = tk.Entry(
            padre,
            width=ancho,
            show=mostrar,
            font=tema.FUENTE_TEXTO,
            bg=tema.SECUNDARIO,
            fg=tema.TEXTO,
            insertbackground=tema.TEXTO,
            disabledbackground=tema.SECUNDARIO,
            disabledforeground=tema.TEXTO_SUAVE,
            relief="flat",
            bd=0,
        )

        if metodo is None and (llenar or expandir or lado or margen_x or margen_y):
            entrada.pack(fill=llenar, expand=expandir, side=lado, padx=margen_x, pady=margen_y, ipady=7)

        if metodo is not None:
            self.ubicar(entrada, metodo, margen_x=margen_x, margen_y=margen_y, **ubicacion)

        return entrada

    def crear_selector(self, padre, opciones, metodo=None, margen_x=0, margen_y=0, **ubicacion):
        self.configurar_selectores(padre.winfo_toplevel())
        selector = ttk.Combobox(padre, values=opciones, state="readonly", font=tema.FUENTE_TEXTO, style="Selector.TCombobox")
        selector.current(0)
        if metodo is not None:
            self.ubicar(selector, metodo, margen_x=margen_x, margen_y=margen_y, **ubicacion)
        return selector

    def crear_tabla(self, padre, columnas, alto=5, metodo=None, margen_x=0, margen_y=0, **ubicacion):
        estilo = ttk.Style(padre)
        estilo.theme_use("clam")
        estilo.configure("Tabla.Treeview", background=tema.SECUNDARIO, fieldbackground=tema.SECUNDARIO, foreground=tema.TEXTO, rowheight=28, bordercolor=tema.BORDE, lightcolor=tema.BORDE, darkcolor=tema.BORDE, relief="flat")
        estilo.configure("Tabla.Treeview.Heading", background=tema.PANEL_SUAVE, foreground=tema.TEXTO, bordercolor=tema.BORDE, lightcolor=tema.BORDE, darkcolor=tema.BORDE, font=("Arial", 9, "bold"), relief="flat")
        estilo.map("Tabla.Treeview", background=[("selected", tema.PRIMARIO), ("!selected", tema.SECUNDARIO)], fieldbackground=[("!selected", tema.SECUNDARIO)], foreground=[("selected", tema.PRIMARIO_TEXTO), ("!selected", tema.TEXTO)])
        estilo.map("Tabla.Treeview.Heading", background=[("active", tema.PANEL_SUAVE), ("!active", tema.PANEL_SUAVE)], foreground=[("active", tema.TEXTO), ("!active", tema.TEXTO)])
        tabla = ttk.Treeview(padre, columns=tuple(columna[0] for columna in columnas), show="headings", style="Tabla.Treeview", height=alto)
        for clave, texto, ancho in columnas:
            tabla.heading(clave, text=texto)
            tabla.column(clave, width=ancho, anchor="center", stretch=True)
        if metodo is not None:
            self.ubicar(tabla, metodo, margen_x=margen_x, margen_y=margen_y, **ubicacion)
        return tabla

    def crear_scroll_tematico(self, padre, contenido):
        scroll = tk.Scrollbar(
            padre,
            orient="vertical",
            command=contenido.yview,
            bg=tema.SECUNDARIO,
            activebackground=tema.PRIMARIO,
            troughcolor=tema.PANEL,
            highlightbackground=tema.BORDE,
            highlightcolor=tema.BORDE,
            relief="flat",
            bd=0,
            width=12,
            elementborderwidth=0,
            cursor="hand2",
        )
        contenido.configure(yscrollcommand=scroll.set)
        return scroll

    @staticmethod
    def habilitar_rueda(contenido, *componentes):
        def desplazar(evento):
            if getattr(evento, "num", None) in (4, 5):
                unidades = -1 if evento.num == 4 else 1
            else:
                delta = getattr(evento, "delta", 0)
                unidades = -int(delta / 120) if abs(delta) >= 120 else (-1 if delta > 0 else 1)
            contenido.yview_scroll(unidades, "units")
            return "break"

        for componente in (contenido,) + componentes:
            componente.bind("<MouseWheel>", desplazar)
            componente.bind("<Button-4>", desplazar)
            componente.bind("<Button-5>", desplazar)

    @staticmethod
    def sincronizar_tabla(tabla, filas):
        """Actualiza un Treeview conservando las filas existentes."""
        existentes = set(tabla.get_children())
        for iid in existentes - set(filas):
            tabla.delete(iid)
        for posicion, (iid, valores) in enumerate(filas.items()):
            if iid in existentes:
                if tuple(tabla.item(iid, "values")) != tuple(str(valor) for valor in valores):
                    tabla.item(iid, values=valores)
                tabla.move(iid, "", posicion)
            else:
                tabla.insert("", "end", iid=iid, values=valores)

    def crear_tarjeta_acceso_menu(self, padre, titulo, descripcion, comando=None, metodo=None, margen_x=0, margen_y=0, **ubicacion):
        tarjeta = self.crear_frame(padre, tema.PANEL_SUAVE, tema.BORDE, 1, 16, 16)
        self.crear_label(tarjeta, titulo, tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE).pack(anchor="w")
        self.crear_label(tarjeta, descripcion, tema.FUENTE_TEXTO, tema.TEXTO_SUAVE, tema.PANEL_SUAVE, 260, "left").pack(anchor="w", fill="x", pady=(8, 18))
        self.crear_boton(tarjeta, "Abrir", False, 14, comando).pack(anchor="w", side="bottom")
        if metodo is not None:
            self.ubicar(tarjeta, metodo, margen_x=margen_x, margen_y=margen_y, **ubicacion)
        return tarjeta
