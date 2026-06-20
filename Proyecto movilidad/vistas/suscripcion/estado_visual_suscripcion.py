from abc import ABC, abstractmethod


class EstadoVisualSuscripcion(ABC):
    """State base para las etapas visuales de alta de una suscripcion."""

    def __init__(self, vista):
        self.vista = vista

    @abstractmethod
    def aplicar(self):
        pass


class EstadoFormulario(EstadoVisualSuscripcion):
    def aplicar(self):
        self.vista.tarjeta.ocultar()
        self.vista.formulario.mostrar()
        self.vista.formulario.habilitar(True)


class EstadoCotizacion(EstadoVisualSuscripcion):
    def aplicar(self):
        self.vista.formulario.ocultar()
        self.vista.tarjeta.mostrar()
        self.vista.tarjeta.bloquear_confirmacion(False)
        self.vista.tarjeta.mostrar_cotizacion()


class EstadoConfirmacionPago(EstadoVisualSuscripcion):
    def aplicar(self):
        self.vista.formulario.ocultar()
        self.vista.tarjeta.mostrar()
        self.vista.tarjeta.bloquear_confirmacion(False)
        self.vista.tarjeta.mostrar_confirmacion()


class EstadoProcesandoPago(EstadoVisualSuscripcion):
    def aplicar(self):
        self.vista.tarjeta.mostrar()
        self.vista.tarjeta.mostrar_confirmacion()
        self.vista.tarjeta.bloquear_confirmacion(True)


class FlujoVisualSuscripcion:
    """Contexto State que mantiene una unica etapa visual activa."""

    def __init__(self, vista):
        self.vista = vista
        self.estado = None

    def cambiar(self, clase_estado):
        self.estado = clase_estado(self.vista)
        self.estado.aplicar()
