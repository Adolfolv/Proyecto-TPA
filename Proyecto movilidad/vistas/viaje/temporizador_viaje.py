class TemporizadorViaje:
    """Reloj visual reutilizable por viajes normales y suscripciones."""

    INTERVALO_MS = 1_000

    def __init__(self, widget):
        self.widget = widget

    def repetir(self, actualizar):
        if not self.widget.winfo_exists():
            return
        actualizar()
        self.widget.after(self.INTERVALO_MS, self.repetir, actualizar)

    def contar_ascendente(self, duracion, actualizar, al_finalizar, segundos=0):
        actualizar(segundos)
        if segundos >= duracion:
            al_finalizar()
            return
        self.widget.after(
            self.INTERVALO_MS,
            self.contar_ascendente,
            duracion,
            actualizar,
            al_finalizar,
            segundos + 1,
        )

    @staticmethod
    def formatear(delta):
        segundos = max(0, int(delta.total_seconds()))
        horas, resto = divmod(segundos, 3600)
        minutos, segundos = divmod(resto, 60)
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

    @staticmethod
    def porcentaje(ahora, inicio, duracion_segundos):
        duracion = max(1, duracion_segundos)
        return min(100, max(0, int(((ahora - inicio).total_seconds() / duracion) * 100)))
