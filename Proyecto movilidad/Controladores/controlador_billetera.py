class ControladorResumenBilletera:

    def __init__(self, servicio_billetera):
        self.servicio_billetera = servicio_billetera

    def saldo_billetera(self, usuario):
        return self.servicio_billetera.obtener_billetera(usuario).saldo

    def obtener_resumen(self, usuario):
        return self.servicio_billetera.obtener_resumen(usuario)


class ControladorTarjetas:

    def __init__(self, servicio_tarjeta):
        self.servicio_tarjeta = servicio_tarjeta

    def agregar_tarjeta(self, usuario, tipo, titular, numero, vencimiento, cvv):
        return self.servicio_tarjeta.agregar_tarjeta(
            usuario,
            tipo,
            titular,
            numero,
            vencimiento,
            cvv,
        )

    def eliminar_tarjeta(self, usuario, numero):
        return self.servicio_tarjeta.eliminar_tarjeta(usuario, numero)

    def listar_tarjetas(self, usuario):
        return self.servicio_tarjeta.obtener_tarjetas(usuario)


class ControladorMovimientosBilletera:
    OPERACIONES_MOVIMIENTO = {
        "Tarjeta a billetera": "cargar",
        "Billetera a tarjeta": "retirar",
    }

    def __init__(self, servicio_billetera):
        self.servicio_billetera = servicio_billetera

    def pagar(self, usuario, monto):
        return self.servicio_billetera.ejecutar("pagar", usuario, monto)

    def recibir(self, usuario, monto):
        return self.servicio_billetera.ejecutar("recibir", usuario, monto)

    def cargar_desde_tarjeta(self, usuario, numero_tarjeta, monto):
        return self.servicio_billetera.ejecutar(
            "cargar",
            usuario,
            monto,
            numero_tarjeta,
        )

    def retirar_a_tarjeta(self, usuario, numero_tarjeta, monto):
        return self.servicio_billetera.ejecutar(
            "retirar",
            usuario,
            monto,
            numero_tarjeta,
        )

    def mover_saldo(self, usuario, numero_tarjeta, direccion, monto):
        return self.servicio_billetera.ejecutar(
            self._operacion_por_direccion(direccion),
            usuario,
            monto,
            numero_tarjeta,
        )

    def _operacion_por_direccion(self, direccion):
        operacion = self.OPERACIONES_MOVIMIENTO.get(direccion)
        if operacion is None:
            raise ValueError("Dirección de movimiento inválida.")
        return operacion
