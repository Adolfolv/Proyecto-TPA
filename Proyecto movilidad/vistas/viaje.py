"""Pantalla visual de viaje sin navegacion real."""

import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk

from tkintermapview import TkinterMapView

if __package__:
    from .constantes_vistas import CONDUCTORES_DEMO, COORDENADAS_OSORNO, GEOMETRIA_VIAJE, LUGARES_OSORNO, TAMANO_MINIMO_VIAJE, TITULO_VIAJE
    from .estilizacion import tema
    from .estilizacion.widgets import Moldes
else:
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from vistas.constantes_vistas import CONDUCTORES_DEMO, COORDENADAS_OSORNO, GEOMETRIA_VIAJE, LUGARES_OSORNO, TAMANO_MINIMO_VIAJE, TITULO_VIAJE
    from vistas.estilizacion import tema
    from vistas.estilizacion.widgets import Moldes


class VistaViaje(tk.Frame):
    def __init__(self, master, navegar=None):
        self.navegar = navegar
        self.moldes = Moldes()
        self.moldes.configurar_selectores(master)
        self.mapa = None

        super().__init__(master, bg=tema.FONDO)
        self.pack(fill="both", expand=True)
        self.crear_widgets()

    def crear_widgets(self):
        contenedor = self.moldes.crear_frame(self, tema.FONDO, llenar="both", expandir=True, margen_x=20, margen_y=20, columnas_peso=((0, 0), (1, 1)), filas_peso=((0, 1),))
        contenedor.grid_columnconfigure(0, minsize=420)
        contenedor.grid_columnconfigure(1, minsize=640)
        lateral = self.crear_marco(contenedor)
        lateral.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        lateral.grid_columnconfigure(0, weight=1)
        lateral.grid_rowconfigure(0, weight=1)
        mapa = self.crear_marco(contenedor)
        mapa.grid(row=0, column=1, sticky="nsew", padx=(12, 0))
        mapa.grid_columnconfigure(0, weight=1)
        mapa.grid_rowconfigure(1, weight=1)
        self.crear_panel_lateral(lateral)
        self.crear_panel_mapa(mapa)

    def crear_marco(self, padre):
        return self.moldes.crear_frame(padre, tema.PANEL, tema.BORDE, 1)

    def crear_panel_lateral(self, padre):
        canvas = tk.Canvas(padre, bg=tema.PANEL, bd=0, highlightthickness=0)
        barra = ttk.Scrollbar(padre, orient="vertical", command=canvas.yview)
        panel = self.moldes.crear_frame(canvas, tema.PANEL)
        ventana = canvas.create_window((0, 0), window=panel, anchor="nw")
        panel.bind("<Configure>", lambda evento: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda evento: canvas.itemconfigure(ventana, width=evento.width))
        canvas.configure(yscrollcommand=barra.set)
        canvas.grid(row=0, column=0, sticky="nsew")
        barra.grid(row=0, column=1, sticky="ns")
        self.crear_formulario(panel)

    def crear_formulario(self, panel):
        panel.grid_columnconfigure(0, weight=1)
        cabecera = self.moldes.crear_frame(panel, tema.PANEL, fila=0, columna=0, sticky="ew", margen_x=16, margen_y=(16, 12), columnas_peso=((0, 1),))
        self.moldes.crear_label(cabecera, "Solicitud de viaje", ("Arial", 18, "bold"), tema.TEXTO, tema.PANEL).grid(row=0, column=0, sticky="w")
        self.moldes.crear_boton(cabecera, "Volver", False, None, None).grid(row=0, column=1, sticky="e")
        self.crear_servicio(panel)
        self.crear_ruta(panel)
        self.crear_tabla(panel)
        self.crear_confirmacion(panel)
        self.crear_estado(panel)
        self.crear_progreso(panel)

    def crear_servicio(self, panel):
        self.crear_etiqueta(panel, "Servicio", 1)
        self.moldes.crear_label(panel, "Viaje normal", ("Arial", 11, "bold"), tema.TEXTO, tema.PANEL_SUAVE).grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 10), ipady=8)
        datos = self.moldes.crear_frame(panel, tema.PANEL, fila=3, columna=0, sticky="ew", margen_x=16, margen_y=(0, 6), columnas_peso=((0, 1), (1, 1)))
        self.crear_campo(datos, "Cantidad usuarios", "1", 0, 0)
        self.crear_campo(datos, "Peso aprox. total (kg)", "0", 0, 1)

    def crear_ruta(self, panel):
        self.crear_selector_ruta(panel, "Desde", 4, 0)
        self.crear_selector_ruta(panel, "Hasta", 6, 3)
        self.moldes.crear_boton(panel, "Buscar vehiculos", True, None, None).grid(row=8, column=0, sticky="ew", padx=16, pady=(4, 10))
        self.moldes.crear_label(panel, "Completa los datos y revisa vehiculos disponibles para tu ruta.", tema.FUENTE_TEXTO, tema.TEXTO_SUAVE, tema.PANEL, 320, "left").grid(row=9, column=0, sticky="ew", padx=16, pady=(0, 10))

    def crear_tabla(self, panel):
        contenedor = self.moldes.crear_frame(panel, tema.PANEL, fila=10, columna=0, sticky="nsew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1),))
        self.moldes.crear_label(contenedor, "Vehiculos disponibles", ("Arial", 11, "bold"), tema.TEXTO, tema.PANEL).grid(row=0, column=0, sticky="w", pady=(0, 6))
        self.configurar_tabla()
        self.tabla = ttk.Treeview(contenedor, columns=("nombre", "detalle", "precio", "tiempo"), show="headings", style="Viaje.Treeview", height=5)
        for columna, texto, ancho in (("nombre", "Nombre", 105), ("detalle", "Detalle", 140), ("precio", "Precio", 80), ("tiempo", "Tiempo", 70)):
            self.tabla.heading(columna, text=texto)
            self.tabla.column(columna, width=ancho, anchor="center", stretch=True)
        for indice, fila in enumerate(CONDUCTORES_DEMO):
            self.tabla.insert("", "end", iid=str(indice), values=fila)
        self.tabla.grid(row=1, column=0, sticky="nsew")
        self.moldes.crear_boton(panel, "Confirmar pago", True, None, None).grid(row=11, column=0, sticky="ew", padx=16, pady=(0, 8))

    def crear_confirmacion(self, panel):
        confirmacion = self.moldes.crear_frame(panel, tema.FONDO, tema.BORDE, 1, fila=12, columna=0, sticky="ew", margen_x=16, margen_y=(0, 8), columnas_peso=((0, 1), (1, 1)))
        self.moldes.crear_label(confirmacion, "Confirmar pago del viaje seleccionado?", ("Arial", 10, "bold"), tema.TEXTO, tema.FONDO, 280, "left").grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(8, 6))
        self.moldes.crear_boton(confirmacion, "Si, confirmar", True, None, None).grid(row=1, column=0, sticky="ew", padx=(10, 4), pady=(0, 8))
        self.moldes.crear_boton(confirmacion, "Cancelar", False, None, None).grid(row=1, column=1, sticky="ew", padx=(4, 10), pady=(0, 8))

    def crear_estado(self, panel):
        self.moldes.crear_label(panel, "Sin vehiculo seleccionado.", tema.FUENTE_TEXTO, tema.TEXTO, tema.PANEL, 320, "left").grid(row=13, column=0, sticky="ew", padx=16, pady=(0, 8))
        self.moldes.crear_label(panel, "Viaje en curso", ("Arial", 13, "bold"), tema.PRIMARIO, tema.PANEL, 320, "left").grid(row=14, column=0, sticky="ew", padx=16, pady=(0, 8))
        self.moldes.crear_label(panel, "Listo para buscar vehiculos cercanos.", tema.FUENTE_TEXTO, tema.TEXTO_SUAVE, tema.PANEL, 320, "center").grid(row=15, column=0, sticky="ew", padx=16, pady=(0, 14))

    def crear_progreso(self, panel):
        progreso = self.moldes.crear_frame(panel, tema.PANEL, fila=16, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1),))
        self.moldes.crear_label(progreso, "Progreso del trayecto", ("Arial", 11, "bold"), tema.TEXTO, tema.PANEL).grid(row=0, column=0, sticky="w", pady=(0, 8))
        ttk.Progressbar(progreso, maximum=100, mode="determinate", value=35).grid(row=1, column=0, sticky="ew")
        self.moldes.crear_label(progreso, "35%", ("Arial", 10, "bold"), tema.PRIMARIO, tema.PANEL).grid(row=2, column=0, sticky="w", pady=(6, 0))

    def crear_panel_mapa(self, panel):
        cabecera = self.moldes.crear_frame(panel, tema.PANEL, fila=0, columna=0, sticky="ew", margen_x=18, margen_y=(16, 8), columnas_peso=((0, 1),))
        self.moldes.crear_label(cabecera, "Mapa de Osorno", ("Arial", 20, "bold"), tema.TEXTO, tema.PANEL).grid(row=0, column=0, sticky="w")
        self.moldes.crear_label(cabecera, "Ruta, disponibles y puntos de encuentro", tema.FUENTE_TEXTO, tema.TEXTO_SUAVE, tema.PANEL).grid(row=1, column=0, sticky="w")
        contenedor = self.moldes.crear_frame(panel, tema.FONDO, fila=1, columna=0, sticky="nsew", margen_x=18, margen_y=(0, 18), columnas_peso=((0, 1),), filas_peso=((0, 1),))
        self.mapa = TkinterMapView(contenedor, corner_radius=0)
        self.mapa.grid(row=0, column=0, sticky="nsew")
        self.mapa.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png", max_zoom=16)
        self.mapa.set_position(-40.5739, -73.1335)
        self.mapa.set_zoom(13)
        self.pintar_mapa_real()

    def pintar_mapa_real(self):
        origen = COORDENADAS_OSORNO[LUGARES_OSORNO[0]]
        destino = COORDENADAS_OSORNO[LUGARES_OSORNO[3]]
        medio = ((origen[0] + destino[0]) / 2, (origen[1] + destino[1]) / 2)
        self.mapa.set_marker(origen[0], origen[1], text=f"Origen: {LUGARES_OSORNO[0]}")
        self.mapa.set_marker(destino[0], destino[1], text=f"Destino: {LUGARES_OSORNO[3]}")
        self.mapa.set_marker(-40.5712, -73.1285, text="Camila R.")
        self.mapa.set_marker(-40.5808, -73.1395, text="Ignacio P.")
        self.mapa.set_marker(-40.5686, -73.1183, text="Valentina M.")
        self.mapa.set_path([origen, medio, destino], color=tema.PRIMARIO, width=5)
        self.mapa.set_position(medio[0], medio[1])

    def crear_etiqueta(self, padre, texto, fila):
        self.moldes.crear_label(padre, texto, ("Arial", 10, "bold"), tema.TEXTO, tema.PANEL).grid(row=fila, column=0, sticky="w", padx=16, pady=(0, 4))

    def crear_selector_ruta(self, padre, etiqueta, fila, indice):
        self.crear_etiqueta(padre, etiqueta, fila)
        selector = self.moldes.crear_selector(padre, LUGARES_OSORNO)
        selector.current(indice)
        selector.grid(row=fila + 1, column=0, sticky="ew", padx=16, pady=(0, 10), ipady=3)

    def crear_campo(self, padre, etiqueta, valor, fila, columna):
        marco = self.moldes.crear_frame(padre, tema.PANEL, fila=fila, columna=columna, sticky="ew", margen_x=(0, 8) if columna == 0 else (8, 0), columnas_peso=((0, 1),))
        self.moldes.crear_label(marco, etiqueta, ("Arial", 9, "bold"), tema.TEXTO, tema.PANEL).grid(row=0, column=0, sticky="w", pady=(0, 4))
        entrada = self.moldes.crear_entrada(marco)
        entrada.insert(0, valor)
        entrada.grid(row=1, column=0, sticky="ew", ipady=3)

    def configurar_tabla(self):
        estilo = ttk.Style(self)
        estilo.configure("Viaje.Treeview", background=tema.SECUNDARIO, fieldbackground=tema.SECUNDARIO, foreground=tema.TEXTO, rowheight=28, bordercolor=tema.BORDE)
        estilo.configure("Viaje.Treeview.Heading", background=tema.PANEL_SUAVE, foreground=tema.TEXTO, font=("Arial", 9, "bold"))
        estilo.map("Viaje.Treeview", background=[("selected", tema.PRIMARIO)], foreground=[("selected", tema.PRIMARIO_TEXTO)])


def ejecutar():
    ventana = tk.Tk()
    ventana.title(TITULO_VIAJE)
    ventana.geometry(GEOMETRIA_VIAJE)
    ventana.minsize(*TAMANO_MINIMO_VIAJE)
    VistaViaje(ventana)
    ventana.mainloop()


if __name__ == "__main__":
    ejecutar()
