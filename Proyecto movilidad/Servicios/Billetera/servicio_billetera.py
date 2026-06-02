from Modelos.Billetera.tarjetas import ServicioTarjeta
from Modelos.Billetera.movimiento import HistorialTransacciones, Pago, MoverSaldo
from Validaciones.billetera import ValidadorMontoPositivo, ValidadorTarjetaEncontrada

#archivo para manejar la lógica de negocio relacionada con la billetera, 
# incluyendo la gestión de tarjetas, movimientos de saldo, pagos y recepciones. ,
# Este servicio se encarga de realizar las operaciones necesarias para agregar o eliminar tarjetas, 
# realizar pagos, recibir pagos, cargar o retirar fondos, y consultar el saldo y las tarjetas asociadas a la billetera del usuario.
class ServicioBilletera:

    def __init__(self, servicio_usuario=None):
        self.servicio_usuario = servicio_usuario
        self.tarjeta_service = ServicioTarjeta()
        self.mover = MoverSaldo()
        self.pago = Pago()
        self.historial = HistorialTransacciones()
        self.validador_monto_positivo = ValidadorMontoPositivo()
        self.validador_tarjeta_encontrada = ValidadorTarjetaEncontrada()

    def agregar_tarjeta(self, usuario, tipo, titular, numero, vencimiento, cvv):
        if not self.tarjeta_service.agregar_tarjeta(usuario, tipo, titular, numero, vencimiento, cvv):
            self._fallar("No se pudo agregar la tarjeta. Revisa tipo, numero, vencimiento, CVV o duplicados.")
        self.guardar()
        return True

    def eliminar_tarjeta(self, usuario, numero_tarjeta):
        if not self.tarjeta_service.eliminar_tarjeta(usuario, numero_tarjeta):
            self._fallar("No se pudo eliminar la tarjeta. Revisa el numero seleccionado.")
        self.guardar()
        return True

    def pagar(self, usuario, monto):
        if not self.pago.pagar(usuario.billetera, monto):
            self._fallar("No se pudo realizar el pago. Revisa monto o saldo disponible.")
        self.historial.crear_transaccion(usuario.billetera, "Pago", monto)
        self.guardar()
        return True

    def recibir_pago(self, usuario, monto):
        if not self.pago.recibir_pago(usuario.billetera, monto):
            self._fallar("No se pudo recibir el pago. Revisa que el monto sea valido.")
        self.historial.crear_transaccion(usuario.billetera, "Pago recibido", monto)
        self.guardar()
        return True

    def cargar_desde_tarjeta(self, usuario, numero_tarjeta, monto):

        if not self.validador_monto_positivo.validar(monto):
            self._fallar("No se pudo cargar desde la tarjeta. Revisa que el monto sea valido.")

        tarjeta = self._buscar_tarjeta(usuario, numero_tarjeta)

        if not self.validador_tarjeta_encontrada.validar(tarjeta):
            self._fallar("No se pudo cargar desde la tarjeta. Revisa la tarjeta seleccionada.")

        if not self.mover.mover_saldo(tarjeta, usuario.billetera, monto):
            self._fallar("No se pudo cargar desde la tarjeta. Revisa el saldo disponible.")
        self.historial.crear_transaccion(usuario.billetera, "Carga desde tarjeta", monto)
        self.guardar()
        return True

    def retirar_a_tarjeta(self, usuario, numero_tarjeta, monto):

        if not self.validador_monto_positivo.validar(monto):
            self._fallar("No se pudo retirar a la tarjeta. Revisa que el monto sea valido.")

        tarjeta = self._buscar_tarjeta(usuario, numero_tarjeta)

        if not self.validador_tarjeta_encontrada.validar(tarjeta):
            self._fallar("No se pudo retirar a la tarjeta. Revisa la tarjeta seleccionada.")

        if not self.mover.mover_saldo(usuario.billetera, tarjeta, monto):
            self._fallar("No se pudo retirar a la tarjeta. Revisa el saldo disponible.")
        self.historial.crear_transaccion(usuario.billetera, "Retiro a tarjeta", monto)
        self.guardar()
        return True

    def _buscar_tarjeta(self, usuario, numero):
        for t in usuario.billetera.tarjetas:
            if t.numero_tarjeta == numero:
                return t
        return None

    def _fallar(self, mensaje):
        print(f"ValueError: {mensaje}")
        raise ValueError(mensaje)

    def guardar(self):
        if self.servicio_usuario is not None:
            self.servicio_usuario.guardar()
