class ControladorBilletera:

    def __init__(self, servicio_billetera, servicio_usuario):
        self.servicio = servicio_billetera
        self.servicio_usuario = servicio_usuario

    def conectar_vista(self, vista, usuario):
        vista.conectar_controlador(self, usuario)

    def agregar_tarjeta(self, usuario, tipo, titular, numero, vencimiento, cvv):
        self.servicio.agregar_tarjeta(usuario, tipo, titular, numero, vencimiento, cvv)
        return self._guardar()

    def eliminar_tarjeta(self, usuario, numero):
        self.servicio.eliminar_tarjeta(usuario, numero)
        return self._guardar()

    def pagar(self, usuario, monto):
        self.servicio.pagar(usuario, float(monto))
        return self._guardar()

    def recibir(self, usuario, monto):
        self.servicio.recibir_pago(usuario, float(monto))
        return self._guardar()

    def cargar_desde_tarjeta(self, usuario, numero_tarjeta, monto):
        self.servicio.cargar_desde_tarjeta(usuario, numero_tarjeta, float(monto))
        return self._guardar()

    def retirar_a_tarjeta(self, usuario, numero_tarjeta, monto):
        self.servicio.retirar_a_tarjeta(usuario, numero_tarjeta, float(monto))
        return self._guardar()

    def listar_tarjetas(self, usuario):
        return usuario.billetera.tarjetas

    def saldo_billetera(self, usuario):
        return usuario.billetera.saldo

    def _guardar(self):
        self.servicio_usuario.guardar()
        return True
