from Modelos.Billetera.movimiento import HistorialTransacciones, Pago, MoverSaldo

#archivo para manejar la lógica de negocio relacionada con la billetera, 
# incluyendo la gestión de tarjetas, movimientos de saldo, pagos y recepciones.  
# realizar pagos, recibir pagos, cargar o retirar fondos, y consultar el saldo a la billetera del usuario.
class ServicioBilletera:

    def __init__(self, repositorio_billetera, servicio_tarjeta):
        self.repositorio_billetera = repositorio_billetera
        self.servicio_tarjeta = servicio_tarjeta
        self.mover = MoverSaldo()
        self.pago = Pago()
        self.historial = HistorialTransacciones()

    def obtener_billetera(self, usuario):
        billetera = self.repositorio_billetera.obtener_por_usuario(usuario.id_usuario)
        usuario.billetera = billetera
        return billetera

    def pagar(self, usuario, monto):
        billetera = self.obtener_billetera(usuario)
        self.pago.pagar(billetera, monto)
        self.historial.crear_transaccion(billetera, "Pago", monto)
        self.guardar(usuario, billetera)
        return True

    def recibir_pago(self, usuario, monto):
        billetera = self.obtener_billetera(usuario)
        self.pago.recibir_pago(billetera, monto)
        self.historial.crear_transaccion(billetera, "Pago recibido", monto)
        self.guardar(usuario, billetera)
        return True

    def cargar_desde_tarjeta(self, usuario, numero_tarjeta, monto):
        billetera = self.obtener_billetera(usuario)
        tarjeta = self.servicio_tarjeta.obtener_tarjeta(usuario, numero_tarjeta)
        self.mover.mover_saldo(tarjeta, billetera, monto)
        self.historial.crear_transaccion(billetera, "Carga desde tarjeta", monto)
        self.guardar(usuario, billetera)
        return True

    def retirar_a_tarjeta(self, usuario, numero_tarjeta, monto):
        billetera = self.obtener_billetera(usuario)
        tarjeta = self.servicio_tarjeta.obtener_tarjeta(usuario, numero_tarjeta)
        self.mover.mover_saldo(billetera, tarjeta, monto)
        self.historial.crear_transaccion(billetera, "Retiro a tarjeta", monto)
        self.guardar(usuario, billetera)
        return True

    def guardar(self, usuario=None, billetera=None):
        if usuario is None:
            self.repositorio_billetera.guardar()
            return

        billetera = billetera or self.obtener_billetera(usuario)
        self.repositorio_billetera.guardar_por_usuario(usuario.id_usuario, billetera)
