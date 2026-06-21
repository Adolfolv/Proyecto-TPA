class PlanificadorSuscripciones:
    """Conecta el ciclo de Tkinter con el procesador temporal del dominio."""

    INTERVALO_MS = 30_000

    def __init__(self, ventana, procesador):
        self.ventana = ventana
        self.procesador = procesador
        self.id_tarea = None

    def iniciar(self):
        if self.id_tarea is None:
            self.id_tarea = self.ventana.after(1_000, self._comprobar)

    def _comprobar(self):
        self.id_tarea = None
        try:
            self.procesador.procesar()
        finally:
            if self.ventana.winfo_exists():
                self.id_tarea = self.ventana.after(self.INTERVALO_MS, self._comprobar)
