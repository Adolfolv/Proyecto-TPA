from datetime import date

from abstracciones import Validador
from Validaciones.registro import ValidadorNombre


def normalizar_numero_tarjeta(numero):
    return str(numero or "").strip().replace(" ", "").replace("-", "")


def _mensaje_entero(nombre, permite_cero):
    minimo = "mayor o igual a 0" if permite_cero else "mayor a 0"
    return f"El {nombre} debe ser un número entero {minimo}."


def _normalizar_entero(valor, nombre, permite_cero=False):
    if isinstance(valor, bool):
        raise ValueError(_mensaje_entero(nombre, permite_cero))

    if isinstance(valor, int):
        numero = valor
    elif isinstance(valor, float):
        if not valor.is_integer():
            raise ValueError(_mensaje_entero(nombre, permite_cero))
        numero = int(valor)
    else:
        texto = str(valor or "").strip()
        if texto.endswith(".0"):
            texto = texto[:-2]
        if not texto.isdigit():
            raise ValueError(_mensaje_entero(nombre, permite_cero))
        numero = int(texto)

    if numero < 0 or (numero == 0 and not permite_cero):
        raise ValueError(_mensaje_entero(nombre, permite_cero))

    return numero


def normalizar_monto_entero(valor):
    return _normalizar_entero(valor, "monto", False)


def normalizar_saldo_entero(valor):
    return _normalizar_entero(valor, "saldo", True)


class ValidadorMontoPositivo(Validador):
    def validar(self, valor):
        normalizar_monto_entero(valor)
        return True


class ValidadorSaldoSuficiente(Validador):
    def __init__(self):
        self.validador_monto = ValidadorMontoPositivo()

    def validar(self, datos):
        objeto, monto = datos
        self.validador_monto.validar(monto)

        saldo = normalizar_saldo_entero(getattr(objeto, "saldo", 0))
        monto = normalizar_monto_entero(monto)

        if saldo < monto:
            raise ValueError("Saldo insuficiente.")

        return True


class ValidadorTarjetaEncontrada(Validador):
    def validar(self, valor):
        if valor is None:
            raise ValueError("No se encontró la tarjeta seleccionada.")

        return True


class ValidadorTarjetaNoDuplicada(Validador):
    def validar(self, datos):
        origen, numero = datos
        billetera = getattr(origen, "billetera", origen)
        numero_tarjeta = normalizar_numero_tarjeta(numero)

        for tarjeta_guardada in billetera.tarjetas:
            numero_guardado = normalizar_numero_tarjeta(
                tarjeta_guardada.numero_tarjeta
            )
            if numero_guardado == numero_tarjeta:
                raise ValueError("La tarjeta ya se encuentra agregada.")

        return True


class ValidadorSaldoDefinido(Validador):
    def validar(self, valor):
        if not hasattr(valor, "saldo") or valor.saldo is None:
            raise ValueError("Saldo no disponible.")
        normalizar_saldo_entero(valor.saldo)
        return True


class ValidadorFechaVencimientoTarjeta(Validador):
    def validar(self, valor):
        partes = str(valor or "").strip().split("/")

        if len(partes) != 2:
            raise ValueError("Fecha de vencimiento inválida. Usa formato MM/AA.")

        mes, ano = partes

        if not mes.isdigit() or not ano.isdigit():
            raise ValueError("Fecha de vencimiento inválida. Usa formato MM/AA.")

        if len(mes) != 2 or len(ano) != 2:
            raise ValueError("Fecha de vencimiento inválida. Usa formato MM/AA.")

        mes = int(mes)
        ano = 2000 + int(ano)

        if mes < 1 or mes > 12:
            raise ValueError("Fecha de vencimiento inválida. Usa formato MM/AA.")

        hoy = date.today()
        if not (ano > hoy.year or (ano == hoy.year and mes >= hoy.month)):
            raise ValueError("La tarjeta está vencida.")

        return True


class ValidadorNumeroTarjetaVisa(Validador):
    def validar(self, valor):
        numero = normalizar_numero_tarjeta(valor)
        if (
            not numero.isdigit()
            or not numero.startswith("4")
            or not 13 <= len(numero) <= 19
        ):
            raise ValueError("Número de tarjeta Visa inválido.")

        return True


class ValidadorNumeroTarjetaMastercard(Validador):
    def validar(self, valor):
        numero = normalizar_numero_tarjeta(valor)

        if len(numero) != 16 or not numero.isdigit():
            raise ValueError("Número de tarjeta Mastercard inválido.")

        dos = int(numero[:2])
        cuatro = int(numero[:4])
        if not (51 <= dos <= 55 or 2221 <= cuatro <= 2720):
            raise ValueError("Número de tarjeta Mastercard inválido.")

        return True


class ValidadorNumeroTarjetaAmericanExpress(Validador):
    def validar(self, valor):
        numero = normalizar_numero_tarjeta(valor)
        if (
            not numero.isdigit()
            or len(numero) != 15
            or not numero.startswith(("34", "37"))
        ):
            raise ValueError("Número de tarjeta American Express inválido.")

        return True


class ValidacionesTarjeta:
    def __init__(self, tipos_tarjeta):
        self.tipos_tarjeta = tipos_tarjeta
        self.validador_titular = ValidadorNombre()
        self.validador_fecha_vencimiento = ValidadorFechaVencimientoTarjeta()
        self.validador_tarjeta_no_duplicada = ValidadorTarjetaNoDuplicada()

    def validar(self, titular, billetera, tipo, numero, vencimiento, cvv):
        clase_tarjeta = self._obtener_clase_tarjeta(tipo)
        tarjeta_validadora = clase_tarjeta()
        self.validador_titular.validar(titular)
        tarjeta_validadora.numero_valido(numero)
        self._validar_cvv(tarjeta_validadora, cvv)
        self.validador_fecha_vencimiento.validar(vencimiento)
        self.validador_tarjeta_no_duplicada.validar((billetera, numero))

    def _obtener_clase_tarjeta(self, tipo):
        clase_tarjeta = self.tipos_tarjeta.get(tipo)

        if clase_tarjeta is None:
            raise ValueError("Tipo de tarjeta inválido.")

        return clase_tarjeta

    def _validar_cvv(self, tarjeta_validadora, cvv):
        cvv = str(cvv or "").strip()
        if len(cvv) != tarjeta_validadora.longitud_cvv or not cvv.isdigit():
            raise ValueError("CVV inválido para el tipo de tarjeta seleccionado.")

        return True
