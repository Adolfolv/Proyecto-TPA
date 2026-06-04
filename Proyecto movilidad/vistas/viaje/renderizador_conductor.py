from PIL import Image, ImageTk


class RenderizadorConductor:
    """Pinta resultados propios del flujo del conductor."""

    def __init__(self, vista):
        self.vista = vista

    def actualizar_cronometro_busqueda(self, al_finalizar, segundos=0):
        duracion = 5
        self.vista.label_cronometro.config(text=f"00:{segundos:02d}")

        if segundos >= duracion:
            al_finalizar()
            return

        self.vista.label_cronometro.after(
            1000,
            self.actualizar_cronometro_busqueda,
            al_finalizar,
            segundos + 1,
        )

    def mostrar_pasajero_encontrado(self):
        # Completa los widgets ya creados con los datos del pasajero.
        pasajero = self.vista.info_pasajero_busqueda
        imagen = Image.open(self.vista.ruta_imagenes_usuarios / pasajero.imagen)
        imagen.thumbnail((64, 64))
        self.vista.imagen_pasajero = ImageTk.PhotoImage(imagen)
        self.vista.label_imagen_pasajero.config(image=self.vista.imagen_pasajero)

        self.vista.label_nombre_pasajero.config(text=pasajero.nombre_completo)
        self.vista.label_trayecto_pasajero.config(text=pasajero.trayecto)
        self.vista.label_vehiculo_pasajero.config(
            text=f"Vehiculo: {pasajero.vehiculo}"
        )
        self.vista.label_pago_pasajero.config(text=f"Pago: ${pasajero.precio}")
        self.vista.label_llegada_pasajero.config(
            text=f"Llegar: {pasajero.km_para_llegar} km | {pasajero.tiempo_para_llegar} s"
        )
        self.vista.label_traslado_pasajero.config(
            text=f"Traslado: {pasajero.km_transportando} km | {pasajero.tiempo_transportando} s"
        )

    def mostrar_estado_viaje(self, mensaje):
        self.vista.label_estado_viaje.config(text=mensaje)

    def actualizar_progreso_viaje(self, progreso, estado):
        self.vista.barra_progreso["value"] = progreso
        self.vista.label_estado_progreso.config(text=estado)
        self.vista.label_porcentaje_progreso.config(text=f"{progreso}%")
