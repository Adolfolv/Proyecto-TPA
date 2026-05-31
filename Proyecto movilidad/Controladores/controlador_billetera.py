from Modelos.Billetera.datos_billetera import Tarjetas

# archivo de controlador para manejar las operaciones relacionadas con la billetera del usuario,
#  como agregar o eliminar tarjetas, realizar pagos, recibir pagos, cargar o retirar fondos, y consultar el saldo y las tarjetas asociadas a la billetera.
#  Este controlador interactúa con los servicios de billetera y usuario para realizar las operaciones necesarias y guardar los cambios en el perfil del usuario.
class ControladorBilletera:

    def __init__(self, servicio_billetera, servicio_usuario):
        self.servicio = servicio_billetera
        self.servicio_usuario = servicio_usuario

    def agregar_tarjeta(self, usuario, numero, cvv, vencimiento):

        tarjeta = Tarjetas(
            numero_tarjeta=numero,
            vencimiento=vencimiento,
            cvv=cvv,
            saldo=None
        )

        resultado = self.servicio.agregar_tarjeta(usuario, tarjeta)
        return resultado

    def eliminar_tarjeta(self, usuario, numero):

        resultado = self.servicio.eliminar_tarjeta(usuario, numero)
        return resultado

    def pagar(self, usuario, monto):

        resultado = self.servicio.pagar(usuario, float(monto))


        return resultado

    def recibir(self, usuario, monto):

        resultado = self.servicio.recibir_pago(usuario, float(monto))

        return resultado

    def cargar_desde_tarjeta(self, usuario, numero_tarjeta, monto):

        resultado = self.servicio.cargar_desde_tarjeta(
            usuario,
            numero_tarjeta,
            float(monto)
        )
        return resultado

    def retirar_a_tarjeta(self, usuario, numero_tarjeta, monto):

        resultado = self.servicio.retirar_a_tarjeta(
            usuario,
            numero_tarjeta,
            float(monto)
        )
        return resultado

    def listar_tarjetas(self, usuario):
        return usuario.billetera.tarjetas

    def saldo_billetera(self, usuario):
        return usuario.billetera.saldo
