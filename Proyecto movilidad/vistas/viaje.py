"""Vista de viaje separada por responsabilidades.

Flujo numerado desde que se abre la pantalla viaje:
1. Navegacion crea VistaViaje y le entrega usuario, controlador y callbacks.
2. VistaViaje arma el contenedor principal.
3. PanelViaje crea el panel izquierdo: formulario, busqueda, pasajero, confirmacion y progreso.
4. MapaViaje crea el mapa derecho, bloquea zoom y pinta lugares de Osorno.
5. Si el conductor presiona "Buscar pasajeros", FlujoConductor pide datos al controlador.
6. Se bloquea la busqueda y empieza el cronometro.
7. Cuando termina el cronometro, se muestra el pasajero y se dibuja su trayectoria.
8. Mientras hay pregunta activa, Volver muestra una advertencia.
9. Si el conductor confirma, se bloquean botones y se muestra "viaje en proceso".
10. AnimacionViaje mueve el marcador y actualiza la barra de progreso.
11. Cuando termina la animacion, se muestra "viaje finalizado".
12. Volver se habilita de nuevo y aparece "Buscar otro viaje" para reiniciar la pantalla.
"""

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

# --- componentes comunes del panel izquierdo ---

class ComponenteViaje:
    def __init__(self, panel):
        # Cada componente recibe el panel principal para reutilizar moldes,
        # tipo de usuario y callbacks sin repetir tantos parametros.
        self.panel = panel
        self.moldes = panel.moldes
        self.callbacks = panel.callbacks
        self.tipo_usuario = panel.tipo_usuario

