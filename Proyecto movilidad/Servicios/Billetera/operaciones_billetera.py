from abstracciones import OperacionBilletera
from Modelos.Billetera.movimiento import HistorialTransacciones, MoverSaldo, Pago


class OperacionMovimiento(OperacionBilletera):
    tipo_transaccion = ""

    def __init__(self, repositorio_billetera, historial=None):
        self.repositorio_billetera = repositorio_billetera
        self.historial = historial or HistorialTransacciones()

    def _completar(self, usuario, billetera, monto):
        self.historial.crear_transaccion(billetera, self.tipo_transaccion, monto)
        self.repositorio_billetera.guardar_por_usuario(usuario.id_usuario, billetera)
        return True

    def _obtener_billetera(self, usuario):
        billetera = self.repositorio_billetera.obtener_por_usuario(usuario.id_usuario)
        usuario.billetera = billetera
        return billetera

class OperacionPagoBase(OperacionMovimiento):
    metodo_pago = ""

    def __init__(self, repositorio_billetera, pago=None, historial=None):
        super().__init__(repositorio_billetera, historial)
        self.pago = pago or Pago()

    def ejecutar(self, solicitud):
        billetera = self._obtener_billetera(solicitud.usuario)
        getattr(self.pago, self.metodo_pago)(billetera, solicitud.monto)
        return self._completar(solicitud.usuario, billetera, solicitud.monto)


class OperacionPago(OperacionPagoBase):
    tipo_transaccion = "Pago"
    metodo_pago = "pagar"


class OperacionPagoRecibido(OperacionPagoBase):
    tipo_transaccion = "Pago recibido"
    metodo_pago = "recibir_pago"


class OperacionMovimientoTarjeta(OperacionMovimiento):
    origen_es_billetera = False

    def __init__(
        self,
        repositorio_billetera,
        servicio_tarjeta,
        mover=None,
        historial=None,
    ):
        super().__init__(repositorio_billetera, historial)
        self.servicio_tarjeta = servicio_tarjeta
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


class OperacionCargaTarjeta(OperacionMovimientoTarjeta):
    tipo_transaccion = "Carga desde tarjeta"


class OperacionRetiroTarjeta(OperacionMovimientoTarjeta):
    tipo_transaccion = "Retiro a tarjeta"
    origen_es_billetera = True
