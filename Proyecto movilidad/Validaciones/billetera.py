from abstracciones import Validador
from datetime import date


class ValidadorMontoPositivo(Validador):
    def validar(self, valor):
        try:
            return float(valor) > 0

        except (TypeError, ValueError):
            return False


class ValidadorSaldoSuficiente(Validador):
    def __init__(self):
        self.validador_monto = ValidadorMontoPositivo()

    def validar(self, datos):
        objeto, monto = datos

        if not self.validador_monto.validar(monto):
            return False

        return getattr(objeto, "saldo", 0) >= monto


class ValidadorTarjetaEncontrada(Validador):
    def validar(self, valor):
        return valor is not None


class ValidadorTarjetaNoDuplicada(Validador):
    def validar(self, datos):
        usuario, tarjeta = datos

        for tarjeta_guardada in usuario.billetera.tarjetas:
            if tarjeta_guardada.numero_tarjeta == tarjeta.numero_tarjeta:
                return False

        return True


class ValidadorSaldoDefinido(Validador):
    def validar(self, valor):
        return hasattr(valor, "saldo") and valor.saldo is not None


class ValidadorFechaVencimientoTarjeta(Validador):
    def validar(self, valor):
        partes = str(valor or "").strip().split("/")

        if len(partes) != 2:
            return False

        mes, ano = partes

        if not mes.isdigit() or not ano.isdigit():
            return False

        if len(mes) != 2 or len(ano) != 2:
            return False

        mes = int(mes)
        ano = 2000 + int(ano)

        if mes < 1 or mes > 12:
            return False

        hoy = date.today()
        return ano > hoy.year or (ano == hoy.year and mes >= hoy.month)


class ValidadorNumeroTarjetaVisa(Validador):
    def validar(self, valor):
        numero = str(valor or "")
        return numero.startswith("4") and 13 <= len(numero) <= 19


class ValidadorNumeroTarjetaMastercard(Validador):
    def validar(self, valor):
        numero = str(valor or "")

        if len(numero) != 16 or not numero.isdigit():
            return False

        dos = int(numero[:2])
        cuatro = int(numero[:4])
        return 51 <= dos <= 55 or 2221 <= cuatro <= 2720


class ValidadorNumeroTarjetaAmericanExpress(Validador):
    def validar(self, valor):
        numero = str(valor or "")
        return len(numero) == 15 and numero.startswith(("34", "37"))
