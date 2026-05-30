import abstracciones
TarjetaBase = abstracciones.TarjetaBase
import random

# Archivo para manejar las clases relacionadas con las tarjetas de crédito o débito que los usuarios pueden agregar a su billetera, 
# incluyendo la validación de números de tarjeta, el formato del CVV, y la gestión de las tarjetas asociadas a la billetera del usuario. 
# Este módulo también incluye un servicio para agregar o eliminar tarjetas de la billetera del usuario,
#  y para cargar fondos desde una tarjeta a la billetera o retirar fondos de la billetera a una tarjeta.
class TarjetaVisa(TarjetaBase):

    longitud_cvv = 3
    def numero_valido(self, numero):
        return (numero.startswith("4") and 13 <= len(numero) <= 19)

class TarjetaMastercard(TarjetaBase):

    longitud_cvv = 3
    def numero_valido(self, numero):
        if len(numero) != 16:
            return False

        dos = int(numero[:2])
        cuatro = int(numero[:4])
        return (51 <= dos <= 55 or 2221 <= cuatro <= 2720)

class TarjetaAmericanExpress(TarjetaBase):

    longitud_cvv = 4
    def numero_valido(self, numero):
        return (len(numero) == 15 and numero.startswith(("34", "37")))
    

class ServicioTarjeta:

    def agregar_tarjeta(self, usuario, tarjeta):

        for t in usuario.billetera.tarjetas:

            if t.numero_tarjeta == tarjeta.numero_tarjeta:
                return False
        if not hasattr(tarjeta, "saldo") or tarjeta.saldo is None:
            tarjeta.saldo = random.randint(10000, 500000)

        usuario.billetera.tarjetas.append(tarjeta)
        return True

    def eliminar_tarjeta(self, usuario, numero_tarjeta):

        for t in usuario.billetera.tarjetas:

            if t.numero_tarjeta == numero_tarjeta:
                usuario.billetera.tarjetas.remove(t)
                return True

        return False
