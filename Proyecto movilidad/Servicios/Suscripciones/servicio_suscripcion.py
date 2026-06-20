from datetime import date, datetime, timedelta
from uuid import uuid4

from Modelos.Suscripcion.modelos_suscripcion import (
    ESTADO_ACTIVA,
    ESTADO_CANCELADA,
    ESTADO_FINALIZADA,
    ESTADO_PAUSADA,
    VIAJE_BUSCANDO,
    VIAJE_CANCELADO,
    VIAJE_CONFIRMADO,
    VIAJE_FALLIDO,
    VIAJE_PROGRAMADO,
    ResumenSuscripcion,
    SuscripcionViaje,
    ViajeProgramado,
)
from Validaciones.suscripcion import ValidacionesSuscripcion
from Servicios.Suscripciones.calculadora_cotizacion import (
    CalculadoraCotizacionSuscripcion,
)


class ServicioSuscripcion:
    """Casos de uso para crear, administrar y ejecutar viajes recurrentes."""

    MARGEN_ATRASO = timedelta(minutes=15)

    def __init__(
        self,
        repositorio,
        repositorio_usuario,
        servicio_viaje,
        reloj=None,
        calculadora_cotizacion=None,
    ):
        self.repositorio = repositorio
        self.repositorio_usuario = repositorio_usuario
        self.servicio_viaje = servicio_viaje
        self.validaciones = ValidacionesSuscripcion()
        self.reloj = reloj or datetime.now
        self.calculadora_cotizacion = (
            calculadora_cotizacion
            or CalculadoraCotizacionSuscripcion(servicio_viaje.comun)
        )

    def previsualizar(self, usuario, origen, destino, fecha_inicio, fecha_fin, dias_semana, hora, cantidad):
        inicio, fin, dias, horario, pasajeros = self.validaciones.validar(
            usuario, origen, destino, fecha_inicio, fecha_fin, dias_semana, hora, cantidad
        )
        ahora = self.reloj()
        fechas = self._obtener_fechas_viaje(inicio, fin, dias, horario, ahora)
        if not fechas:
            raise ValueError("El periodo elegido no contiene horarios futuros para esos dias.")
        self.validaciones.validar_dias_con_horarios_futuros(fechas, dias)
        precio_por_viaje = self.calculadora_cotizacion.calcular_precio_por_viaje(
            origen, destino, pasajeros
        )
        return ResumenSuscripcion(
            origen=origen,
            destino=destino,
            fecha_inicio=inicio.isoformat(),
            fecha_fin=fin.isoformat(),
            dias_semana=dias,
            hora=horario.strftime("%H:%M"),
            cantidad_pasajeros=pasajeros,
            fechas_viaje=tuple(fecha.isoformat(timespec="minutes") for fecha in fechas),
            precio_por_viaje=precio_por_viaje,
            precio_total=precio_por_viaje * len(fechas),
        )

    def confirmar(self, usuario, origen, destino, fecha_inicio, fecha_fin, dias_semana, hora, cantidad):
        resumen = self.previsualizar(
            usuario, origen, destino, fecha_inicio, fecha_fin, dias_semana, hora, cantidad
        )
        self.servicio_viaje.cobrar_suscripcion(usuario, resumen.precio_total)
        ahora = self.reloj()
        id_suscripcion = uuid4().hex
        suscripcion = SuscripcionViaje(
            id_suscripcion=id_suscripcion,
            id_pasajero=str(usuario.id_usuario),
            origen=resumen.origen,
            destino=resumen.destino,
            fecha_inicio=resumen.fecha_inicio,
            fecha_fin=resumen.fecha_fin,
            dias_semana=resumen.dias_semana,
            hora=resumen.hora,
            cantidad_pasajeros=resumen.cantidad_pasajeros,
            creada_en=ahora.isoformat(timespec="seconds"),
            cantidad_viajes=resumen.cantidad_viajes,
            precio_por_viaje=resumen.precio_por_viaje,
            precio_total=resumen.precio_total,
            pagada_anticipadamente=True,
        )
        viajes = self._generar_viajes(suscripcion, resumen.fechas_viaje)
        try:
            self.repositorio.agregar(suscripcion, viajes)
        except OSError:
            self.servicio_viaje.reembolsar_suscripcion(usuario, resumen.precio_total)
            raise
        return suscripcion

    def crear(self, usuario, origen, destino, fecha_inicio, fecha_fin, dias_semana, hora, cantidad):
        return self.confirmar(
            usuario, origen, destino, fecha_inicio, fecha_fin, dias_semana, hora, cantidad
        )

    def _obtener_fechas_viaje(self, inicio, fin, dias, horario, ahora):
        fechas = []
        fecha_actual = inicio
        while fecha_actual <= fin:
            fecha_hora = datetime.combine(fecha_actual, horario)
            if fecha_actual.weekday() in dias and fecha_hora > ahora:
                fechas.append(fecha_hora)
            fecha_actual += timedelta(days=1)
        return fechas

    def _generar_viajes(self, suscripcion, fechas_viaje):
        viajes = []
        for fecha_hora in fechas_viaje:
            viajes.append(
                ViajeProgramado(
                    id_viaje_programado=uuid4().hex,
                    id_suscripcion=suscripcion.id_suscripcion,
                    id_pasajero=suscripcion.id_pasajero,
                    origen=suscripcion.origen,
                    destino=suscripcion.destino,
                    cantidad_pasajeros=suscripcion.cantidad_pasajeros,
                    fecha_hora=fecha_hora,
                    precio=suscripcion.precio_por_viaje,
                    pagado_anticipadamente=suscripcion.pagada_anticipadamente,
                )
            )
        return viajes

    def listar_suscripciones(self, usuario):
        return self.repositorio.listar_suscripciones(usuario.id_usuario)

    def listar_viajes(self, usuario, limite=None):
        viajes = sorted(
            self.repositorio.listar_viajes(id_pasajero=usuario.id_usuario),
            key=lambda item: item.fecha_hora,
        )
        return viajes[:limite] if limite else viajes

    def cambiar_estado(self, usuario, id_suscripcion, nuevo_estado):
        suscripcion = self._obtener_propia(usuario, id_suscripcion)
        transiciones = {
            ESTADO_ACTIVA: {ESTADO_PAUSADA, ESTADO_CANCELADA},
            ESTADO_PAUSADA: {ESTADO_ACTIVA, ESTADO_CANCELADA},
        }
        if nuevo_estado not in transiciones.get(suscripcion.estado, set()):
            raise ValueError("Ese cambio de estado no esta permitido.")

        suscripcion.estado = nuevo_estado
        if nuevo_estado == ESTADO_CANCELADA:
            for viaje in self.repositorio.listar_viajes(id_suscripcion=id_suscripcion):
                if viaje.estado == VIAJE_PROGRAMADO:
                    self._reembolsar_viaje(viaje, usuario)
                    viaje.estado = VIAJE_CANCELADO
                    viaje.error = "Suscripcion cancelada por el pasajero."
        self.repositorio.guardar_cambios()
        return suscripcion

    def cancelar_viaje(self, usuario, id_viaje):
        viaje = next(
            (
                item for item in self.repositorio.listar_viajes(id_pasajero=usuario.id_usuario)
                if item.id_viaje_programado == id_viaje
            ),
            None,
        )
        if viaje is None:
            raise ValueError("No se encontro el viaje programado.")
        if viaje.estado != VIAJE_PROGRAMADO:
            raise ValueError("Solo se pueden cancelar viajes que aun estan programados.")
        self._reembolsar_viaje(viaje, usuario)
        viaje.estado = VIAJE_CANCELADO
        viaje.error = "Cancelado por el pasajero."
        self.repositorio.guardar_cambios()
        return viaje

    def procesar_pendientes(self, ahora=None):
        ahora = ahora or self.reloj()
        procesados = []
        cambios = False
        for viaje in self.repositorio.listar_viajes():
            if viaje.estado != VIAJE_PROGRAMADO:
                continue
            fecha_hora = datetime.fromisoformat(viaje.fecha_hora)
            if fecha_hora > ahora:
                continue

            suscripcion = self.repositorio.obtener_suscripcion(viaje.id_suscripcion)
            if suscripcion is None or suscripcion.estado == ESTADO_CANCELADA:
                self._reembolsar_viaje(viaje)
                viaje.estado = VIAJE_CANCELADO
                viaje.error = "La suscripcion ya no esta disponible."
                cambios = True
                continue
            if suscripcion.estado == ESTADO_PAUSADA:
                continue
            if ahora - fecha_hora > self.MARGEN_ATRASO:
                self._reembolsar_viaje(viaje)
                viaje.estado = VIAJE_FALLIDO
                viaje.error = "El horario vencio mientras la aplicacion estaba cerrada."
                cambios = True
                continue

            viaje.estado = VIAJE_BUSCANDO
            self.repositorio.guardar_cambios()
            self._confirmar_automaticamente(viaje)
            procesados.append(viaje)
            cambios = True

        cambios = self._finalizar_suscripciones(ahora.date()) or cambios
        if cambios:
            self.repositorio.guardar_cambios()
        return procesados

    def _confirmar_automaticamente(self, viaje):
        usuario = self._buscar_usuario(viaje.id_pasajero)
        if usuario is None:
            self._marcar_fallido(viaje, "No se encontro el pasajero de la suscripcion.")
            return

        resultado = self.servicio_viaje.buscar_vehiculos(
            viaje.cantidad_pasajeros,
            viaje.origen,
            viaje.destino,
        )
        if not resultado.exitoso or not resultado.vehiculos:
            self._marcar_fallido(viaje, resultado.error or "No hay conductores disponibles.")
            return

        vehiculo = min(resultado.vehiculos, key=lambda item: item.precio)
        confirmacion = self.servicio_viaje.confirmar_viaje_pasajero(
            usuario,
            vehiculo,
            viaje.origen,
            viaje.destino,
            cobrar=not viaje.pagado_anticipadamente,
        )
        if not confirmacion.exitoso:
            self._marcar_fallido(viaje, confirmacion.error)
            return

        viaje.estado = VIAJE_CONFIRMADO
        viaje.conductor = vehiculo.nombre_completo
        viaje.vehiculo = f"{vehiculo.vehiculo} ({vehiculo.patente})"
        viaje.error = ""

    def _marcar_fallido(self, viaje, mensaje):
        self._reembolsar_viaje(viaje)
        viaje.estado = VIAJE_FALLIDO
        viaje.error = mensaje

    def _reembolsar_viaje(self, viaje, usuario=None):
        if not viaje.pagado_anticipadamente or viaje.reembolsado or viaje.precio <= 0:
            return
        usuario = usuario or self._buscar_usuario(viaje.id_pasajero)
        if usuario is None:
            return
        self.servicio_viaje.reembolsar_suscripcion(usuario, viaje.precio)
        viaje.reembolsado = True

    def _buscar_usuario(self, id_usuario):
        return next(
            (
                usuario for usuario in self.repositorio_usuario.listar()
                if str(usuario.id_usuario) == str(id_usuario)
            ),
            None,
        )

    def _obtener_propia(self, usuario, id_suscripcion):
        suscripcion = self.repositorio.obtener_suscripcion(id_suscripcion)
        if suscripcion is None or str(suscripcion.id_pasajero) != str(usuario.id_usuario):
            raise ValueError("No se encontro la suscripcion.")
        return suscripcion

    def _finalizar_suscripciones(self, fecha_actual):
        hubo_cambios = False
        for suscripcion in self.repositorio.listar_suscripciones():
            if suscripcion.estado == ESTADO_ACTIVA and date.fromisoformat(suscripcion.fecha_fin) < fecha_actual:
                suscripcion.estado = ESTADO_FINALIZADA
                hubo_cambios = True
        return hubo_cambios
