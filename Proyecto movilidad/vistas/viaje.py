"""Vista de viaje separada por responsabilidades."""

import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from PIL import Image, ImageTk
from tkintermapview import TkinterMapView

from Servicios.Viajes.datos_viaje import COORDENADAS_REALES_OSORNO, IMAGENES_LUGARES_OSORNO, LUGARES_OSORNO, OSORNO_LAT_NORTE, OSORNO_LAT_SUR, OSORNO_LNG_ESTE, OSORNO_LNG_OESTE
from .animacion_viaje import AnimacionViaje
from .estilizacion import tema
from .estilizacion.widgets import Moldes


RUTA_IMAGENES_LUGARES = Path(__file__).resolve().parent / "estilizacion" / "Imagenes" / "imagenes_lugares"
RUTA_IMAGENES_USUARIOS = Path(__file__).resolve().parent / "estilizacion" / "Imagenes" / "imagenes_usuarios"

#Comunes

class ComponenteViaje:
    def __init__(self, panel):
        self.panel = panel
        self.moldes = panel.moldes
        self.tipo_usuario = panel.tipo_usuario
        self.callbacks = panel.callbacks

class ProgresoViaje(ComponenteViaje):
    def crear(self):
        progreso = self.moldes.crear_frame(self.panel.frame, tema.PANEL, fila=8, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1),))
        self.label_estado = self.moldes.crear_label(progreso, "Progreso del trayecto", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w", margen_y=(0, 8))
        self.barra = ttk.Progressbar(progreso, maximum=100, mode="determinate", value=0)
        self.barra.grid(row=1, column=0, sticky="ew")
        self.label_porcentaje = self.moldes.crear_label(progreso, "0%", tema.FUENTE_BOTON, tema.PRIMARIO, tema.PANEL, metodo="grid", fila=2, columna=0, sticky="w", margen_y=(6, 0))

class FormularioViaje(ComponenteViaje):
    def crear(self):
        datos = self.moldes.crear_frame(self.panel.frame, tema.PANEL, fila=3, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1), (1, 1)))
        if self.tipo_usuario == "conductor":
            self.selector_ubicacion = self.moldes.crear_selector(datos, tuple(LUGARES_OSORNO), metodo="grid", fila=1, columna=0, columnas=2, sticky="ew", ipady=4)
            return
        self.entrada_usuarios = self.crear_campo(datos, "Cantidad usuarios", "1", 0, (0, 8))
        self.entrada_peso = self.crear_campo(datos, "Peso aprox. total (kg)", "0", 1, (8, 0))

    def crear_campo(self, padre, titulo, valor_inicial, columna, margen_x):
        campo = self.moldes.crear_frame(padre, tema.PANEL, fila=0, columna=columna, sticky="ew", margen_x=margen_x, columnas_peso=((0, 1),))
        self.moldes.crear_label(campo, titulo, ("Arial", 9, "bold"), tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w", margen_y=(0, 4))
        entrada = self.moldes.crear_entrada(campo)
        entrada.insert(0, valor_inicial)
        entrada.grid(row=1, column=0, sticky="ew", ipady=3)
        return entrada

    def obtener_ubicacion_inicial(self):
        return self.selector_ubicacion.get()

    def bloquear(self):
        self.selector_ubicacion.config(state="disabled")

class GrupoBotonesViaje(ComponenteViaje):
    pass

class BotonesCabeceraViaje(GrupoBotonesViaje):
    def crear(self):
        cabecera = self.moldes.crear_frame(self.panel.frame, tema.PANEL, fila=0, columna=0, sticky="ew", margen_x=16, margen_y=(16, 12), columnas_peso=((0, 1),))
        self.moldes.crear_label(cabecera, "Solicitud de viaje", ("Arial", 18, "bold"), tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")
        self.boton_volver = self.moldes.crear_boton(cabecera, "Volver", False, None, self.callbacks["volver_menu"], metodo="grid", fila=0, columna=1, sticky="e")

    def cambiar_volver(self, comando):
        self.boton_volver.config(command=comando)

class BotonesBusquedaViaje(GrupoBotonesViaje):
    def crear(self):
        contenedor = self.moldes.crear_frame(self.panel.frame, tema.PANEL, fila=4, columna=0, sticky="nsew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1),))
        if self.tipo_usuario == "conductor":
            self.boton_buscar_pasajeros = self.moldes.crear_boton(contenedor, "Buscar pasajeros", True, None, self.callbacks["buscar_pasajero"], metodo="grid", fila=0, columna=0, sticky="ew", margen_y=(0, 8))
            self.panel.cronometro.crear(contenedor)
            return
        self.moldes.crear_boton(contenedor, "Buscar vehiculos", True, None, None, metodo="grid", fila=0, columna=0, sticky="ew", margen_y=(0, 8))
        self.moldes.crear_label(contenedor, "Vehiculos disponibles", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=1, columna=0, sticky="w", margen_y=(0, 6))
        self.tabla = self.moldes.crear_tabla(contenedor, (("nombre", "Nombre", 105), ("detalle", "Detalle", 140), ("precio", "Precio", 80), ("tiempo", "Tiempo", 70)), 5, metodo="grid", fila=2, columna=0, sticky="nsew")
        self.moldes.crear_boton(self.panel.frame, "Iniciar Viaje", True, None, None, metodo="grid", fila=5, columna=0, sticky="ew", margen_x=16, margen_y=(0, 8))

    def bloquear_busqueda(self):
        self.boton_buscar_pasajeros.config(state="disabled", cursor="arrow")

class BotonesConfirmacionViaje(GrupoBotonesViaje):
    def crear(self):
        self.frame_confirmacion = self.moldes.crear_frame(self.panel.frame, tema.FONDO, tema.BORDE, 1, fila=7, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1), (1, 1)))
        texto = "Confirmar viaje?" if self.tipo_usuario == "conductor" else "Confirmar pago del viaje seleccionado?"
        self.label_pregunta = self.moldes.crear_label(self.frame_confirmacion, texto, tema.FUENTE_BOTON, tema.TEXTO, tema.FONDO, 280, "left", metodo="grid", fila=0, columna=0, columnas=2, sticky="ew", margen_x=10, margen_y=(8, 6))
        self.boton_confirmar = self.moldes.crear_boton(self.frame_confirmacion, "Si, confirmar", True, None, self.callbacks["confirmar_viaje"], metodo="grid", fila=1, columna=0, sticky="ew", margen_x=(10, 4), margen_y=(0, 8))
        self.boton_cancelar = self.moldes.crear_boton(self.frame_confirmacion, "Cancelar", False, None, self.callbacks["cancelar"], metodo="grid", fila=1, columna=1, sticky="ew", margen_x=(4, 10), margen_y=(0, 8))
        self.label_estado = self.moldes.crear_label(self.frame_confirmacion, "", tema.FUENTE_BOTON, tema.PRIMARIO, tema.FONDO, metodo="grid", fila=0, columna=0, columnas=2, sticky="ew", margen_x=10, margen_y=10)
        self.label_estado.grid_remove()
        if self.tipo_usuario == "conductor":
            self.frame_confirmacion.grid_remove()

    def bloquear_confirmacion(self):
        self.boton_confirmar.config(state="disabled", cursor="arrow")
        self.boton_cancelar.config(state="disabled", cursor="arrow")

    def mostrar_estado_en_proceso(self):
        self.label_pregunta.grid_remove()
        self.boton_confirmar.grid_remove()
        self.boton_cancelar.grid_remove()
        self.label_estado.config(text="viaje en proceso")
        self.label_estado.grid()

    def mostrar_estado_finalizado(self):
        self.label_estado.config(text="viaje finalizado")

class BotonesBuscarOtroViaje(GrupoBotonesViaje):
    def crear(self):
        self.boton_buscar_otro = self.moldes.crear_boton(self.panel.frame, "Buscar otro viaje", True, None, self.callbacks["cancelar"], metodo="grid", fila=9, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10))
        self.boton_buscar_otro.grid_remove()

    def mostrar_estado_finalizado(self):
        self.boton_buscar_otro.grid()

