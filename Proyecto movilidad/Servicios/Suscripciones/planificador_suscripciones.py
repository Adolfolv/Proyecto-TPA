class PlanificadorSuscripciones:
    """Adaptador de reloj para Tkinter; la logica temporal permanece en el servicio."""

    INTERVALO_MS = 30_000

    def __init__(self, ventana, servicio_suscripcion):
        self.ventana = ventana
        self.servicio_suscripcion = servicio_suscripcion
        self.id_tarea = None

    def iniciar(self):
        if self.id_tarea is None:
            self.id_tarea = self.ventana.after(1_000, self._comprobar)

    def _comprobar(self):
        self.id_tarea = None
        try:
            self.servicio_suscripcion.procesar_pendientes()
        finally:
            if self.ventana.winfo_exists():
                self.id_tarea = self.ventana.after(self.INTERVALO_MS, self._comprobar)

