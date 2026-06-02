from pathlib import Path
from tkinter import messagebox
from tkinter import ttk

from ..estilizacion import tema
from ..estilizacion.widgets import Moldes
from .animacion_viaje import AnimacionViaje
from .mapa_viaje import MapaViaje


RUTA_IMAGENES_CONDUCTORES = Path(__file__).resolve().parent.parent / "estilizacion" / "Imagenes" / "imagenes_conductores"

class VistaViajePasajero:
    """Vista principal del flujo de pasajero."""

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
        self.mapa_viaje = None
        self.acciones = AccionesBotonesPasajero(self)
        self.crear_widgets()

    def crear_widgets(self):
        contenedor = self.moldes.crear_frame(self.padre, tema.FONDO, llenar="both", expandir=True, margen_x=20, margen_y=20, columnas_peso=((0, 0), (1, 1)), filas_peso=((0, 1),))
        contenedor.grid_columnconfigure(0, minsize=420)
        contenedor.grid_columnconfigure(1, minsize=640)
        FrameIzquierdoPasajero(self).crear(contenedor)
        FrameDerechoPasajero(self).crear(contenedor)

    def finalizar_viaje(self):
        self.label_estado_viaje.config(text="viaje finalizado")
        self.boton_buscar_otro_viaje.grid()
        