class BotonesViaje(ComponenteViaje):
    def crear_cabecera(self):
        self.cabecera = BotonesCabeceraViaje(self.panel)
        self.cabecera.crear()

    def crear_busqueda(self):
        self.busqueda = BotonesBusquedaViaje(self.panel)
        self.busqueda.crear()

    def crear_confirmacion(self):
        self.confirmacion = BotonesConfirmacionViaje(self.panel)
        self.confirmacion.crear()

    def crear_buscar_otro(self):
        self.buscar_otro = BotonesBuscarOtroViaje(self.panel)
        self.buscar_otro.crear()

    def bloquear_busqueda(self):
        self.busqueda.bloquear_busqueda()

    def bloquear_confirmacion(self):
        self.confirmacion.bloquear_confirmacion()
        self.busqueda.bloquear_busqueda()

    def mostrar_estado_en_proceso(self):
        self.confirmacion.mostrar_estado_en_proceso()

    def mostrar_estado_finalizado(self):
        self.confirmacion.mostrar_estado_finalizado()
        self.buscar_otro.mostrar_estado_finalizado()

    def cambiar_volver(self, comando):
        self.cabecera.cambiar_volver(comando)

    @property
    def frame_confirmacion(self):
        return self.confirmacion.frame_confirmacion

class PanelViaje:
    def __init__(self, padre, moldes, tipo_usuario, callbacks):
        self.padre = padre
        self.moldes = moldes
        self.tipo_usuario = tipo_usuario
        self.callbacks = callbacks

    def crear(self):
        self.frame = self.moldes.crear_frame(self.padre, tema.PANEL, tema.BORDE, 1, fila=0, columna=0, sticky="nsew", margen_x=(0, 12))
        self.frame.grid_columnconfigure(0, weight=1)
        self.formulario = FormularioViaje(self)
        self.cronometro = CronometroViaje(self)
        self.progreso = ProgresoViaje(self)
        self.botones = BotonesViaje(self)
        self.botones.crear_cabecera()
        self.crear_servicio()
        self.formulario.crear()
        self.botones.crear_busqueda()
        self.panel_pasajero = PanelPasajero(self.frame, self.moldes, self.tipo_usuario)
        self.botones.crear_confirmacion()
        self.progreso.crear()
        self.botones.crear_buscar_otro()

    def crear_servicio(self):
        self.moldes.crear_label(self.frame, "Servicio", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=1, columna=0, sticky="w", margen_x=16, margen_y=(0, 4))
        self.moldes.crear_label(self.frame, "Viaje normal", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=2, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), ipady=8)

    def mostrar_pasajero(self, datos_pasajero):
        self.panel_pasajero.mostrar(datos_pasajero)
        self.botones.frame_confirmacion.grid()

    def bloquear_busqueda(self):
        self.botones.bloquear_busqueda()
        self.formulario.bloquear()

    def bloquear_confirmacion(self):
        self.botones.bloquear_confirmacion()
        self.formulario.bloquear()

    def mostrar_estado_en_proceso(self):
        self.botones.mostrar_estado_en_proceso()

    def mostrar_estado_finalizado(self):
        self.botones.mostrar_estado_finalizado()

    def cambiar_volver(self, comando):
        self.botones.cambiar_volver(comando)

    def obtener_ubicacion_inicial(self):
        return self.formulario.obtener_ubicacion_inicial()
    
