import random
from abstracciones import TarjetaBase
from Validaciones.billetera import (
    ValidadorNumeroTarjetaAmericanExpress,
    ValidadorNumeroTarjetaMastercard,
    ValidadorNumeroTarjetaVisa,
)

# Archivo para manejar las clases relacionadas con las tarjetas de crédito o débito que los usuarios pueden agregar a su billetera, 
# incluyendo la validación de números de tarjeta, el formato del CVV, y la gestión de las tarjetas asociadas a la billetera del usuario. 
# Este módulo también incluye un servicio para agregar o eliminar tarjetas de la billetera del usuario,
#  y para cargar fondos desde una tarjeta a la billetera o retirar fondos de la billetera a una tarjeta..
class TarjetaVisa(TarjetaBase):
    clase_validador_numero = ValidadorNumeroTarjetaVisa
    longitud_cvv = 3


class TarjetaMastercard(TarjetaBase):
    clase_validador_numero = ValidadorNumeroTarjetaMastercard
    longitud_cvv = 3


class TarjetaAmericanExpress(TarjetaBase):
    clase_validador_numero = ValidadorNumeroTarjetaAmericanExpress
    longitud_cvv = 4


class GeneradorSaldoTarjeta:

    def generar(self):
        return random.randint(
            10000,
            500000,
        )
    

