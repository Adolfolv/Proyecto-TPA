"""Unidad de trabajo para el agregado Suscripcion + ViajesProgramados."""


class UnidadTrabajoSuscripcion:
    """Agrupa cambios en memoria y realiza una única escritura al confirmar.

    Unit of Work no intenta incluir la billetera: dos archivos JSON distintos no
    pueden confirmarse atómicamente. Los pagos se coordinan mediante compensación
    en los servicios de alta, cancelación y liquidación del conductor.
    """

    def __init__(self, repositorio):
        self.repositorio = repositorio
        self._snapshot = None
        self._confirmada = False

    def __enter__(self):
        self._snapshot = self.repositorio.crear_snapshot()
        return self

    def confirmar(self):
        self.repositorio.guardar_cambios()
        self._confirmada = True

    def marcar_sin_cambios(self):
        """Cierra una lectura sin escribir ni reemplazar objetos en memoria."""
        self._confirmada = True

    def __exit__(self, tipo_error, error, traceback):
        if tipo_error is not None or not self._confirmada:
            self.repositorio.restaurar_snapshot(self._snapshot)
        return False
