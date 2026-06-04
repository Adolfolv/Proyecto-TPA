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
        return self.servicio_billetera.ejecutar("pagar", usuario, float(monto))

    def recibir(self, usuario, monto):
        return self.servicio_billetera.ejecutar("recibir", usuario, float(monto))

    def cargar_desde_tarjeta(self, usuario, numero_tarjeta, monto):
        return self.servicio_billetera.ejecutar(
            "cargar",
            usuario,
            float(monto),
            numero_tarjeta,
        )

    def retirar_a_tarjeta(self, usuario, numero_tarjeta, monto):
        return self.servicio_billetera.ejecutar(
            "retirar",
            usuario,
            float(monto),
            numero_tarjeta,
        )

    def mover_saldo(self, usuario, numero_tarjeta, direccion, monto):
        if direccion == "Tarjeta a billetera":
            return self.cargar_desde_tarjeta(usuario, numero_tarjeta, monto)

        return self.retirar_a_tarjeta(usuario, numero_tarjeta, monto)

    def listar_tarjetas(self, usuario):
        return self.servicio_tarjeta.obtener_tarjetas(usuario)

    def saldo_billetera(self, usuario):
        return self.servicio_billetera.obtener_billetera(usuario).saldo

    def obtener_resumen(self, usuario):
        billetera = self.servicio_billetera.obtener_billetera(usuario)
        return {
            "saldo_billetera": billetera.saldo,
            "tarjetas": billetera.tarjetas,
            "transacciones": billetera.transacciones,
        }
