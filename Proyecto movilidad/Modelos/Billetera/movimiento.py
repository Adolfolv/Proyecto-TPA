from datetime import datetime

from Modelos.Billetera.datos_billetera import Transaccion
from Validaciones.billetera import (
    ValidadorMontoPositivo,
    ValidadorSaldoSuficiente,
    normalizar_monto_entero,
)

# Archivo para manejar las operaciones relacionadas con 
# el movimiento de saldo entre la billetera y las tarjetas, ,
# así como los pagos y recepciones de dinero.. Este módulo incluye clases para agregar o quitar saldo, 
# mover saldo entre diferentes objetos (como tarjetas y billeteras), y realizar pagos o recibir pagos utilizando la billetera del usuario.
class AdicionMonto:

    def __init__(self):
        self.validador_monto_positivo = ValidadorMontoPositivo()
        self.validador_saldo_suficiente = ValidadorSaldoSuficiente()

    def agregar_saldo(self, objeto, monto):
        self.validador_monto_positivo.validar(monto)
        monto = normalizar_monto_entero(monto)
        # objeto puede ser una billetera o una tarjeta; ambos tienen atributo saldo.
        objeto.saldo += monto
        return True


    def quitar_saldo(self, billetera, monto):
        # Antes de descontar se comprueba que el origen tenga saldo suficiente.
        self.validador_saldo_suficiente.validar((billetera, monto))
        monto = normalizar_monto_entero(monto)
        billetera.saldo -= monto
        return True



class MoverSaldo(AdicionMonto):

    def mover_saldo(self, origen, destino, monto):
        self.validador_monto_positivo.validar(monto)
        # Movimiento atomico a nivel de dominio: resta del origen y suma al destino.
        self.quitar_saldo(origen, monto)
        self.agregar_saldo(destino, monto)
        return True
    
class Pago(AdicionMonto):
    def pagar(self, billetera, monto):
        # Pagar es simplemente descontar saldo desde la billetera.
        return self.quitar_saldo(billetera, monto)


    def recibir_pago(self, billetera, monto):
        # Recibir pago es agregar saldo a la billetera.
        return self.agregar_saldo(
            billetera,
            monto
        )


class HistorialTransacciones:
    def crear_transaccion(self, billetera, tipo, monto):
        # El historial queda guardado dentro de la misma billetera del usuario.
        transaccion = Transaccion(
            id_transaccion=self._generar_id(billetera),
            tipo=tipo,
            monto=normalizar_monto_entero(monto),
            fecha=datetime.now().strftime("%d-%m-%Y %H:%M"),
        )
        billetera.transacciones.append(transaccion)
        return transaccion

    def _generar_id(self, billetera):
        # El ID se calcula por posicion: TRX0001, TRX0002, etc.
        return f"TRX{len(billetera.transacciones) + 1:04d}"



    



