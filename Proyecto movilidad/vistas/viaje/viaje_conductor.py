import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from PIL import Image, ImageTk

from ..estilizacion import tema
from ..estilizacion.widgets import Moldes
from .animacion_viaje import AnimacionViaje
from .mapa_viaje import MapaViaje


RUTA_IMAGENES_USUARIOS = Path(__file__).resolve().parent.parent / "estilizacion" / "Imagenes" / "imagenes_usuarios"


class FrameIzquierdoConductor:
    """Panel lateral del flujo de conductor."""

    def __init__(self, vista):
        self.vista = vista
        self.moldes = vista.moldes

    def crear(self, padre):
        self.vista.frame = self.moldes.crear_frame(padre, tema.PANEL, tema.BORDE, 1, fila=0, columna=0, sticky="nsew", margen_x=(0, 12))
        self.vista.frame.grid_columnconfigure(0, weight=1)
        self.crear_cabecera()
        self.crear_servicio()
        self.crear_formulario()
        self.crear_busqueda()
        self.crear_panel_pasajero()
        self.crear_confirmacion()
        self.crear_progreso()
        self.crear_boton_buscar_otro()

    def crear_cabecera(self):
        cabecera = self.moldes.crear_frame(self.vista.frame, tema.PANEL, fila=0, columna=0, sticky="ew", margen_x=16, margen_y=(16, 12), columnas_peso=((0, 1),))
        self.moldes.crear_label(cabecera, "Solicitud de viaje", ("Arial", 18, "bold"), tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")
        self.vista.boton_volver = self.moldes.crear_boton(cabecera, "Volver", False, None, self.vista.comando_volver_menu, metodo="grid", fila=0, columna=1, sticky="e")

    def crear_servicio(self):
        self.moldes.crear_label(self.vista.frame, "Servicio", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=1, columna=0, sticky="w", margen_x=16, margen_y=(0, 4))
        self.moldes.crear_label(self.vista.frame, "Viaje normal", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=2, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), ipady=8)

    def crear_formulario(self):
        datos = self.moldes.crear_frame(self.vista.frame, tema.PANEL, fila=3, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1),))
        lugares = self.vista.controlador_conductor.obtener_lugares_disponibles()
        self.vista.selector_ubicacion = self.moldes.crear_selector(datos, lugares, metodo="grid", fila=1, columna=0, columnas=2, sticky="ew", ipady=4)

    def crear_busqueda(self):
        contenedor = self.moldes.crear_frame(self.vista.frame, tema.PANEL, fila=4, columna=0, sticky="nsew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1),))
        self.vista.boton_buscar_pasajeros = self.moldes.crear_boton(contenedor, "Buscar pasajeros", True, None, self.vista.acciones.presionar_boton_buscar_pasajero, metodo="grid", fila=0, columna=0, sticky="ew", margen_y=(0, 8))
        self.moldes.crear_label(contenedor, "Cronometro", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=1, columna=0, sticky="w", margen_y=(0, 6))
        self.vista.label_cronometro = self.moldes.crear_label(contenedor, "00:00", ("Arial", 28, "bold"), tema.PRIMARIO, tema.PANEL_SUAVE, metodo="grid", fila=2, columna=0, sticky="ew", ipady=24)

    def crear_panel_pasajero(self):
        self.vista.frame_pasajero = self.moldes.crear_frame(self.vista.frame, tema.PANEL_SUAVE, tema.BORDE, 1, fila=6, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 0), (1, 1)))
        self.vista.frame_pasajero.grid_remove()

    def crear_confirmacion(self):
        self.vista.frame_confirmacion = self.moldes.crear_frame(self.vista.frame, tema.FONDO, tema.BORDE, 1, fila=7, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1), (1, 1)))
        self.vista.label_pregunta_confirmacion = self.moldes.crear_label(self.vista.frame_confirmacion, "Confirmar viaje?", tema.FUENTE_BOTON, tema.TEXTO, tema.FONDO, 280, "left", metodo="grid", fila=0, columna=0, columnas=2, sticky="ew", margen_x=10, margen_y=(8, 6))
        self.vista.boton_confirmar_viaje = self.moldes.crear_boton(self.vista.frame_confirmacion, "Si, confirmar", True, None, self.vista.acciones.presionar_boton_confirmar_viaje, metodo="grid", fila=1, columna=0, sticky="ew", margen_x=(10, 4), margen_y=(0, 8))
        self.vista.boton_cancelar_viaje = self.moldes.crear_boton(self.vista.frame_confirmacion, "Cancelar", False, None, self.vista.acciones.presionar_boton_cancelar, metodo="grid", fila=1, columna=1, sticky="ew", margen_x=(4, 10), margen_y=(0, 8))
        self.vista.label_estado_viaje = self.moldes.crear_label(self.vista.frame_confirmacion, "", tema.FUENTE_BOTON, tema.PRIMARIO, tema.FONDO, metodo="grid", fila=0, columna=0, columnas=2, sticky="ew", margen_x=10, margen_y=10)
        self.vista.label_estado_viaje.grid_remove()
        self.vista.frame_confirmacion.grid_remove()

    def crear_progreso(self):
        progreso = self.moldes.crear_frame(self.vista.frame, tema.PANEL, fila=8, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1),))
        self.vista.label_estado_progreso = self.moldes.crear_label(progreso, "Progreso del trayecto", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w", margen_y=(0, 8))
        self.vista.barra_progreso = ttk.Progressbar(progreso, maximum=100, mode="determinate", value=0)
        self.vista.barra_progreso.grid(row=1, column=0, sticky="ew")
        self.vista.label_porcentaje_progreso = self.moldes.crear_label(progreso, "0%", tema.FUENTE_BOTON, tema.PRIMARIO, tema.PANEL, metodo="grid", fila=2, columna=0, sticky="w", margen_y=(6, 0))

    def crear_boton_buscar_otro(self):
        self.vista.boton_buscar_otro_viaje = self.moldes.crear_boton(self.vista.frame, "Buscar otro viaje", True, None, self.vista.acciones.presionar_boton_cancelar, metodo="grid", fila=9, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10))
        self.vista.boton_buscar_otro_viaje.grid_remove()


