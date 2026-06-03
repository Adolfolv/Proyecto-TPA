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
    

class ServicioTarjeta:

    TIPOS_TARJETA = {
        "Visa": TarjetaVisa,
        "Mastercard": TarjetaMastercard,
        "American Express": TarjetaAmericanExpress,
    }

    def __init__(
        self,
        repositorio_billetera,
        buscador_tarjeta,
        validaciones_tarjeta=None,
        generador_saldo_tarjeta=None,
    ):
        self.repositorio_billetera = repositorio_billetera
        self.buscador_tarjeta = buscador_tarjeta
        self.validaciones_tarjeta = (
            validaciones_tarjeta
            or ValidacionesTarjeta(self.TIPOS_TARJETA)
        )
        self.generador_saldo_tarjeta = (
            generador_saldo_tarjeta
            or GeneradorSaldoTarjeta()
        )
        self.validador_saldo_definido = (
            ValidadorSaldoDefinido()
        )
        self.validador_tarjeta_encontrada = ValidadorTarjetaEncontrada()

    def obtener_tarjetas(self, usuario):
        self.repositorio_billetera.obtener(usuario)
        return usuario.billetera.tarjetas

    def obtener_tarjeta(self, usuario, numero_tarjeta):
        self.repositorio_billetera.obtener(usuario)
        tarjeta = self.buscador_tarjeta.buscar(usuario, numero_tarjeta)
        self.validador_tarjeta_encontrada.validar(tarjeta)
        return tarjeta

    def agregar_tarjeta(self, usuario, tipo, titular, numero, vencimiento, cvv):
        self.repositorio_billetera.obtener(usuario)

        tarjeta = Tarjetas(
            titular=titular,
            numero_tarjeta=numero,
            vencimiento=vencimiento,
            cvv=cvv,
            saldo=None,
        )

        self.validaciones_tarjeta.validar(
            usuario,
            tarjeta,
            tipo,
            numero,
            vencimiento,
            cvv,
        )

        if not self.validador_saldo_definido.validar(
            tarjeta
        ):
            tarjeta.saldo = self.generador_saldo_tarjeta.generar()

        usuario.billetera.tarjetas.append(
            tarjeta
        )
        self.repositorio_billetera.guardar_usuario(usuario)

        return True

    def eliminar_tarjeta(self, usuario, numero_tarjeta):
        tarjeta = self.obtener_tarjeta(usuario, numero_tarjeta)
        usuario.billetera.tarjetas.remove(tarjeta)
        self.repositorio_billetera.guardar_usuario(usuario)
        return True
