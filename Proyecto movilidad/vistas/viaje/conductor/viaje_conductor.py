from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

from ...estilizacion import tema
from ...estilizacion.widgets import Moldes
from .estado_visual_conductor import EstadoVisualConductor
from ..mapa_viaje import MapaViajeConductor
from .renderizador_conductor import RenderizadorConductor


RUTA_IMAGENES = Path(__file__).resolve().parents[2] / "estilizacion" / "Imagenes"
RUTA_IMAGENES_USUARIOS = RUTA_IMAGENES / "imagenes_usuarios"


class PanelIzquierdoConductor:
    """Panel lateral del flujo de conductor."""

    def __init__(self, vista):
        self.vista = vista
        self.moldes = vista.moldes

    def crear(self, padre):
        self.vista.panel = self.moldes.crear_frame(padre, tema.PANEL, tema.BORDE, 1, fila=0, columna=0, sticky="nsew", margen_x=(0, 12))
        self.vista.panel.grid_columnconfigure(0, weight=1)
        self.crear_cabecera()
        self.crear_servicio()
        self.crear_formulario()
        self.crear_busqueda()
        self.crear_panel_pasajero()
        self.crear_confirmacion()
        self.crear_progreso()
        self.crear_boton_buscar_otro()

    def crear_cabecera(self):
        cabecera = self.moldes.crear_frame(self.vista.panel, tema.PANEL, fila=0, columna=0, sticky="ew", margen_x=16, margen_y=(16, 12), columnas_peso=((0, 1),))
        self.moldes.crear_label(cabecera, "Solicitud de viaje", ("Arial", 18, "bold"), tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")
        self.vista.boton_volver = self.moldes.crear_boton(cabecera, "Volver", False, None, self.vista.comando_volver_menu, metodo="grid", fila=0, columna=1, sticky="e")

    def crear_servicio(self):
        self.moldes.crear_label(self.vista.panel, "Servicio", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=1, columna=0, sticky="w", margen_x=16, margen_y=(0, 4))
        self.moldes.crear_label(self.vista.panel, "Viaje normal", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=2, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), ipady=8)

    def crear_formulario(self):
        datos = self.moldes.crear_frame(self.vista.panel, tema.PANEL, fila=3, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1),))
        lugares = self.vista.controlador_conductor.obtener_lugares_disponibles()
        self.vista.selector_ubicacion = self.moldes.crear_selector(datos, lugares, metodo="grid", fila=1, columna=0, columnas=2, sticky="ew", ipady=4)

    def crear_busqueda(self):
        contenedor = self.moldes.crear_frame(self.vista.panel, tema.PANEL, fila=4, columna=0, sticky="nsew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1),))
        self.vista.boton_buscar_pasajeros = self.moldes.crear_boton(contenedor, "Buscar pasajeros", True, None, self.vista.acciones.presionar_boton_buscar_pasajero, metodo="grid", fila=0, columna=0, sticky="ew", margen_y=(0, 8))
        self.moldes.crear_label(contenedor, "Cronómetro", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=1, columna=0, sticky="w", margen_y=(0, 6))
        self.vista.label_cronometro = self.moldes.crear_label(contenedor, "00:00", ("Arial", 28, "bold"), tema.PRIMARIO, tema.PANEL_SUAVE, metodo="grid", fila=2, columna=0, sticky="ew", ipady=24)

    def crear_panel_pasajero(self):
        self.vista.panel_pasajero = self.moldes.crear_frame(self.vista.panel, tema.PANEL_SUAVE, tema.BORDE, 1, fila=6, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 0), (1, 1)))
        self.vista.label_imagen_pasajero = tk.Label(
            self.vista.panel_pasajero,
            bg=tema.PANEL_SUAVE,
        )
        self.vista.label_imagen_pasajero.grid(row=0, column=0, rowspan=4, sticky="nw", padx=10, pady=10)
        self.vista.label_nombre_pasajero = self.moldes.crear_label(self.vista.panel_pasajero, "", ("Arial", 12, "bold"), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=1, sticky="w", margen_x=8, margen_y=(10, 2))
        self.vista.label_trayecto_pasajero = self.moldes.crear_label(self.vista.panel_pasajero, "", ("Arial", 9), tema.TEXTO, tema.PANEL_SUAVE, 300, "left", metodo="grid", fila=1, columna=1, sticky="w", margen_x=8)
        self.vista.label_vehiculo_pasajero = self.moldes.crear_label(self.vista.panel_pasajero, "", ("Arial", 9), tema.TEXTO_SUAVE, tema.PANEL_SUAVE, metodo="grid", fila=2, columna=1, sticky="w", margen_x=8)
        self.vista.label_pago_pasajero = self.moldes.crear_label(self.vista.panel_pasajero, "", ("Arial", 9, "bold"), tema.PRIMARIO, tema.PANEL_SUAVE, metodo="grid", fila=3, columna=1, sticky="w", margen_x=8, margen_y=(0, 10))
        self.vista.label_llegada_pasajero = self.moldes.crear_label(self.vista.panel_pasajero, "", ("Arial", 9), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=4, columna=0, columnas=2, sticky="w", margen_x=10, margen_y=(0, 2))
        self.vista.label_traslado_pasajero = self.moldes.crear_label(self.vista.panel_pasajero, "", ("Arial", 9), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=5, columna=0, columnas=2, sticky="w", margen_x=10, margen_y=(0, 10))
        self.vista.panel_pasajero.grid_remove()

    def crear_confirmacion(self):
        self.vista.panel_confirmacion = self.moldes.crear_frame(self.vista.panel, tema.FONDO, tema.BORDE, 1, fila=7, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1), (1, 1)))
        self.vista.label_pregunta_confirmacion = self.moldes.crear_label(self.vista.panel_confirmacion, "¿Confirmar viaje?", tema.FUENTE_BOTON, tema.TEXTO, tema.FONDO, 280, "left", metodo="grid", fila=0, columna=0, columnas=2, sticky="ew", margen_x=10, margen_y=(8, 6))
        self.vista.boton_confirmar_viaje = self.moldes.crear_boton(self.vista.panel_confirmacion, "Sí, confirmar", True, None, self.vista.acciones.presionar_boton_confirmar_viaje, metodo="grid", fila=1, columna=0, sticky="ew", margen_x=(10, 4), margen_y=(0, 8))
        self.vista.boton_cancelar_viaje = self.moldes.crear_boton(self.vista.panel_confirmacion, "Cancelar", False, None, self.vista.acciones.presionar_boton_cancelar, metodo="grid", fila=1, columna=1, sticky="ew", margen_x=(4, 10), margen_y=(0, 8))
        self.vista.label_estado_viaje = self.moldes.crear_label(self.vista.panel_confirmacion, "", tema.FUENTE_BOTON, tema.PRIMARIO, tema.FONDO, metodo="grid", fila=0, columna=0, columnas=2, sticky="ew", margen_x=10, margen_y=10)
        self.vista.label_estado_viaje.grid_remove()
        self.vista.panel_confirmacion.grid_remove()

    def crear_progreso(self):
        progreso = self.moldes.crear_frame(self.vista.panel, tema.PANEL, fila=8, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1),))
        self.vista.label_estado_progreso = self.moldes.crear_label(progreso, "Progreso del trayecto", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w", margen_y=(0, 8))
        self.vista.barra_progreso = ttk.Progressbar(progreso, maximum=100, mode="determinate", value=0)
        self.vista.barra_progreso.grid(row=1, column=0, sticky="ew")
        self.vista.label_porcentaje_progreso = self.moldes.crear_label(progreso, "0%", tema.FUENTE_BOTON, tema.PRIMARIO, tema.PANEL, metodo="grid", fila=2, columna=0, sticky="w", margen_y=(6, 0))

    def crear_boton_buscar_otro(self):
        self.vista.boton_buscar_otro_viaje = self.moldes.crear_boton(self.vista.panel, "Buscar otro viaje", True, None, self.vista.acciones.presionar_boton_cancelar, metodo="grid", fila=9, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10))
        self.vista.boton_buscar_otro_viaje.grid_remove()


