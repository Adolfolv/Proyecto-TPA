from pathlib import Path
from tkinter import ttk

from Servicios.Viajes.datos_viaje import LUGARES_OSORNO

from Servicios.Viajes.animacion_viaje import AnimacionViaje
from ..estilizacion import tema
from ..estilizacion.widgets import Moldes
from .mapa_viaje import MapaViaje


RUTA_IMAGENES_CONDUCTORES = Path(__file__).resolve().parent.parent / "estilizacion" / "Imagenes" / "imagenes_conductores"


class VistaViajePasajero:
    def __init__(self, padre, navegar, comando_volver_menu, controlador_viaje, usuario_actual):
        self.padre = padre
        self.navegar = navegar
        self.comando_volver_menu = comando_volver_menu
        self.controlador_viaje = controlador_viaje
        self.usuario_actual = usuario_actual
        self.animacion_viaje = AnimacionViaje()
        self.moldes = Moldes()
        self.info_vehiculos_busqueda = []
        self.vehiculos_por_item = {}
        self.vehiculo_seleccionado = None
        self.viaje_en_proceso = False
        self.crear_widgets()

    def crear_widgets(self):
        contenedor = self.moldes.crear_frame(self.padre, tema.FONDO, llenar="both", expandir=True, margen_x=20, margen_y=20, columnas_peso=((0, 0), (1, 1)), filas_peso=((0, 1),))
        contenedor.grid_columnconfigure(0, minsize=420)
        contenedor.grid_columnconfigure(1, minsize=640)
        self.crear_panel_izquierdo(contenedor)
        self.mapa_viaje = MapaViaje(contenedor, self.moldes)
        self.mapa_viaje.crear(False)

    def crear_panel_izquierdo(self, padre):
        self.frame = self.moldes.crear_frame(padre, tema.PANEL, tema.BORDE, 1, fila=0, columna=0, sticky="nsew", margen_x=(0, 12))
        self.frame.grid_columnconfigure(0, weight=1)
        self.crear_cabecera()
        self.crear_servicio()
        self.crear_formulario()
        self.crear_busqueda_vehiculos()
        self.crear_boton_pagar()
        self.crear_confirmacion()
        self.crear_progreso()
        self.crear_boton_buscar_otro()

    def crear_cabecera(self):
        cabecera = self.moldes.crear_frame(self.frame, tema.PANEL, fila=0, columna=0, sticky="ew", margen_x=16, margen_y=(16, 12), columnas_peso=((0, 1),))
        self.moldes.crear_label(cabecera, "Solicitud de viaje", ("Arial", 18, "bold"), tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")
        self.moldes.crear_boton(cabecera, "Volver", False, None, self.comando_volver_menu, metodo="grid", fila=0, columna=1, sticky="e")

    def crear_servicio(self):
        self.moldes.crear_label(self.frame, "Servicio", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=1, columna=0, sticky="w", margen_x=16, margen_y=(0, 4))
        self.moldes.crear_label(self.frame, "Viaje normal", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=2, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), ipady=8)

    def crear_formulario(self):
        datos = self.moldes.crear_frame(self.frame, tema.PANEL, fila=3, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1), (1, 1)))
        self.selector_ubicacion_inicial = self.crear_selector_ubicacion(datos, "Ubicacion inicial", 0, 0, (0, 5))
        self.selector_ubicacion_final = self.crear_selector_ubicacion(datos, "Ubicacion final", 0, 1, (5, 0))
        self.selector_ubicacion_final.current(1)
        self.entrada_usuarios = self.crear_campo(datos, "Cantidad usuarios", "1", 2, 0, 2)

    def crear_selector_ubicacion(self, padre, titulo, fila, columna, margen_x):
        apartado = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, tema.BORDE, 1, fila=fila, columna=columna, sticky="ew", margen_x=margen_x, margen_y=(0, 8), columnas_peso=((0, 1),))
        self.moldes.crear_label(apartado, titulo, ("Arial", 9, "bold"), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, sticky="w", margen_x=10, margen_y=(8, 4))
        selector = self.moldes.crear_selector(apartado, tuple(LUGARES_OSORNO), metodo="grid", fila=1, columna=0, sticky="ew", margen_x=10, margen_y=(0, 10), ipady=4)
        return selector

    def crear_campo(self, padre, titulo, valor_inicial, fila, columna, columnas=1):
        campo = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, tema.BORDE, 1, fila=fila, columna=columna, columnas=columnas, sticky="ew", margen_y=(0, 0), columnas_peso=((0, 1),))
        self.moldes.crear_label(campo, titulo, ("Arial", 9, "bold"), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, sticky="w", margen_x=10, margen_y=(8, 4))
        entrada = self.moldes.crear_entrada(campo)
        entrada.insert(0, valor_inicial)
        entrada.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10), ipady=3)
        return entrada

    def crear_busqueda_vehiculos(self):
        contenedor = self.moldes.crear_frame(self.frame, tema.PANEL, fila=4, columna=0, sticky="nsew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1),))
        self.boton_buscar_vehiculos = self.moldes.crear_boton(contenedor, "Buscar vehiculos", True, None, self.presionar_buscar_vehiculos, metodo="grid", fila=0, columna=0, sticky="ew", margen_y=(0, 4))
        self.label_error_busqueda = self.moldes.crear_label(contenedor, "", ("Arial", 9), tema.ERROR, tema.PANEL, 300, "left", metodo="grid", fila=1, columna=0, sticky="w", margen_y=(0, 8))
        self.label_vehiculos_disponibles = self.moldes.crear_label(contenedor, "Vehiculos disponibles", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=2, columna=0, sticky="w", margen_y=(0, 6))
        self.tabla_vehiculos = self.moldes.crear_tabla(contenedor, (("nombre", "Nombre", 105), ("detalle", "Detalle", 140), ("precio", "Precio", 80), ("tiempo", "Tiempo", 70)), 5, metodo="grid", fila=3, columna=0, sticky="nsew")
        self.tabla_vehiculos.tag_configure("fila", background=tema.SECUNDARIO, foreground=tema.TEXTO)
        self.tabla_vehiculos.bind("<<TreeviewSelect>>", self.presionar_seleccionar_vehiculo)

    def crear_confirmacion(self):
        self.frame_confirmacion = self.moldes.crear_frame(self.frame, tema.FONDO, tema.BORDE, 1, fila=7, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1), (1, 1)))
        self.label_pregunta_confirmacion = self.moldes.crear_label(self.frame_confirmacion, "Confirmar pago del viaje seleccionado?", tema.FUENTE_BOTON, tema.TEXTO, tema.FONDO, 280, "left", metodo="grid", fila=0, columna=0, columnas=2, sticky="ew", margen_x=10, margen_y=(8, 6))
        self.boton_confirmar_pago = self.moldes.crear_boton(self.frame_confirmacion, "Si, confirmar", True, None, self.presionar_confirmar_pago, metodo="grid", fila=1, columna=0, sticky="ew", margen_x=(10, 4), margen_y=(0, 8))
        self.boton_cancelar_pago = self.moldes.crear_boton(self.frame_confirmacion, "Cancelar", False, None, self.presionar_cancelar, metodo="grid", fila=1, columna=1, sticky="ew", margen_x=(4, 10), margen_y=(0, 8))
        self.label_estado_viaje = self.moldes.crear_label(self.frame_confirmacion, "", tema.FUENTE_BOTON, tema.PRIMARIO, tema.FONDO, metodo="grid", fila=0, columna=0, columnas=2, sticky="ew", margen_x=10, margen_y=10)
        self.label_estado_viaje.grid_remove()
        self.frame_confirmacion.grid_remove()

    def crear_boton_pagar(self):
        self.boton_pagar = self.moldes.crear_boton(self.frame, "Pagar viaje seleccionado", True, None, self.presionar_pagar, metodo="grid", fila=6, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10))
        self.boton_pagar.grid_remove()

    def crear_progreso(self):
        progreso = self.moldes.crear_frame(self.frame, tema.PANEL, fila=8, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1),))
        self.label_estado_progreso = self.moldes.crear_label(progreso, "Progreso del trayecto", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w", margen_y=(0, 8))
        self.barra_progreso = ttk.Progressbar(progreso, maximum=100, mode="determinate", value=0)
        self.barra_progreso.grid(row=1, column=0, sticky="ew")
        self.label_porcentaje_progreso = self.moldes.crear_label(progreso, "0%", tema.FUENTE_BOTON, tema.PRIMARIO, tema.PANEL, metodo="grid", fila=2, columna=0, sticky="w", margen_y=(6, 0))

    def crear_boton_buscar_otro(self):
        self.boton_buscar_otro_viaje = self.moldes.crear_boton(self.frame, "Buscar otro viaje", True, None, self.presionar_cancelar, metodo="grid", fila=9, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10))
        self.boton_buscar_otro_viaje.grid_remove()

    def presionar_buscar_vehiculos(self):
        cantidad_usuarios = self.entrada_usuarios.get()
        ubicacion_inicial = self.selector_ubicacion_inicial.get()
        ubicacion_final = self.selector_ubicacion_final.get()
        resultado = self.controlador_viaje.buscar_vehiculos(
            cantidad_usuarios,
            ubicacion_inicial,
            ubicacion_final,
        )

        if not resultado["ok"]:
            self.label_error_busqueda.config(text=resultado["error"])
            self.frame_confirmacion.grid_remove()
            self.boton_pagar.grid_remove()
            self.limpiar_tabla_vehiculos()
            self.mapa_viaje.limpiar_conductores()
            self.mapa_viaje.limpiar_lugares()
            self.mapa_viaje.limpiar_trayectorias()
            return

        self.info_vehiculos_busqueda = resultado["vehiculos"]
        self.ubicacion_inicial_busqueda = ubicacion_inicial
        self.ubicacion_final_busqueda = ubicacion_final
        self.vehiculo_seleccionado = None
        self.label_error_busqueda.config(text="")
        self.frame_confirmacion.grid_remove()
        self.boton_pagar.grid_remove()
        ruta = self.formar_trayecto_busqueda()
        if ruta is None:
            self.limpiar_tabla_vehiculos()
            self.mapa_viaje.limpiar_conductores()
            self.mapa_viaje.limpiar_lugares()
            self.mapa_viaje.limpiar_trayectorias()
            return

        self.mostrar_vehiculos()
        self.mostrar_trayecto_en_mapa(ruta)
        self.mostrar_conductores_en_mapa()

    def mostrar_vehiculos(self):
        self.limpiar_tabla_vehiculos()

        for vehiculo in self.info_vehiculos_busqueda:
            item = self.tabla_vehiculos.insert(
                "",
                "end",
                values=(
                    vehiculo["nombre_completo"],
                    f"{vehiculo['vehiculo']} | {vehiculo['patente']} | {vehiculo['distancia']} km",
                    f"${vehiculo['precio']}",
                    f"{vehiculo['tiempo']} s",
                ),
                tags=("fila",),
            )
            self.vehiculos_por_item[item] = vehiculo

    def limpiar_tabla_vehiculos(self):
        for item in self.tabla_vehiculos.get_children():
            self.tabla_vehiculos.delete(item)
        self.vehiculos_por_item = {}

    def mostrar_conductores_en_mapa(self):
        self.mapa_viaje.mostrar_conductores(self.info_vehiculos_busqueda)
        self.mapa_viaje.mostrar_lugares((self.ubicacion_inicial_busqueda, self.ubicacion_final_busqueda))

    def formar_trayecto_busqueda(self):
        try:
            return self.controlador_viaje.formar_trayectoria(
                self.ubicacion_inicial_busqueda,
                self.ubicacion_final_busqueda,
            )
        except Exception:
            self.label_error_busqueda.config(text="No se pudo obtener la ruta profesional. Intenta nuevamente.")
            return None

    def mostrar_trayecto_en_mapa(self, ruta):
        self.mapa_viaje.dibujar_trayectoria(ruta)

    def presionar_seleccionar_vehiculo(self, _evento=None):
        seleccion = self.tabla_vehiculos.selection()
        if not seleccion:
            return

        vehiculo = self.vehiculos_por_item.get(seleccion[0])
        if vehiculo is None:
            return

        self.vehiculo_seleccionado = vehiculo
        self.frame_confirmacion.grid_remove()
        self.boton_pagar.grid()

    def presionar_pagar(self):
        if self.vehiculo_seleccionado is None:
            return

        self.frame_confirmacion.grid()

    def presionar_confirmar_pago(self):
        if self.viaje_en_proceso:
            return

        if self.vehiculo_seleccionado is None:
            return

        self.label_error_busqueda.config(text="")
        rutas_viaje = self.formar_rutas_inicio_viaje()
        if rutas_viaje is None:
            return

        self.controlador_viaje.pagar_pasajero(
                self.usuario_actual,
                self.vehiculo_seleccionado["precio"],
            )
        

        self.viaje_en_proceso = True
        self.boton_confirmar_pago.config(state="disabled", cursor="arrow")
        self.boton_cancelar_pago.config(state="disabled", cursor="arrow")
        self.boton_buscar_vehiculos.config(state="disabled", cursor="arrow")
        self.boton_pagar.config(state="disabled", cursor="arrow")
        self.boton_pagar.grid_remove()
        self.selector_ubicacion_inicial.config(state="disabled")
        self.selector_ubicacion_final.config(state="disabled")
        self.entrada_usuarios.config(state="disabled")
        self.tabla_vehiculos.config(selectmode="none")
        self.label_pregunta_confirmacion.grid_remove()
        self.boton_confirmar_pago.grid_remove()
        self.boton_cancelar_pago.grid_remove()
        self.label_estado_viaje.config(text="viaje en proceso")
        self.label_estado_viaje.grid()
        self.iniciar_animacion_viaje(rutas_viaje)
 
    def formar_rutas_inicio_viaje(self):
        try:
            ruta_llegada = self.controlador_viaje.formar_trayectoria_por_puntos(
                self.vehiculo_seleccionado["ubicacion_relativa"],
                LUGARES_OSORNO[self.ubicacion_inicial_busqueda],
            )
            ruta_viaje = self.controlador_viaje.formar_trayectoria(
                self.ubicacion_inicial_busqueda,
                self.ubicacion_final_busqueda,
            )
            return {
                "llegada": ruta_llegada,
                "viaje": ruta_viaje,
            }
        except Exception:
            self.label_error_busqueda.config(text="No se pudo iniciar la ruta profesional. Intenta nuevamente.")
            return None

    def iniciar_animacion_viaje(self, rutas_viaje):
        self.mapa_viaje.limpiar_lugares()
        self.mapa_viaje.limpiar_trayectorias()
        self.animacion_viaje.animacion_viaje_pasajero(
            self.mapa_viaje.mapa,
            self.mapa_viaje.marcadores_conductores,
            RUTA_IMAGENES_CONDUCTORES,
            self.vehiculo_seleccionado,
            self.ubicacion_inicial_busqueda,
            self.ubicacion_final_busqueda,
            self.barra_progreso,
            self.label_estado_progreso,
            self.label_porcentaje_progreso,
            self.finalizar_viaje,
            rutas_viaje["llegada"],
            rutas_viaje["viaje"],
        )

    def finalizar_viaje(self):
        self.label_estado_viaje.config(text="viaje finalizado")
        self.boton_buscar_otro_viaje.grid()

    def presionar_cancelar(self):
        self.navegar("viaje")
