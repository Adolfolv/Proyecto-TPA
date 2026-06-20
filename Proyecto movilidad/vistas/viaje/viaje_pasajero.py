from tkinter import ttk

from ..estilizacion import tema
from ..estilizacion.widgets import Moldes
from .estado_visual_pasajero import EstadoVisualPasajero
from .mapa_viaje import MapaViajePasajero
from .renderizador_pasajero import RenderizadorPasajero


class VistaViajePasajero:
    """Vista principal del flujo de pasajero."""

    def __init__(self, padre, navegar, comando_volver_menu, controlador_pasajero, usuario_actual):
        self.padre = padre
        self.navegar = navegar
        self.comando_volver_menu = comando_volver_menu
        self.controlador_pasajero = controlador_pasajero
        self.usuario_actual = usuario_actual
        self.moldes = Moldes()
        # State visual: controla que botones/paneles se muestran segun el flujo.
        self.estado_visual = EstadoVisualPasajero(self)
        # Renderizador: pinta datos en tabla, mapa y labels sin decidir la logica.
        self.renderizador = RenderizadorPasajero(self)
        self.acciones = AccionesBotonesPasajero(self)
        self.crear_widgets()

    def crear_widgets(self):
        contenedor = self.moldes.crear_frame(self.padre, tema.FONDO, llenar="both", expandir=True, margen_x=20, margen_y=20, columnas_peso=((0, 0), (1, 1)), filas_peso=((0, 1),))
        contenedor.grid_columnconfigure(0, minsize=420)
        contenedor.grid_columnconfigure(1, minsize=640)
        PanelIzquierdoPasajero(self).crear(contenedor)
        PanelDerechoPasajero(self).crear(contenedor)

    def finalizar_viaje(self):
        self.renderizador.mostrar_estado_viaje("viaje finalizado")
        self.estado_visual.viaje_finalizado()
        
