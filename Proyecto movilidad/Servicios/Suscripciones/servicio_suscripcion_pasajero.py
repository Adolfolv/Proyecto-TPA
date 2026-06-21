"""Casos de uso de suscripciones disponibles para el pasajero."""

from datetime import datetime, timedelta

from Modelos.Suscripcion.modelos_suscripcion import ESTADO_ACTIVA, ESTADO_CANCELADA, ESTADO_PAUSADA, VIAJE_ASIGNADO, VIAJE_CANCELADO, VIAJE_EN_CURSO, VIAJE_FINALIZADO, VIAJE_PROGRAMADO, ResumenSuscripcion
from Servicios.Suscripciones.puertos import FabricaUnidadTrabajo, PasarelaPagosSuscripcion, RepositorioSuscripciones
from Validaciones.suscripcion import ESTADOS_VIAJE_ACTIVO, ESTADOS_VIAJE_PENDIENTE


class ServicioSuscripcionPasajero:
    """SRP por actor: concentra el flujo completo del pasajero.

    La clase coordina casos de uso. Delega creación a Factory, validaciones a
    políticas, persistencia transaccional a Unit of Work y dinero a su puerto.
    """

    MARGEN_ATRASO = timedelta(minutes=15)
    CARGO_CANCELACION = 0.05

    def __init__(self, repositorio: RepositorioSuscripciones, viajes, pagos: PasarelaPagosSuscripcion, validaciones, politica_horarios, politica_pasajero, calculadora, fabrica, crear_unidad_trabajo: FabricaUnidadTrabajo, reloj):
        self.repositorio = repositorio
        self.viajes = viajes
        self.pagos = pagos
        self.validaciones = validaciones
        self.politica_horarios = politica_horarios
        self.politica_pasajero = politica_pasajero
        self.calculadora = calculadora
        self.fabrica = fabrica
        self.crear_unidad_trabajo = crear_unidad_trabajo
        self.reloj = reloj

    # --- Alta y consultas -------------------------------------------------
    def previsualizar(self, usuario, origen, destino, fecha_inicio, fecha_fin, dias_semana, hora, cantidad):
        ahora = self.reloj()
        inicio, fin, dias, horario, pasajeros = self.validaciones.validar(usuario, origen, destino, fecha_inicio, fecha_fin, dias_semana, hora, cantidad, ahora=ahora)
        fechas = self.politica_horarios.generar_fechas(inicio, fin, dias, horario, ahora)
        if not fechas:
            raise ValueError("El periodo elegido no contiene horarios futuros para esos dias.")
        existentes = tuple(viaje for viaje in self.repositorio.listar_viajes(id_pasajero=usuario.id_usuario) if viaje.estado in ESTADOS_VIAJE_ACTIVO)
        self.politica_pasajero.validar_alta(ahora, tuple(fechas), existentes)
        self.validaciones.validar_dias_con_horarios_futuros(fechas, dias)
        precio = self.calculadora.calcular_precio_por_viaje(origen, destino, pasajeros)
        return ResumenSuscripcion(origen=origen, destino=destino, fecha_inicio=inicio.isoformat(), fecha_fin=fin.isoformat(), dias_semana=dias, hora=horario.strftime("%H:%M"), cantidad_pasajeros=pasajeros, fechas_viaje=tuple(fecha.isoformat(timespec="minutes") for fecha in fechas), precio_por_viaje=precio, precio_total=precio * len(fechas))

    def confirmar(self, usuario, origen, destino, fecha_inicio, fecha_fin, dias_semana, hora, cantidad, conductor=None):
        if conductor is None:
            raise ValueError("Selecciona un conductor antes de crear la suscripcion.")
        resumen = self.previsualizar(usuario, origen, destino, fecha_inicio, fecha_fin, dias_semana, hora, cantidad)
        suscripcion, viajes = self.fabrica.crear_desde_resumen(usuario, resumen, conductor)

        # Saga: el cobro está fuera del archivo de suscripciones. Si el commit
        # falla, un reembolso compensa el movimiento ya realizado.
        self.pagos.cobrar_suscripcion(usuario, resumen.precio_total)
        try:
            with self.crear_unidad_trabajo() as unidad:
                unidad.repositorio.agregar_sin_guardar(suscripcion, viajes)
                unidad.confirmar()
        except OSError:
            self.pagos.reembolsar_suscripcion(usuario, resumen.precio_total)
            raise
        return suscripcion

    def buscar_conductores(self, cantidad_pasajeros, origen, destino):
        return self.viajes.buscar_vehiculos(cantidad_pasajeros, origen, destino)

    def obtener_lugares_disponibles(self):
        return self.viajes.comun.obtener_lugares_disponibles()

    def listar_suscripciones(self, usuario):
        return self.repositorio.listar_suscripciones(usuario.id_usuario)

    def listar_viajes(self, usuario, limite=None):
        viajes = sorted(self.repositorio.listar_viajes(id_pasajero=usuario.id_usuario), key=lambda item: item.fecha_hora)
        return viajes[:limite] if limite else viajes

    # --- Ciclo de vida de los viajes -------------------------------------
    def confirmar_inicio(self, usuario, id_viaje):
        viaje = next((item for item in self.repositorio.listar_viajes(id_pasajero=usuario.id_usuario) if item.id_viaje_programado == id_viaje), None)
        if viaje is None:
            raise ValueError("No se encontro el viaje programado.")
        if viaje.estado not in (VIAJE_PROGRAMADO, VIAJE_ASIGNADO):
            raise ValueError("Este viaje ya no esta pendiente de confirmacion.")
        ahora, horario = self.reloj(), datetime.fromisoformat(viaje.fecha_hora)
        if ahora < horario - timedelta(minutes=5):
            raise ValueError("Podras confirmar el inicio desde 5 minutos antes.")
        if ahora > horario + self.MARGEN_ATRASO:
            raise ValueError("El plazo para confirmar este viaje ya vencio.")
        suscripcion = self.repositorio.obtener_suscripcion(viaje.id_suscripcion)
        if suscripcion is None or suscripcion.estado != ESTADO_ACTIVA:
            raise ValueError("La suscripcion debe estar activa para iniciar el viaje.")
        with self.crear_unidad_trabajo() as unidad:
            viaje.pasajero_confirmo_en = ahora.isoformat(timespec="seconds")
            viaje.inicio_confirmado_en = ahora.isoformat(timespec="seconds")
            viaje.estado = VIAJE_EN_CURSO
            unidad.confirmar()
        return viaje

    def completar_viaje_pasajero(self, usuario, id_viaje):
        viaje = next((item for item in self.repositorio.listar_viajes(id_pasajero=usuario.id_usuario) if item.id_viaje_programado == id_viaje), None)
        if viaje is None or viaje.estado != VIAJE_EN_CURSO:
            raise ValueError("Solo se puede completar un viaje en curso.")
        with self.crear_unidad_trabajo() as unidad:
            viaje.estado = VIAJE_FINALIZADO
            suscripcion = self.repositorio.obtener_suscripcion(viaje.id_suscripcion)
            if suscripcion is not None:
                suscripcion.monto_consumido = round(suscripcion.monto_consumido + viaje.precio, 2)
            unidad.confirmar()
        return viaje

    def cancelar_viaje(self, usuario, id_viaje):
        cancelables = [item for item in self.repositorio.listar_viajes(id_pasajero=usuario.id_usuario) if item.estado in ESTADOS_VIAJE_PENDIENTE]
        viaje = next((item for item in cancelables if item.id_viaje_programado == id_viaje), None)
        if viaje is None:
            raise ValueError("No se encontro el viaje programado.")
        if self.politica_horarios.proximo(cancelables) is not viaje:
            raise ValueError("Solo se puede cancelar el proximo viaje programado.")
        with self.crear_unidad_trabajo() as unidad:
            viaje.estado = VIAJE_CANCELADO
            viaje.error = "Cancelado por el pasajero. El saldo se liquida al cancelar la suscripcion."
            unidad.confirmar()
        return viaje

    # --- Estado y cancelación del plan -----------------------------------
    def cambiar_estado(self, usuario, id_suscripcion, nuevo_estado):
        suscripcion = self._obtener_propia(usuario, id_suscripcion)
        if nuevo_estado == ESTADO_CANCELADA:
            self.politica_pasajero.validar_sin_viaje_inminente(self.repositorio.listar_viajes(id_pasajero=usuario.id_usuario), self.reloj())
        transiciones = {ESTADO_ACTIVA: {ESTADO_PAUSADA, ESTADO_CANCELADA}, ESTADO_PAUSADA: {ESTADO_ACTIVA, ESTADO_CANCELADA}}
        if nuevo_estado not in transiciones.get(suscripcion.estado, set()):
            raise ValueError("Ese cambio de estado no esta permitido.")
        if nuevo_estado != ESTADO_CANCELADA:
            with self.crear_unidad_trabajo() as unidad:
                suscripcion.estado = nuevo_estado
                unidad.confirmar()
            return suscripcion
        return self._cancelar_suscripcion(usuario, suscripcion)

    def _cancelar_suscripcion(self, usuario, suscripcion):
        viajes = self.repositorio.listar_viajes(id_suscripcion=suscripcion.id_suscripcion)
        if any(viaje.estado == VIAJE_EN_CURSO for viaje in viajes):
            raise ValueError("No se puede cancelar mientras existe un viaje en curso.")
        estado_anterior = suscripcion.estado
        estados_viajes = {viaje.id_viaje_programado: (viaje.estado, viaje.error, viaje.reembolsado) for viaje in viajes}
        suscripcion.estado = ESTADO_CANCELADA
        for viaje in viajes:
            if viaje.estado in (VIAJE_PROGRAMADO, VIAJE_ASIGNADO):
                viaje.estado, viaje.error, viaje.reembolsado = VIAJE_CANCELADO, "Suscripcion cancelada por el pasajero.", True
        consumido = sum(viaje.precio for viaje in viajes if viaje.estado == VIAJE_FINALIZADO)
        suscripcion.monto_consumido = max(suscripcion.monto_consumido, consumido)
        saldo = max(0, suscripcion.precio_total - suscripcion.monto_consumido)
        cargo = round(saldo * self.CARGO_CANCELACION, 2)
        reembolso = round(max(0, saldo - cargo), 2)

        # Saga persistente: PROCESANDO evita duplicar un reembolso si la app se
        # interrumpe entre el movimiento de dinero y el guardado final.
        if reembolso and not suscripcion.monto_reembolsado:
            suscripcion.cargo_cancelacion, suscripcion.reembolso_pendiente, suscripcion.reembolso_estado = cargo, reembolso, "PROCESANDO"
            self.repositorio.guardar_cambios()
            try:
                self.pagos.reembolsar_suscripcion(usuario, reembolso)
            except (ValueError, OSError):
                suscripcion.estado, suscripcion.reembolso_estado, suscripcion.reembolso_pendiente = estado_anterior, "PENDIENTE", 0.0
                for viaje in viajes:
                    viaje.estado, viaje.error, viaje.reembolsado = estados_viajes[viaje.id_viaje_programado]
                self.repositorio.guardar_cambios()
                raise
            suscripcion.monto_reembolsado, suscripcion.reembolso_pendiente, suscripcion.reembolso_estado = reembolso, 0.0, "PAGADO"
        elif not reembolso:
            suscripcion.reembolso_estado = "SIN_SALDO"
        self.repositorio.guardar_cambios()
        return suscripcion

    def _obtener_propia(self, usuario, id_suscripcion):
        suscripcion = self.repositorio.obtener_suscripcion(id_suscripcion)
        if suscripcion is None or str(suscripcion.id_pasajero) != str(usuario.id_usuario):
            raise ValueError("No se encontro la suscripcion.")
        return suscripcion
