
# Archivo para manejar las operaciones relacionadas con 
# el movimiento de saldo entre la billetera y las tarjetas, 
# así como los pagos y recepciones de dinero. Este módulo incluye clases para agregar o quitar saldo, 
# mover saldo entre diferentes objetos (como tarjetas y billeteras), y realizar pagos o recibir pagos utilizando la billetera del usuario.
class AdicionMonto:

    def agregar_saldo(self, objeto, monto):

        if monto > 0:

            objeto.saldo += monto
            return True

        return False


    def quitar_saldo(self, billetera, monto):

        if monto > 0 and billetera.saldo >= monto:

            billetera.saldo -= monto
            return True

        return False



class MoverSaldo(AdicionMonto):

    def mover_saldo(self, origen, destino, monto):

        if monto <= 0:

            return False
        if self.quitar_saldo(origen, monto):

            self.agregar_saldo(destino, monto)
            return True
        return False
    
class Pago(AdicionMonto):
    def pagar(self, billetera, monto):

        pago_realizado = self.quitar_saldo(billetera, monto)
        if pago_realizado:
            return True
        return False


    def recibir_pago(self, billetera, monto):
        pago_recibido = self.agregar_saldo(
            billetera,
            monto
        )

        if pago_recibido:
            return True
        return False


"""""""""""
import datos_billetera

tarjeta = datos_billetera.tarjetas(
    numero_tarjeta="1234567812345678",
    vencimiento="12/30",
    cvv="123",
    saldo=10000
)

# -------------------------
# CREAR BILLETERA
# -------------------------

billetera = datos_billetera.billetera(
    saldo=2000
)

# -------------------------
# MOSTRAR SALDOS INICIALES
# -------------------------

print("SALDOS INICIALES")
print("Tarjeta:", tarjeta.saldo)
print("Billetera:", billetera.saldo)

# -------------------------
# MOVER SALDO
# TARJETA -> BILLETERA
# -------------------------

movimiento = MoverSaldo()

movimiento.mover_saldo(
    tarjeta,
    billetera,
    5000
)

# -------------------------
# MOSTRAR SALDOS FINALES
# -------------------------

print("\nSALDOS FINALES")
print("Tarjeta:", tarjeta.saldo)
print("Billetera:", billetera.saldo)
"""""""""


    