class PanelDerechoConductor:
    def __init__(self, vista):
        self.vista = vista

    def crear(self, padre):
        self.vista.mapa_viaje = MapaViajeConductor(padre, self.vista.moldes)
        self.vista.mapa_viaje.crear()


class AccionesBotonesConductor:
    """Acciones de botones del conductor, separadas del armado de widgets."""

    def __init__(self, vista):
        self.vista = vista

    def presionar_boton_buscar_pasajero(self):
        vista = self.vista
        # La vista captura la ubicacion del conductor; el controlador busca un pasajero.
        ubicacion_conductor = vista.selector_ubicacion.get()
        resultado = vista.controlador_conductor.buscar_pasajero_conductor(
            ubicacion_conductor
        )
        vista.ubicacion_conductor_busqueda = ubicacion_conductor
        vista.info_pasajero_busqueda = resultado.pasajero
        ruta_pasajero = resultado.ruta_pasajero
        vista.estado_visual.buscando_pasajero()
        vista.renderizador.actualizar_cronometro_busqueda(
            lambda: self.finalizar_busqueda_pasajero(ruta_pasajero),
            vista.info_pasajero_busqueda.duracion_busqueda,
        )
    #5 segundos despues(al finalizar el cronometro despues de 
    # presionar el boton buscar pasajero)
    def finalizar_busqueda_pasajero(self, ruta_pasajero):
        self.vista.renderizador.mostrar_pasajero_encontrado()
        self.vista.mapa_viaje.dibujar_trayectoria(ruta_pasajero)
        self.vista.estado_visual.pasajero_encontrado()

    def presionar_boton_confirmar_viaje(self):
        vista = self.vista
        vista.renderizador.mostrar_estado_viaje("viaje en proceso")
        vista.estado_visual.viaje_en_proceso()
        resultado = vista.controlador_conductor.iniciar_viaje_conductor(
            vista.info_pasajero_busqueda,
            vista.usuario_actual,
        )
        vista.viaje_actual = resultado.viaje
        self.iniciar_animacion_viaje(resultado.rutas_viaje)

    def presionar_boton_cancelar(self):
        self.vista.navegar("viaje")

    def presionar_boton_volver_pregunta_activa(self):
        messagebox.showwarning("Viaje pendiente", "Debes seleccionar una opción.")

    def presionar_boton_volver_flujo_activo(self):
        messagebox.showwarning("Viaje en proceso", "No se puede volver ya que hay un viaje en proceso.")

    def iniciar_animacion_viaje(self, rutas_viaje):
        vista = self.vista
        vista.mapa_viaje.animar_viaje_conductor(
            vista.info_pasajero_busqueda,
            rutas_viaje,
            vista.renderizador.actualizar_progreso_viaje,
            vista.finalizar_viaje,
        )

