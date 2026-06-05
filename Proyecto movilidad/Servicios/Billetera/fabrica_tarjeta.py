from Modelos.Billetera.datos_billetera import Tarjetas
from Modelos.Billetera.tarjetas import GeneradorSaldoTarjeta


class FabricaTarjeta:
    """Construye tarjetas nuevas sin modificar los datos recibidos.."""

    def __init__(self, generador_saldo=None):
        self.generador_saldo = generador_saldo or GeneradorSaldoTarjeta()

    def crear(self, titular, numero, vencimiento, cvv):
        # Toda tarjeta nueva parte con un saldo simulado generado automaticamente.
        return Tarjetas(
            titular=titular,
            numero_tarjeta=numero,
            vencimiento=vencimiento,
            cvv=cvv,
            saldo=self.generador_saldo.generar(),
        )