class VistaViaje(tk.Frame):
    def __init__(self, master, navegar, tipo_usuario, comando_volver_menu, controlador_viaje, usuario_actual):
        self.navegar = navegar
        self.tipo_usuario = tipo_usuario
        self.comando_volver_menu = comando_volver_menu
        self.controlador_viaje = controlador_viaje
        self.usuario_actual = usuario_actual
        self.animacion_viaje = AnimacionViaje()
        self.moldes = Moldes()
        self.moldes.configurar_selectores(master)
        self.viaje_en_proceso = False
        super().__init__(master, bg=tema.FONDO)
        self.pack(fill="both", expand=True)
        self.crear_widgets()

    def crear_widgets(self):
        contenedor = self.moldes.crear_frame(self, tema.FONDO, llenar="both", expandir=True, margen_x=20, margen_y=20, columnas_peso=((0, 0), (1, 1)), filas_peso=((0, 1),))
        contenedor.grid_columnconfigure(0, minsize=420)
        contenedor.grid_columnconfigure(1, minsize=640)
        callbacks = {"volver_menu": self.comando_volver_menu, "buscar_pasajero": self.presionar_buscar_pasajero, "confirmar_viaje": self.presionar_confirmar_viaje, "cancelar": self.presionar_cancelar}
        self.panel = PanelViaje(contenedor, self.moldes, self.tipo_usuario, callbacks)
        self.panel.crear()
        self.mapa_viaje = MapaViaje(contenedor, self.moldes)
        self.mapa_viaje.crear()
        self.flujo_conductor = FlujoConductor(self, self.panel, self.mapa_viaje)

    def presionar_buscar_pasajero(self):
        self.flujo_conductor.presionar_buscar_pasajero()

    def presionar_confirmar_viaje(self):
        self.flujo_conductor.presionar_confirmar_viaje()

    def presionar_cancelar(self):
        self.navegar("viaje")

    def presionar_volver_pregunta_activa(self):
        messagebox.showwarning("Viaje pendiente", "Debo seleccionar una opcion.")

    def presionar_volver_flujo_activo(self):
        messagebox.showwarning("Viaje en proceso", "No se puede volver ya que hay un viaje en proceso.")