class FrameIzquierdoPasajero:
    def __init__(self, vista):
        self.vista = vista
        self.moldes = vista.moldes

    def crear(self, padre):
        self.vista.frame = self.moldes.crear_frame(padre, tema.PANEL, tema.BORDE, 1, fila=0, columna=0, sticky="nsew", margen_x=(0, 12))
        self.vista.frame.grid_columnconfigure(0, weight=1)
        self.crear_cabecera()
        self.crear_servicio()
        self.crear_formulario()
        self.crear_busqueda_vehiculos()
        self.crear_boton_pagar()
        self.crear_confirmacion()
        self.crear_progreso()
        self.crear_boton_buscar_otro()

    def crear_cabecera(self):
        cabecera = self.moldes.crear_frame(self.vista.frame, tema.PANEL, fila=0, columna=0, sticky="ew", margen_x=16, margen_y=(16, 12), columnas_peso=((0, 1),))
        self.moldes.crear_label(cabecera, "Solicitud de viaje", ("Arial", 18, "bold"), tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")
        self.moldes.crear_boton(cabecera, "Volver", False, None, self.vista.comando_volver_menu, metodo="grid", fila=0, columna=1, sticky="e")

    def crear_servicio(self):
        self.moldes.crear_label(self.vista.frame, "Servicio", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=1, columna=0, sticky="w", margen_x=16, margen_y=(0, 4))
        self.moldes.crear_label(self.vista.frame, "Viaje normal", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=2, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), ipady=8)

    def crear_formulario(self):
        datos = self.moldes.crear_frame(self.vista.frame, tema.PANEL, fila=3, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1), (1, 1)))
        self.vista.selector_ubicacion_inicial = self.crear_selector_ubicacion(datos, "Ubicacion inicial", 0, 0, (0, 5))
        self.vista.selector_ubicacion_final = self.crear_selector_ubicacion(datos, "Ubicacion final", 0, 1, (5, 0))
        self.vista.selector_ubicacion_final.current(1)
        self.vista.entrada_usuarios = self.crear_campo(datos, "Cantidad usuarios", "1", 2, 0, 2)

    def crear_selector_ubicacion(self, padre, titulo, fila, columna, margen_x):
        apartado = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, tema.BORDE, 1, fila=fila, columna=columna, sticky="ew", margen_x=margen_x, margen_y=(0, 8), columnas_peso=((0, 1),))
        self.moldes.crear_label(apartado, titulo, ("Arial", 9, "bold"), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, sticky="w", margen_x=10, margen_y=(8, 4))
        lugares = self.vista.controlador_viaje.obtener_lugares_disponibles()
        return self.moldes.crear_selector(apartado, lugares, metodo="grid", fila=1, columna=0, sticky="ew", margen_x=10, margen_y=(0, 10), ipady=4)

    def crear_campo(self, padre, titulo, valor_inicial, fila, columna, columnas=1):
        campo = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, tema.BORDE, 1, fila=fila, columna=columna, columnas=columnas, sticky="ew", margen_y=(0, 0), columnas_peso=((0, 1),))
        self.moldes.crear_label(campo, titulo, ("Arial", 9, "bold"), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, sticky="w", margen_x=10, margen_y=(8, 4))
        entrada = self.moldes.crear_entrada(campo)
        entrada.insert(0, valor_inicial)
        entrada.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10), ipady=3)
        return entrada

    def crear_busqueda_vehiculos(self):
        contenedor = self.moldes.crear_frame(self.vista.frame, tema.PANEL, fila=4, columna=0, sticky="nsew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1),))
        self.vista.boton_buscar_vehiculos = self.moldes.crear_boton(contenedor, "Buscar vehiculos", True, None, self.vista.acciones.presionar_boton_buscar_vehiculos, metodo="grid", fila=0, columna=0, sticky="ew", margen_y=(0, 4))
        self.vista.label_error_busqueda = self.moldes.crear_label(contenedor, "", ("Arial", 9), tema.ERROR, tema.PANEL, 300, "left", metodo="grid", fila=1, columna=0, sticky="w", margen_y=(0, 8))
        self.vista.label_vehiculos_disponibles = self.moldes.crear_label(contenedor, "Vehiculos disponibles", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=2, columna=0, sticky="w", margen_y=(0, 6))
        self.vista.tabla_vehiculos = self.moldes.crear_tabla(contenedor, (("nombre", "Nombre", 105), ("detalle", "Detalle", 140), ("precio", "Precio", 80), ("tiempo", "Tiempo", 70)), 5, metodo="grid", fila=3, columna=0, sticky="nsew")
        self.vista.tabla_vehiculos.tag_configure("fila", background=tema.SECUNDARIO, foreground=tema.TEXTO)
        self.vista.tabla_vehiculos.bind("<<TreeviewSelect>>", self.vista.acciones.presionar_boton_seleccionar_vehiculo)

    def crear_boton_pagar(self):
        self.vista.boton_pagar = self.moldes.crear_boton(self.vista.frame, "Pagar viaje seleccionado", True, None, self.vista.acciones.presionar_boton_pagar, metodo="grid", fila=6, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10))
        self.vista.boton_pagar.grid_remove()

    def crear_confirmacion(self):
        self.vista.frame_confirmacion = self.moldes.crear_frame(self.vista.frame, tema.FONDO, tema.BORDE, 1, fila=7, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1), (1, 1)))
        self.vista.label_pregunta_confirmacion = self.moldes.crear_label(self.vista.frame_confirmacion, "Confirmar pago del viaje seleccionado?", tema.FUENTE_BOTON, tema.TEXTO, tema.FONDO, 280, "left", metodo="grid", fila=0, columna=0, columnas=2, sticky="ew", margen_x=10, margen_y=(8, 6))
        self.vista.boton_confirmar_pago = self.moldes.crear_boton(self.vista.frame_confirmacion, "Si, confirmar", True, None, self.vista.acciones.presionar_boton_confirmar_pago, metodo="grid", fila=1, columna=0, sticky="ew", margen_x=(10, 4), margen_y=(0, 8))
        self.vista.boton_cancelar_pago = self.moldes.crear_boton(self.vista.frame_confirmacion, "Cancelar", False, None, self.vista.acciones.presionar_boton_cancelar, metodo="grid", fila=1, columna=1, sticky="ew", margen_x=(4, 10), margen_y=(0, 8))
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


class FrameDerechoPasajero:
    def __init__(self, vista):
        self.vista = vista

    def crear(self, padre):
        try:
            self.vista.mapa_viaje = MapaViaje(padre, self.vista.moldes)
            self.vista.mapa_viaje.crear(False)
        except Exception as error:
            self.vista.mapa_viaje = None
            self.vista.boton_buscar_vehiculos.config(state="disabled", cursor="arrow")
            self.vista.label_error_busqueda.config(text=f"No se pudo cargar el mapa: {error}")