class PanelIzquierdoPasajero:
    def __init__(self, vista):
        self.vista = vista
        self.moldes = vista.moldes

    def crear(self, padre):
        self.vista.panel = self.moldes.crear_frame(padre, tema.PANEL, tema.BORDE, 1, fila=0, columna=0, sticky="nsew", margen_x=(0, 12))
        self.vista.panel.grid_columnconfigure(0, weight=1)
        self.crear_cabecera()
        self.crear_servicio()
        self.crear_formulario()
        self.crear_busqueda_vehiculos()
        self.crear_boton_pagar()
        self.crear_confirmacion()
        self.crear_progreso()
        self.crear_boton_buscar_otro()

    def crear_cabecera(self):
        cabecera = self.moldes.crear_frame(self.vista.panel, tema.PANEL, fila=0, columna=0, sticky="ew", margen_x=16, margen_y=(16, 12), columnas_peso=((0, 1),))
        self.moldes.crear_label(cabecera, "Solicitud de viaje", ("Arial", 18, "bold"), tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")
        self.moldes.crear_boton(cabecera, "Volver", False, None, self.vista.comando_volver_menu, metodo="grid", fila=0, columna=1, sticky="e")

    def crear_servicio(self):
        self.moldes.crear_label(self.vista.panel, "Servicio", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=1, columna=0, sticky="w", margen_x=16, margen_y=(0, 4))
        self.moldes.crear_label(self.vista.panel, "Viaje normal", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=2, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), ipady=8)

    def crear_formulario(self):
        datos = self.moldes.crear_frame(self.vista.panel, tema.PANEL, fila=3, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1), (1, 1)))
        self.vista.selector_ubicacion_inicial = self.crear_selector_ubicacion(datos, "Ubicacion inicial", 0, 0, (0, 5))
        self.vista.selector_ubicacion_final = self.crear_selector_ubicacion(datos, "Ubicacion final", 0, 1, (5, 0))
        self.vista.selector_ubicacion_final.current(1)
        self.vista.entrada_usuarios = self.crear_campo(datos, "Cantidad usuarios", "1", 2, 0, 2)

    def crear_selector_ubicacion(self, padre, titulo, fila, columna, margen_x):
        apartado = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, tema.BORDE, 1, fila=fila, columna=columna, sticky="ew", margen_x=margen_x, margen_y=(0, 8), columnas_peso=((0, 1),))
        self.moldes.crear_label(apartado, titulo, ("Arial", 9, "bold"), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, sticky="w", margen_x=10, margen_y=(8, 4))
        lugares = self.vista.controlador_pasajero.obtener_lugares_disponibles()
        return self.moldes.crear_selector(apartado, lugares, metodo="grid", fila=1, columna=0, sticky="ew", margen_x=10, margen_y=(0, 10), ipady=4)

    def crear_campo(self, padre, titulo, valor_inicial, fila, columna, columnas=1):
        campo = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, tema.BORDE, 1, fila=fila, columna=columna, columnas=columnas, sticky="ew", margen_y=(0, 0), columnas_peso=((0, 1),))
        self.moldes.crear_label(campo, titulo, ("Arial", 9, "bold"), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, sticky="w", margen_x=10, margen_y=(8, 4))
        entrada = self.moldes.crear_entrada(campo)
        entrada.insert(0, valor_inicial)
        entrada.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10), ipady=3)
        return entrada

    def crear_busqueda_vehiculos(self):
        contenedor = self.moldes.crear_frame(self.vista.panel, tema.PANEL, fila=4, columna=0, sticky="nsew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1),))
        self.vista.boton_buscar_vehiculos = self.moldes.crear_boton(contenedor, "Buscar vehiculos", True, None, self.vista.acciones.presionar_boton_buscar_vehiculos, metodo="grid", fila=0, columna=0, sticky="ew", margen_y=(0, 4))
        self.vista.label_error_busqueda = self.moldes.crear_label(contenedor, "", ("Arial", 9), tema.ERROR, tema.PANEL, 300, "left", metodo="grid", fila=1, columna=0, sticky="w", margen_y=(0, 8))
        self.vista.label_vehiculos_disponibles = self.moldes.crear_label(contenedor, "Vehiculos disponibles", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=2, columna=0, sticky="w", margen_y=(0, 6))
        self.vista.tabla_vehiculos = self.moldes.crear_tabla(contenedor, (("nombre", "Nombre", 105), ("detalle", "Detalle", 140), ("precio", "Precio", 80), ("tiempo", "Tiempo", 70)), 5, metodo="grid", fila=3, columna=0, sticky="nsew")
        self.vista.tabla_vehiculos.tag_configure("fila", background=tema.SECUNDARIO, foreground=tema.TEXTO)
        self.vista.tabla_vehiculos.bind("<<TreeviewSelect>>", self.vista.acciones.presionar_boton_seleccionar_vehiculo)

    def crear_boton_pagar(self):
        self.vista.boton_pagar = self.moldes.crear_boton(self.vista.panel, "Pagar viaje seleccionado", True, None, self.vista.acciones.presionar_boton_pagar, metodo="grid", fila=6, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10))
        self.vista.boton_pagar.grid_remove()

    def crear_confirmacion(self):
        self.vista.panel_confirmacion = self.moldes.crear_frame(self.vista.panel, tema.FONDO, tema.BORDE, 1, fila=7, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1), (1, 1)))
        self.vista.label_pregunta_confirmacion = self.moldes.crear_label(self.vista.panel_confirmacion, "Confirmar pago del viaje seleccionado?", tema.FUENTE_BOTON, tema.TEXTO, tema.FONDO, 280, "left", metodo="grid", fila=0, columna=0, columnas=2, sticky="ew", margen_x=10, margen_y=(8, 6))
        self.vista.boton_confirmar_pago = self.moldes.crear_boton(self.vista.panel_confirmacion, "Si, confirmar", True, None, self.vista.acciones.presionar_boton_confirmar_pago, metodo="grid", fila=1, columna=0, sticky="ew", margen_x=(10, 4), margen_y=(0, 8))
        self.vista.boton_cancelar_pago = self.moldes.crear_boton(self.vista.panel_confirmacion, "Cancelar", False, None, self.vista.acciones.presionar_boton_cancelar, metodo="grid", fila=1, columna=1, sticky="ew", margen_x=(4, 10), margen_y=(0, 8))
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


