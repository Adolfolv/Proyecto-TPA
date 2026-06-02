import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from PIL import Image, ImageTk

from Servicios.Viajes.datos_viaje import LUGARES_OSORNO
from Servicios.Viajes.animacion_viaje import AnimacionViaje
from ..estilizacion import tema
from ..estilizacion.widgets import Moldes
from .mapa_viaje import MapaViaje


RUTA_IMAGENES_USUARIOS = Path(__file__).resolve().parent.parent / "estilizacion" / "Imagenes" / "imagenes_usuarios"


class VistaViajeConductor:
    def __init__(self, padre, navegar, comando_volver_menu, controlador_viaje, usuario_actual):
        self.padre = padre
        self.navegar = navegar
        self.comando_volver_menu = comando_volver_menu
        self.controlador_viaje = controlador_viaje
        self.usuario_actual = usuario_actual
        self.animacion_viaje = AnimacionViaje()
        self.moldes = Moldes()
        self.viaje_en_proceso = False
        self.crear_widgets()

    def crear_widgets(self):
        contenedor = self.moldes.crear_frame(self.padre, tema.FONDO, llenar="both", expandir=True, margen_x=20, margen_y=20, columnas_peso=((0, 0), (1, 1)), filas_peso=((0, 1),))
        contenedor.grid_columnconfigure(0, minsize=420)
        contenedor.grid_columnconfigure(1, minsize=640)
        self.crear_panel_izquierdo(contenedor)
        self.mapa_viaje = MapaViaje(contenedor, self.moldes)
        self.mapa_viaje.crear()

    def crear_panel_izquierdo(self, padre):
        self.frame = self.moldes.crear_frame(padre, tema.PANEL, tema.BORDE, 1, fila=0, columna=0, sticky="nsew", margen_x=(0, 12))
        self.frame.grid_columnconfigure(0, weight=1)
        self.crear_cabecera()
        self.crear_servicio()
        self.crear_formulario()
        self.crear_busqueda()
        self.crear_panel_pasajero()
        self.crear_confirmacion()
        self.crear_progreso()
        self.crear_boton_buscar_otro()

    def crear_cabecera(self):
        cabecera = self.moldes.crear_frame(self.frame, tema.PANEL, fila=0, columna=0, sticky="ew", margen_x=16, margen_y=(16, 12), columnas_peso=((0, 1),))
        self.moldes.crear_label(cabecera, "Solicitud de viaje", ("Arial", 18, "bold"), tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")
        self.boton_volver = self.moldes.crear_boton(cabecera, "Volver", False, None, self.comando_volver_menu, metodo="grid", fila=0, columna=1, sticky="e")

    def crear_servicio(self):
        self.moldes.crear_label(self.frame, "Servicio", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=1, columna=0, sticky="w", margen_x=16, margen_y=(0, 4))
        self.moldes.crear_label(self.frame, "Viaje normal", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=2, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), ipady=8)

    def crear_formulario(self):
        datos = self.moldes.crear_frame(self.frame, tema.PANEL, fila=3, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1),))
        self.selector_ubicacion = self.moldes.crear_selector(datos, tuple(LUGARES_OSORNO), metodo="grid", fila=1, columna=0, columnas=2, sticky="ew", ipady=4)

    def crear_busqueda(self):
        contenedor = self.moldes.crear_frame(self.frame, tema.PANEL, fila=4, columna=0, sticky="nsew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1),))
        self.boton_buscar_pasajeros = self.moldes.crear_boton(contenedor, "Buscar pasajeros", True, None, self.presionar_buscar_pasajero, metodo="grid", fila=0, columna=0, sticky="ew", margen_y=(0, 8))
        self.moldes.crear_label(contenedor, "Cronometro", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=1, columna=0, sticky="w", margen_y=(0, 6))
        self.label_cronometro = self.moldes.crear_label(contenedor, "00:00", ("Arial", 28, "bold"), tema.PRIMARIO, tema.PANEL_SUAVE, metodo="grid", fila=2, columna=0, sticky="ew", ipady=24)

    def crear_panel_pasajero(self):
        self.frame_pasajero = self.moldes.crear_frame(self.frame, tema.PANEL_SUAVE, tema.BORDE, 1, fila=6, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 0), (1, 1)))
        self.frame_pasajero.grid_remove()

    def crear_confirmacion(self):
        self.frame_confirmacion = self.moldes.crear_frame(self.frame, tema.FONDO, tema.BORDE, 1, fila=7, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1), (1, 1)))
        self.label_pregunta_confirmacion = self.moldes.crear_label(self.frame_confirmacion, "Confirmar viaje?", tema.FUENTE_BOTON, tema.TEXTO, tema.FONDO, 280, "left", metodo="grid", fila=0, columna=0, columnas=2, sticky="ew", margen_x=10, margen_y=(8, 6))
        self.boton_confirmar_viaje = self.moldes.crear_boton(self.frame_confirmacion, "Si, confirmar", True, None, self.presionar_confirmar_viaje, metodo="grid", fila=1, columna=0, sticky="ew", margen_x=(10, 4), margen_y=(0, 8))
        self.boton_cancelar_viaje = self.moldes.crear_boton(self.frame_confirmacion, "Cancelar", False, None, self.presionar_cancelar, metodo="grid", fila=1, columna=1, sticky="ew", margen_x=(4, 10), margen_y=(0, 8))
        self.label_estado_viaje = self.moldes.crear_label(self.frame_confirmacion, "", tema.FUENTE_BOTON, tema.PRIMARIO, tema.FONDO, metodo="grid", fila=0, columna=0, columnas=2, sticky="ew", margen_x=10, margen_y=10)
        self.label_estado_viaje.grid_remove()
        self.frame_confirmacion.grid_remove()

    def crear_progreso(self):
        progreso = self.moldes.crear_frame(self.frame, tema.PANEL, fila=8, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1),))
        self.label_estado_progreso = self.moldes.crear_label(progreso, "Progreso del trayecto", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w", margen_y=(0, 8))
        self.barra_progreso = ttk.Progressbar(progreso, maximum=100, mode="determinate", value=0)
        self.barra_progreso.grid(row=1, column=0, sticky="ew")
        self.label_porcentaje_progreso = self.moldes.crear_label(progreso, "0%", tema.FUENTE_BOTON, tema.PRIMARIO, tema.PANEL, metodo="grid", fila=2, columna=0, sticky="w", margen_y=(6, 0))

    def crear_boton_buscar_otro(self):
        self.boton_buscar_otro_viaje = self.moldes.crear_boton(self.frame, "Buscar otro viaje", True, None, self.presionar_cancelar, metodo="grid", fila=9, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10))
        self.boton_buscar_otro_viaje.grid_remove()

    def presionar_buscar_pasajero(self):
        self.ubicacion_inicial_busqueda = self.selector_ubicacion.get()
        self.info_pasajero_busqueda = self.controlador_viaje.buscar_pasajeros(self.ubicacion_inicial_busqueda)
        self.boton_buscar_pasajeros.config(state="disabled", cursor="arrow")
        self.selector_ubicacion.config(state="disabled")
        self.actualizar_cronometro_busqueda()

    def actualizar_cronometro_busqueda(self, segundos_transcurridos=0):
        duracion_busqueda = self.info_pasajero_busqueda["duracion_busqueda"]
        self.label_cronometro.config(text=f"00:{segundos_transcurridos:02d}")
        if segundos_transcurridos < duracion_busqueda:
            self.label_cronometro.after(1000, lambda: self.actualizar_cronometro_busqueda(segundos_transcurridos + 1))
            return
        self.mostrar_pasajero_encontrado()

    def mostrar_pasajero_encontrado(self):
        imagen = Image.open(RUTA_IMAGENES_USUARIOS / self.info_pasajero_busqueda["imagen"])
        imagen.thumbnail((64, 64))
        self.imagen_pasajero = ImageTk.PhotoImage(imagen)
        tk.Label(self.frame_pasajero, image=self.imagen_pasajero, bg=tema.PANEL_SUAVE).grid(row=0, column=0, rowspan=4, sticky="nw", padx=10, pady=10)

        llegada = f"Llegar: {self.info_pasajero_busqueda['km_para_llegar']} km | {self.info_pasajero_busqueda['tiempo_para_llegar']} s"
        traslado = f"Traslado: {self.info_pasajero_busqueda['km_transportando']} km | {self.info_pasajero_busqueda['tiempo_transportando']} s"
        self.moldes.crear_label(self.frame_pasajero, self.info_pasajero_busqueda["nombre_completo"], ("Arial", 12, "bold"), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=1, sticky="w", margen_x=8, margen_y=(10, 2))
        self.moldes.crear_label(self.frame_pasajero, self.info_pasajero_busqueda["trayecto"], ("Arial", 9), tema.TEXTO, tema.PANEL_SUAVE, 300, "left", metodo="grid", fila=1, columna=1, sticky="w", margen_x=8)
        self.moldes.crear_label(self.frame_pasajero, f"Vehiculo: {self.info_pasajero_busqueda['vehiculo']}", ("Arial", 9), tema.TEXTO_SUAVE, tema.PANEL_SUAVE, metodo="grid", fila=2, columna=1, sticky="w", margen_x=8)
        self.moldes.crear_label(self.frame_pasajero, f"Pago: ${self.info_pasajero_busqueda['precio']}", ("Arial", 9, "bold"), tema.PRIMARIO, tema.PANEL_SUAVE, metodo="grid", fila=3, columna=1, sticky="w", margen_x=8, margen_y=(0, 10))
        self.moldes.crear_label(self.frame_pasajero, llegada, ("Arial", 9), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=4, columna=0, columnas=2, sticky="w", margen_x=10, margen_y=(0, 2))
        self.moldes.crear_label(self.frame_pasajero, traslado, ("Arial", 9), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=5, columna=0, columnas=2, sticky="w", margen_x=10, margen_y=(0, 10))

        ruta_pasajero = self.controlador_viaje.formar_trayectoria(
            self.info_pasajero_busqueda["ubicacion_inicial"],
            self.info_pasajero_busqueda["ubicacion_final"],
        )
        self.mapa_viaje.dibujar_trayectoria(ruta_pasajero)
        self.frame_pasajero.grid()
        self.frame_confirmacion.grid()
        self.boton_volver.config(command=self.presionar_volver_pregunta_activa)

    def presionar_confirmar_viaje(self):
        if self.viaje_en_proceso:
            return

        self.viaje_en_proceso = True
        self.boton_confirmar_viaje.config(state="disabled", cursor="arrow")
        self.boton_cancelar_viaje.config(state="disabled", cursor="arrow")
        self.boton_buscar_pasajeros.config(state="disabled", cursor="arrow")
        self.selector_ubicacion.config(state="disabled")
        self.boton_volver.config(command=self.presionar_volver_flujo_activo)
        self.label_pregunta_confirmacion.grid_remove()
        self.boton_confirmar_viaje.grid_remove()
        self.boton_cancelar_viaje.grid_remove()
        self.label_estado_viaje.config(text="viaje en proceso")
        self.label_estado_viaje.grid()
        self.animacion_viaje.animacion_viaje_conductor(
            self.mapa_viaje.mapa,
            self.mapa_viaje.marcadores_lugares,
            RUTA_IMAGENES_USUARIOS,
            self.info_pasajero_busqueda,
            self.barra_progreso,
            self.label_estado_progreso,
            self.label_porcentaje_progreso,
            self.finalizar_viaje,
        )
        self.controlador_viaje.iniciar_viaje(
            self.ubicacion_inicial_busqueda,
            self.info_pasajero_busqueda,
            self.usuario_actual,
        )

    def finalizar_viaje(self):
        self.label_estado_viaje.config(text="viaje finalizado")
        self.boton_volver.config(command=self.comando_volver_menu)
        self.boton_buscar_otro_viaje.grid()

    def presionar_cancelar(self):
        self.navegar("viaje")

    def presionar_volver_pregunta_activa(self):
        messagebox.showwarning("Viaje pendiente", "Debo seleccionar una opcion.")

    def presionar_volver_flujo_activo(self):
        messagebox.showwarning("Viaje en proceso", "No se puede volver ya que hay un viaje en proceso.")