class FrameDerechoConductor:
    def __init__(self, vista):
        self.vista = vista

    def crear(self, padre):
        self.vista.mapa_viaje = MapaViaje(padre, self.vista.moldes)
        self.vista.mapa_viaje.crear()


class AccionesBotonesConductor:
    """Acciones de botones del conductor, separadas del armado de widgets."""

    def __init__(self, vista):
        self.vista = vista

    def presionar_boton_buscar_pasajero(self):
        vista = self.vista
        # La vista captura la ubicacion; el controlador busca el pasajero.
        vista.ubicacion_inicial_busqueda = vista.selector_ubicacion.get()
        vista.info_pasajero_busqueda = vista.controlador_conductor.buscar_pasajero_conductor(vista.ubicacion_inicial_busqueda)
        vista.boton_buscar_pasajeros.config(state="disabled", cursor="arrow")
        vista.selector_ubicacion.config(state="disabled")
        self.actualizar_cronometro_busqueda()

    def presionar_boton_confirmar_viaje(self):
        vista = self.vista
        if vista.viaje_en_proceso:
            return

        self.bloquear_formulario_en_viaje()
        vista.controlador_conductor.iniciar_viaje_conductor(
            vista.info_pasajero_busqueda,
            vista.usuario_actual,
        )
        self.iniciar_animacion_viaje(
            vista.controlador_conductor.obtener_rutas_viaje_conductor(),
        )

    def presionar_boton_cancelar(self):
        self.vista.navegar("viaje")

    def presionar_boton_volver_pregunta_activa(self):
        messagebox.showwarning("Viaje pendiente", "Debo seleccionar una opcion.")

    def presionar_boton_volver_flujo_activo(self):
        messagebox.showwarning("Viaje en proceso", "No se puede volver ya que hay un viaje en proceso.")

    def actualizar_cronometro_busqueda(self, segundos_transcurridos=0):
        vista = self.vista
        duracion_busqueda = vista.info_pasajero_busqueda.duracion_busqueda
        vista.label_cronometro.config(text=f"00:{segundos_transcurridos:02d}")
        if segundos_transcurridos < duracion_busqueda:
            vista.label_cronometro.after(1000, lambda: self.actualizar_cronometro_busqueda(segundos_transcurridos + 1))
            return
        self.mostrar_pasajero_encontrado()

    def mostrar_pasajero_encontrado(self):
        vista = self.vista
        pasajero = vista.info_pasajero_busqueda
        imagen = Image.open(RUTA_IMAGENES_USUARIOS / pasajero.imagen)
        imagen.thumbnail((64, 64))
        vista.imagen_pasajero = ImageTk.PhotoImage(imagen)
        tk.Label(vista.frame_pasajero, image=vista.imagen_pasajero, bg=tema.PANEL_SUAVE).grid(row=0, column=0, rowspan=4, sticky="nw", padx=10, pady=10)

        llegada = f"Llegar: {pasajero.km_para_llegar} km | {pasajero.tiempo_para_llegar} s"
        traslado = f"Traslado: {pasajero.km_transportando} km | {pasajero.tiempo_transportando} s"
        vista.moldes.crear_label(vista.frame_pasajero, pasajero.nombre_completo, ("Arial", 12, "bold"), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=1, sticky="w", margen_x=8, margen_y=(10, 2))
        vista.moldes.crear_label(vista.frame_pasajero, pasajero.trayecto, ("Arial", 9), tema.TEXTO, tema.PANEL_SUAVE, 300, "left", metodo="grid", fila=1, columna=1, sticky="w", margen_x=8)
        vista.moldes.crear_label(vista.frame_pasajero, f"Vehiculo: {pasajero.vehiculo}", ("Arial", 9), tema.TEXTO_SUAVE, tema.PANEL_SUAVE, metodo="grid", fila=2, columna=1, sticky="w", margen_x=8)
        vista.moldes.crear_label(vista.frame_pasajero, f"Pago: ${pasajero.precio}", ("Arial", 9, "bold"), tema.PRIMARIO, tema.PANEL_SUAVE, metodo="grid", fila=3, columna=1, sticky="w", margen_x=8, margen_y=(0, 10))
        vista.moldes.crear_label(vista.frame_pasajero, llegada, ("Arial", 9), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=4, columna=0, columnas=2, sticky="w", margen_x=10, margen_y=(0, 2))
        vista.moldes.crear_label(vista.frame_pasajero, traslado, ("Arial", 9), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=5, columna=0, columnas=2, sticky="w", margen_x=10, margen_y=(0, 10))

        # El controlador entrega la ruta; la vista solo la dibuja.
        ruta_pasajero = vista.controlador_conductor.formar_ruta_pasajero_conductor(pasajero)
        vista.mapa_viaje.dibujar_trayectoria(ruta_pasajero)
        vista.frame_pasajero.grid()
        vista.frame_confirmacion.grid()
        vista.boton_volver.config(command=self.presionar_boton_volver_pregunta_activa)

    def bloquear_formulario_en_viaje(self):
        vista = self.vista
        vista.viaje_en_proceso = True
        vista.boton_confirmar_viaje.config(state="disabled", cursor="arrow")
        vista.boton_cancelar_viaje.config(state="disabled", cursor="arrow")
        vista.boton_buscar_pasajeros.config(state="disabled", cursor="arrow")
        vista.selector_ubicacion.config(state="disabled")
        vista.boton_volver.config(command=self.presionar_boton_volver_flujo_activo)
        vista.label_pregunta_confirmacion.grid_remove()
        vista.boton_confirmar_viaje.grid_remove()
        vista.boton_cancelar_viaje.grid_remove()
        vista.label_estado_viaje.config(text="viaje en proceso")
        vista.label_estado_viaje.grid()

    def iniciar_animacion_viaje(self, rutas_viaje):
        vista = self.vista
        vista.animacion_viaje.animacion_viaje_conductor(vista.mapa_viaje.mapa, vista.mapa_viaje.marcadores_lugares, RUTA_IMAGENES_USUARIOS, vista.info_pasajero_busqueda, rutas_viaje, vista.barra_progreso, vista.label_estado_progreso, vista.label_porcentaje_progreso, vista.finalizar_viaje)


