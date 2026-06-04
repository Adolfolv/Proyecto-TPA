class EstadoVisualPasajero:
    """State visual del pasajero: decide que widgets se muestran o bloquean."""

    def __init__(self, vista):
        # La vista sigue siendo duena de los widgets; esta clase solo cambia su estado.
        self.vista = vista

    def busqueda_exitosa(self, ubicacion_inicial, ubicacion_final, vehiculos):
        # Estado posterior a una busqueda valida: guarda datos para tabla, mapa y pago.
        self.vista.info_vehiculos_busqueda = list(vehiculos)
        self.vista.ubicacion_inicial_busqueda = ubicacion_inicial
        self.vista.ubicacion_final_busqueda = ubicacion_final
        self.vista.vehiculo_seleccionado = None
        self.vista.label_error_busqueda.config(text="")
        self.vista.frame_confirmacion.grid_remove()
        self.vista.boton_pagar.grid_remove()

    def busqueda_con_error(self):
        # Si la busqueda falla, se ocultan acciones que solo sirven con resultados.
        self.vista.frame_confirmacion.grid_remove()
        self.vista.boton_pagar.grid_remove()

    def vehiculo_seleccionado(self, vehiculo):
        # Estado donde ya existe un vehiculo elegido y se puede pasar al pago.
        self.vista.vehiculo_seleccionado = vehiculo
        self.vista.frame_confirmacion.grid_remove()
        self.vista.boton_pagar.grid()

    def confirmando_pago(self):
        # Muestra el panel de confirmacion sin iniciar todavia el viaje.
        self.vista.frame_confirmacion.grid()

    def viaje_en_proceso(self):
        # Estado bloqueante: evita cambiar datos mientras corre la animacion del viaje.
        self.vista.viaje_en_proceso = True
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
        self.vista.label_estado_viaje.config(text="viaje en proceso")
        self.vista.label_estado_viaje.grid()

    def viaje_finalizado(self):
        # Estado final: informa cierre del viaje y habilita reiniciar el flujo.
        self.vista.label_estado_viaje.config(text="viaje finalizado")
        self.vista.boton_buscar_otro_viaje.grid()
