from datetime import date, datetime, timedelta

from Servicios.Viajes.datos_viaje import LUGARES_OSORNO


class ValidacionesSuscripcion:
    FORMATO_FECHA = "%Y-%m-%d"
    FORMATO_HORA = "%H:%M"
    MAXIMO_DIAS_PERIODO = 365
    NOMBRES_DIAS = ("lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo")

    def validar(self, usuario, origen, destino, fecha_inicio, fecha_fin, dias_semana, hora, cantidad):
        if getattr(usuario, "tipo_usuario", "") != "pasajero":
            raise ValueError("Solo los pasajeros pueden crear suscripciones de viaje.")
        if origen not in LUGARES_OSORNO or destino not in LUGARES_OSORNO:
            raise ValueError("Selecciona ubicaciones disponibles.")
        if origen == destino:
            raise ValueError("El origen y el destino deben ser distintos.")

        inicio = self._fecha(fecha_inicio)
        fin = self._fecha(fecha_fin)
        horario = self._hora(hora)
        if inicio < date.today():
            raise ValueError("La fecha inicial no puede estar en el pasado.")
        if fin < inicio:
            raise ValueError("La fecha final debe ser posterior a la inicial.")
        if (fin - inicio).days > self.MAXIMO_DIAS_PERIODO:
            raise ValueError("El periodo no puede superar un ano.")

        dias = tuple(sorted(set(dias_semana)))
        if not dias or any(dia not in range(7) for dia in dias):
            raise ValueError("Selecciona al menos un dia de la semana.")
        self._validar_dias_dentro_del_periodo(inicio, fin, dias)
        try:
            pasajeros = int(cantidad)
        except (TypeError, ValueError) as error:
            raise ValueError("La cantidad de pasajeros debe ser un numero.") from error
        if pasajeros < 1 or pasajeros > 4:
            raise ValueError("La cantidad de pasajeros debe estar entre 1 y 4.")

        return inicio, fin, dias, horario, pasajeros

    def _validar_dias_dentro_del_periodo(self, inicio, fin, dias_seleccionados):
        dias_del_periodo = {
            (inicio + timedelta(days=desplazamiento)).weekday()
            for desplazamiento in range((fin - inicio).days + 1)
        }
        dias_faltantes = [
            self.NOMBRES_DIAS[dia]
            for dia in dias_seleccionados
            if dia not in dias_del_periodo
        ]
        if dias_faltantes:
            nombres = ", ".join(dias_faltantes)
            raise ValueError(
                f"El periodo seleccionado no contiene estos dias marcados: {nombres}."
            )

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
