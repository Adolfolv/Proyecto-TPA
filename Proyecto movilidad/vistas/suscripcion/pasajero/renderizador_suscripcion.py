from Modelos.Suscripcion.modelos_suscripcion import ESTADO_CANCELADA, NOMBRES_DIAS, VIAJE_CANCELADO, VIAJE_FINALIZADO
from ...viaje.temporizador_viaje import TemporizadorViaje


class RenderizadorSuscripcionPasajero:
    """Pinta resultados, cronómetros y tablas; no ejecuta casos de uso."""

    def __init__(self, vista):
        self.vista = vista
        self.temporizador = TemporizadorViaje(vista.label_busqueda)

    def mostrar_mensaje(self, texto, exitoso=False):
        self.vista._mostrar_mensaje(texto, exitoso)

    def iniciar_busqueda_conductor(self, al_finalizar, duracion=5):
        self.vista.label_busqueda.configure(text="Buscando conductor - 00:00")
        self.temporizador.contar_ascendente(duracion, lambda segundos: self.vista.label_busqueda.configure(text=f"Buscando conductor - 00:{segundos:02d}"), al_finalizar)

    def mostrar_conductores(self, conductores):
        vista = self.vista
        for item in vista.tabla_conductores.get_children():
            vista.tabla_conductores.delete(item)
        vista.conductores_por_item = {}
        for conductor in conductores:
            item = vista.tabla_conductores.insert("", "end", values=(conductor.nombre_completo, f"{conductor.vehiculo} ({conductor.patente})", f"${conductor.precio:,.0f}"))
            vista.conductores_por_item[item] = conductor
        vista.label_busqueda.configure(text="Conductores encontrados. Selecciona el que prefieras.")

    def mostrar_resumen(self, resumen, conductor):
        valores = {"ruta": f"{resumen.origen} -> {resumen.destino}", "periodo": f"{resumen.fecha_inicio} al {resumen.fecha_fin}", "dias": ", ".join(NOMBRES_DIAS[dia] for dia in resumen.dias_semana), "hora": resumen.hora, "cantidad_viajes": str(resumen.cantidad_viajes), "pasajeros": str(resumen.cantidad_pasajeros), "precio_viaje": f"${resumen.precio_por_viaje:,.0f}", "vehiculo": f"{conductor.vehiculo} ({conductor.patente}) - ${conductor.precio:,.0f} por viaje", "precio_total": f"${resumen.precio_total:,.0f}"}
        for clave, valor in valores.items():
            self.vista.valores_resumen[clave].configure(text=valor)

    def actualizar_listados(self, suscripciones, viajes):
        vista = self.vista
        suscripciones = [item for item in suscripciones if item.estado != ESTADO_CANCELADA]
        viajes = [item for item in viajes if item.estado not in (VIAJE_CANCELADO, VIAJE_FINALIZADO)]
        vista.suscripciones = {item.id_suscripcion: item for item in suscripciones}
        vista.viajes = {item.id_viaje_programado: item for item in viajes}
        filas_suscripciones = {}
        for item in suscripciones:
            dias = ",".join(NOMBRES_DIAS[dia] for dia in item.dias_semana)
            filas_suscripciones[item.id_suscripcion] = (f"{item.origen} -> {item.destino}", f"{dias} {item.hora}", item.conductor or "Sin asignar", f"${item.precio_total:,.0f}", item.estado)
        filas_viajes = {}
        for item in viajes:
            detalle = item.conductor or item.error or "Pendiente"
            filas_viajes[item.id_viaje_programado] = (item.fecha_hora.replace("T", " "), f"{item.origen} -> {item.destino}", item.estado, f"{detalle} - ${item.precio:,.0f}" if item.precio else detalle)
        vista.moldes.sincronizar_tabla(vista.tabla_suscripciones, filas_suscripciones)
        vista.moldes.sincronizar_tabla(vista.tabla_viajes, filas_viajes)

    def mostrar_cronometro(self, texto):
        self.vista.texto_temporizador.configure(text=texto)

    def mostrar_progreso(self, porcentaje):
        self.vista.barra_progreso["value"] = porcentaje
        self.vista.label_progreso.configure(text=f"{porcentaje}%")
