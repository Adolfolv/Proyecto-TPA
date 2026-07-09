import tkinter as tk
from datetime import datetime, timedelta
from tkinter import ttk

from Modelos.Suscripcion.modelos_suscripcion import VIAJE_ASIGNADO, VIAJE_EN_CURSO, VIAJE_FINALIZADO, VIAJE_PROGRAMADO
from ...estilizacion import tema
from ...estilizacion.decoraciones import crear_logo_suscripcion_conductor
from ...estilizacion.widgets import Moldes
from .estado_visual_suscripcion import EstadoVisualSuscripcionConductor
from .renderizador_suscripcion import RenderizadorSuscripcionConductor


class PanelIzquierdoSuscripcionConductor:
    """Crea la búsqueda y selección de ofertas del lado izquierdo."""

    def __init__(self, vista):
        self.vista = vista
        self.moldes = vista.moldes

    def crear(self, padre):
        vista = self.vista
        agenda = vista.panel_agenda = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, tema.BORDE, 1, 18, 18, fila=0, columna=0, sticky="nsew", margen_x=(0, 8), columnas_peso=((0, 1),), filas_peso=((5, 1),))
        self.moldes.crear_label(agenda, "Agendar nueva suscripción", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, sticky="w")
        vista.boton_buscar_ofertas = self.moldes.crear_boton(agenda, "Buscar ofertas", True, None, vista.acciones.presionar_boton_buscar_ofertas, metodo="grid", fila=1, columna=0, sticky="ew", margen_y=(10, 0))
        vista.label_busqueda_ofertas = self.moldes.crear_label(agenda, "Ofertas sin buscar", tema.FUENTE_BOTON, tema.TEXTO_SUAVE, tema.PANEL_SUAVE, metodo="grid", fila=2, columna=0, sticky="w", margen_y=(6, 0))
        vista.tabla_disponibles = self.moldes.crear_tabla(agenda, (("ruta", "Ruta", 170), ("horario", "Días y hora", 135), ("pasajeros", "Pasajeros", 75)), alto=7, metodo="grid", fila=3, columna=0, sticky="nsew", margen_y=(8, 10))
        vista.tabla_disponibles.bind("<<TreeviewSelect>>", vista.acciones.presionar_boton_seleccionar_disponible)
        vista.boton_agregar = self.moldes.crear_boton(agenda, "Agregar a mi agenda", True, None, vista.acciones.presionar_boton_agregar_suscripcion, metodo="grid", fila=4, columna=0, sticky="ew")
        vista.label_mensaje_agenda = self.moldes.crear_label(agenda, "Selecciona una suscripción disponible.", tema.FUENTE_BOTON, tema.TEXTO_SUAVE, tema.PANEL_SUAVE, 350, "left", metodo="grid", fila=5, columna=0, sticky="ew", margen_y=(8, 0))
        vista.logo_suscripcion = crear_logo_suscripcion_conductor(agenda)
        vista.logo_suscripcion.grid(row=6, column=0, sticky="s", pady=(18, 4))
        vista.boton_agregar.grid_remove()
        vista.label_mensaje_agenda.grid_remove()
        self._crear_tarjeta_oferta(padre)

    def _crear_tarjeta_oferta(self, padre):
        vista = self.vista
        vista.valores_oferta = {}
        vista.panel_tarjeta_oferta = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, tema.BORDE, 2, fila=0, columna=0, sticky="nsew", margen_x=(0, 8), columnas_peso=((0, 1),), filas_peso=((1, 1),))
        cabecera = self.moldes.crear_frame(vista.panel_tarjeta_oferta, tema.PANEL, relleno_x=22, relleno_y=16, fila=0, columna=0, sticky="ew", columnas_peso=((0, 1),))
        self.moldes.crear_label(cabecera, "OFERTA DE SUSCRIPCIÓN", ("Arial", 9, "bold"), tema.PRIMARIO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")
        self.moldes.crear_label(cabecera, "Agenda recurrente", ("Arial", 17, "bold"), tema.TEXTO, tema.PANEL, metodo="grid", fila=1, columna=0, sticky="w", margen_y=(3, 0))
        self.moldes.crear_label(cabecera, "Revisa todos los datos antes de agregarla", ("Arial", 10), tema.TEXTO_SUAVE, tema.PANEL, metodo="grid", fila=2, columna=0, sticky="w", margen_y=(4, 0))
        contenido = self.moldes.crear_frame(vista.panel_tarjeta_oferta, tema.PANEL_SUAVE, relleno_x=22, relleno_y=18, fila=1, columna=0, sticky="nsew", columnas_peso=((0, 1),))
        ruta = self.moldes.crear_frame(contenido, tema.SECUNDARIO, tema.BORDE, 1, 16, 12, fila=0, columna=0, sticky="ew", columnas_peso=((0, 1),))
        self.moldes.crear_label(ruta, "RUTA PROGRAMADA", ("Arial", 8, "bold"), tema.TEXTO_SUAVE, tema.SECUNDARIO, metodo="grid", fila=0, columna=0, sticky="w")
        vista.valores_oferta["ruta"] = self.moldes.crear_label(ruta, "-", ("Arial", 13, "bold"), tema.TEXTO, tema.SECUNDARIO, 390, "left", metodo="grid", fila=1, columna=0, sticky="w", margen_y=(5, 0))
        detalles = self.moldes.crear_frame(contenido, tema.PANEL_SUAVE, fila=1, columna=0, sticky="ew", margen_y=(16, 0), columnas_peso=((0, 1), (1, 1)))
        campos = (("Período", "periodo"), ("Días de viaje", "dias"), ("Hora de salida", "hora"), ("Viajes incluidos", "cantidad"), ("Pasajeros", "pasajeros"), ("Ganancia por viaje", "ganancia"), ("Tu vehículo", "vehiculo"))
        for indice, (titulo, clave) in enumerate(campos):
            fila, columna = divmod(indice, 2)
            bloque = self.moldes.crear_frame(detalles, tema.PANEL_SUAVE, fila=fila, columna=columna, sticky="ew", margen_x=(0, 10) if columna == 0 else (10, 0), margen_y=(0, 12), columnas_peso=((0, 1),))
            self.moldes.crear_label(bloque, titulo.upper(), ("Arial", 8, "bold"), tema.TEXTO_SUAVE, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, sticky="w")
            vista.valores_oferta[clave] = self.moldes.crear_label(bloque, "-", tema.FUENTE_TEXTO, tema.TEXTO, tema.PANEL_SUAVE, 170, "left", metodo="grid", fila=1, columna=0, sticky="w", margen_y=(3, 0))
        total = self.moldes.crear_frame(contenido, tema.PANEL, tema.BORDE, 1, 16, 12, fila=2, columna=0, sticky="ew", columnas_peso=((0, 1),))
        self.moldes.crear_label(total, "GANANCIA TOTAL ESTIMADA", tema.FUENTE_BOTON, tema.TEXTO_SUAVE, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")
        vista.valores_oferta["ganancia_total"] = self.moldes.crear_label(total, "$0", ("Arial", 20, "bold"), tema.PRIMARIO, tema.PANEL, metodo="grid", fila=0, columna=1, sticky="e")
        acciones = self.moldes.crear_frame(vista.panel_tarjeta_oferta, tema.PANEL, relleno_x=22, relleno_y=14, fila=2, columna=0, sticky="ew", columnas_peso=((0, 1), (1, 1)))
        self.moldes.crear_boton(acciones, "Cancelar", False, None, vista.acciones.presionar_boton_cancelar_oferta, metodo="grid", fila=0, columna=0, sticky="ew", margen_x=(0, 6))
        self.moldes.crear_boton(acciones, "Confirmar y agregar", True, None, vista.acciones.presionar_boton_confirmar_oferta, metodo="grid", fila=0, columna=1, sticky="ew", margen_x=(6, 0))
        vista.panel_tarjeta_oferta.grid_remove()


class PanelDerechoSuscripcionConductor:
    """Crea la agenda y el próximo viaje del lado derecho."""

    def __init__(self, vista):
        self.vista = vista
        self.moldes = vista.moldes

    def crear(self, padre):
        vista = self.vista
        gestion = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, tema.BORDE, 1, 18, 18, fila=0, columna=1, sticky="nsew", margen_x=(8, 0), columnas_peso=((0, 1),), filas_peso=((1, 1), (4, 1)))
        self.moldes.crear_label(gestion, "Mis suscripciones", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, sticky="w")
        vista.tabla_suscripciones = self.moldes.crear_tabla(gestion, (("ruta", "Ruta", 180), ("periodo", "Período", 155), ("horario", "Días y hora", 145)), alto=5, metodo="grid", fila=1, columna=0, sticky="nsew", margen_y=(8, 12))
        vista.tabla_suscripciones.bind("<<TreeviewSelect>>", vista.acciones.presionar_boton_seleccionar_suscripcion)
        controles = self.moldes.crear_frame(gestion, tema.PANEL_SUAVE, fila=2, columna=0, sticky="ew", margen_y=(0, 14))
        vista.boton_cancelar_suscripcion = self.moldes.crear_boton(controles, "Cancelar suscripción", False, None, vista.acciones.presionar_boton_cancelar_suscripcion, lado="left")
        vista.confirmacion_suscripcion = self.moldes.crear_frame(controles, tema.PANEL_SUAVE, lado="left", margen_x=(8, 0))
        self.moldes.crear_label(vista.confirmacion_suscripcion, "¿Confirmar?", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, lado="left", margen_x=(0, 5))
        self.moldes.crear_boton(vista.confirmacion_suscripcion, "Sí", True, None, vista.acciones.presionar_boton_confirmar_cancelacion_suscripcion, lado="left", margen_x=3)
        self.moldes.crear_boton(vista.confirmacion_suscripcion, "No", False, None, vista.acciones.presionar_boton_ocultar_cancelacion_suscripcion, lado="left")
        vista.confirmacion_suscripcion.pack_forget()
        self.moldes.crear_label(gestion, "Viajes programados", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=3, columna=0, sticky="w")
        vista.tabla_viajes = self.moldes.crear_tabla(gestion, (("fecha", "Fecha y hora", 145), ("estado", "Estado", 110), ("ganancia", "Ganancia", 90), ("detalle", "Detalle", 170)), alto=5, metodo="grid", fila=4, columna=0, sticky="nsew", margen_y=(8, 10))
        vista.tabla_viajes.configure(selectmode="none", takefocus=False)
        proximo = self.moldes.crear_frame(gestion, tema.PANEL, tema.BORDE, 1, 14, 12, fila=5, columna=0, sticky="ew", columnas_peso=((0, 1),))
        self.moldes.crear_label(proximo, "PRÓXIMO VIAJE", ("Arial", 8, "bold"), tema.PRIMARIO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")
        vista.label_cronometro = self.moldes.crear_label(proximo, "No hay viajes próximos", ("Arial", 12, "bold"), tema.TEXTO, tema.PANEL, metodo="grid", fila=1, columna=0, sticky="w", margen_y=(4, 7))
        acciones = self.moldes.crear_frame(proximo, tema.PANEL, fila=1, columna=1, sticky="e")
        vista.boton_pasajero_abordo = self.moldes.crear_boton(acciones, "Pasajero a bordo", True, None, vista.acciones.presionar_boton_pasajero_abordo, lado="left", margen_x=4)
        vista.boton_cancelar = self.moldes.crear_boton(acciones, "Cancelar viaje", False, None, vista.acciones.presionar_boton_cancelar_viaje, lado="left")
        vista.label_mensaje = self.moldes.crear_label(proximo, "Selecciona una suscripción.", tema.FUENTE_BOTON, tema.TEXTO_SUAVE, tema.PANEL, 500, "left", metodo="grid", fila=2, columna=0, columnas=2, sticky="ew", margen_y=(4, 0))
        vista.confirmacion_viaje = self.moldes.crear_frame(proximo, tema.PANEL, fila=3, columna=1, sticky="e", margen_y=(8, 0))
        self.moldes.crear_label(vista.confirmacion_viaje, "¿Confirmar cancelación?", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, lado="left", margen_x=(0, 5))
        self.moldes.crear_boton(vista.confirmacion_viaje, "Sí", True, None, vista.acciones.presionar_boton_confirmar_cancelacion_viaje, lado="left", margen_x=3)
        self.moldes.crear_boton(vista.confirmacion_viaje, "No", False, None, vista.acciones.presionar_boton_ocultar_cancelacion_viaje, lado="left")
        vista.confirmacion_viaje.grid_remove()
        vista.panel_progreso = self.moldes.crear_frame(proximo, tema.PANEL, fila=4, columna=0, columnas=2, sticky="ew", margen_y=(8, 0), columnas_peso=((0, 1),))
        vista.barra_progreso = ttk.Progressbar(vista.panel_progreso, maximum=100, mode="determinate", value=0)
        vista.barra_progreso.grid(row=0, column=0, sticky="ew")
        vista.label_progreso = self.moldes.crear_label(vista.panel_progreso, "0%", tema.FUENTE_BOTON, tema.PRIMARIO, tema.PANEL, metodo="grid", fila=0, columna=1, sticky="e", margen_x=(10, 0))


class AccionesBotonesSuscripcionConductor:
    """Conecta eventos con controlador, renderizador y State visual."""

    def __init__(self, vista):
        self.vista = vista

    def presionar_boton_refrescar(self):
        vista = self.vista
        agenda, error = vista.controlador.consultar(vista.usuario_actual)
        if not error:
            suscripciones, viajes = agenda
            vista.suscripciones = {item.id_suscripcion: item for item in suscripciones}
            vista.viajes_agenda = {viaje.id_viaje_programado: viaje for viaje in viajes}
            vista.renderizador.mostrar_suscripciones(suscripciones)
            vista.renderizador.mostrar_viajes(sorted((viaje for viaje in viajes if viaje.estado != VIAJE_FINALIZADO), key=lambda viaje: viaje.fecha_hora))
        else:
            vista.renderizador.mostrar_mensaje(error)

    def presionar_boton_buscar_ofertas(self):
        vista = self.vista
        ofertas, error = vista.controlador.buscar_ofertas(vista.usuario_actual)
        vista.disponibles = {}
        vista.renderizador.mostrar_disponibles(())
        vista.estado_visual.buscando_ofertas()
        vista.renderizador.iniciar_busqueda(lambda: self.presionar_boton_finalizar_busqueda_ofertas(ofertas, error))

    def presionar_boton_finalizar_busqueda_ofertas(self, ofertas, error):
        vista = self.vista
        if error or not ofertas:
            vista.boton_buscar_ofertas.configure(state="normal", cursor="hand2")
            vista.label_busqueda_ofertas.configure(text=error or "Ya agregaste todas las ofertas del catálogo")
            return
        vista.disponibles = {item.id_suscripcion: item for item in ofertas}
        vista.renderizador.mostrar_disponibles(ofertas)
        vista.label_busqueda_ofertas.configure(text="Ofertas encontradas")
        vista.estado_visual.ofertas_disponibles()

    def presionar_boton_seleccionar_disponible(self, _evento=None):
        seleccion = self.vista.tabla_disponibles.selection()
        habilitado = bool(seleccion and self.vista.disponibles.get(seleccion[0]))
        self.vista.boton_agregar.configure(state="normal" if habilitado else "disabled", cursor="hand2" if habilitado else "arrow")

    def presionar_boton_agregar_suscripcion(self):
        seleccion = self.vista.tabla_disponibles.selection()
        oferta = self.vista.disponibles.get(seleccion[0]) if seleccion else None
        if oferta is None:
            self.vista.renderizador.mostrar_mensaje_agenda("Selecciona una suscripción para agregar.")
            return
        self.vista.oferta_pendiente = oferta
        self.vista.renderizador.mostrar_detalle_oferta(oferta, self.vista.usuario_actual)
        self.vista.estado_visual.oferta_en_revision()

    def presionar_boton_confirmar_oferta(self):
        vista = self.vista
        oferta = vista.oferta_pendiente
        if oferta is None:
            self.presionar_boton_cancelar_oferta()
            return
        _, error = vista.controlador.agregar_suscripcion(vista.usuario_actual, oferta.id_suscripcion)
        if not error:
            vista.oferta_pendiente = None
            vista.estado_visual.agenda_visible()
            vista.boton_agregar.grid_remove()
            vista.label_mensaje_agenda.grid_remove()
            vista.disponibles = {}
            vista.renderizador.mostrar_disponibles(())
            vista.label_busqueda_ofertas.configure(text="Ofertas sin buscar")
            vista.renderizador.mostrar_mensaje_agenda("Suscripción agregada a tu agenda.", True)
            self.presionar_boton_refrescar()
        else:
            vista.estado_visual.agenda_visible()
            vista.label_mensaje_agenda.grid()
            vista.renderizador.mostrar_mensaje_agenda(error)

    def presionar_boton_cancelar_oferta(self):
        self.vista.oferta_pendiente = None
        self.vista.estado_visual.agenda_visible()

    def presionar_boton_seleccionar_suscripcion(self, _evento=None):
        seleccion = self.vista.tabla_suscripciones.selection()
        if seleccion and self.vista.suscripciones.get(seleccion[0]) is not None:
            self.vista.renderizador.mostrar_mensaje("La tabla muestra todos tus viajes, ordenados por fecha.")

    def presionar_boton_cancelar_suscripcion(self):
        seleccion = self.vista.tabla_suscripciones.selection()
        suscripcion = self.vista.suscripciones.get(seleccion[0]) if seleccion else None
        if suscripcion is None:
            self.vista.renderizador.mostrar_mensaje("Selecciona una suscripción.")
            return
        self.vista.suscripcion_pendiente_cancelacion = suscripcion
        self.vista.confirmacion_suscripcion.pack(side="left", padx=(8, 0))

    def presionar_boton_ocultar_cancelacion_suscripcion(self):
        self.vista.suscripcion_pendiente_cancelacion = None
        self.vista.confirmacion_suscripcion.pack_forget()

    def presionar_boton_confirmar_cancelacion_suscripcion(self):
        suscripcion = self.vista.suscripcion_pendiente_cancelacion
        self.presionar_boton_ocultar_cancelacion_suscripcion()
        if suscripcion is not None:
            _, error = self.vista.controlador.cancelar_suscripcion(self.vista.usuario_actual, suscripcion.id_suscripcion)
            self.vista.renderizador.mostrar_mensaje(error or "Suscripción cancelada correctamente.", not error)
            if not error:
                self.presionar_boton_refrescar()

    def presionar_boton_pasajero_abordo(self):
        candidatos = [viaje for viaje in self.vista.viajes_agenda.values() if viaje.estado in (VIAJE_PROGRAMADO, VIAJE_ASIGNADO)]
        viaje = min(candidatos, key=lambda item: item.fecha_hora) if candidatos else None
        if viaje is not None:
            _, error = self.vista.controlador.confirmar_pasajero_abordo(self.vista.usuario_actual, viaje.id_viaje_programado)
            self.vista.renderizador.mostrar_mensaje(error or "Pasajero a bordo; trayecto iniciado.", not error)
            if not error:
                self.presionar_boton_refrescar()

    def presionar_boton_cancelar_viaje(self):
        candidatos = [viaje for viaje in self.vista.viajes_agenda.values() if viaje.estado in (VIAJE_PROGRAMADO, VIAJE_ASIGNADO)]
        viaje = min(candidatos, key=lambda item: item.fecha_hora) if candidatos else None
        if viaje is None:
            self.vista.renderizador.mostrar_mensaje("No hay un próximo viaje disponible para cancelar.")
            return
        self.vista.viaje_pendiente_cancelacion = viaje
        self.vista.estado_visual.confirmar_cancelacion_viaje(True)

    def presionar_boton_ocultar_cancelacion_viaje(self):
        self.vista.viaje_pendiente_cancelacion = None
        self.vista.estado_visual.confirmar_cancelacion_viaje(False)

    def presionar_boton_confirmar_cancelacion_viaje(self):
        viaje = self.vista.viaje_pendiente_cancelacion
        self.presionar_boton_ocultar_cancelacion_viaje()
        if viaje is None:
            return
        _, error = self.vista.controlador.cancelar_viaje(self.vista.usuario_actual, viaje.id_viaje_programado)
        self.vista.renderizador.mostrar_mensaje(error or "Viaje cancelado sin liquidación.", not error)
        if not error:
            self.presionar_boton_refrescar()

    def presionar_boton_completar_viaje(self, viaje):
        _, error = self.vista.controlador.finalizar_viaje(self.vista.usuario_actual, viaje.id_viaje_programado)
        self.vista.renderizador.mostrar_mensaje(error or "Viaje finalizado; avanzando al siguiente.", not error)
        if not error:
            self.presionar_boton_refrescar()

    def presionar_boton_actualizar_proximo_viaje(self):
        vista = self.vista
        candidatos = [viaje for viaje in vista.viajes_agenda.values() if viaje.estado in (VIAJE_PROGRAMADO, VIAJE_ASIGNADO, VIAJE_EN_CURSO)]
        if not candidatos:
            vista.renderizador.mostrar_cronometro("No hay viajes próximos")
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
        salida = horario - timedelta(seconds=max(0, viaje.tiempo_para_llegar))
        if ahora < salida:
            vista.renderizador.mostrar_cronometro(f"Debes salir en {vista.renderizador.temporizador.formatear(salida - ahora)}")
            vista.estado_visual.esperando_viaje()
        elif ahora < horario:
            vista.renderizador.mostrar_cronometro(f"Ve al origen - viaje en {vista.renderizador.temporizador.formatear(horario - ahora)}")
            vista.estado_visual.esperando_viaje()
        else:
            vista.renderizador.mostrar_cronometro("El pasajero está listo para abordar")
            vista.estado_visual.pasajero_listo()


class VistaSuscripcionConductor(tk.Frame):
    """Vista principal: ensambla constructor, acciones, renderizador y State."""

    INTERVALO_REFRESCO_MS = 15_000

    def __init__(self, padre, navegar, controlador, usuario_actual):
        super().__init__(padre, bg=tema.FONDO)
        self.pack(fill="both", expand=True)
        self.navegar = navegar
        self.controlador = controlador
        self.usuario_actual = usuario_actual
        self.moldes = Moldes()
        self.disponibles = {}
        self.suscripciones = {}
        self.viajes_agenda = {}
        self.oferta_pendiente = None
        self.suscripcion_pendiente_cancelacion = None
        self.viaje_pendiente_cancelacion = None
        self.completando_id = None
        self.acciones = AccionesBotonesSuscripcionConductor(self)
        self.crear_widgets()
        self.renderizador = RenderizadorSuscripcionConductor(self)
        self.estado_visual = EstadoVisualSuscripcionConductor(self)
        self.estado_visual.sin_viajes()
        self.acciones.presionar_boton_refrescar()

        def observar_viaje():
            if self.winfo_exists():
                self.acciones.presionar_boton_actualizar_proximo_viaje()
                self.after(1_000, observar_viaje)

        def refrescar_agenda():
            if self.winfo_exists():
                self.acciones.presionar_boton_refrescar()
                self.after(self.INTERVALO_REFRESCO_MS, refrescar_agenda)

        observar_viaje()
        self.after(self.INTERVALO_REFRESCO_MS, refrescar_agenda)

    def crear_widgets(self):
        principal = self.moldes.crear_frame(self, tema.PANEL, tema.BORDE, 1, 22, 22, llenar="both", expandir=True, margen_x=24, margen_y=24, columnas_peso=((0, 1),), filas_peso=((1, 1),))
        cabecera = self.moldes.crear_frame(principal, tema.PANEL, fila=0, columna=0, sticky="ew", margen_y=(0, 16), columnas_peso=((0, 1),))
        textos = self.moldes.crear_frame(cabecera, tema.PANEL, fila=0, columna=0, sticky="w")
        self.moldes.crear_label(textos, "Agenda de suscripciones", tema.FUENTE_TITULO, tema.TEXTO, tema.PANEL).pack(anchor="w")
        self.moldes.crear_label(textos, "Agrega planes compatibles y gestiona sus próximos viajes.", tema.FUENTE_TEXTO, tema.TEXTO_SUAVE, tema.PANEL).pack(anchor="w", pady=(4, 0))
        self.moldes.crear_boton(cabecera, "Volver", False, None, lambda: self.navegar("menu"), metodo="grid", fila=0, columna=1, sticky="e")
        cuerpo = self.moldes.crear_frame(principal, tema.PANEL, fila=1, columna=0, sticky="nsew", columnas_peso=((0, 2), (1, 3)), filas_peso=((0, 1),))
        cuerpo.grid_columnconfigure(0, weight=2, uniform="suscripcion_conductor")
        cuerpo.grid_columnconfigure(1, weight=3, uniform="suscripcion_conductor")
        PanelIzquierdoSuscripcionConductor(self).crear(cuerpo)
        PanelDerechoSuscripcionConductor(self).crear(cuerpo)
