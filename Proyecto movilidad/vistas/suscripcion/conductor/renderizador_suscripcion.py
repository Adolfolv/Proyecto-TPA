from random import randint

from Modelos.Suscripcion.modelos_suscripcion import NOMBRES_DIAS
from ...estilizacion import tema
from ...viaje.temporizador_viaje import TemporizadorViaje


class RenderizadorSuscripcionConductor:
    """Renderiza tablas, búsquedas y seguimiento; no llama controladores."""

    def __init__(self, vista):
        self.vista = vista
        self.temporizador = TemporizadorViaje(vista.label_cronometro)

    def mostrar_suscripciones(self, suscripciones):
        filas = {item.id_suscripcion: (f"{item.origen} -> {item.destino}", f"{item.fecha_inicio} / {item.fecha_fin}", f"{','.join(NOMBRES_DIAS[dia] for dia in item.dias_semana)} {item.hora}", item.cantidad_pasajeros) for item in suscripciones}
        self.vista.moldes.sincronizar_tabla(self.vista.tabla_suscripciones, filas)

    def mostrar_disponibles(self, suscripciones):
        filas = {item.id_suscripcion: (f"{item.origen} -> {item.destino}", f"{','.join(NOMBRES_DIAS[dia] for dia in item.dias_semana)} {item.hora}", item.cantidad_pasajeros) for item in suscripciones}
        self.vista.moldes.sincronizar_tabla(self.vista.tabla_disponibles, filas)

    def mostrar_viajes(self, viajes):
        filas = {item.id_viaje_programado: (item.fecha_hora.replace("T", " "), item.estado, f"${(item.pago_conductor or round(item.precio * 0.80)):,.0f}", item.error or item.conductor or "Pendiente") for item in viajes}
        self.vista.moldes.sincronizar_tabla(self.vista.tabla_viajes, filas)

    def mostrar_mensaje(self, texto, exitoso=False):
        self.vista.label_mensaje.configure(text=texto, fg=tema.EXITO if exitoso else tema.TEXTO_SUAVE)

    def mostrar_mensaje_agenda(self, texto, exitoso=False):
        self.vista.label_mensaje_agenda.configure(text=texto, fg=tema.EXITO if exitoso else tema.TEXTO_SUAVE)

    def mostrar_detalle_oferta(self, suscripcion, conductor):
        ganancia = round(suscripcion.precio_por_viaje * 0.80)
        valores = {"ruta": f"{suscripcion.origen} -> {suscripcion.destino}", "periodo": f"{suscripcion.fecha_inicio} al {suscripcion.fecha_fin}", "dias": ", ".join(NOMBRES_DIAS[dia] for dia in suscripcion.dias_semana), "hora": suscripcion.hora, "cantidad": str(suscripcion.cantidad_viajes), "pasajeros": str(suscripcion.cantidad_pasajeros), "ganancia": f"${ganancia:,.0f}", "ganancia_total": f"${ganancia * suscripcion.cantidad_viajes:,.0f}", "vehiculo": f"{conductor.auto.marca} {conductor.auto.modelo} ({conductor.auto.patente})"}
        for clave, valor in valores.items():
            self.vista.valores_oferta[clave].configure(text=valor)

    def iniciar_busqueda(self, al_finalizar):
        duracion = randint(5, 10)
        self.vista.label_busqueda_ofertas.configure(text="Buscando ofertas - 00:00")
        self.temporizador.contar_ascendente(duracion, lambda segundos: self.vista.label_busqueda_ofertas.configure(text=f"Buscando ofertas - 00:{segundos:02d}"), al_finalizar)

    def mostrar_cronometro(self, texto):
        self.vista.label_cronometro.configure(text=texto)

    def mostrar_progreso(self, porcentaje):
        self.vista.barra_progreso["value"] = porcentaje
        self.vista.label_progreso.configure(text=f"{porcentaje}%")
