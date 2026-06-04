class EstadoVisualPasajero:
    """State visual del pasajero: decide que widgets se muestran o bloquean."""

    def __init__(self, vista):
        # La vista sigue siendo duena de los widgets; esta clase solo cambia su estado.
        self.vista = vista

    def reiniciar_busqueda(self):
        self.vista.frame_confirmacion.grid_remove()
        self.vista.boton_pagar.grid_remove()

    def vehiculo_seleccionado(self):
        # Estado donde ya existe un vehiculo elegido y se puede pasar al pago.
        self.vista.frame_confirmacion.grid_remove()
        self.vista.boton_pagar.grid()

    def confirmando_pago(self):
        # Muestra el panel de confirmacion sin iniciar todavia el viaje.
        self.vista.frame_confirmacion.grid()

    def viaje_en_proceso(self):
        # Estado bloqueante: evita cambiar datos mientras corre la animacion del viaje.
        self.vista.boton_confirmar_pago.config(state="disabled", cursor="arrow")
        self.vista.boton_cancelar_pago.config(state="disabled", cursor="arrow")
        self.vista.boton_buscar_vehiculos.config(state="disabled", cursor="arrow")
        self.vista.boton_pagar.config(state="disabled", cursor="arrow")
        self.vista.boton_pagar.grid_remove()
        self.vista.selector_ubicacion_inicial.config(state="disabled")
        self.vista.selector_ubicacion_final.config(state="disabled")
        self.vista.entrada_usuarios.config(state="disabled")
        self.vista.tabla_vehiculos.config(selectmode="none")
        self.vista.label_pregunta_confirmacion.grid_remove()
        self.vista.boton_confirmar_pago.grid_remove()
        self.vista.boton_cancelar_pago.grid_remove()
        self.vista.label_estado_viaje.grid()

    def viaje_finalizado(self):
        # Estado final: informa cierre del viaje y habilita reiniciar el flujo.
        self.vista.boton_buscar_otro_viaje.grid()