class MapaViaje:
    def __init__(self, padre, moldes):
        self.padre = padre
        self.moldes = moldes
        self.imagenes_lugares = {}
        self.marcadores_lugares = []

    def crear(self):
        frame = self.moldes.crear_frame(self.padre, tema.PANEL, tema.BORDE, 1, fila=0, columna=1, sticky="nsew", margen_x=(12, 0))
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        self.crear_cabecera(frame)
        self.crear_mapa(frame)

    def crear_cabecera(self, panel):
        cabecera = self.moldes.crear_frame(panel, tema.PANEL, fila=0, columna=0, sticky="ew", margen_x=18, margen_y=(16, 8), columnas_peso=((0, 1),))
        self.moldes.crear_label(cabecera, "Mapa de Osorno", tema.FUENTE_TITULO, tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")

    def crear_mapa(self, panel):
        contenedor = self.moldes.crear_frame(panel, tema.FONDO, fila=1, columna=0, sticky="nsew", margen_x=18, margen_y=(0, 18), columnas_peso=((0, 1),), filas_peso=((0, 1),))
        self.mapa = TkinterMapView(contenedor, corner_radius=0)
        self.mapa.grid(row=0, column=0, sticky="nsew")
        self.mapa.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png", max_zoom=16)
        self.mapa.set_position(-40.5739, -73.1335)
        self.mapa.set_zoom(15)
        self.bloquear_zoom()
        self.restringir_mapa_osorno()
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

    def pintar_mapa_real(self):
        for lugar in LUGARES_OSORNO:
            latitud, longitud = COORDENADAS_REALES_OSORNO[lugar]
            if lugar not in self.imagenes_lugares:
                imagen = Image.open(RUTA_IMAGENES_LUGARES / IMAGENES_LUGARES_OSORNO[lugar])
                imagen.thumbnail((42, 42))
                self.imagenes_lugares[lugar] = ImageTk.PhotoImage(imagen)
            marcador = self.mapa.set_marker(latitud, longitud, text=lugar, icon=self.imagenes_lugares[lugar], image_zoom_visibility=(0, float("inf")))
            self.marcadores_lugares.append(marcador)

    def dibujar_trayectoria(self, ruta):
        return self.mapa.set_path(ruta, color="#1a73e8", width=5)
    


#CONDUCTOR
class FlujoConductor:
    def __init__(self, vista, panel, mapa_viaje):
        self.vista = vista
        self.panel = panel
        self.mapa_viaje = mapa_viaje
        self.info_pasajero_busqueda = None
        self.ubicacion_inicial_busqueda = None

    def presionar_buscar_pasajero(self):
        self.ubicacion_inicial_busqueda = self.panel.obtener_ubicacion_inicial()
        self.info_pasajero_busqueda = self.vista.controlador_viaje.buscar_pasajeros(self.ubicacion_inicial_busqueda)
        self.panel.bloquear_busqueda()
        self.actualizar_cronometro_busqueda()

    def actualizar_cronometro_busqueda(self, segundos_transcurridos=0):
        duracion_busqueda = self.info_pasajero_busqueda["duracion_busqueda"]
        self.panel.cronometro.actualizar(segundos_transcurridos)
        if segundos_transcurridos < duracion_busqueda:
            self.panel.cronometro.despues(1000, lambda: self.actualizar_cronometro_busqueda(segundos_transcurridos + 1))
            return
        self.mostrar_pasajero_encontrado()

    def mostrar_pasajero_encontrado(self):
        self.panel.mostrar_pasajero(self.info_pasajero_busqueda)
        ruta_pasajero = self.vista.controlador_viaje.formar_trayectoria(self.info_pasajero_busqueda["ubicacion_inicial"], self.info_pasajero_busqueda["ubicacion_final"])
        self.mapa_viaje.dibujar_trayectoria(ruta_pasajero)
        self.panel.cambiar_volver(self.vista.presionar_volver_pregunta_activa)

    def presionar_confirmar_viaje(self):
        self.vista.viaje_en_proceso = True
        self.panel.bloquear_confirmacion()
        self.panel.mostrar_estado_en_proceso()
        self.panel.cambiar_volver(self.vista.presionar_volver_flujo_activo)
        self.vista.animacion_viaje.animacion_viaje_conductor(self.mapa_viaje.mapa, self.mapa_viaje.marcadores_lugares, RUTA_IMAGENES_USUARIOS, self.info_pasajero_busqueda, self.panel.progreso.barra, self.panel.progreso.label_estado, self.panel.progreso.label_porcentaje, self.finalizar_viaje)
        self.vista.controlador_viaje.iniciar_viaje(self.ubicacion_inicial_busqueda, self.info_pasajero_busqueda, self.vista.usuario_actual)

    def finalizar_viaje(self):
        self.panel.mostrar_estado_finalizado()
        self.panel.cambiar_volver(self.vista.comando_volver_menu)

class CronometroViaje(ComponenteViaje):
    def crear(self, contenedor):
        self.moldes.crear_label(contenedor, "Cronometro", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=1, columna=0, sticky="w", margen_y=(0, 6))
        self.label = self.moldes.crear_label(contenedor, "00:00", ("Arial", 28, "bold"), tema.PRIMARIO, tema.PANEL_SUAVE, metodo="grid", fila=2, columna=0, sticky="ew", ipady=24)

    def actualizar(self, segundos):
        self.label.config(text=f"00:{segundos:02d}")

    def despues(self, milisegundos, accion):
        self.label.after(milisegundos, accion)

class PanelPasajero:
    def __init__(self, padre, moldes, tipo_usuario):
        self.moldes = moldes
        self.frame = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, tema.BORDE, 1, fila=6, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 0), (1, 1)))
        if tipo_usuario == "conductor":
            self.frame.grid_remove()

    def mostrar(self, datos_pasajero):
        imagen = Image.open(RUTA_IMAGENES_USUARIOS / datos_pasajero["imagen"])
        imagen.thumbnail((64, 64))
        self.imagen_pasajero = ImageTk.PhotoImage(imagen)
        tk.Label(self.frame, image=self.imagen_pasajero, bg=tema.PANEL_SUAVE).grid(row=0, column=0, rowspan=4, sticky="nw", padx=10, pady=10)
        llegada = f"Llegar: {datos_pasajero['km_para_llegar']} km | {datos_pasajero['tiempo_para_llegar']} s"
        traslado = f"Traslado: {datos_pasajero['km_transportando']} km | {datos_pasajero['tiempo_transportando']} s"
        self.moldes.crear_label(self.frame, datos_pasajero["nombre_completo"], ("Arial", 12, "bold"), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=1, sticky="w", margen_x=8, margen_y=(10, 2))
        self.moldes.crear_label(self.frame, datos_pasajero["trayecto"], ("Arial", 9), tema.TEXTO, tema.PANEL_SUAVE, 300, "left", metodo="grid", fila=1, columna=1, sticky="w", margen_x=8)
        self.moldes.crear_label(self.frame, f"Vehiculo: {datos_pasajero['vehiculo']}", ("Arial", 9), tema.TEXTO_SUAVE, tema.PANEL_SUAVE, metodo="grid", fila=2, columna=1, sticky="w", margen_x=8)
        self.moldes.crear_label(self.frame, f"Pago: ${datos_pasajero['precio']}", ("Arial", 9, "bold"), tema.PRIMARIO, tema.PANEL_SUAVE, metodo="grid", fila=3, columna=1, sticky="w", margen_x=8, margen_y=(0, 10))
        self.moldes.crear_label(self.frame, llegada, ("Arial", 9), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=4, columna=0, columnas=2, sticky="w", margen_x=10, margen_y=(0, 2))
        self.moldes.crear_label(self.frame, traslado, ("Arial", 9), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=5, columna=0, columnas=2, sticky="w", margen_x=10, margen_y=(0, 10))
        self.frame.grid()
