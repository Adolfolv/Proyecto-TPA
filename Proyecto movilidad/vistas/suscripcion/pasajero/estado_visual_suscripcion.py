class EstadoVisualSuscripcionPasajero:
    """State parcial: solo modifica widgets visibles o habilitados."""

    def __init__(self, vista):
        self.vista = vista

    def formulario(self):
        vista = self.vista
        vista.panel_formulario.grid()
        vista.panel_resumen.grid()
        vista.panel_formulario.tkraise()
        vista.tabla_conductores.grid_remove()
        vista.area_acciones_formulario.grid_remove()
        vista.boton_buscar_conductor.grid()
        vista.logo_suscripcion.grid()
        vista.label_busqueda.configure(text="")
        vista.conductores_por_item = {}
        self._habilitar_campos(True)
        self._configurar(vista.boton_buscar_conductor, not vista.bloqueo_creacion)

    def buscando_conductor(self):
        self._habilitar_campos(False)
        self._configurar(self.vista.boton_buscar_conductor, False)

    def conductores_disponibles(self):
        vista = self.vista
        vista.boton_buscar_conductor.grid_remove()
        vista.logo_suscripcion.grid_remove()
        vista.tabla_conductores.grid()
        vista.area_acciones_formulario.grid()
        self._configurar(vista.boton_crear_suscripcion, False)

    def cotizacion(self):
        self._mostrar_resumen()
        self._ocultar_botones_resumen()
        self.vista.boton_editar_resumen.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.vista.boton_pagar_resumen.pack(side="right", fill="x", expand=True, padx=(6, 0))

    def confirmacion_pago(self):
        self._mostrar_resumen()
        self._ocultar_botones_resumen()
        self.vista.boton_cancelar_pago.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.vista.boton_confirmar_pago.pack(side="right", fill="x", expand=True, padx=(6, 0))
        self._configurar(self.vista.boton_cancelar_pago, True)
        self._configurar(self.vista.boton_confirmar_pago, True)

    def procesando_pago(self):
        self.confirmacion_pago()
        self._configurar(self.vista.boton_cancelar_pago, False)
        self._configurar(self.vista.boton_confirmar_pago, False)

    def confirmar_cancelacion_suscripcion(self, mostrar):
        self.vista.confirmacion_suscripcion.pack(side="left", padx=(8, 0)) if mostrar else self.vista.confirmacion_suscripcion.pack_forget()

    def confirmar_cancelacion_viaje(self, mostrar):
        self.vista.confirmacion_viaje.grid() if mostrar else self.vista.confirmacion_viaje.grid_remove()

    def sin_viajes(self):
        self._configurar(self.vista.boton_confirmar_inicio, False)
        self._configurar(self.vista.boton_cancelar_suscripcion, True)
        self.vista.panel_progreso.grid_remove()
        self.bloquear_creacion(False)

    def esperando_inicio(self, bloquear=False):
        self._configurar(self.vista.boton_confirmar_inicio, False)
        self._configurar(self.vista.boton_cancelar_suscripcion, not bloquear)
        self.vista.panel_progreso.grid_remove()
        self.bloquear_creacion(bloquear)

    def inicio_disponible(self):
        self._configurar(self.vista.boton_confirmar_inicio, True)
        self._configurar(self.vista.boton_cancelar_suscripcion, False)
        self.vista.panel_progreso.grid_remove()
        self.bloquear_creacion(True)

    def trayecto_en_curso(self):
        self._configurar(self.vista.boton_confirmar_inicio, False)
        self._configurar(self.vista.boton_cancelar_suscripcion, False)
        self.vista.panel_progreso.grid()
        self.bloquear_creacion(True)

    def bloquear_creacion(self, bloquear):
        vista = self.vista
        bloquear = bloquear or getattr(vista.usuario_actual, "tipo_usuario", "") != "pasajero"
        vista.bloqueo_creacion = bloquear
        if getattr(vista.usuario_actual, "tipo_usuario", "") != "pasajero":
            self._habilitar_campos(False)
        if vista.boton_buscar_conductor.winfo_manager():
            self._configurar(vista.boton_buscar_conductor, not bloquear)
        if vista.area_acciones_formulario.winfo_manager():
            self._configurar(vista.boton_crear_suscripcion, not bloquear and bool(vista.tabla_conductores.selection()))

    def _mostrar_resumen(self):
        self.vista.panel_formulario.grid()
        self.vista.panel_resumen.grid()
        self.vista.panel_resumen.tkraise()

    def _ocultar_botones_resumen(self):
        for boton in (self.vista.boton_editar_resumen, self.vista.boton_pagar_resumen, self.vista.boton_confirmar_pago, self.vista.boton_cancelar_pago):
            boton.pack_forget()

    def _habilitar_campos(self, habilitado):
        estado_entrada = "normal" if habilitado else "disabled"
        estado_selector = "readonly" if habilitado else "disabled"
        for entrada in (self.vista.fecha_inicio, self.vista.fecha_fin, self.vista.hora):
            entrada.configure(state=estado_entrada)
        for selector in (self.vista.origen, self.vista.destino, self.vista.pasajeros):
            selector.configure(state=estado_selector)
        for check in self.vista.checks_dias:
            check.configure(state=estado_entrada)

    @staticmethod
    def _configurar(boton, habilitado):
        boton.configure(state="normal" if habilitado else "disabled", cursor="hand2" if habilitado else "arrow")
