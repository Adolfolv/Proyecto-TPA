class EstadoVisualSuscripcionConductor:
    """State parcial: únicamente muestra y habilita widgets de la vista."""

    def __init__(self, vista):
        self.vista = vista

    def sin_viajes(self):
        self._configurar(self.vista.boton_pasajero_abordo, False)
        self._configurar(self.vista.boton_cancelar, False)
        self.vista.panel_progreso.grid_remove()

    def esperando_viaje(self):
        self._configurar(self.vista.boton_pasajero_abordo, False)
        self._configurar(self.vista.boton_cancelar, True)
        self.vista.panel_progreso.grid_remove()

    def pasajero_listo(self):
        self._configurar(self.vista.boton_pasajero_abordo, True)
        self._configurar(self.vista.boton_cancelar, True)
        self.vista.panel_progreso.grid_remove()

    def trayecto_en_curso(self):
        self._configurar(self.vista.boton_pasajero_abordo, False)
        self._configurar(self.vista.boton_cancelar, False)
        self.vista.panel_progreso.grid()

    def buscando_ofertas(self):
        self._configurar(self.vista.boton_buscar_ofertas, False)
        self.vista.boton_agregar.grid_remove()
        self.vista.label_mensaje_agenda.grid_remove()

    def ofertas_disponibles(self):
        self._configurar(self.vista.boton_buscar_ofertas, True)
        self.vista.boton_agregar.grid()
        self.vista.label_mensaje_agenda.grid()
        self._configurar(self.vista.boton_agregar, False)

    def oferta_en_revision(self):
        self.vista.panel_tarjeta_oferta.grid()
        self.vista.panel_tarjeta_oferta.tkraise()

    def agenda_visible(self):
        self.vista.panel_tarjeta_oferta.grid_remove()
        self.vista.panel_agenda.tkraise()

    def confirmar_cancelacion_viaje(self, mostrar):
        self.vista.confirmacion_viaje.grid() if mostrar else self.vista.confirmacion_viaje.grid_remove()

    @staticmethod
    def _configurar(boton, habilitado):
        boton.configure(state="normal" if habilitado else "disabled", cursor="hand2" if habilitado else "arrow")
