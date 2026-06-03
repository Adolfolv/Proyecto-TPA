class ControladorBilletera:

    def __init__(self, servicio_billetera, servicio_tarjeta):
        self.servicio_billetera = servicio_billetera
        self.servicio_tarjeta = servicio_tarjeta

    def conectar_vista(self, vista, usuario):
        vista.conectar_controlador(self, usuario)

    def agregar_tarjeta(self, usuario, tipo, titular, numero, vencimiento, cvv):
        return self.servicio_tarjeta.agregar_tarjeta(usuario, tipo, titular, numero, vencimiento, cvv)

    def eliminar_tarjeta(self, usuario, numero):
        return self.servicio_tarjeta.eliminar_tarjeta(usuario, numero)

    def pagar(self, usuario, monto):
        return self.servicio_billetera.pagar(usuario, float(monto))

    def recibir(self, usuario, monto):
        return self.servicio_billetera.recibir_pago(usuario, float(monto))

    def cargar_desde_tarjeta(self, usuario, numero_tarjeta, monto):
        return self.servicio_billetera.cargar_desde_tarjeta(usuario, numero_tarjeta, float(monto))

    def retirar_a_tarjeta(self, usuario, numero_tarjeta, monto):
        return self.servicio_billetera.retirar_a_tarjeta(usuario, numero_tarjeta, float(monto))

    def listar_tarjetas(self, usuario):
        return self.servicio_tarjeta.obtener_tarjetas(usuario)

    def saldo_billetera(self, usuario):
        return usuario.billetera.saldo
