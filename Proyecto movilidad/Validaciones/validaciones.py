import re
from datetime import datetime, date

from abstracciones import Validador


def es_numero(valor):
    return str(valor or "").strip().isdigit()

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









#