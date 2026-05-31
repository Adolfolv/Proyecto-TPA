import re
from datetime import datetime, date

from abstracciones import Validador


def es_numero(valor):
    return str(valor or "").strip().isdigit()

class ValidadorNombre(Validador):
    def validar(self, valor):
        if not valor:
            return False
        if es_numero(valor):
            return False
        return True


class ValidadorApellido(Validador):
    def validar(self, valor):
        if not valor:
            return False
        if es_numero(valor):
            return False
        return True

class ValidadorCorreo(Validador):
    def validar(self, valor):
        return bool(
            re.fullmatch(
                r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
                str(valor or "").strip(),
            )
        )
class ValidadorEdad(Validador):

    def validar(self, valor):
        if not es_numero(valor):
            return False

        return 18 <= int(valor) <= 100

class ValidadorTelefono(Validador):

    def validar(self, valor):
        if not es_numero(valor):
            return False

        return len(str(valor).strip()) == 8

class ValidadorPatente(Validador):

    def validar(self, valor):
        patente = (
            str(valor or "")
            .upper()
            .replace("-", "")
            .replace(" ", "")
            .strip()
        )

        return bool(
            re.fullmatch(r"[A-Z]{4}[0-9]{2}", patente)
            or re.fullmatch(r"[A-Z]{2}[0-9]{4}", patente)
        )

class ValidadorAsientos(Validador):

    def validar(self, valor):
        if not es_numero(valor):
            return False

        return 1 <= int(valor) <= 9

class ValidadorEquipaje(Validador):

    def validar(self, valor):
        try:
            peso = float(valor)
            return 0 <= peso <= 500

        except (TypeError, ValueError):
            return False
class ValidadorNumeroLicencia(Validador):

    def validar(self, valor):
        rut = (
            str(valor or "")
            .upper()
            .replace(".", "")
            .replace("-", "")
        )

        if len(rut) < 8:
            return False

        cuerpo = rut[:-1]
        dv = rut[-1]

        if not cuerpo.isdigit():
            return False

        suma = 0
        multiplicador = 2

        for digito in reversed(cuerpo):
            suma += int(digito) * multiplicador
            multiplicador = (
                2 if multiplicador == 7
                else multiplicador + 1
            )

        resto = 11 - (suma % 11)

        dv_esperado = {
            11: "0",
            10: "K",
        }.get(resto, str(resto))

        return dv == dv_esperado
class ValidadorVencimientoLicencia(Validador):

    def validar(self, valor):
        try:
            fecha = datetime.strptime(
                str(valor).strip(),
                "%d-%m-%Y",
            ).date()

            return fecha >= date.today()

        except ValueError:
            return False
class ValidadorCorreoUnico(Validador):

    def __init__(self, servicio_usuario):
        self.servicio_usuario = servicio_usuario

    def validar(self, valor):
        return self.servicio_usuario.buscar_por_correo(valor) is None

class ValidadorUsuarioEncontrado(Validador):

    def validar(self, valor):
        return valor is not None

class ValidadorContrasenaUsuario(Validador):

    def validar(self, datos):
        usuario, contrasena = datos
        return getattr(usuario, "contrasena", None) == contrasena

class ValidadorPerfilCargado(Validador):

    def validar(self, valor):
        return valor is not None

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

class ValidadorContrasena(Validador):

    def validar(self, valor):
        contrasena = str(valor or "")
        return len(contrasena) >= 6
