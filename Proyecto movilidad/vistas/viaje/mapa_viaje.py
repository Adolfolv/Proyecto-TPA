from pathlib import Path

from PIL import Image, ImageTk
from tkintermapview import TkinterMapView

from Servicios.Viajes.datos_viaje import COORDENADAS_REALES_OSORNO, IMAGENES_LUGARES_OSORNO, LUGARES_OSORNO, OSORNO_LAT_NORTE, OSORNO_LAT_SUR, OSORNO_LNG_ESTE, OSORNO_LNG_OESTE
from ..estilizacion import tema


RUTA_IMAGENES_LUGARES = Path(__file__).resolve().parent.parent / "estilizacion" / "Imagenes" / "imagenes_lugares"
RUTA_IMAGENES_CONDUCTORES = Path(__file__).resolve().parent.parent / "estilizacion" / "Imagenes" / "imagenes_conductores"
RUTA_IMAGENES_USUARIOS = Path(__file__).resolve().parent.parent / "estilizacion" / "Imagenes" / "imagenes_usuarios"


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

  #crear se ejecuta cuando se muestra el mapa, para evitar cargar 
  #recursos antes de tiempo. Se pueden agregar mas 
  #parametros para pintar cosas especificas segun el caso de uso.
    def crear(self, pintar_lugares=True):
        frame = self.moldes.crear_frame(self.padre, tema.PANEL, tema.BORDE, 1, fila=0, columna=1, sticky="nsew", margen_x=(12, 0))
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        self.crear_cabecera(frame)
        self.crear_mapa(frame, pintar_lugares)

    def crear_cabecera(self, panel):
        cabecera = self.moldes.crear_frame(panel, tema.PANEL, fila=0, columna=0, sticky="ew", margen_x=18, margen_y=(16, 8), columnas_peso=((0, 1),))
        self.moldes.crear_label(cabecera, "Mapa de Osorno", tema.FUENTE_TITULO, tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")

    def crear_mapa(self, panel, pintar_lugares=True):
        contenedor = self.moldes.crear_frame(panel, tema.FONDO, fila=1, columna=0, sticky="nsew", margen_x=18, margen_y=(0, 18), columnas_peso=((0, 1),), filas_peso=((0, 1),))
        self.mapa = TkinterMapView(contenedor, corner_radius=0)
        self.mapa.grid(row=0, column=0, sticky="nsew")
        self.mapa.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png", max_zoom=16)
        self.mapa.set_position(-40.5739, -73.1335)
        self.mapa.set_zoom(15)
        self.bloquear_zoom()
        self.restringir_mapa_osorno()
        if pintar_lugares is True:
            self.pintar_mapa_real()

    def bloquear_zoom(self):
        self.mapa.min_zoom = self.mapa.max_zoom = 15
        for evento in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.mapa.canvas.unbind(evento)
        for boton in (self.mapa.button_zoom_in, self.mapa.button_zoom_out):
            boton.command = None
            for elemento in (boton.canvas_rect, boton.canvas_text):
                self.mapa.canvas.itemconfigure(elemento, state="hidden")

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

    def dibujar_trayectoria(self, ruta, color="#1a73e8", limpiar=True):
        if limpiar:
            self.limpiar_trayectorias()
        if len(ruta) < 2:
            return
        trayectoria = self.mapa.set_path(ruta, color=color, width=5)
        self.trayectorias.append(trayectoria)

    def limpiar_trayectorias(self):
        for trayectoria in self.trayectorias:
            trayectoria.delete()
        self.trayectorias = []

    def limpiar_marcadores(self, marcadores):
        for marcador in marcadores:
            marcador.delete()
        marcadores.clear()

    def crear_marcador_imagen(self, coordenada, imagen):
        return self.mapa.set_marker(*coordenada, icon=imagen,)

    def crear_marcadores_extremos(self, ruta_llegada, ruta_viaje):
        self.marcador_inicio_viaje = self.mapa.set_marker(*ruta_llegada[-1], text="Ubicacion inicial")
        self.marcador_destino_viaje = self.mapa.set_marker(*ruta_viaje[-1], text="Ubicacion final")
        self.ocultar_simbolo_marcador(self.marcador_inicio_viaje)
        self.ocultar_simbolo_marcador(self.marcador_destino_viaje)

    def ocultar_simbolo_marcador(self, marcador):
        def ocultar():
            for atributo in ("polygon", "big_circle", "canvas_icon", "canvas_image", "canvas_marker", "canvas_circle"):
                item = getattr(marcador, atributo, None)
                if item is not None:
                    self.mapa.canvas.itemconfigure(item, state="hidden")

        ocultar()
        self.mapa.after(100, ocultar)

    def obtener_foto(self, ruta_imagen):
        imagen = Image.open(ruta_imagen)
        imagen.thumbnail((46, 46))
        return ImageTk.PhotoImage(imagen)

    def animar_trayectos(self, marcadores, rutas, duraciones, estados, al_actualizar_progreso, al_terminar_viaje, tramo=0, indice=0):
        marcador, ruta, duracion, estado = marcadores[tramo], rutas[tramo], max(1, duraciones[tramo]), estados[tramo]
        progreso = int((indice / max(1, len(ruta) - 1)) * 100)
        al_actualizar_progreso(progreso, estado)
        if marcador is not None:
            marcador.set_position(*ruta[indice])
        if indice >= len(ruta) - 1:
            al_actualizar_progreso(100, estado)
            siguiente = (lambda: self.animar_trayectos(marcadores, rutas, duraciones, estados, al_actualizar_progreso, al_terminar_viaje, tramo + 1)) if tramo + 1 < len(rutas) else al_terminar_viaje
            self.mapa.after(600, siguiente)
            return
        intervalo = max(120, int((duracion * 1000) / max(1, len(ruta) - 1)))
        self.mapa.after(intervalo, lambda: self.animar_trayectos(marcadores, rutas, duraciones, estados, al_actualizar_progreso, al_terminar_viaje, tramo, indice + 1))


class MapaViajeConductor(MapaViajeComun):
    """Mapa base del conductor: lugares de Osorno y trayecto del pasajero."""

    def pintar_mapa_real(self, lugares=LUGARES_OSORNO):
        for lugar in lugares:
            if lugar not in self.imagenes_lugares:
                imagen = Image.open(RUTA_IMAGENES_LUGARES / IMAGENES_LUGARES_OSORNO[lugar])
                imagen.thumbnail((42, 42))
                self.imagenes_lugares[lugar] = ImageTk.PhotoImage(imagen)
            marcador = self.crear_marcador_imagen(COORDENADAS_REALES_OSORNO[lugar], self.imagenes_lugares[lugar])
            self.marcadores_lugares.append(marcador)

    def limpiar_lugares(self):
        self.limpiar_marcadores(self.marcadores_lugares)

    def mostrar_lugares(self, lugares):
        self.limpiar_lugares()
        self.pintar_mapa_real(lugares)

    def animar_viaje_conductor(self, pasajero, rutas_viaje, al_actualizar_progreso, al_terminar_viaje):
        self.limpiar_lugares()

        ruta_llegada = rutas_viaje.llegada
        ruta_viaje = rutas_viaje.viaje
        self.imagen_pasajero_viaje = self.obtener_foto(RUTA_IMAGENES_USUARIOS / pasajero.imagen)
        self.dibujar_trayectoria(ruta_llegada, color="#f59e0b")
        self.dibujar_trayectoria(ruta_viaje, limpiar=False)
        self.crear_marcadores_extremos(ruta_llegada, ruta_viaje)
        marcador_pasajero = self.crear_marcador_imagen(ruta_llegada[-1], self.imagen_pasajero_viaje)
        self.animar_trayectos((None, marcador_pasajero), (ruta_llegada, ruta_viaje), (pasajero.tiempo_para_llegar, pasajero.tiempo_transportando), ("Llegando al punto de partida", "Transportando pasajero"), al_actualizar_progreso, al_terminar_viaje)


class MapaViajePasajero(MapaViajeConductor):
    """Extension del mapa que tambien muestra conductores disponibles."""

    def limpiar_conductores(self):
        self.limpiar_marcadores(self.marcadores_conductores)

    def mostrar_conductores(self, vehiculos):
        self.limpiar_lugares()
        self.limpiar_conductores()
        for vehiculo in vehiculos:
            imagen = self.obtener_imagen_conductor(vehiculo.imagen)
            marcador = self.crear_marcador_imagen(vehiculo.ubicacion_real, imagen)
            self.marcadores_conductores.append(marcador)

    def obtener_imagen_conductor(self, nombre_imagen):
        if nombre_imagen not in self.imagenes_conductores:
            imagen = Image.open(RUTA_IMAGENES_CONDUCTORES / nombre_imagen)
            imagen.thumbnail((42, 42))
            self.imagenes_conductores[nombre_imagen] = ImageTk.PhotoImage(imagen)
        return self.imagenes_conductores[nombre_imagen]

    def limpiar_busqueda(self):
        self.limpiar_conductores()
        self.limpiar_lugares()
        self.limpiar_trayectorias()

    def mostrar_busqueda_pasajero(self, vehiculos, ubicacion_inicial, ubicacion_final, ruta):
        self.dibujar_trayectoria(ruta)
        self.mostrar_conductores(vehiculos)
        self.mostrar_lugares((ubicacion_inicial, ubicacion_final))

    def animar_viaje_pasajero(self, vehiculo, rutas_viaje, al_actualizar_progreso, al_terminar_viaje):
        self.limpiar_busqueda()

        ruta_llegada = rutas_viaje.llegada
        ruta_viaje = rutas_viaje.viaje
        self.imagen_conductor_viaje = self.obtener_foto(RUTA_IMAGENES_CONDUCTORES / vehiculo.imagen)

        self.dibujar_trayectoria(ruta_llegada, color="#f59e0b")
        self.dibujar_trayectoria(ruta_viaje, limpiar=False)
        self.crear_marcadores_extremos(ruta_llegada, ruta_viaje)
        marcador_conductor = self.crear_marcador_imagen(ruta_llegada[0], self.imagen_conductor_viaje)

        duracion = vehiculo.tiempo
        self.animar_trayectos((marcador_conductor, marcador_conductor), (ruta_llegada, ruta_viaje), (duracion, duracion), ("Conductor en camino", "Viajando al destino"), al_actualizar_progreso, al_terminar_viaje)
