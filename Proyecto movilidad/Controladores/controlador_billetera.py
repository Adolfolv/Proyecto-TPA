class ControladorBilletera:

    def __init__(self, servicio_billetera, servicio_usuario):
        self.servicio = servicio_billetera
        self.servicio_usuario = servicio_usuario

    def agregar_tarjeta(self, usuario, numero, cvv, vencimiento):

        tarjeta = type("Tarjeta", (), {})()
        tarjeta.numero_tarjeta = numero
        tarjeta.cvv = cvv
        tarjeta.vencimiento = vencimiento
        tarjeta.saldo = None  

        resultado = self.servicio.agregar_tarjeta(usuario, tarjeta)

        if resultado:
            self.servicio_usuario.guardar() 
        return resultado

    def eliminar_tarjeta(self, usuario, numero):

        resultado = self.servicio.eliminar_tarjeta(usuario, numero)

        if resultado:
            self.servicio_usuario.guardar()  

        return resultado

    def pagar(self, usuario, monto):

        resultado = self.servicio.pagar(usuario, float(monto))

        if resultado:
            self.servicio_usuario.guardar()

        return resultado

    def recibir(self, usuario, monto):

        resultado = self.servicio.recibir_pago(usuario, float(monto))

        if resultado:
            self.servicio_usuario.guardar()

        return resultado

    def cargar_desde_tarjeta(self, usuario, numero_tarjeta, monto):

        resultado = self.servicio.cargar_desde_tarjeta(
            usuario,
            numero_tarjeta,
            float(monto)
        )

        if resultado:
            self.servicio_usuario.guardar()

        return resultado

    def retirar_a_tarjeta(self, usuario, numero_tarjeta, monto):

        resultado = self.servicio.retirar_a_tarjeta(
            usuario,
            numero_tarjeta,
            float(monto)
        )

        if resultado:
            self.servicio_usuario.guardar()

        return resultado

    def listar_tarjetas(self, usuario):
        return usuario.billetera.tarjetas

    def saldo_billetera(self, usuario):
        return usuario.billetera.saldo