class AccionesBotonesPasajero:
    """Acciones de botones del pasajero, separadas de la construccion visual."""

    def __init__(self, vista):
        self.vista = vista

    def presionar_boton_buscar_vehiculos(self):
        vista = self.vista
        # La vista solo lee los campos; la validacion y la ruta quedan en el controlador.
        cantidad_usuarios = vista.entrada_usuarios.get()
        ubicacion_inicial = vista.selector_ubicacion_inicial.get()
        ubicacion_final = vista.selector_ubicacion_final.get()
        busqueda_exitosa = vista.controlador_viaje.buscar_vehiculos_pasajero(
            cantidad_usuarios,
            ubicacion_inicial,
            ubicacion_final,
        )

        if busqueda_exitosa is False:
            self.mostrar_error_busqueda(
                vista.controlador_viaje.obtener_error_busqueda_vehiculos()
            )
            return

        self.preparar_busqueda_exitosa(ubicacion_inicial, ubicacion_final)
        ruta = vista.controlador_viaje.obtener_ruta_busqueda_pasajero()
        if ruta is None:
            self.mostrar_error_busqueda(
                "No se pudo obtener la ruta profesional. Intenta nuevamente."
            )
            return

        self.mostrar_vehiculos()
        try:
            self.mostrar_trayecto_en_mapa(ruta)
            self.mostrar_conductores_en_mapa()
        except Exception as error:
            vista.label_error_busqueda.config(text=f"No se pudo mostrar el viaje en el mapa: {error}")

    def preparar_busqueda_exitosa(self, ubicacion_inicial, ubicacion_final):
        vista = self.vista
        # La vista conserva solo el estado visual que necesita para pintar tabla y mapa.
        vista.info_vehiculos_busqueda = vista.controlador_viaje.obtener_vehiculos_encontrados()
        vista.ubicacion_inicial_busqueda = ubicacion_inicial
        vista.ubicacion_final_busqueda = ubicacion_final
        vista.vehiculo_seleccionado = None
        vista.label_error_busqueda.config(text="")
        vista.frame_confirmacion.grid_remove()
        vista.boton_pagar.grid_remove()

    def mostrar_error_busqueda(self, mensaje):
        vista = self.vista
        # Limpia la interfaz de resultados cuando el controlador rechaza la busqueda.
        vista.label_error_busqueda.config(text=mensaje)
        vista.frame_confirmacion.grid_remove()
        vista.boton_pagar.grid_remove()
        self.limpiar_tabla_vehiculos()
        self.limpiar_mapa_busqueda()

    def presionar_boton_seleccionar_vehiculo(self, _evento=None):
        vista = self.vista
        seleccion = vista.tabla_vehiculos.selection()
        if not seleccion:
            return

        vehiculo = vista.vehiculos_por_item.get(seleccion[0])
        if vehiculo is None:
            return

        vista.vehiculo_seleccionado = vehiculo
        vista.frame_confirmacion.grid_remove()
        vista.boton_pagar.grid()

    def presionar_boton_pagar(self):
        if self.vista.vehiculo_seleccionado is None:
            return
        self.vista.frame_confirmacion.grid()

    def presionar_boton_confirmar_pago(self):
        vista = self.vista
        if vista.viaje_en_proceso or vista.vehiculo_seleccionado is None:
            return

        vista.label_error_busqueda.config(text="")
        # El controlador prepara rutas y cobra; la vista solo muestra el resultado.
        pago_confirmado = vista.controlador_viaje.confirmar_pago_pasajero(
            vista.usuario_actual,
            vista.vehiculo_seleccionado,
            vista.ubicacion_inicial_busqueda,
            vista.ubicacion_final_busqueda,
        )
        if pago_confirmado is False:
            self.mostrar_error_viaje(vista.controlador_viaje.obtener_error_viaje())
            return

        self.bloquear_formulario_en_viaje()
        try:
            vista.controlador_viaje.iniciar_viaje_pasajero_confirmado(
                vista.vehiculo_seleccionado,
                vista.usuario_actual,
            )
            self.iniciar_animacion_viaje(
                vista.controlador_viaje.obtener_rutas_viaje_pasajero(),
            )
        except Exception as error:
            vista.label_estado_viaje.config(text="No se pudo iniciar el viaje")
            vista.label_error_busqueda.config(text=f"No se pudo iniciar la animacion del viaje: {error}")

    def mostrar_error_viaje(self, mensaje):
        self.vista.label_error_busqueda.config(text=mensaje)

    def presionar_boton_cancelar(self):
        self.vista.navegar("viaje")

    def limpiar_tabla_vehiculos(self):
        vista = self.vista
        for item in vista.tabla_vehiculos.get_children():
            vista.tabla_vehiculos.delete(item)
        vista.vehiculos_por_item = {}

    def limpiar_mapa_busqueda(self):
        mapa = self.vista.mapa_viaje
        if mapa is None:
            return
        mapa.limpiar_conductores()
        mapa.limpiar_lugares()
        mapa.limpiar_trayectorias()

    def mostrar_vehiculos(self):
        vista = self.vista
        self.limpiar_tabla_vehiculos()
        for vehiculo in vista.info_vehiculos_busqueda:
            item = vista.tabla_vehiculos.insert("", "end", values=(vehiculo.nombre_completo, f"{vehiculo.vehiculo} | {vehiculo.patente} | {vehiculo.distancia} km", f"${vehiculo.precio}", f"{vehiculo.tiempo} s"), tags=("fila",))
            vista.vehiculos_por_item[item] = vehiculo

    def mostrar_conductores_en_mapa(self):
        vista = self.vista
        if vista.mapa_viaje is None:
            return
        vista.mapa_viaje.mostrar_conductores(vista.info_vehiculos_busqueda)
        vista.mapa_viaje.mostrar_lugares((vista.ubicacion_inicial_busqueda, vista.ubicacion_final_busqueda))

    def mostrar_trayecto_en_mapa(self, ruta):
        if self.vista.mapa_viaje is None:
            return
        self.vista.mapa_viaje.dibujar_trayectoria(ruta)

    def bloquear_formulario_en_viaje(self):
        vista = self.vista
        vista.viaje_en_proceso = True
        vista.boton_confirmar_pago.config(state="disabled", cursor="arrow")
        vista.boton_cancelar_pago.config(state="disabled", cursor="arrow")
        vista.boton_buscar_vehiculos.config(state="disabled", cursor="arrow")
        vista.boton_pagar.config(state="disabled", cursor="arrow")
        vista.boton_pagar.grid_remove()
        vista.selector_ubicacion_inicial.config(state="disabled")
        vista.selector_ubicacion_final.config(state="disabled")
        vista.entrada_usuarios.config(state="disabled")
        vista.tabla_vehiculos.config(selectmode="none")
        vista.label_pregunta_confirmacion.grid_remove()
        vista.boton_confirmar_pago.grid_remove()
        vista.boton_cancelar_pago.grid_remove()
        vista.label_estado_viaje.config(text="viaje en proceso")
        vista.label_estado_viaje.grid()

    def iniciar_animacion_viaje(self, rutas_viaje):
        vista = self.vista
        if vista.mapa_viaje is None:
            messagebox.showerror("No se pudo iniciar el viaje", "El mapa no esta disponible.")
            return

        vista.mapa_viaje.limpiar_lugares()
        vista.mapa_viaje.limpiar_trayectorias()
        vista.animacion_viaje.animacion_viaje_pasajero(vista.mapa_viaje.mapa, vista.mapa_viaje.marcadores_conductores, RUTA_IMAGENES_CONDUCTORES, vista.vehiculo_seleccionado, rutas_viaje, vista.barra_progreso, vista.label_estado_progreso, vista.label_porcentaje_progreso, vista.finalizar_viaje)
