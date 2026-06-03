import abstracciones
TarjetaBase = abstracciones.TarjetaBase
import random
from Validaciones.billetera import (
    ValidadorNumeroTarjetaAmericanExpress,
    ValidadorNumeroTarjetaMastercard,
    ValidadorNumeroTarjetaVisa,
    ValidadorSaldoDefinido,
    ValidadorTarjetaEncontrada,
    ValidacionesTarjeta,
)
from Modelos.Billetera.datos_billetera import Tarjetas

# Archivo para manejar las clases relacionadas con las tarjetas de crédito o débito que los usuarios pueden agregar a su billetera, 
# incluyendo la validación de números de tarjeta, el formato del CVV, y la gestión de las tarjetas asociadas a la billetera del usuario. 
# Este módulo también incluye un servicio para agregar o eliminar tarjetas de la billetera del usuario,
#  y para cargar fondos desde una tarjeta a la billetera o retirar fondos de la billetera a una tarjeta.
class TarjetaVisa(TarjetaBase):

    longitud_cvv = 3

    def __init__(self):
        self.validador_numero = ValidadorNumeroTarjetaVisa() #validador
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


class GeneradorSaldoTarjeta:

    def generar(self):
        return random.randint(
            10000,
            500000,
        )
    


