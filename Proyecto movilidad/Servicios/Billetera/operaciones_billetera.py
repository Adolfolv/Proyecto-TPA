from abstracciones import OperacionBilletera
from Modelos.Billetera.movimiento import HistorialTransacciones, MoverSaldo, Pago


class OperacionMovimiento(OperacionBilletera):

    def __init__(self, repositorio_billetera, tipo_transaccion, historial=None):
        self.repositorio_billetera = repositorio_billetera
        self.tipo_transaccion = tipo_transaccion
        self.historial = historial or HistorialTransacciones()

    def _completar(self, usuario, billetera, monto):
        self.historial.crear_transaccion(billetera, self.tipo_transaccion, monto)
        self.repositorio_billetera.guardar_por_usuario(usuario.id_usuario, billetera)
        return True

    def _obtener_billetera(self, usuario):
        return self.repositorio_billetera.obtener(usuario)


class OperacionPago(OperacionMovimiento):

    def __init__(
        self,
        repositorio_billetera,
        tipo_transaccion,
        metodo_pago,
        pago=None,
        historial=None,
    ):
        super().__init__(repositorio_billetera, tipo_transaccion, historial)
        self.metodo_pago = metodo_pago
        self.pago = pago or Pago()

    def ejecutar(self, solicitud):
        billetera = self._obtener_billetera(solicitud.usuario)
        getattr(self.pago, self.metodo_pago)(billetera, solicitud.monto)
        return self._completar(solicitud.usuario, billetera, solicitud.monto)


class OperacionMovimientoTarjeta(OperacionMovimiento):

    def __init__(
        self,
        repositorio_billetera,
        servicio_tarjeta,
        tipo_transaccion,
        origen_es_billetera=False,
        mover=None,
        historial=None,
    ):
        super().__init__(repositorio_billetera, tipo_transaccion, historial)
        self.servicio_tarjeta = servicio_tarjeta
        self.origen_es_billetera = origen_es_billetera
        self.mover = mover or MoverSaldo()

    def ejecutar(self, solicitud):
        billetera = self._obtener_billetera(solicitud.usuario)
        tarjeta = self.servicio_tarjeta.obtener_tarjeta(
            solicitud.usuario,
            solicitud.numero_tarjeta,
        )
        origen, destino = (
            (billetera, tarjeta)
            if self.origen_es_billetera
            else (tarjeta, billetera)
        )
        self.mover.mover_saldo(origen, destino, solicitud.monto)
        return self._completar(solicitud.usuario, billetera, solicitud.monto)