#2, se crean los widgets necesarios
class VistaViajeConductor:
    """Vista principal del flujo de conductor."""

    def __init__(self, padre, navegar, comando_volver_menu, controlador_conductor, usuario_actual):
        self.padre = padre
        self.navegar = navegar
        self.comando_volver_menu = comando_volver_menu
        self.controlador_conductor = controlador_conductor
        self.usuario_actual = usuario_actual
        self.moldes = Moldes()
        self.ruta_imagenes_usuarios = RUTA_IMAGENES_USUARIOS
        # State visual: controla botones/paneles durante busqueda, confirmacion y viaje.
        self.estado_visual = EstadoVisualConductor(self)
        # Renderizador: pinta cronometro, pasajero encontrado y ruta en el mapa.
        self.renderizador = RenderizadorConductor(self)
        self.acciones = AccionesBotonesConductor(self)
        self.crear_widgets()

    def crear_widgets(self):
        contenedor = self.moldes.crear_frame(self.padre, tema.FONDO, llenar="both", expandir=True, margen_x=20, margen_y=20, columnas_peso=((0, 0), (1, 1)), filas_peso=((0, 1),))
        contenedor.grid_columnconfigure(0, minsize=420)
        contenedor.grid_columnconfigure(1, minsize=640)
        PanelIzquierdoConductor(self).crear(contenedor)
        PanelDerechoConductor(self).crear(contenedor)

    def finalizar_viaje(self):
        self.controlador_conductor.finalizar_viaje(self.viaje_actual)
        self.renderizador.mostrar_estado_viaje("viaje finalizado")
        self.estado_visual.viaje_finalizado()
