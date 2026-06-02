import re
from datetime import datetime, date

from abstracciones import Validador
from Validaciones.comunes import es_numero
#-

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
        telefono = re.sub(r"\D", "", str(valor or ""))

        if telefono.startswith("569"):
            return len(telefono) == 11

        return len(telefono) == 8


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


class ValidadorSelfie(Validador):
    def validar(self, valor):
        return bool(str(valor or "").strip())


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


class ValidadorContrasena(Validador):
    def validar(self, valor):
        contrasena = str(valor or "")
        return len(contrasena) >= 6


class ValidadorConfirmacionContrasena(Validador):
    def validar(self, datos):
        contrasena, confirmar_contrasena = datos
        return contrasena == confirmar_contrasena
