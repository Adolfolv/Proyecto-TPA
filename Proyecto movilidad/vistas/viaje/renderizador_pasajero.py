class RenderizadorPasajero:
    """Pinta resultados propios del flujo del pasajero."""

    def __init__(self, vista):
        self.vista = vista

    def mostrar_mensaje_error(self, mensaje):
        self.vista.label_error_busqueda.config(text=mensaje)

    def mostrar_estado_viaje(self, mensaje):
        self.vista.label_estado_viaje.config(text=mensaje)

    def actualizar_progreso_viaje(self, progreso, estado):
        self.vista.barra_progreso["value"] = progreso
        self.vista.label_estado_progreso.config(text=estado)
        self.vista.label_porcentaje_progreso.config(text=f"{progreso}%")

    def limpiar_tabla_vehiculos(self):
        # La tabla se reconstruye completa porque cada busqueda trae nuevos vehiculos.
        for item in self.vista.tabla_vehiculos.get_children():
            self.vista.tabla_vehiculos.delete(item)
    def mostrar_vehiculos(self):
        # Inserta cada vehiculo encontrado y devuelve su relacion con la fila creada.
        self.limpiar_tabla_vehiculos()
        vehiculos_por_item = {}
        for vehiculo in self.vista.info_vehiculos_busqueda:
            item = self.vista.tabla_vehiculos.insert(
                "",
                "end",
                values=(
                    vehiculo.nombre_completo,
                    f"{vehiculo.vehiculo} | {vehiculo.patente} | {vehiculo.distancia} km",
                    f"${vehiculo.precio}",
                    f"{vehiculo.tiempo} s",
                ),
                tags=("fila",),
            )
            vehiculos_por_item[item] = vehiculo
        return vehiculos_por_item
