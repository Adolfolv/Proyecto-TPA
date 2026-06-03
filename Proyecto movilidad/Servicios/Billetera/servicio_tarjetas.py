from Modelos.Billetera.tarjetas import (
    TarjetaVisa,
    TarjetaMastercard,
    TarjetaAmericanExpress,
    GeneradorSaldoTarjeta,
)
from Validaciones.billetera import (
    ValidadorSaldoDefinido,
    ValidadorTarjetaEncontrada,
    ValidacionesTarjeta,
)

from Modelos.Billetera.datos_billetera import Tarjetas

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
        billetera = self.repositorio_billetera.obtener_por_usuario(usuario.id_usuario)
        usuario.billetera = billetera
        return billetera.tarjetas

    def obtener_tarjeta(self, usuario, numero_tarjeta):
        billetera = self.repositorio_billetera.obtener_por_usuario(usuario.id_usuario)
        usuario.billetera = billetera
        tarjeta = self.buscador_tarjeta.buscar(billetera, numero_tarjeta)
        self.validador_tarjeta_encontrada.validar(tarjeta)
        return tarjeta

    def agregar_tarjeta(self, usuario, tipo, titular, numero, vencimiento, cvv):
        billetera = self.repositorio_billetera.obtener_por_usuario(usuario.id_usuario)
        usuario.billetera = billetera

        tarjeta = Tarjetas(
            titular=titular,
            numero_tarjeta=numero,
            vencimiento=vencimiento,
            cvv=cvv,
            saldo=None,
        )

        self.validaciones_tarjeta.validar(
            titular,
            billetera,
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

        billetera.tarjetas.append(
            tarjeta
        )
        self.repositorio_billetera.guardar_por_usuario(usuario.id_usuario, billetera)

        return True

    def eliminar_tarjeta(self, usuario, numero_tarjeta):
        billetera = self.repositorio_billetera.obtener_por_usuario(usuario.id_usuario)
        usuario.billetera = billetera
        tarjeta = self.obtener_tarjeta(usuario, numero_tarjeta)
        billetera.tarjetas.remove(tarjeta)
        self.repositorio_billetera.guardar_por_usuario(usuario.id_usuario, billetera)
        return True
