from pathlib import Path

from PIL import Image, ImageTk
from tkintermapview import TkinterMapView

from Servicios.Viajes.datos_viaje import (
    COORDENADAS_REALES_OSORNO,
    IMAGENES_LUGARES_OSORNO,
    LUGARES_OSORNO,
    OSORNO_LAT_NORTE,
    OSORNO_LAT_SUR,
    OSORNO_LNG_ESTE,
    OSORNO_LNG_OESTE,
)
from ..estilizacion import tema


RUTA_IMAGENES_LUGARES = Path(__file__).resolve().parent.parent / "estilizacion" / "Imagenes" / "imagenes_lugares"
RUTA_IMAGENES_CONDUCTORES = Path(__file__).resolve().parent.parent / "estilizacion" / "Imagenes" / "imagenes_conductores"


class MapaViajeComun:
    """Componente visual reutilizable para pintar rutas y marcadores."""

    def __init__(self, padre, moldes):
        self.padre = padre
        self.moldes = moldes
        self.imagenes_lugares = {}
        self.imagenes_conductores = {}
        self.marcadores_lugares = []
        self.marcadores_conductores = []
        self.trayectorias = []

    def crear(self, pintar_lugares=True):
        frame = self.moldes.crear_frame(
            self.padre,
            tema.PANEL,
            tema.BORDE,
            1,
            fila=0,
            columna=1,
            sticky="nsew",
            margen_x=(12, 0),
        )
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        self.crear_cabecera(frame)
        self.crear_mapa(frame, pintar_lugares)

    def crear_cabecera(self, panel):
        cabecera = self.moldes.crear_frame(
            panel,
            tema.PANEL,
            fila=0,
            columna=0,
            sticky="ew",
            margen_x=18,
            margen_y=(16, 8),
            columnas_peso=((0, 1),),
        )
        self.moldes.crear_label(
            cabecera,
            "Mapa de Osorno",
            tema.FUENTE_TITULO,
            tema.TEXTO,
            tema.PANEL,
            metodo="grid",
            fila=0,
            columna=0,
            sticky="w",
        )

    def crear_mapa(self, panel, pintar_lugares=True):
        contenedor = self.moldes.crear_frame(
            panel,
            tema.FONDO,
            fila=1,
            columna=0,
            sticky="nsew",
            margen_x=18,
            margen_y=(0, 18),
            columnas_peso=((0, 1),),
            filas_peso=((0, 1),),
        )
        self.mapa = TkinterMapView(contenedor, corner_radius=0)
        self.mapa.grid(row=0, column=0, sticky="nsew")
        self.mapa.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png", max_zoom=16)
        self.mapa.set_position(-40.5739, -73.1335)
        self.mapa.set_zoom(15)
        self.bloquear_zoom()
        self.restringir_mapa_osorno()
        if pintar_lugares:
            self.pintar_mapa_real()

    def bloquear_zoom(self):
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

    def dibujar_trayectoria(self, ruta):
        self.limpiar_trayectorias()
        trayectoria = self.mapa.set_path(ruta, color="#1a73e8", width=5)
        self.trayectorias.append(trayectoria)
        return trayectoria

    def limpiar_trayectorias(self):
        for trayectoria in self.trayectorias:
            trayectoria.delete()
        self.trayectorias = []


class MapaViajeConductor(MapaViajeComun):
    """Mapa base del conductor: lugares de Osorno y trayecto del pasajero."""

    def pintar_mapa_real(self, lugares=None):
        lugares = lugares or tuple(LUGARES_OSORNO)
        for lugar in lugares:
            latitud, longitud = COORDENADAS_REALES_OSORNO[lugar]
            if lugar not in self.imagenes_lugares:
                imagen = Image.open(RUTA_IMAGENES_LUGARES / IMAGENES_LUGARES_OSORNO[lugar])
                imagen.thumbnail((42, 42))
                self.imagenes_lugares[lugar] = ImageTk.PhotoImage(imagen)

            marcador = self.mapa.set_marker(
                latitud,
                longitud,
                text=lugar,
                icon=self.imagenes_lugares[lugar],
                image_zoom_visibility=(0, float("inf")),
            )
            self.marcadores_lugares.append(marcador)

    def limpiar_lugares(self):
        for marcador in self.marcadores_lugares:
            marcador.delete()
        self.marcadores_lugares = []

    def mostrar_lugares(self, lugares):
        self.limpiar_lugares()
        self.pintar_mapa_real(lugares)


class MapaViajePasajero(MapaViajeConductor):
    """Extension del mapa que tambien muestra conductores disponibles."""

    def limpiar_conductores(self):
        for marcador in self.marcadores_conductores:
            marcador.delete()
        self.marcadores_conductores = []

    def mostrar_conductores(self, vehiculos):
        self.limpiar_lugares()
        self.limpiar_conductores()
        for vehiculo in vehiculos:
            latitud, longitud = vehiculo.ubicacion_real
            imagen = self.obtener_imagen_conductor(vehiculo.imagen)
            marcador = self.mapa.set_marker(
                latitud,
                longitud,
                text=vehiculo.nombre_completo,
                icon=imagen,
                image_zoom_visibility=(0, float("inf")),
            )
            self.marcadores_conductores.append(marcador)

    def obtener_imagen_conductor(self, nombre_imagen):
        if nombre_imagen not in self.imagenes_conductores:
            imagen = Image.open(RUTA_IMAGENES_CONDUCTORES / nombre_imagen)
            imagen.thumbnail((42, 42))
            self.imagenes_conductores[nombre_imagen] = ImageTk.PhotoImage(imagen)
        return self.imagenes_conductores[nombre_imagen]


class MapaViaje(MapaViajePasajero):
    pass
