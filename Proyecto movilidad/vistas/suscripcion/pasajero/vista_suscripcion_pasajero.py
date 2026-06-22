import tkinter as tk
from datetime import datetime, timedelta
from tkinter import ttk

from Modelos.Suscripcion.modelos_suscripcion import NOMBRES_DIAS, VIAJE_ASIGNADO, VIAJE_EN_CURSO, VIAJE_PROGRAMADO
from ...estilizacion import tema
from ...estilizacion.decoraciones import crear_logo_suscripcion_pasajero, crear_panel_mensaje
from ...estilizacion.widgets import Moldes
from .estado_visual_suscripcion import EstadoVisualSuscripcionPasajero
from .renderizador_suscripcion import RenderizadorSuscripcionPasajero


class PanelIzquierdoSuscripcionPasajero:
    """Crea todos los widgets de alta y resumen del lado izquierdo."""

    def __init__(self, vista, lugares):
        self.vista = vista
        self.lugares = lugares
        self.moldes = vista.moldes

    def crear(self, padre):
        contenedor = self.moldes.crear_frame(padre, tema.PANEL, fila=0, columna=0, sticky="nsew", margen_x=(0, 8), columnas_peso=((0, 1),), filas_peso=((0, 1),))
        contenedor.grid_propagate(False)
        self._crear_formulario(contenedor)
        self._crear_resumen(contenedor)

    def _crear_formulario(self, padre):
        vista = self.vista
        vista.panel_formulario = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, tema.BORDE, 1, 18, 18, fila=0, columna=0, sticky="nsew", columnas_peso=((0, 1), (1, 1)))
        self.moldes.crear_label(vista.panel_formulario, "Nueva suscripcion", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, columnas=2, sticky="w", margen_y=(0, 10))
        vista.origen = self._crear_selector("Origen", self.lugares, 1, 0)
        vista.destino = self._crear_selector("Destino", self.lugares, 1, 1)
        if len(self.lugares) > 1:
            vista.destino.current(1)
        hora_inicial = (datetime.now() + timedelta(minutes=10)).replace(second=0, microsecond=0)
        vista.fecha_inicio = self._crear_entrada("Fecha inicial (AAAA-MM-DD)", 3, 0, hora_inicial.date().isoformat())
        vista.fecha_fin = self._crear_entrada("Fecha final (AAAA-MM-DD)", 3, 1, (hora_inicial.date() + timedelta(days=30)).isoformat())
        vista.hora = self._crear_entrada("Hora (HH:MM)", 5, 0, hora_inicial.strftime("%H:%M"))
        vista.pasajeros = self._crear_selector("Pasajeros", ("1", "2", "3", "4"), 5, 1)
        self._crear_dias(7)
        vista.boton_buscar_conductor = self.moldes.crear_boton(vista.panel_formulario, "Buscar conductor", True, None, vista.acciones.presionar_boton_buscar_conductor, metodo="grid", fila=9, columna=0, columnas=2, sticky="ew", margen_y=(14, 0))
        vista.label_busqueda = self.moldes.crear_label(vista.panel_formulario, "", tema.FUENTE_BOTON, tema.PRIMARIO, tema.PANEL_SUAVE, 340, "center", metodo="grid", fila=10, columna=0, columnas=2, sticky="ew", margen_y=(8, 0))
        vista.tabla_conductores = self.moldes.crear_tabla(vista.panel_formulario, (("conductor", "Conductor", 125), ("vehiculo", "Vehiculo", 175), ("precio", "Precio por viaje", 110)), alto=4)
        vista.tabla_conductores.grid(row=11, column=0, columnspan=2, sticky="nsew", pady=(8, 0))
        vista.tabla_conductores.bind("<<TreeviewSelect>>", vista.acciones.presionar_boton_seleccionar_conductor)
        vista.area_acciones_formulario = self.moldes.crear_frame(vista.panel_formulario, tema.PANEL_SUAVE, fila=12, columna=0, columnas=2, sticky="ew", margen_y=(8, 0), columnas_peso=((0, 1), (1, 1)))
        vista.boton_ajustar = self.moldes.crear_boton(vista.area_acciones_formulario, "Volver a ajustar", False, None, vista.acciones.presionar_boton_volver_ajustar, metodo="grid", fila=0, columna=0, sticky="ew", margen_x=(0, 5))
        vista.boton_crear_suscripcion = self.moldes.crear_boton(vista.area_acciones_formulario, "Crear suscripcion", True, None, vista.acciones.presionar_boton_previsualizar_suscripcion, metodo="grid", fila=0, columna=1, sticky="ew", margen_x=(5, 0))
        vista.logo_suscripcion = crear_logo_suscripcion_pasajero(vista.panel_formulario)
        vista.logo_suscripcion.grid(row=13, column=0, columnspan=2, sticky="s", pady=(30, 8))
        vista.panel_formulario.grid_rowconfigure(13, weight=1)

    def _crear_resumen(self, padre):
        vista = self.vista
        vista.valores_resumen = {}
        vista.panel_resumen = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, tema.BORDE, 2, fila=0, columna=0, sticky="nsew", columnas_peso=((0, 1),), filas_peso=((1, 1),))
        cabecera = self.moldes.crear_frame(vista.panel_resumen, tema.PANEL, relleno_x=22, relleno_y=16, fila=0, columna=0, sticky="ew", columnas_peso=((0, 1),))
        self.moldes.crear_label(cabecera, "RESUMEN DE COMPRA", ("Arial", 9, "bold"), tema.PRIMARIO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")
        self.moldes.crear_label(cabecera, "Tu suscripcion de viaje", ("Arial", 17, "bold"), tema.TEXTO, tema.PANEL, metodo="grid", fila=1, columna=0, sticky="w", margen_y=(3, 0))
        contenido = self.moldes.crear_frame(vista.panel_resumen, tema.PANEL_SUAVE, relleno_x=22, relleno_y=18, fila=1, columna=0, sticky="nsew", columnas_peso=((0, 1),))
        ruta = self.moldes.crear_frame(contenido, tema.SECUNDARIO, tema.BORDE, 1, 16, 12, fila=0, columna=0, sticky="ew", columnas_peso=((0, 1),))
        self.moldes.crear_label(ruta, "RUTA PROGRAMADA", ("Arial", 8, "bold"), tema.TEXTO_SUAVE, tema.SECUNDARIO, metodo="grid", fila=0, columna=0, sticky="w")
        vista.valores_resumen["ruta"] = self.moldes.crear_label(ruta, "-", ("Arial", 13, "bold"), tema.TEXTO, tema.SECUNDARIO, 390, "left", metodo="grid", fila=1, columna=0, sticky="w", margen_y=(5, 0))
        detalles = self.moldes.crear_frame(contenido, tema.PANEL_SUAVE, fila=1, columna=0, sticky="ew", margen_y=(16, 0), columnas_peso=((0, 1), (1, 1)))
        campos = (("Periodo", "periodo"), ("Dias de viaje", "dias"), ("Hora de salida", "hora"), ("Viajes incluidos", "cantidad_viajes"), ("Pasajeros", "pasajeros"), ("Valor por viaje", "precio_viaje"), ("Vehiculo seleccionado", "vehiculo"))
        for indice, (titulo, clave) in enumerate(campos):
            fila, columna = divmod(indice, 2)
            bloque = self.moldes.crear_frame(detalles, tema.PANEL_SUAVE, fila=fila, columna=columna, sticky="ew", margen_x=(0, 12) if columna == 0 else (12, 0), margen_y=(0, 13), columnas_peso=((0, 1),))
            self.moldes.crear_label(bloque, titulo.upper(), ("Arial", 8, "bold"), tema.TEXTO_SUAVE, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, sticky="w")
            vista.valores_resumen[clave] = self.moldes.crear_label(bloque, "-", tema.FUENTE_TEXTO, tema.TEXTO, tema.PANEL_SUAVE, 180, "left", metodo="grid", fila=1, columna=0, sticky="w", margen_y=(3, 0))
        total = self.moldes.crear_frame(contenido, tema.PANEL, tema.BORDE, 1, 16, 12, fila=2, columna=0, sticky="ew", columnas_peso=((0, 1),))
        self.moldes.crear_label(total, "TOTAL A PAGAR", tema.FUENTE_BOTON, tema.TEXTO_SUAVE, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")
        vista.valores_resumen["precio_total"] = self.moldes.crear_label(total, "$0", ("Arial", 20, "bold"), tema.PRIMARIO, tema.PANEL, metodo="grid", fila=0, columna=1, sticky="e")
        vista.area_acciones_resumen = self.moldes.crear_frame(vista.panel_resumen, tema.PANEL, relleno_x=22, relleno_y=14, fila=2, columna=0, sticky="ew")
        vista.boton_editar_resumen = self.moldes.crear_boton(vista.area_acciones_resumen, "Volver y editar", False, None, vista.acciones.presionar_boton_editar_datos)
        vista.boton_pagar_resumen = self.moldes.crear_boton(vista.area_acciones_resumen, "Continuar al pago", True, None, vista.acciones.presionar_boton_solicitar_pago)
        vista.boton_confirmar_pago = self.moldes.crear_boton(vista.area_acciones_resumen, "Confirmar y pagar", True, None, vista.acciones.presionar_boton_confirmar_pago)
        vista.boton_cancelar_pago = self.moldes.crear_boton(vista.area_acciones_resumen, "Cancelar", False, None, vista.acciones.presionar_boton_cancelar_alta)
        vista.panel_resumen.grid_remove()

    def _crear_etiqueta(self, texto, fila, columna):
        self.moldes.crear_label(self.vista.panel_formulario, texto, tema.FUENTE_BOTON, tema.TEXTO_SUAVE, tema.PANEL_SUAVE, metodo="grid", fila=fila, columna=columna, sticky="w", margen_x=5, margen_y=(5, 3))

    def _crear_selector(self, titulo, opciones, fila, columna):
        self._crear_etiqueta(titulo, fila, columna)
        return self.moldes.crear_selector(self.vista.panel_formulario, opciones, metodo="grid", fila=fila + 1, columna=columna, sticky="ew", margen_x=5, margen_y=(0, 5))

    def _crear_entrada(self, titulo, fila, columna, valor):
        self._crear_etiqueta(titulo, fila, columna)
        entrada = self.moldes.crear_entrada(self.vista.panel_formulario, metodo="grid", fila=fila + 1, columna=columna, sticky="ew", margen_x=5, margen_y=(0, 5))
        entrada.insert(0, valor)
        return entrada

    def _crear_dias(self, fila):
        vista = self.vista
        self.moldes.crear_label(vista.panel_formulario, "Dias de la semana", tema.FUENTE_BOTON, tema.TEXTO_SUAVE, tema.PANEL_SUAVE, metodo="grid", fila=fila, columna=0, columnas=2, sticky="w", margen_x=5, margen_y=(8, 3))
        contenedor = self.moldes.crear_frame(vista.panel_formulario, tema.PANEL_SUAVE, fila=fila + 1, columna=0, columnas=2, sticky="ew")
        for indice, nombre in enumerate(NOMBRES_DIAS):
            variable = tk.BooleanVar(value=indice < 5)
            check = tk.Checkbutton(contenedor, text=nombre, variable=variable, bg=tema.PANEL_SUAVE, fg=tema.TEXTO, selectcolor=tema.SECUNDARIO, activebackground=tema.PANEL_SUAVE, activeforeground=tema.TEXTO, disabledforeground=tema.TEXTO_SUAVE, font=("Arial", 9))
            check.pack(side="left", expand=True)
            vista.variables_dias.append(variable)
            vista.checks_dias.append(check)


class PanelDerechoSuscripcionPasajero:
    """Crea todos los widgets de gestión del lado derecho."""

    def __init__(self, vista):
        self.vista = vista
        self.moldes = vista.moldes

    def crear(self, padre):
        vista = self.vista
        panel = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, tema.BORDE, 1, 16, 16, fila=0, columna=1, sticky="nsew", margen_x=(8, 0), columnas_peso=((0, 1),), filas_peso=((1, 1), (4, 1)))
        self.moldes.crear_label(panel, "Mis suscripciones", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, sticky="w")
        vista.tabla_suscripciones = self.moldes.crear_tabla(panel, (("ruta", "Ruta", 190), ("horario", "Horario", 115), ("conductor", "Conductor", 130), ("total", "Total", 80), ("estado", "Estado", 95)), alto=5, metodo="grid", fila=1, columna=0, sticky="nsew", margen_y=(8, 5))
        botones = self.moldes.crear_frame(panel, tema.PANEL_SUAVE, fila=2, columna=0, sticky="ew", margen_y=(3, 12))
        vista.boton_cancelar_suscripcion = self.moldes.crear_boton(botones, "Cancelar suscripcion", False, None, vista.acciones.presionar_boton_cancelar_suscripcion, lado="left")
        vista.confirmacion_suscripcion = self.moldes.crear_frame(botones, tema.PANEL_SUAVE, lado="left", margen_x=(8, 0))
        self.moldes.crear_label(vista.confirmacion_suscripcion, "¿Confirmar?", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, lado="left", margen_x=(0, 5))
        self.moldes.crear_boton(vista.confirmacion_suscripcion, "Si", True, None, vista.acciones.presionar_boton_confirmar_cancelacion_suscripcion, lado="left", margen_x=3)
        self.moldes.crear_boton(vista.confirmacion_suscripcion, "No", False, None, vista.acciones.presionar_boton_ocultar_cancelacion_suscripcion, lado="left")
        vista.confirmacion_suscripcion.pack_forget()
        self.moldes.crear_label(panel, "Viajes programados", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=3, columna=0, sticky="w")
        vista.tabla_viajes = self.moldes.crear_tabla(panel, (("fecha", "Fecha y hora", 120), ("ruta", "Ruta", 165), ("estado", "Estado", 120), ("detalle", "Conductor / detalle", 155)), alto=5, metodo="grid", fila=4, columna=0, sticky="nsew", margen_y=(8, 5))
        pie = self.moldes.crear_frame(panel, tema.PANEL, tema.BORDE, 1, 14, 12, fila=5, columna=0, sticky="ew", margen_y=(10, 0), columnas_peso=((0, 1),))
        self.moldes.crear_label(pie, "PROXIMO VIAJE", ("Arial", 8, "bold"), tema.PRIMARIO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")
        vista.texto_temporizador = self.moldes.crear_label(pie, "No hay viajes proximos", ("Arial", 13, "bold"), tema.TEXTO, tema.PANEL, metodo="grid", fila=1, columna=0, sticky="w", margen_y=(4, 8))
        vista.boton_confirmar_inicio = self.moldes.crear_boton(pie, "Confirmar inicio", True, None, vista.acciones.presionar_boton_confirmar_inicio, metodo="grid", fila=1, columna=1, sticky="e", margen_x=5)
        vista.boton_cancelar_viaje = self.moldes.crear_boton(pie, "Cancelar viaje", False, None, vista.acciones.presionar_boton_cancelar_viaje, metodo="grid", fila=1, columna=2, sticky="e")
        vista.panel_progreso = self.moldes.crear_frame(pie, tema.PANEL, fila=2, columna=0, columnas=3, sticky="ew", columnas_peso=((0, 1),))
        vista.barra_progreso = ttk.Progressbar(vista.panel_progreso, maximum=100, mode="determinate", value=0)
        vista.barra_progreso.grid(row=0, column=0, sticky="ew")
        vista.label_progreso = self.moldes.crear_label(vista.panel_progreso, "0%", tema.FUENTE_BOTON, tema.PRIMARIO, tema.PANEL, metodo="grid", fila=0, columna=1, sticky="e", margen_x=(10, 0))
        vista.confirmacion_viaje = self.moldes.crear_frame(pie, tema.PANEL, fila=3, columna=2, sticky="e", margen_y=(8, 0))
        self.moldes.crear_label(vista.confirmacion_viaje, "¿Confirmar?", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, lado="left", margen_x=(0, 5))
        self.moldes.crear_boton(vista.confirmacion_viaje, "Si", True, None, vista.acciones.presionar_boton_confirmar_cancelacion_viaje, lado="left", margen_x=3)
        self.moldes.crear_boton(vista.confirmacion_viaje, "No", False, None, vista.acciones.presionar_boton_ocultar_cancelacion_viaje, lado="left")
        vista.confirmacion_viaje.grid_remove()


class AccionesBotonesSuscripcionPasajero:
    """Conecta widgets con controlador, renderizador y State visual."""

    def __init__(self, vista):
        self.vista = vista

    def presionar_boton_buscar_conductor(self):
        vista = self.vista
        datos = {"origen": vista.origen.get(), "destino": vista.destino.get(), "fecha_inicio": vista.fecha_inicio.get(), "fecha_fin": vista.fecha_fin.get(), "dias_semana": tuple(indice for indice, variable in enumerate(vista.variables_dias) if variable.get()), "hora": vista.hora.get(), "cantidad_pasajeros": vista.pasajeros.get()}
        _, error = vista.controlador.previsualizar(vista.usuario_actual, datos)
        if error:
            vista.renderizador.mostrar_mensaje(f"Revisa este dato: {error}")
            return
        resultado = vista.controlador.buscar_conductores(datos["cantidad_pasajeros"], datos["origen"], datos["destino"])
        vista.datos_pendientes = datos
        vista.conductor_seleccionado = None
        vista.estado_visual.buscando_conductor()
        vista.renderizador.iniciar_busqueda_conductor(lambda: self.presionar_boton_finalizar_busqueda_conductor(resultado))

    def presionar_boton_finalizar_busqueda_conductor(self, resultado):
        vista = self.vista
        if not resultado.exitoso or not resultado.vehiculos:
            vista.estado_visual.formulario()
            vista.renderizador.mostrar_mensaje(f"No se encontraron conductores: {resultado.error or 'intenta nuevamente.'}")
            return
        vista.renderizador.mostrar_conductores(resultado.vehiculos)
        vista.estado_visual.conductores_disponibles()
        vista.renderizador.mostrar_mensaje("Selecciona el conductor que prefieras para continuar.", True)

    def presionar_boton_seleccionar_conductor(self, _evento=None):
        seleccion = self.vista.tabla_conductores.selection()
        conductor = self.vista.conductores_por_item.get(seleccion[0]) if seleccion else None
        if conductor is None:
            return
        self.vista.conductor_seleccionado = conductor
        self.vista.label_busqueda.configure(text=f"{conductor.vehiculo} seleccionado. A continuacion, crea tu suscripcion.")
        self.vista.boton_crear_suscripcion.configure(state="disabled" if self.vista.bloqueo_creacion else "normal", cursor="arrow" if self.vista.bloqueo_creacion else "hand2")
        self.vista.renderizador.mostrar_mensaje(f"Vehiculo seleccionado: {conductor.vehiculo} - ${conductor.precio:,.0f} por viaje.", True)

    def presionar_boton_previsualizar_suscripcion(self):
        vista = self.vista
        if vista.conductor_seleccionado is None:
            vista.renderizador.mostrar_mensaje("Revisa este dato: selecciona un conductor.")
            return
        datos = {"origen": vista.origen.get(), "destino": vista.destino.get(), "fecha_inicio": vista.fecha_inicio.get(), "fecha_fin": vista.fecha_fin.get(), "dias_semana": tuple(indice for indice, variable in enumerate(vista.variables_dias) if variable.get()), "hora": vista.hora.get(), "cantidad_pasajeros": vista.pasajeros.get()}
        datos["conductor"] = vista.conductor_seleccionado
        resumen, error = vista.controlador.previsualizar(vista.usuario_actual, datos)
        if error:
            vista.renderizador.mostrar_mensaje(f"Revisa este dato: {error}")
            return
        vista.datos_pendientes = datos
        vista.renderizador.mostrar_resumen(resumen, vista.conductor_seleccionado)
        vista.estado_visual.cotizacion()
        vista.renderizador.mostrar_mensaje("Cotizacion generada. Revisa los datos antes de pagar.", True)

    def presionar_boton_volver_ajustar(self):
        self.vista.datos_pendientes = None
        self.vista.conductor_seleccionado = None
        self.vista.estado_visual.formulario()

    def presionar_boton_editar_datos(self):
        self.vista.estado_visual.formulario()

    def presionar_boton_solicitar_pago(self):
        self.vista.estado_visual.confirmacion_pago()

    def presionar_boton_confirmar_pago(self):
        vista = self.vista
        if vista.datos_pendientes is None:
            vista.estado_visual.formulario()
            return
        vista.estado_visual.procesando_pago()
        _, error = vista.controlador.confirmar(vista.usuario_actual, vista.datos_pendientes)
        if error:
            vista.estado_visual.confirmacion_pago()
            vista.renderizador.mostrar_mensaje(f"No se pudo pagar: {error}")
            return
        vista.datos_pendientes = None
        vista.conductor_seleccionado = None
        vista.estado_visual.formulario()
        self.presionar_boton_refrescar()
        vista.renderizador.mostrar_mensaje("Pago realizado. La suscripcion ya aparece en tus listados.", True)

    def presionar_boton_cancelar_alta(self):
        self.vista.datos_pendientes = None
        self.vista.conductor_seleccionado = None
        self.vista.estado_visual.formulario()

    def presionar_boton_cancelar_suscripcion(self):
        seleccion = self.vista.tabla_suscripciones.selection()
        suscripcion = self.vista.suscripciones.get(seleccion[0]) if seleccion else None
        if suscripcion is None:
            self.vista.renderizador.mostrar_mensaje("Selecciona una suscripcion.")
            return
        self.vista.suscripcion_pendiente_cancelacion = suscripcion
        self.vista.estado_visual.confirmar_cancelacion_suscripcion(True)

    def presionar_boton_confirmar_cancelacion_suscripcion(self):
        suscripcion = self.vista.suscripcion_pendiente_cancelacion
        self.presionar_boton_ocultar_cancelacion_suscripcion()
        if suscripcion is None:
            return
        _, error = self.vista.controlador.cancelar_suscripcion(self.vista.usuario_actual, suscripcion.id_suscripcion)
        self.vista.renderizador.mostrar_mensaje(error or "Suscripcion cancelada correctamente.", not error)
        if not error:
            self.presionar_boton_refrescar()

    def presionar_boton_ocultar_cancelacion_suscripcion(self):
        self.vista.suscripcion_pendiente_cancelacion = None
        self.vista.estado_visual.confirmar_cancelacion_suscripcion(False)

    def presionar_boton_cancelar_viaje(self):
        candidatos = [viaje for viaje in self.vista.viajes.values() if viaje.estado in (VIAJE_PROGRAMADO, VIAJE_ASIGNADO)]
        viaje = min(candidatos, key=lambda item: item.fecha_hora) if candidatos else None
        if viaje is None:
            self.vista.renderizador.mostrar_mensaje("No hay un proximo viaje disponible para cancelar.")
            return
        self.vista.viaje_pendiente_cancelacion = viaje
        self.vista.estado_visual.confirmar_cancelacion_viaje(True)

    def presionar_boton_confirmar_cancelacion_viaje(self):
        viaje = self.vista.viaje_pendiente_cancelacion
        self.presionar_boton_ocultar_cancelacion_viaje()
        if viaje is not None:
            _, error = self.vista.controlador.cancelar_viaje(self.vista.usuario_actual, viaje.id_viaje_programado)
            self.vista.renderizador.mostrar_mensaje(error or "Viaje cancelado.", not error)
            if not error:
                self.presionar_boton_refrescar()

    def presionar_boton_ocultar_cancelacion_viaje(self):
        self.vista.viaje_pendiente_cancelacion = None
        self.vista.estado_visual.confirmar_cancelacion_viaje(False)

    def presionar_boton_confirmar_inicio(self):
        candidatos = [viaje for viaje in self.vista.viajes.values() if viaje.estado in (VIAJE_PROGRAMADO, VIAJE_ASIGNADO, VIAJE_EN_CURSO)]
        viaje = min(candidatos, key=lambda item: (0 if item.estado == VIAJE_EN_CURSO else 1, item.fecha_hora)) if candidatos else None
        if viaje is not None:
            _, error = self.vista.controlador.confirmar_inicio(self.vista.usuario_actual, viaje.id_viaje_programado)
            self.vista.renderizador.mostrar_mensaje(error or "Viaje iniciado. Ya corre el temporizador del trayecto.", not error)
            if not error:
                self.presionar_boton_refrescar()

    def presionar_boton_completar_viaje(self, viaje):
        _, error = self.vista.controlador.completar_viaje(self.vista.usuario_actual, viaje.id_viaje_programado)
        self.vista.renderizador.mostrar_mensaje(error or "Viaje finalizado correctamente.", not error)
        if not error:
            self.presionar_boton_refrescar()

    def presionar_boton_refrescar(self):
        listados, error = self.vista.controlador.consultar(self.vista.usuario_actual)
        if not error:
            suscripciones, viajes = listados
            self.vista.renderizador.actualizar_listados(suscripciones, viajes)
        else:
            self.vista.renderizador.mostrar_mensaje(error)

    def presionar_boton_actualizar_proximo_viaje(self):
        vista = self.vista
        candidatos = [viaje for viaje in vista.viajes.values() if viaje.estado in (VIAJE_PROGRAMADO, VIAJE_ASIGNADO, VIAJE_EN_CURSO)]
        if not candidatos:
            vista.renderizador.mostrar_cronometro("No hay viajes proximos")
            vista.estado_visual.sin_viajes()
            return
        viaje = min(candidatos, key=lambda item: (0 if item.estado == VIAJE_EN_CURSO else 1, item.fecha_hora))
        ahora = datetime.now()
        horario = datetime.fromisoformat(viaje.fecha_hora)
        if viaje.estado == VIAJE_EN_CURSO and viaje.inicio_confirmado_en:
            inicio = datetime.fromisoformat(viaje.inicio_confirmado_en)
            duracion = max(1, viaje.duracion_trayecto_segundos)
            porcentaje = vista.renderizador.temporizador.porcentaje(ahora, inicio, duracion)
            vista.renderizador.mostrar_cronometro(f"Trayecto en curso - restante {vista.renderizador.temporizador.formatear(inicio + timedelta(seconds=duracion) - ahora)}")
            vista.renderizador.mostrar_progreso(porcentaje)
            vista.estado_visual.trayecto_en_curso()
            if porcentaje >= 100 and vista.completando_id != viaje.id_viaje_programado:
                vista.completando_id = viaje.id_viaje_programado
                self.presionar_boton_completar_viaje(viaje)
            return
        apertura = horario - timedelta(minutes=5)
        cierre = horario + timedelta(minutes=15)
        if ahora < apertura:
            restante = horario - ahora
            vista.renderizador.mostrar_cronometro(f"Viaje en {vista.renderizador.temporizador.formatear(restante)}")
            vista.estado_visual.esperando_inicio(restante <= timedelta(minutes=10))
        elif ahora <= cierre:
            vista.renderizador.mostrar_cronometro(f"Confirma el inicio - {vista.renderizador.temporizador.formatear(cierre - ahora)} restantes")
            vista.estado_visual.inicio_disponible()
        else:
            vista.renderizador.mostrar_cronometro("El tiempo para iniciar este viaje vencio")
            vista.estado_visual.esperando_inicio(False)


class VistaSuscripcionPasajero(tk.Frame):
    """Vista principal: ensambla paneles, acciones, renderizador y State."""

    INTERVALO_REFRESCO_MS = 30_000

    def __init__(self, padre, navegar, controlador, usuario_actual):
        super().__init__(padre, bg=tema.FONDO)
        self.pack(fill="both", expand=True)
        self.navegar = navegar
        self.controlador = controlador
        self.usuario_actual = usuario_actual
        self.moldes = Moldes()
        self.variables_dias = []
        self.checks_dias = []
        self.conductores_por_item = {}
        self.suscripciones = {}
        self.viajes = {}
        self.bloqueo_creacion = False
        self.datos_pendientes = None
        self.conductor_seleccionado = None
        self.suscripcion_pendiente_cancelacion = None
        self.viaje_pendiente_cancelacion = None
        self.completando_id = None
        self.acciones = AccionesBotonesSuscripcionPasajero(self)
        self.crear_widgets(tuple(controlador.obtener_lugares_disponibles()))
        self.renderizador = RenderizadorSuscripcionPasajero(self)
        self.estado_visual = EstadoVisualSuscripcionPasajero(self)
        self.estado_visual.formulario()
        self.acciones.presionar_boton_refrescar()
        if getattr(usuario_actual, "tipo_usuario", "") != "pasajero":
            self.estado_visual.bloquear_creacion(True)
            self.renderizador.mostrar_mensaje("Solo las cuentas de pasajero pueden crear suscripciones.")

        def observar_viaje():
            if self.winfo_exists():
                self.acciones.presionar_boton_actualizar_proximo_viaje()
                self.after(1_000, observar_viaje)

        def refrescar_listados():
            if self.winfo_exists():
                self.acciones.presionar_boton_refrescar()
                self.after(self.INTERVALO_REFRESCO_MS, refrescar_listados)

        observar_viaje()
        self.after(self.INTERVALO_REFRESCO_MS, refrescar_listados)

    def crear_widgets(self, lugares):
        principal = self.moldes.crear_frame(self, tema.PANEL, tema.BORDE, 1, 22, 22, llenar="both", expandir=True, margen_x=24, margen_y=24, columnas_peso=((0, 1),), filas_peso=((1, 1),))
        cabecera = self.moldes.crear_frame(principal, tema.PANEL, fila=0, columna=0, sticky="ew", columnas_peso=((0, 1),))
        self.moldes.crear_label(cabecera, "Suscripcion de viaje", tema.FUENTE_TITULO, tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")
        self.moldes.crear_boton(cabecera, "Volver", False, None, lambda: self.navegar("menu"), metodo="grid", fila=0, columna=1, sticky="e")
        cuerpo = self.moldes.crear_frame(principal, tema.PANEL, fila=1, columna=0, sticky="nsew", margen_y=(16, 8), columnas_peso=((0, 2), (1, 3)), filas_peso=((0, 1),))
        cuerpo.grid_columnconfigure(0, weight=2, uniform="suscripcion")
        cuerpo.grid_columnconfigure(1, weight=3, uniform="suscripcion")
        PanelIzquierdoSuscripcionPasajero(self, lugares).crear(cuerpo)
        PanelDerechoSuscripcionPasajero(self).crear(cuerpo)
        area_mensaje = self.moldes.crear_frame(principal, tema.PANEL, fila=2, columna=0, sticky="ew")
        self._mostrar_mensaje = crear_panel_mensaje(area_mensaje, compacto=True)
