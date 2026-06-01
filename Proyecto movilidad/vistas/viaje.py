"""Pantalla visual de viaje sin navegacion real."""

import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from PIL import Image, ImageTk
from tkintermapview import TkinterMapView

from .estilizacion import tema
from .estilizacion.constantes_vistas import (
    COORDENADAS_REALES_OSORNO,
    IMAGENES_LUGARES_OSORNO,
    LUGARES_OSORNO,
    OSORNO_LAT_NORTE,
    OSORNO_LAT_SUR,
    OSORNO_LNG_ESTE,
    OSORNO_LNG_OESTE,
)
from .estilizacion.widgets import Moldes


RUTA_IMAGENES_LUGARES = (
    Path(__file__).resolve().parent
    / "estilizacion"
    / "Imagenes"
    / "imagenes_lugares"
)

RUTA_IMAGENES_USUARIOS = (
    Path(__file__).resolve().parent
    / "estilizacion"
    / "Imagenes"
    / "imagenes_usuarios"
)


class VistaViaje(tk.Frame):
    def __init__(
        self,
        master,
        navegar=None,
        tipo_usuario="pasajero",
        comando_volver_menu=None,
        controlador_viaje=None,
    ):
        self.navegar = navegar
        self.tipo_usuario = tipo_usuario
        self.comando_volver_menu = comando_volver_menu
        self.controlador_viaje = controlador_viaje
        self.moldes = Moldes()
        self.moldes.configurar_selectores(master)

        self.mapa = None
        self.imagenes_lugares = {}
        self.boton_volver = None
        self.boton_buscar_pasajeros = None
        self.boton_confirmar_viaje = None
        self.boton_cancelar_viaje = None
        self.selector_ubicacion = None
        self.label_cronometro = None
        self.frame_pasajero = None
        self.frame_confirmacion = None
        self.pasajero_encontrado = None
        self.imagen_pasajero = None
        self.info_pasajero_busqueda = None
        self.trayectoria_pasajero = None
        self.ubicacion_inicial_busqueda = None

        super().__init__(master, bg=tema.FONDO)
        self.pack(fill="both", expand=True)

        self.crear_widgets()

    def crear_widgets(self):
        contenedor = self.moldes.crear_frame(self, tema.FONDO, llenar="both", expandir=True, margen_x=20, margen_y=20, columnas_peso=((0, 0), (1, 1)), filas_peso=((0, 1),))

        contenedor.grid_columnconfigure(0, minsize=420)
        contenedor.grid_columnconfigure(1, minsize=640)

        self.crear_frame_izquierdo(contenedor)
        self.crear_frame_derecho(contenedor)

    def crear_frame_izquierdo(self, padre):
        frame = self.moldes.crear_frame(padre, tema.PANEL, tema.BORDE, 1, fila=0, columna=0, sticky="nsew", margen_x=(0, 12))
        frame.grid_columnconfigure(0, weight=1)

        cabecera = self.moldes.crear_frame(frame, tema.PANEL, fila=0, columna=0, sticky="ew", margen_x=16, margen_y=(16, 12), columnas_peso=((0, 1),))
        self.moldes.crear_label(cabecera, "Solicitud de viaje", ("Arial", 18, "bold"), tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")
        self.boton_volver = self.moldes.crear_boton(cabecera, "Volver", False, None, self.comando_volver_menu, metodo="grid", fila=0, columna=1, sticky="e")

        self.moldes.crear_label(frame, "Servicio", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=1, columna=0, sticky="w", margen_x=16, margen_y=(0, 4))
        self.moldes.crear_label(frame, "Viaje normal", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=2, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), ipady=8)

        datos = self.moldes.crear_frame(frame, tema.PANEL, fila=3, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1), (1, 1)))
        if self.tipo_usuario == "conductor":
            self.selector_ubicacion = self.moldes.crear_selector(datos, tuple(LUGARES_OSORNO), metodo="grid", fila=1, columna=0, columnas=2, sticky="ew", ipady=4)
        else:
            campo_usuarios = self.moldes.crear_frame(datos, tema.PANEL, fila=0, columna=0, sticky="ew", margen_x=(0, 8), columnas_peso=((0, 1),))
            self.moldes.crear_label(campo_usuarios, "Cantidad usuarios", ("Arial", 9, "bold"), tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w", margen_y=(0, 4))
            entrada_usuarios = self.moldes.crear_entrada(campo_usuarios)
            entrada_usuarios.insert(0, "1")
            entrada_usuarios.grid(row=1, column=0, sticky="ew", ipady=3)

            campo_peso = self.moldes.crear_frame(datos, tema.PANEL, fila=0, columna=1, sticky="ew", margen_x=(8, 0), columnas_peso=((0, 1),))
            self.moldes.crear_label(campo_peso, "Peso aprox. total (kg)", ("Arial", 9, "bold"), tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w", margen_y=(0, 4))
            entrada_peso = self.moldes.crear_entrada(campo_peso)
            entrada_peso.insert(0, "0")
            entrada_peso.grid(row=1, column=0, sticky="ew", ipady=3)

        contenedor_tabla = self.moldes.crear_frame(frame, tema.PANEL, fila=4, columna=0, sticky="nsew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1),))
        if self.tipo_usuario == "conductor":
            self.boton_buscar_pasajeros = self.moldes.crear_boton(contenedor_tabla, "Buscar pasajeros", True, None, self.buscar_pasajeros, metodo="grid", fila=0, columna=0, sticky="ew", margen_y=(0, 8))
            self.moldes.crear_label(contenedor_tabla, "Cronometro", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=1, columna=0, sticky="w", margen_y=(0, 6))
            self.label_cronometro = self.moldes.crear_label(contenedor_tabla, "00:00", ("Arial", 28, "bold"), tema.PRIMARIO, tema.PANEL_SUAVE, metodo="grid", fila=2, columna=0, sticky="ew", ipady=24)
        else:
            self.moldes.crear_boton(contenedor_tabla, "Buscar vehiculos", True, None, None, metodo="grid", fila=0, columna=0, sticky="ew", margen_y=(0, 8))
            self.moldes.crear_label(contenedor_tabla, "Vehiculos disponibles", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=1, columna=0, sticky="w", margen_y=(0, 6))
            self.tabla = self.moldes.crear_tabla(contenedor_tabla, (("nombre", "Nombre", 105), ("detalle", "Detalle", 140), ("precio", "Precio", 80), ("tiempo", "Tiempo", 70)), 5, metodo="grid", fila=2, columna=0, sticky="nsew")

        if self.tipo_usuario != "conductor":
            self.moldes.crear_boton(frame, "Iniciar Viaje", True, None, None, metodo="grid", fila=5, columna=0, sticky="ew", margen_x=16, margen_y=(0, 8))

        self.frame_pasajero = self.moldes.crear_frame(frame, tema.PANEL_SUAVE, tema.BORDE, 1, fila=6, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 0), (1, 1)))
        if self.tipo_usuario == "conductor":
            self.frame_pasajero.grid_remove()

        confirmacion = self.moldes.crear_frame(frame, tema.FONDO, tema.BORDE, 1, fila=7, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1), (1, 1)))
        self.frame_confirmacion = confirmacion
        texto_confirmacion = "Confirmar viaje?" if self.tipo_usuario == "conductor" else "Confirmar pago del viaje seleccionado?"
        self.moldes.crear_label(confirmacion, texto_confirmacion, tema.FUENTE_BOTON, tema.TEXTO, tema.FONDO, 280, "left", metodo="grid", fila=0, columna=0, columnas=2, sticky="ew", margen_x=10, margen_y=(8, 6))
        self.boton_confirmar_viaje = self.moldes.crear_boton(confirmacion, "Si, confirmar", True, None, self.iniciar_viaje, metodo="grid", fila=1, columna=0, sticky="ew", margen_x=(10, 4), margen_y=(0, 8))
        self.boton_cancelar_viaje = self.moldes.crear_boton(confirmacion, "Cancelar", False, None, self.cancelar_busqueda_pasajeros, metodo="grid", fila=1, columna=1, sticky="ew", margen_x=(4, 10), margen_y=(0, 8))
        if self.tipo_usuario == "conductor":
            self.frame_confirmacion.grid_remove()

        progreso = self.moldes.crear_frame(frame, tema.PANEL, fila=8, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1),))
        self.moldes.crear_label(progreso, "Progreso del trayecto", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w", margen_y=(0, 8))
        ttk.Progressbar(progreso, maximum=100, mode="determinate", value=35).grid(row=1, column=0, sticky="ew")
        self.moldes.crear_label(progreso, "35%", tema.FUENTE_BOTON, tema.PRIMARIO, tema.PANEL, metodo="grid", fila=2, columna=0, sticky="w", margen_y=(6, 0))

#mapa + funciones basicas mapa
    def crear_frame_derecho(self, padre):
        frame = self.moldes.crear_frame(padre, tema.PANEL, tema.BORDE, 1, fila=0, columna=1, sticky="nsew", margen_x=(12, 0))
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        self.crear_cabecera_mapa(frame)
        self.crear_mapa(frame)

    def crear_cabecera_mapa(self, panel):
        cabecera = self.moldes.crear_frame(panel, tema.PANEL, fila=0, columna=0, sticky="ew", margen_x=18, margen_y=(16, 8), columnas_peso=((0, 1),))
        self.moldes.crear_label(cabecera, "Mapa de Osorno", tema.FUENTE_TITULO, tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")

    def crear_mapa(self, panel):
        contenedor = self.moldes.crear_frame(panel, tema.FONDO, fila=1, columna=0, sticky="nsew", margen_x=18, margen_y=(0, 18), columnas_peso=((0, 1),), filas_peso=((0, 1),))
        self.mapa = TkinterMapView(contenedor, corner_radius=0)

        self.mapa.grid(row=0, column=0, sticky="nsew")
        self.mapa.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png", max_zoom=16)
        self.mapa.set_position(-40.5739, -73.1335)
        self.mapa.set_zoom(15)
        self.bloquear_zoom_mapa()
        self.restringir_mapa_osorno()
        self.pintar_mapa_real()

    def bloquear_zoom_mapa(self):
        self.mapa.min_zoom = 15
        self.mapa.max_zoom = 15
        self.mapa.canvas.unbind("<MouseWheel>")
        self.mapa.canvas.unbind("<Button-4>")
        self.mapa.canvas.unbind("<Button-5>")

        for boton in (self.mapa.button_zoom_in, self.mapa.button_zoom_out):
            boton.command = None
            self.mapa.canvas.itemconfigure(boton.canvas_rect, state="hidden")
            self.mapa.canvas.itemconfigure(boton.canvas_text, state="hidden")

    def restringir_mapa_osorno(self, evento=None):
        if evento is None:
            self.mapa.canvas.bind("<ButtonRelease-1>", self.restringir_mapa_osorno)
            return

        self.mapa.mouse_release(evento)
        latitud, longitud = self.mapa.get_position()
        latitud = min(OSORNO_LAT_NORTE, max(OSORNO_LAT_SUR, latitud))
        longitud = min(OSORNO_LNG_ESTE, max(OSORNO_LNG_OESTE, longitud))
        self.mapa.set_position(latitud, longitud)
        self.mapa.fading_possible = False

    def pintar_mapa_real(self):
        for lugar in LUGARES_OSORNO:
            latitud, longitud = COORDENADAS_REALES_OSORNO[lugar]

            if lugar not in self.imagenes_lugares:
                imagen = Image.open(RUTA_IMAGENES_LUGARES / IMAGENES_LUGARES_OSORNO[lugar])
                imagen.thumbnail((42, 42))
                self.imagenes_lugares[lugar] = ImageTk.PhotoImage(imagen)

            self.mapa.set_marker(latitud, longitud, text=lugar, icon=self.imagenes_lugares[lugar], image_zoom_visibility=(0, float("inf")))

#-- flujo viaje pasajero ---#

#-- flujo viaje conductor ---#
    def buscar_pasajeros(self):
        if not self.controlador_viaje:
            return

        ubicacion_inicial = self.selector_ubicacion.get()
        self.ubicacion_inicial_busqueda = ubicacion_inicial
        self.info_pasajero_busqueda = self.controlador_viaje.buscar_pasajeros(
            ubicacion_inicial,
            self.boton_buscar_pasajeros,
            self.selector_ubicacion,
            self.label_cronometro,
            self.frame_pasajero,
            RUTA_IMAGENES_USUARIOS,
            self.moldes,
            tema,
            self.finalizar_busqueda_pasajeros,
        )
        return self.info_pasajero_busqueda

    def finalizar_busqueda_pasajeros(self):
        self.trayectoria_pasajero = self.controlador_viaje.formar_trayectoria(self.mapa,
            self.info_pasajero_busqueda["ubicacion_inicial"],
            self.info_pasajero_busqueda["ubicacion_final"],
        )
        self.frame_pasajero.grid()
        self.frame_confirmacion.grid()
        self.boton_volver.config(command=self.mostrar_aviso_seleccionar_opcion)

    def cancelar_busqueda_pasajeros(self):
        if self.navegar:
            self.navegar("viaje")

    def iniciar_viaje(self):
        self.controlador_viaje.iniciar_viaje(
            self.ubicacion_inicial_busqueda,
            self.info_pasajero_busqueda,
        )
        self.boton_volver.config(command=self.mostrar_aviso_viaje_en_proceso)

    def mostrar_aviso_seleccionar_opcion(self):
        messagebox.showwarning("Viaje pendiente", "Debo seleccionar una opcion.")

    def mostrar_aviso_viaje_en_proceso(self):
        messagebox.showwarning("Viaje en proceso", "No se puede volver ya que hay un viaje en proceso.")


