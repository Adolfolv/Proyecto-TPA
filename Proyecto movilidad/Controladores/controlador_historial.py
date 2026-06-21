class ControladorHistorial:
    def __init__(self, servicio_historial):
        self.servicio_historial = servicio_historial

    def consultar(self, usuario):
        return self.servicio_historial.consultar(usuario)
