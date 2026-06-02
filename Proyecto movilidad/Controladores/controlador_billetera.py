class ControladorBilletera:

    def __init__(self, servicio_billetera):
        self.servicio = servicio_billetera

    def conectar_vista(self, vista, usuario):
        vista.conectar_controlador(self, usuario)

    def agregar_tarjeta(self, usuario, tipo, titular, numero, vencimiento, cvv):
        return self.servicio.agregar_tarjeta(usuario, tipo, titular, numero, vencimiento, cvv)

    def eliminar_tarjeta(self, usuario, numero):
        return self.servicio.eliminar_tarjeta(usuario, numero)

    def pagar(self, usuario, monto):
        return self.servicio.pagar(usuario, float(monto))

    def recibir(self, usuario, monto):
        return self.servicio.recibir_pago(usuario, float(monto))

    def cargar_desde_tarjeta(self, usuario, numero_tarjeta, monto):
        return self.servicio.cargar_desde_tarjeta(usuario, numero_tarjeta, float(monto))

    def retirar_a_tarjeta(self, usuario, numero_tarjeta, monto):
        return self.servicio.retirar_a_tarjeta(usuario, numero_tarjeta, float(monto))

    def listar_tarjetas(self, usuario):
        return usuario.billetera.tarjetas

    def saldo_billetera(self, usuario):
        return usuario.billetera.saldo
