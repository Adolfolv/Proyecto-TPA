"""Validaciones y políticas del dominio de suscripciones.

Las clases permanecen juntas porque todas representan reglas del mismo dominio,
pero se separan por responsabilidad: formato de entrada, horarios, pasajero y
conductor. Esto aplica SRP sin convertir cada comprobación en un archivo.
"""

from datetime import datetime, timedelta

from Modelos.Suscripcion.modelos_suscripcion import ESTADO_ACTIVA, VIAJE_ASIGNADO, VIAJE_EN_CURSO, VIAJE_PROGRAMADO
from Servicios.Viajes.datos_viaje import LUGARES_OSORNO


ESTADOS_VIAJE_ACTIVO = (VIAJE_PROGRAMADO, VIAJE_ASIGNADO, VIAJE_EN_CURSO)
ESTADOS_VIAJE_PENDIENTE = (VIAJE_PROGRAMADO, VIAJE_ASIGNADO)


class ValidacionesSuscripcion:
    """Valida y convierte los valores crudos recibidos desde el formulario."""

    FORMATO_FECHA = "%Y-%m-%d"
    FORMATO_HORA = "%H:%M"
    MAXIMO_DIAS_PERIODO = 365
    NOMBRES_DIAS = ("lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo")

    def validar(self, usuario, origen, destino, fecha_inicio, fecha_fin, dias_semana, hora, cantidad, ahora=None):
        ahora = ahora or datetime.now()
        if getattr(usuario, "tipo_usuario", "") != "pasajero":
            raise ValueError("Solo los pasajeros pueden crear suscripciones de viaje.")
        if origen not in LUGARES_OSORNO or destino not in LUGARES_OSORNO:
            raise ValueError("Selecciona ubicaciones disponibles.")
        if origen == destino:
            raise ValueError("El origen y el destino deben ser distintos.")
        inicio, fin, horario = self._fecha(fecha_inicio), self._fecha(fecha_fin), self._hora(hora)
        if inicio < ahora.date():
            raise ValueError("La fecha inicial no puede estar en el pasado.")
        if fin < inicio:
            raise ValueError("La fecha final debe ser posterior a la inicial.")
        if (fin - inicio).days > self.MAXIMO_DIAS_PERIODO:
            raise ValueError("El periodo no puede superar un ano.")
        dias = tuple(sorted(set(dias_semana)))
        if not dias or any(dia not in range(7) for dia in dias):
            raise ValueError("Selecciona al menos un dia de la semana.")
        self._validar_dias_dentro_del_periodo(inicio, fin, dias)
        if inicio == fin == ahora.date() and inicio.weekday() in dias and datetime.combine(inicio, horario) <= ahora:
            raise ValueError("Para una suscripcion de hoy, la hora debe ser posterior a la actual.")
        try:
            pasajeros = int(cantidad)
        except (TypeError, ValueError) as error:
            raise ValueError("La cantidad de pasajeros debe ser un numero.") from error
        if pasajeros < 1 or pasajeros > 4:
            raise ValueError("La cantidad de pasajeros debe estar entre 1 y 4.")
        return inicio, fin, dias, horario, pasajeros

    def validar_dias_con_horarios_futuros(self, fechas, dias_seleccionados):
        dias_futuros = {fecha.weekday() for fecha in fechas}
        faltantes = [self.NOMBRES_DIAS[dia] for dia in dias_seleccionados if dia not in dias_futuros]
        if faltantes:
            raise ValueError(f"No quedan horarios futuros dentro del periodo para: {', '.join(faltantes)}.")

    def _validar_dias_dentro_del_periodo(self, inicio, fin, dias_seleccionados):
        dias_periodo = {(inicio + timedelta(days=desplazamiento)).weekday() for desplazamiento in range((fin - inicio).days + 1)}
        faltantes = [self.NOMBRES_DIAS[dia] for dia in dias_seleccionados if dia not in dias_periodo]
        if faltantes:
            raise ValueError(f"El periodo seleccionado no contiene estos dias marcados: {', '.join(faltantes)}.")

    def _fecha(self, valor):
        try:
            return datetime.strptime(str(valor).strip(), self.FORMATO_FECHA).date()
        except ValueError as error:
            raise ValueError("Usa fechas con formato AAAA-MM-DD.") from error

    def _hora(self, valor):
        try:
            return datetime.strptime(str(valor).strip(), self.FORMATO_HORA).time()
        except ValueError as error:
            raise ValueError("Usa la hora con formato HH:MM.") from error


