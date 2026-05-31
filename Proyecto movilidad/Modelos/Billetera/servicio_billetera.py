from Billetera.tarjetas import ServicioTarjeta
from Billetera.movimiento import Pago, MoverSaldo

#archivo para manejar la lógica de negocio relacionada con la billetera, 
# incluyendo la gestión de tarjetas, movimientos de saldo, pagos y recepciones. 
# Este servicio se encarga de realizar las operaciones necesarias para agregar o eliminar tarjetas, 
# realizar pagos, recibir pagos, cargar o retirar fondos, y consultar el saldo y las tarjetas asociadas a la billetera del usuario.
class ServicioBilletera:

    def __init__(self):
        self.tarjeta_service = ServicioTarjeta()
        self.mover = MoverSaldo()
        self.pago = Pago()

    def agregar_tarjeta(self, usuario, tarjeta):
        return self.tarjeta_service.agregar_tarjeta(usuario, tarjeta)

    def eliminar_tarjeta(self, usuario, numero_tarjeta):
        return self.tarjeta_service.eliminar_tarjeta(usuario, numero_tarjeta)

    def pagar(self, usuario, monto):
        return self.pago.pagar(usuario.billetera, monto)

    def recibir_pago(self, usuario, monto):
        return self.pago.recibir_pago(usuario.billetera, monto)

    def cargar_desde_tarjeta(self, usuario, numero_tarjeta, monto):

        if monto <= 0:
            return False

        tarjeta = self._buscar_tarjeta(usuario, numero_tarjeta)

        if not tarjeta:
            return False

        return self.mover.mover_saldo(tarjeta, usuario.billetera, monto)

    def retirar_a_tarjeta(self, usuario, numero_tarjeta, monto):

        if monto <= 0:
            return False

        tarjeta = self._buscar_tarjeta(usuario, numero_tarjeta)

        if not tarjeta:
            return False

        return self.mover.mover_saldo(usuario.billetera, tarjeta, monto)

    def _buscar_tarjeta(self, usuario, numero):
        for t in usuario.billetera.tarjetas:
            if t.numero_tarjeta == numero:
                return t
        return None
