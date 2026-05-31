import abstracciones
TarjetaBase = abstracciones.TarjetaBase
import random
from Validaciones.validaciones import (
    ValidadorNumeroTarjetaAmericanExpress,
    ValidadorNumeroTarjetaMastercard,
    ValidadorNumeroTarjetaVisa,
    ValidadorSaldoDefinido,
    ValidadorTarjetaNoDuplicada,
)

# Archivo para manejar las clases relacionadas con las tarjetas de crédito o débito que los usuarios pueden agregar a su billetera, 
# incluyendo la validación de números de tarjeta, el formato del CVV, y la gestión de las tarjetas asociadas a la billetera del usuario. 
# Este módulo también incluye un servicio para agregar o eliminar tarjetas de la billetera del usuario,
#  y para cargar fondos desde una tarjeta a la billetera o retirar fondos de la billetera a una tarjeta.
class TarjetaVisa(TarjetaBase):

    longitud_cvv = 3

    def __init__(self):
        self.validador_numero = ValidadorNumeroTarjetaVisa()

    def numero_valido(self, numero):
        return self.validador_numero.validar(numero)

class TarjetaMastercard(TarjetaBase):

    longitud_cvv = 3

    def __init__(self):
        self.validador_numero = ValidadorNumeroTarjetaMastercard()

    def numero_valido(self, numero):
        return self.validador_numero.validar(numero)

class TarjetaAmericanExpress(TarjetaBase):

    longitud_cvv = 4

    def __init__(self):
        self.validador_numero = ValidadorNumeroTarjetaAmericanExpress()

    def numero_valido(self, numero):
        return self.validador_numero.validar(numero)
    

class ServicioTarjeta:

    def __init__(self):
        self.validador_tarjeta_no_duplicada = ValidadorTarjetaNoDuplicada()
        self.validador_saldo_definido = ValidadorSaldoDefinido()

    def agregar_tarjeta(self, usuario, tarjeta):

        if not self.validador_tarjeta_no_duplicada.validar((usuario, tarjeta)):
            return False

        if not self.validador_saldo_definido.validar(tarjeta):
            tarjeta.saldo = random.randint(10000, 500000)

        usuario.billetera.tarjetas.append(tarjeta)
        return True

    def eliminar_tarjeta(self, usuario, numero_tarjeta):

        for t in usuario.billetera.tarjetas:

            if t.numero_tarjeta == numero_tarjeta:
                usuario.billetera.tarjetas.remove(t)
                return True

        return False
