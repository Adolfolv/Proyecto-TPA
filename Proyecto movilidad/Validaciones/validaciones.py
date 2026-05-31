import re
from datetime import datetime, date

def texto(self, valor):
    return bool(str(valor or "").strip())

def numero(self, valor):
    return str(valor or "").strip().isdigit()


class ValidadorDatosPersonales:
    def correo(self, valor):
        return bool(
            re.fullmatch(
                r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
                str(valor or "").strip(),
            )
        )
    
    def validar_edad(self, valor):
        if not self.numero(valor):
            return False
        edad = int(valor)
        return 18 <= edad <= 100

def validar_telefono(self, valor):
    if not self.numero(valor):
        return False
    telefono = str(valor).strip()
    return len(telefono) == 8

class ValidadorDatosAuto:

    def patente_chilena(self, valor):
        patente = (
            str(valor or "")
            .upper()
            .replace("-", "")
            .replace(" ", "")
            .strip()
        )

        return bool(
            re.fullmatch(r"[A-Z]{4}[0-9]{2}", patente)
            or
            re.fullmatch(r"[A-Z]{2}[0-9]{4}", patente)
        )
    
    def cantidad_asientos(self, valor):
        if not self.numero(valor):
            return False
        asientos = int(valor)
        return 1 <= asientos <= 9
    
    def peso_equipaje(self, valor):
        if not self.numero(valor):
            return False
        peso = float(valor)
        return 0 <= peso <= 500
    
    def licencia_chilena(self, valor):
        rut = str(valor or "").upper().replace(".", "").replace("-", "")

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
            multiplicador = 2 if multiplicador == 7 else multiplicador + 1

        resto = 11 - (suma % 11)

        dv_esperado = {
            11: "0",
            10: "K",
        }.get(resto, str(resto))

        return dv == dv_esperado
    
    from datetime import datetime, date

    def validar_vencimiento_licencia(self, valor):
        try:
            fecha = datetime.strptime(
                str(valor).strip(),
                "%d-%m-%Y"
            ).date()

            return fecha >= date.today()

        except ValueError:
            return False









#