class PanelDerechoPasajero:
    def __init__(self, vista):
        self.vista = vista

    def crear(self, padre):
        self.vista.mapa_viaje = MapaViajePasajero(padre, self.vista.moldes)
        self.vista.mapa_viaje.crear(False)


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
        vista.vehiculo_seleccionado = None
        vista.estado_visual.reiniciar_busqueda()
        resultado = vista.controlador_pasajero.buscar_vehiculos_pasajero(
            cantidad_usuarios,
            ubicacion_inicial,
            ubicacion_final,
        )

        if not resultado.exitoso:
            vista.renderizador.mostrar_mensaje_error(resultado.error)
            vista.renderizador.limpiar_tabla_vehiculos()
            vista.vehiculos_por_item = {}
            vista.mapa_viaje.limpiar_busqueda()
            return

        vista.info_vehiculos_busqueda = resultado.vehiculos
        vista.ubicacion_inicial_busqueda = ubicacion_inicial
        vista.ubicacion_final_busqueda = ubicacion_final
        vista.renderizador.mostrar_mensaje_error("")
        vista.vehiculos_por_item = vista.renderizador.mostrar_vehiculos()
        vista.mapa_viaje.mostrar_busqueda_pasajero(
            vista.info_vehiculos_busqueda,
            ubicacion_inicial,
            ubicacion_final,
            resultado.ruta_busqueda,
        )

    def presionar_boton_seleccionar_vehiculo(self, _evento=None):
        vista = self.vista
        seleccion = vista.tabla_vehiculos.selection()
        if not seleccion:
            return

        vista.vehiculo_seleccionado = vista.vehiculos_por_item[seleccion[0]]
        vista.estado_visual.vehiculo_seleccionado()

    def presionar_boton_pagar(self):
        self.vista.estado_visual.confirmando_pago()

    def presionar_boton_confirmar_pago(self):
        vista = self.vista
        vista.renderizador.mostrar_mensaje_error("")
        # El controlador prepara rutas y cobra; la vista solo muestra el resultado.
        resultado = vista.controlador_pasajero.confirmar_pago_pasajero(
            vista.usuario_actual,
            vista.vehiculo_seleccionado,
            vista.ubicacion_inicial_busqueda,
            vista.ubicacion_final_busqueda,
        )
        {
            True: self.iniciar_viaje_confirmado,
            False: self.mostrar_error_confirmacion,
        }[resultado.exitoso](resultado)

    def iniciar_viaje_confirmado(self, resultado):
        vista = self.vista
        # Desde aqui se bloquea la pantalla hasta que termine la animacion.
        vista.renderizador.mostrar_estado_viaje("viaje en proceso")
        vista.estado_visual.viaje_en_proceso()
        self.iniciar_animacion_viaje(resultado.rutas_viaje)

    def mostrar_error_confirmacion(self, resultado):
        self.vista.renderizador.mostrar_mensaje_error(resultado.error)

    def presionar_boton_cancelar(self):
        self.vista.navegar("viaje")

    def iniciar_animacion_viaje(self, rutas_viaje):
        vista = self.vista
        # La animacion recibe rutas ya calculadas; el mapa se encarga de pintarlas.
        vista.mapa_viaje.animar_viaje_pasajero(
            vista.vehiculo_seleccionado,
            rutas_viaje,
            vista.renderizador.actualizar_progreso_viaje,
            vista.finalizar_viaje,
        )
