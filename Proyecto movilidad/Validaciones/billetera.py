from abstracciones import Validador
from datetime import date


class ValidadorMontoPositivo(Validador):
    def validar(self, valor):
        try:
            if float(valor) <= 0:
                raise ValueError("El monto debe ser mayor a 0.")

        except (TypeError, ValueError):
            raise ValueError("El monto debe ser mayor a 0.")

        return True


class ValidadorSaldoSuficiente(Validador):
    def __init__(self):
        self.validador_monto = ValidadorMontoPositivo()

    def validar(self, datos):
        objeto, monto = datos

        self.validador_monto.validar(monto)
        monto = float(monto)

        if getattr(objeto, "saldo", 0) < monto:
            raise ValueError("Saldo insuficiente.")

        return True


class ValidadorTarjetaEncontrada(Validador):
    def validar(self, valor):
        if valor is None:
            raise ValueError("No se encontro la tarjeta seleccionada.")

        return True


class ValidadorTarjetaNoDuplicada(Validador):
    def validar(self, datos):
        usuario, tarjeta = datos

        for tarjeta_guardada in usuario.billetera.tarjetas:
            if tarjeta_guardada.numero_tarjeta == tarjeta.numero_tarjeta:
                raise ValueError("La tarjeta ya se encuentra agregada.")

        return True


class ValidadorSaldoDefinido(Validador):
    def validar(self, valor):
        return hasattr(valor, "saldo") and valor.saldo is not None


class ValidadorFechaVencimientoTarjeta(Validador):
    def validar(self, valor):
        partes = str(valor or "").strip().split("/")

        if len(partes) != 2:
            raise ValueError("Fecha de vencimiento invalida. Usa formato MM/AA.")

        mes, ano = partes

        if not mes.isdigit() or not ano.isdigit():
            raise ValueError("Fecha de vencimiento invalida. Usa formato MM/AA.")

        if len(mes) != 2 or len(ano) != 2:
            raise ValueError("Fecha de vencimiento invalida. Usa formato MM/AA.")

        mes = int(mes)
        ano = 2000 + int(ano)

        if mes < 1 or mes > 12:
            raise ValueError("Fecha de vencimiento invalida. Usa formato MM/AA.")

        hoy = date.today()
        if not (ano > hoy.year or (ano == hoy.year and mes >= hoy.month)):
            raise ValueError("La tarjeta esta vencida.")

        return True


class ValidadorNumeroTarjetaVisa(Validador):
    def validar(self, valor):
        numero = str(valor or "")
        if not numero.startswith("4") or not 13 <= len(numero) <= 19:
            raise ValueError("Numero de tarjeta Visa invalido.")

        return True


class ValidadorNumeroTarjetaMastercard(Validador):
    def validar(self, valor):
        numero = str(valor or "")

        if len(numero) != 16 or not numero.isdigit():
            raise ValueError("Numero de tarjeta Mastercard invalido.")

        dos = int(numero[:2])
        cuatro = int(numero[:4])
        if not (51 <= dos <= 55 or 2221 <= cuatro <= 2720):
            raise ValueError("Numero de tarjeta Mastercard invalido.")

        return True


class ValidadorNumeroTarjetaAmericanExpress(Validador):
    def validar(self, valor):
        numero = str(valor or "")
        if len(numero) != 15 or not numero.startswith(("34", "37")):
            raise ValueError("Numero de tarjeta American Express invalido.")

        return True
