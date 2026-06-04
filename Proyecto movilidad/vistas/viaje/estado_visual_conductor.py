class EstadoVisualConductor:
    """State visual del conductor: decide que widgets se muestran o bloquean."""

    def __init__(self, vista):
        # La vista conserva los widgets; esta clase solo cambia su estado.
        self.vista = vista

    def buscando_pasajero(self):
        # Mientras corre el cronometro no se puede cambiar la ubicacion ni buscar otra vez.
        self.vista.boton_buscar_pasajeros.config(state="disabled", cursor="arrow")
        self.vista.selector_ubicacion.config(state="disabled")

    def pasajero_encontrado(self):
        # Estado intermedio: se muestra el pasajero encontrado y se pide confirmacion.
        self.vista.frame_pasajero.grid()
        self.vista.frame_confirmacion.grid()
        self.vista.boton_volver.config(
            command=self.vista.acciones.presionar_boton_volver_pregunta_activa
        )

    def viaje_en_proceso(self):
        # Estado bloqueante: evita cancelar/cambiar datos cuando el viaje ya empezo.
        self.vista.boton_confirmar_viaje.config(state="disabled", cursor="arrow")
        self.vista.boton_cancelar_viaje.config(state="disabled", cursor="arrow")
        self.vista.boton_buscar_pasajeros.config(state="disabled", cursor="arrow")
        self.vista.selector_ubicacion.config(state="disabled")
        self.vista.boton_volver.config(
            command=self.vista.acciones.presionar_boton_volver_flujo_activo
        )
        self.vista.label_pregunta_confirmacion.grid_remove()
        self.vista.boton_confirmar_viaje.grid_remove()
        self.vista.boton_cancelar_viaje.grid_remove()
        self.vista.label_estado_viaje.grid()

    def viaje_finalizado(self):
        # Estado final: restablece volver al menu y muestra la opcion de buscar otro viaje.
        self.vista.boton_volver.config(command=self.vista.comando_volver_menu)
        self.vista.boton_buscar_otro_viaje.grid()