class ProgresoViaje(ComponenteViaje):
    def crear(self):
        # Paso 10: crea la barra que se actualiza durante la animacion del viaje.
        progreso = self.moldes.crear_frame(self.panel.frame, tema.PANEL, fila=8, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 1),))
        self.label_estado = self.moldes.crear_label(progreso, "Progreso del trayecto", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w", margen_y=(0, 8))
        self.barra = ttk.Progressbar(progreso, maximum=100, mode="determinate", value=0)
        self.barra.grid(row=1, column=0, sticky="ew")
        self.label_porcentaje = self.moldes.crear_label(progreso, "0%", tema.FUENTE_BOTON, tema.PRIMARIO, tema.PANEL, metodo="grid", fila=2, columna=0, sticky="w", margen_y=(6, 0))

class FormularioViaje(ComponenteViaje):
    def crear(self):
        # Paso 3: para conductor se muestra solo el selector de ubicacion inicial.
        # Para pasajero quedan los campos base de solicitud.
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
        # Paso 5: se lee cuando se presiona "Buscar pasajeros".
        return self.selector_ubicacion.get()

    def bloquear(self):
        # Paso 6: evita cambiar la ubicacion mientras hay busqueda/viaje activo.
        self.selector_ubicacion.config(state="disabled")

class GrupoBotonesViaje(ComponenteViaje):
    pass

class BotonesCabeceraViaje(GrupoBotonesViaje):
    def crear(self):
        # Paso 3: boton Volver normal; al inicio vuelve al menu.
        # Durante pregunta/viaje activo se cambia por avisos.
        cabecera = self.moldes.crear_frame(self.panel.frame, tema.PANEL, fila=0, columna=0, sticky="ew", margen_x=16, margen_y=(16, 12), columnas_peso=((0, 1),))
        self.moldes.crear_label(cabecera, "Solicitud de viaje", ("Arial", 18, "bold"), tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")
        self.boton_volver = self.moldes.crear_boton(cabecera, "Volver", False, None, self.callbacks["volver_menu"], metodo="grid", fila=0, columna=1, sticky="e")

    def cambiar_volver(self, comando):
        # Pasos 8 y 12: permite cambiar que hace Volver segun el estado.
        self.boton_volver.config(command=comando)

class BotonesBusquedaViaje(GrupoBotonesViaje):
    def crear(self):
        # Paso 3: en conductor crea el boton para buscar pasajeros y el cronometro.
        # En pasajero deja preparada la parte visual de vehiculos.
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
        # Paso 6: al empezar la busqueda se deshabilita para no buscar dos veces.
        self.boton_buscar_pasajeros.config(state="disabled", cursor="arrow")

class BotonesConfirmacionViaje(GrupoBotonesViaje):
    def crear(self):
        # Paso 3: este frame primero pregunta si confirma el viaje.
        # Luego se reutiliza para mostrar "viaje en proceso/finalizado".
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
        # Paso 9: protege contra dobles clicks en confirmar/cancelar.
        self.boton_confirmar.config(state="disabled", cursor="arrow")
        self.boton_cancelar.config(state="disabled", cursor="arrow")

    def mostrar_estado_en_proceso(self):
        # Paso 9: reemplaza la pregunta y botones por el texto de estado.
        self.label_pregunta.grid_remove()
        self.boton_confirmar.grid_remove()
        self.boton_cancelar.grid_remove()
        self.label_estado.config(text="viaje en proceso")
        self.label_estado.grid()

    def mostrar_estado_finalizado(self):
        # Paso 11: la animacion avisa cuando termina y el label cambia a finalizado.
        self.label_estado.config(text="viaje finalizado")

class BotonesBuscarOtroViaje(GrupoBotonesViaje):
    def crear(self):
        # Paso 3: permanece oculto hasta que el viaje finaliza.
        self.boton_buscar_otro = self.moldes.crear_boton(self.panel.frame, "Buscar otro viaje", True, None, self.callbacks["cancelar"], metodo="grid", fila=9, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10))
        self.boton_buscar_otro.grid_remove()

    def mostrar_estado_finalizado(self):
        # Paso 12: al presionarlo se navega de nuevo a viaje y se reinicia todo.
        self.boton_buscar_otro.grid()

class BotonesViaje(ComponenteViaje):
    # Agrupa todos los botones para que PanelViaje no hable con cada uno suelto.
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
        # Paso 3: panel izquierdo; contiene formulario, botones, pasajero y progreso.
        self.padre = padre
        self.moldes = moldes
        self.tipo_usuario = tipo_usuario
        self.callbacks = callbacks

    def crear(self):
        # Paso 3: se crean los componentes en el mismo orden visual del frame izquierdo.
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
        # Muestra el tipo de servicio fijo que se esta simulando.
        self.moldes.crear_label(self.frame, "Servicio", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=1, columna=0, sticky="w", margen_x=16, margen_y=(0, 4))
        self.moldes.crear_label(self.frame, "Viaje normal", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=2, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), ipady=8)

    def mostrar_pasajero(self, datos_pasajero):
        # Paso 7: cuando termina el cronometro, se muestra el pasajero y la confirmacion.
        self.panel_pasajero.mostrar(datos_pasajero)
        self.botones.frame_confirmacion.grid()

    def bloquear_busqueda(self):
        # Bloquea lo necesario durante la busqueda.
        self.botones.bloquear_busqueda()
        self.formulario.bloquear()

    def bloquear_confirmacion(self):
        # Bloquea lo necesario cuando el viaje ya fue confirmado.
        self.botones.bloquear_confirmacion()
        self.formulario.bloquear()

    def mostrar_estado_en_proceso(self):
        # Cambia el frame de confirmacion a "viaje en proceso".
        self.botones.mostrar_estado_en_proceso()

    def mostrar_estado_finalizado(self):
        # Cambia el estado a finalizado y muestra "Buscar otro viaje".
        self.botones.mostrar_estado_finalizado()

    def cambiar_volver(self, comando):
        self.botones.cambiar_volver(comando)

    def obtener_ubicacion_inicial(self):
        # El flujo conductor usa este dato para pedir pasajeros al controlador.
        return self.formulario.obtener_ubicacion_inicial()
    