class PoliticaHorariosSuscripcion:
    """Operaciones temporales compartidas por pasajero y conductor."""

    @staticmethod
    def generar_fechas(inicio, fin, dias, horario, ahora):
        fechas, fecha_actual = [], inicio
        while fecha_actual <= fin:
            fecha_hora = datetime.combine(fecha_actual, horario)
            if fecha_actual.weekday() in dias and fecha_hora > ahora:
                fechas.append(fecha_hora)
            fecha_actual += timedelta(days=1)
        return fechas

    @staticmethod
    def validar_separacion(fechas_nuevas, viajes_existentes, separacion, mensaje):
        for fecha_nueva in fechas_nuevas:
            for viaje in viajes_existentes:
                if abs(fecha_nueva - datetime.fromisoformat(viaje.fecha_hora)) <= separacion:
                    raise ValueError(mensaje)

    @staticmethod
    def proximo(viajes, estados=ESTADOS_VIAJE_PENDIENTE):
        candidatos = [viaje for viaje in viajes if viaje.estado in estados]
        return min(candidatos, key=lambda viaje: viaje.fecha_hora) if candidatos else None


class PoliticaSuscripcionPasajero:
    """Specification condensada para operaciones del pasajero."""

    ANTICIPACION_MINIMA = timedelta(minutes=5)
    BLOQUEO_INMINENTE = timedelta(minutes=10)

    def __init__(self, horarios):
        self.horarios = horarios

    def validar_alta(self, ahora, fechas_nuevas, viajes_existentes):
        self.validar_sin_viaje_inminente(viajes_existentes, ahora)
        if fechas_nuevas[0] < ahora + self.ANTICIPACION_MINIMA:
            raise ValueError("La primera fecha de viaje debe estar al menos a 5 minutos de distancia.")
        self.horarios.validar_separacion(fechas_nuevas, viajes_existentes, self.ANTICIPACION_MINIMA, "Cada viaje de una nueva suscripcion debe estar a mas de 5 minutos de los viajes ya creados.")

    def validar_sin_viaje_inminente(self, viajes, ahora):
        for viaje in viajes:
            if viaje.estado not in ESTADOS_VIAJE_PENDIENTE:
                continue
            diferencia = datetime.fromisoformat(viaje.fecha_hora) - ahora
            if timedelta(0) <= diferencia < self.BLOQUEO_INMINENTE:
                raise ValueError("No se pueden crear ni cancelar suscripciones a menos de 10 minutos del proximo viaje.")


class PoliticaSuscripcionConductor:
    """Specification condensada para identidad, capacidad y agenda."""

    SEPARACION_AGENDA = timedelta(hours=1)

    def __init__(self, horarios):
        self.horarios = horarios

    @staticmethod
    def validar_conductor(conductor):
        if getattr(conductor, "tipo_usuario", "") != "conductor":
            raise ValueError("Esta operacion es exclusiva para conductores.")

    def validar_aceptacion(self, conductor, suscripcion, fechas_nuevas, viajes_existentes):
        self.validar_conductor(conductor)
        if suscripcion is None or suscripcion.estado != ESTADO_ACTIVA:
            raise ValueError("La suscripcion ya no esta disponible.")
        if suscripcion.id_conductor and str(suscripcion.id_conductor) != str(conductor.id_usuario):
            raise ValueError("La suscripcion ya fue agregada por otro conductor.")
        self.validar_capacidad(conductor, suscripcion.cantidad_pasajeros)
        self.horarios.validar_separacion(fechas_nuevas, viajes_existentes, self.SEPARACION_AGENDA, "No puedes agregarla: uno de sus viajes esta a una hora o menos de otro viaje de tu agenda.")

    @staticmethod
    def validar_capacidad(conductor, cantidad_pasajeros):
        if int(conductor.auto.cantidad_asientos) < cantidad_pasajeros:
            raise ValueError("El vehiculo no tiene asientos suficientes.")

    def validar_pertenencia(self, conductor, suscripcion):
        self.validar_conductor(conductor)
        if suscripcion is None or str(suscripcion.id_conductor) != str(conductor.id_usuario):
            raise ValueError("La suscripcion no pertenece a tu agenda.")
