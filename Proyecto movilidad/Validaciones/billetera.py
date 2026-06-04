from abstracciones import Validador
from datetime import date
from Validaciones.registro import ValidadorNombre


def normalizar_numero_tarjeta(numero):
    return str(numero or "").replace(" ", "").replace("-", "")


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
        origen, tarjeta = datos
        billetera = getattr(origen, "billetera", origen)
        numero_tarjeta = normalizar_numero_tarjeta(tarjeta.numero_tarjeta)

        for tarjeta_guardada in billetera.tarjetas:
            numero_guardado = normalizar_numero_tarjeta(
                tarjeta_guardada.numero_tarjeta
            )
            if numero_guardado == numero_tarjeta:
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
        numero = normalizar_numero_tarjeta(valor)
        if (
            not numero.isdigit()
            or not numero.startswith("4")
            or not 13 <= len(numero) <= 19
        ):
            raise ValueError("Numero de tarjeta Visa invalido.")

        return True


class ValidadorNumeroTarjetaMastercard(Validador):
    def validar(self, valor):
        numero = normalizar_numero_tarjeta(valor)

        if len(numero) != 16 or not numero.isdigit():
            raise ValueError("Numero de tarjeta Mastercard invalido.")

        dos = int(numero[:2])
        cuatro = int(numero[:4])
        if not (51 <= dos <= 55 or 2221 <= cuatro <= 2720):
            raise ValueError("Numero de tarjeta Mastercard invalido.")

        return True


class ValidadorNumeroTarjetaAmericanExpress(Validador):
    def validar(self, valor):
        numero = normalizar_numero_tarjeta(valor)
        if (
            not numero.isdigit()
            or len(numero) != 15
            or not numero.startswith(("34", "37"))
        ):
            raise ValueError("Numero de tarjeta American Express invalido.")

        return True


class ValidacionesTarjeta:

    def __init__(self, tipos_tarjeta):
        self.tipos_tarjeta = tipos_tarjeta
        self.validador_titular = ValidadorNombre()
        self.validador_fecha_vencimiento = ValidadorFechaVencimientoTarjeta()
        self.validador_tarjeta_no_duplicada = ValidadorTarjetaNoDuplicada()

    def validar(self,titular, billetera, tarjeta, tipo, numero, vencimiento, cvv):
        clase_tarjeta = self._obtener_clase_tarjeta(tipo)
        tarjeta_validadora = clase_tarjeta()
        self.validador_titular.validar(titular)
        tarjeta_validadora.numero_valido(numero)
        self._validar_cvv(tarjeta_validadora, cvv)
        self.validador_fecha_vencimiento.validar(vencimiento)
        self.validador_tarjeta_no_duplicada.validar((billetera, tarjeta))

    def _obtener_clase_tarjeta(self, tipo):
        clase_tarjeta = self.tipos_tarjeta.get(tipo)

        if clase_tarjeta is None:
            raise ValueError("Tipo de tarjeta invalido.")

        return clase_tarjeta

    def _validar_cvv(self, tarjeta_validadora, cvv):
        if len(str(cvv)) != tarjeta_validadora.longitud_cvv:
            raise ValueError("CVV invalido para el tipo de tarjeta seleccionado.")

        return True