class VistaViaje(tk.Frame):
    def __init__(self, master, navegar, tipo_usuario, comando_volver_menu, controlador_viaje, usuario_actual):
        # Paso 1: Navegacion entrega todo lo que la vista necesita para funcionar.
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
        # Paso 2: VistaViaje arma dos zonas: panel izquierdo y mapa derecho.
        contenedor = self.moldes.crear_frame(self, tema.FONDO, llenar="both", expandir=True, margen_x=20, margen_y=20, columnas_peso=((0, 0), (1, 1)), filas_peso=((0, 1),))
        contenedor.grid_columnconfigure(0, minsize=420)
        contenedor.grid_columnconfigure(1, minsize=640)
        # Paso 2: los callbacks conectan botones con metodos de esta vista.
        callbacks = {"volver_menu": self.comando_volver_menu, "buscar_pasajero": self.presionar_buscar_pasajero, "confirmar_viaje": self.presionar_confirmar_viaje, "cancelar": self.presionar_cancelar}
        self.panel = PanelViaje(contenedor, self.moldes, self.tipo_usuario, callbacks)
        self.panel.crear()
        self.mapa_viaje = MapaViaje(contenedor, self.moldes)
        self.mapa_viaje.crear()
        self.flujo_conductor = FlujoConductor(self, self.panel, self.mapa_viaje)

    def presionar_buscar_pasajero(self):
        # Paso 5: el boton delega la busqueda a FlujoConductor.
        self.flujo_conductor.presionar_buscar_pasajero()

    def presionar_confirmar_viaje(self):
        # Paso 9: el boton confirmar delega el inicio del viaje a FlujoConductor.
        self.flujo_conductor.presionar_confirmar_viaje()

    def presionar_cancelar(self):
        # Paso 12: cancelar o buscar otro viaje recrea la pantalla desde cero.
        self.navegar("viaje")

    def presionar_volver_pregunta_activa(self):
        messagebox.showwarning("Viaje pendiente", "Debo seleccionar una opcion.")

    def presionar_volver_flujo_activo(self):
        messagebox.showwarning("Viaje en proceso", "No se puede volver ya que hay un viaje en proceso.")