class VistaViajeConductor:
    """Vista principal del flujo de conductor."""

    def __init__(self, padre, navegar, comando_volver_menu, controlador_conductor, usuario_actual):
        self.padre = padre
        self.navegar = navegar
        self.comando_volver_menu = comando_volver_menu
        self.controlador_conductor = controlador_conductor
        self.usuario_actual = usuario_actual
        self.animacion_viaje = AnimacionViaje()
        self.moldes = Moldes()
        self.viaje_en_proceso = False
        self.mapa_viaje = None
        self.acciones = AccionesBotonesConductor(self)
        self.crear_widgets()

    def crear_widgets(self):
        contenedor = self.moldes.crear_frame(self.padre, tema.FONDO, llenar="both", expandir=True, margen_x=20, margen_y=20, columnas_peso=((0, 0), (1, 1)), filas_peso=((0, 1),))
        contenedor.grid_columnconfigure(0, minsize=420)
        contenedor.grid_columnconfigure(1, minsize=640)
        FrameIzquierdoConductor(self).crear(contenedor)
        FrameDerechoConductor(self).crear(contenedor)

    def finalizar_viaje(self):
        self.label_estado_viaje.config(text="viaje finalizado")
        self.boton_volver.config(command=self.comando_volver_menu)
        self.boton_buscar_otro_viaje.grid()
