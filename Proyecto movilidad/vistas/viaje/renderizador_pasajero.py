from .renderizador_base import RenderizadorViajeBase


class RenderizadorPasajero(RenderizadorViajeBase):
    """Pinta resultados propios del flujo del pasajero."""

    def mostrar_error_busqueda(self, mensaje):
        # El error de busqueda invalida tabla y marcadores anteriores.
        self.vista.label_error_busqueda.config(text=mensaje)
        self.limpiar_tabla_vehiculos()
        self.limpiar_mapa_busqueda()

    def mostrar_error_viaje(self, mensaje):
        # El error de pago/viaje usa el mismo espacio visual de errores.
        self.vista.label_error_busqueda.config(text=mensaje)

    def limpiar_tabla_vehiculos(self):
        # La tabla se reconstruye completa porque cada busqueda trae nuevos vehiculos.
        for item in self.vista.tabla_vehiculos.get_children():
            self.vista.tabla_vehiculos.delete(item)
        self.vista.vehiculos_por_item = {}

    def limpiar_mapa_busqueda(self):
        # Limpia marcadores y rutas asociados a una busqueda anterior.
        mapa = self.vista.mapa_viaje
        if mapa is None:
            return
        mapa.limpiar_conductores()
        mapa.limpiar_lugares()
        mapa.limpiar_trayectorias()

    def mostrar_vehiculos(self):
        # Inserta cada vehiculo encontrado y guarda el objeto real para recuperarlo al seleccionar.
        self.limpiar_tabla_vehiculos()
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
            self.vista.vehiculos_por_item[item] = vehiculo

    def mostrar_conductores_en_mapa(self):
        # Pinta los conductores encontrados y marca origen/destino de la busqueda.
        if self.vista.mapa_viaje is None:
            return
        self.vista.mapa_viaje.mostrar_conductores(self.vista.info_vehiculos_busqueda)
        self.vista.mapa_viaje.mostrar_lugares(
            (
                self.vista.ubicacion_inicial_busqueda,
                self.vista.ubicacion_final_busqueda,
            )
        )