class MapaViaje:
    def __init__(self, padre, moldes):
        # Paso 4: mapa derecho; guarda imagenes para que Tkinter no las pierda
        # y marcadores para poder limpiarlos cuando empieza la animacion.
        self.padre = padre
        self.moldes = moldes
        self.imagenes_lugares = {}
        self.marcadores_lugares = []

    def crear(self):
        # Paso 4: crea el contenedor del mapa y luego inicializa el widget.
        frame = self.moldes.crear_frame(self.padre, tema.PANEL, tema.BORDE, 1, fila=0, columna=1, sticky="nsew", margen_x=(12, 0))
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        self.crear_cabecera(frame)
        self.crear_mapa(frame)

    def crear_cabecera(self, panel):
        # Titulo del bloque derecho.
        cabecera = self.moldes.crear_frame(panel, tema.PANEL, fila=0, columna=0, sticky="ew", margen_x=18, margen_y=(16, 8), columnas_peso=((0, 1),))
        self.moldes.crear_label(cabecera, "Mapa de Osorno", tema.FUENTE_TITULO, tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")

    def crear_mapa(self, panel):
        # Paso 4: configura el mapa real de Osorno y dibuja sus lugares importantes.
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
        # Paso 4: el mapa queda fijo en zoom 15 para mantener una vista controlada.
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
        # Paso 4: si el usuario arrastra fuera de Osorno, se corrige la posicion.
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
        # Paso 4: dibuja marcadores con imagenes para cada lugar guardado en datos_viaje.
        for lugar in LUGARES_OSORNO:
            latitud, longitud = COORDENADAS_REALES_OSORNO[lugar]
            if lugar not in self.imagenes_lugares:
                imagen = Image.open(RUTA_IMAGENES_LUGARES / IMAGENES_LUGARES_OSORNO[lugar])
                imagen.thumbnail((42, 42))
                self.imagenes_lugares[lugar] = ImageTk.PhotoImage(imagen)
            marcador = self.mapa.set_marker(latitud, longitud, text=lugar, icon=self.imagenes_lugares[lugar], image_zoom_visibility=(0, float("inf")))
            self.marcadores_lugares.append(marcador)

    def dibujar_trayectoria(self, ruta):
        # Paso 7: dibuja la ruta azul del pasajero antes de confirmar el viaje.
        return self.mapa.set_path(ruta, color="#1a73e8", width=5)
    


#CONDUCTOR
class FlujoConductor:
    def __init__(self, vista, panel, mapa_viaje):
        # Pasos 5 al 12: controla el orden del flujo conductor.
        self.vista = vista
        self.panel = panel
        self.mapa_viaje = mapa_viaje
        self.info_pasajero_busqueda = None
        self.ubicacion_inicial_busqueda = None

    def presionar_buscar_pasajero(self):
        # Paso 5: lee ubicacion, pide pasajero al controlador e inicia la busqueda.
        self.ubicacion_inicial_busqueda = self.panel.obtener_ubicacion_inicial()
        self.info_pasajero_busqueda = self.vista.controlador_viaje.buscar_pasajeros(self.ubicacion_inicial_busqueda)
        self.panel.bloquear_busqueda()
        self.actualizar_cronometro_busqueda()

    def actualizar_cronometro_busqueda(self, segundos_transcurridos=0):
        # Paso 6: se ejecuta cada segundo con after hasta llegar a duracion_busqueda.
        duracion_busqueda = self.info_pasajero_busqueda["duracion_busqueda"]
        self.panel.cronometro.actualizar(segundos_transcurridos)
        if segundos_transcurridos < duracion_busqueda:
            self.panel.cronometro.despues(1000, lambda: self.actualizar_cronometro_busqueda(segundos_transcurridos + 1))
            return
        self.mostrar_pasajero_encontrado()

    def mostrar_pasajero_encontrado(self):
        # Pasos 7 y 8: muestra pasajero, dibuja trayectoria y cambia Volver a aviso.
        self.panel.mostrar_pasajero(self.info_pasajero_busqueda)
        ruta_pasajero = self.vista.controlador_viaje.formar_trayectoria(self.info_pasajero_busqueda["ubicacion_inicial"], self.info_pasajero_busqueda["ubicacion_final"])
        self.mapa_viaje.dibujar_trayectoria(ruta_pasajero)
        self.panel.cambiar_volver(self.vista.presionar_volver_pregunta_activa)

    def presionar_confirmar_viaje(self):
        # Pasos 9 y 10: bloquea botones, muestra estado, anima y guarda el viaje.
        self.vista.viaje_en_proceso = True
        self.panel.bloquear_confirmacion()
        self.panel.mostrar_estado_en_proceso()
        self.panel.cambiar_volver(self.vista.presionar_volver_flujo_activo)
        self.vista.animacion_viaje.animacion_viaje_conductor(self.mapa_viaje.mapa, self.mapa_viaje.marcadores_lugares, RUTA_IMAGENES_USUARIOS, self.info_pasajero_busqueda, self.panel.progreso.barra, self.panel.progreso.label_estado, self.panel.progreso.label_porcentaje, self.finalizar_viaje)
        self.vista.controlador_viaje.iniciar_viaje(self.ubicacion_inicial_busqueda, self.info_pasajero_busqueda, self.vista.usuario_actual)

    def finalizar_viaje(self):
        # Pasos 11 y 12: callback que ejecuta AnimacionViaje al terminar el recorrido.
        self.panel.mostrar_estado_finalizado()
        self.panel.cambiar_volver(self.vista.comando_volver_menu)

class CronometroViaje(ComponenteViaje):
    def crear(self, contenedor):
        # Paso 3: se muestra junto al boton "Buscar pasajeros".
        self.moldes.crear_label(contenedor, "Cronometro", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=1, columna=0, sticky="w", margen_y=(0, 6))
        self.label = self.moldes.crear_label(contenedor, "00:00", ("Arial", 28, "bold"), tema.PRIMARIO, tema.PANEL_SUAVE, metodo="grid", fila=2, columna=0, sticky="ew", ipady=24)

    def actualizar(self, segundos):
        # Paso 6: actualiza visualmente los segundos de busqueda.
        self.label.config(text=f"00:{segundos:02d}")

    def despues(self, milisegundos, accion):
        # Paso 6: after agenda la siguiente actualizacion del cronometro.
        self.label.after(milisegundos, accion)

class PanelPasajero:
    def __init__(self, padre, moldes, tipo_usuario):
        # Paso 3: empieza oculto para conductor y aparece al encontrar pasajero.
        self.moldes = moldes
        self.frame = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, tema.BORDE, 1, fila=6, columna=0, sticky="ew", margen_x=16, margen_y=(0, 10), columnas_peso=((0, 0), (1, 1)))
        if tipo_usuario == "conductor":
            self.frame.grid_remove()

    def mostrar(self, datos_pasajero):
        # Paso 7: carga imagen y datos del pasajero encontrado.
        # La imagen se guarda en self para que Tkinter la mantenga visible.
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
