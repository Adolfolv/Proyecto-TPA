import re
from datetime import datetime, date

from abstracciones import Validador
from Validaciones.comunes import es_numero
#-

class ValidadorNombre(Validador):
    def validar(self, valor):
        if not valor:
            raise ValueError("El nombre es obligatorio y debe contener letras.")
        if es_numero(valor):
            raise ValueError("El nombre es obligatorio y debe contener letras.")
        return True


class ValidadorApellido(Validador):
    def validar(self, valor):
        if not valor:
            raise ValueError("El apellido es obligatorio y debe contener letras.")
        if es_numero(valor):
            raise ValueError("El apellido es obligatorio y debe contener letras.")
        return True


class ValidadorCorreo(Validador):
    def validar(self, valor):
        if not bool(
            re.fullmatch(
                r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
                str(valor or "").strip(),
            )
        ):
            raise ValueError("Correo invalido. Usa un formato como nombre@correo.com.")

        return True


class ValidadorEdad(Validador):
    def validar(self, valor):
        if not es_numero(valor):
            raise ValueError("Edad invalida. Debe ser un numero entre 18 y 100.")

        if not 18 <= int(valor) <= 100:
            raise ValueError("Edad invalida. Debe ser un numero entre 18 y 100.")

        return True


class ValidadorTelefono(Validador):
    def validar(self, valor):
        telefono = re.sub(r"\D", "", str(valor or ""))

        if telefono.startswith("569"):
            if len(telefono) != 11:
                raise ValueError("Telefono invalido. Usa +56 9 seguido de 8 digitos.")
            return True

        if len(telefono) != 8:
            raise ValueError("Telefono invalido. Usa +56 9 seguido de 8 digitos.")

        return True


class ValidadorPatente(Validador):
    def validar(self, valor):
        patente = (
            str(valor or "")
            .upper()
            .replace("-", "")
            .replace(" ", "")
            .strip()
        )

        if not bool(
            re.fullmatch(r"[A-Z]{4}[0-9]{2}", patente)
            or re.fullmatch(r"[A-Z]{2}[0-9]{4}", patente)
        ):
            raise ValueError("Patente invalida. Usa formato chileno: ABCD12 o AB1234.")

        return True


class ValidadorAsientos(Validador):
    def validar(self, valor):
        if not es_numero(valor):
            raise ValueError("Cantidad de pasajeros invalida. Debe ser un numero entre 1 y 9.")

        if not 1 <= int(valor) <= 9:
            raise ValueError("Cantidad de pasajeros invalida. Debe ser un numero entre 1 y 9.")

        return True


class ValidadorEquipaje(Validador):
    def validar(self, valor):
        try:
            peso = float(valor)
            if not 0 <= peso <= 500:
                raise ValueError("Peso maximo de equipaje invalido. Debe ser un numero entre 0 y 500.")

        except (TypeError, ValueError):
            raise ValueError("Peso maximo de equipaje invalido. Debe ser un numero entre 0 y 500.")

        return True


class ValidadorNumeroLicencia(Validador):
    def validar(self, valor):
        rut = (
            str(valor or "")
            .upper()
            .replace(".", "")
            .replace("-", "")
        )

        if len(rut) < 8:
            raise ValueError("Numero de licencia invalido. Ingresa un RUT valido, con digito verificador.")

        cuerpo = rut[:-1]
        dv = rut[-1]

        if not cuerpo.isdigit():
            raise ValueError("Numero de licencia invalido. Ingresa un RUT valido, con digito verificador.")

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

        if dv != dv_esperado:
            raise ValueError("Numero de licencia invalido. Ingresa un RUT valido, con digito verificador.")

        return True


class ValidadorSelfie(Validador):
    def validar(self, valor):
        if not bool(str(valor or "").strip()):
            raise ValueError("Selfie obligatoria. Selecciona una imagen antes de registrarte.")

        return True


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
    def __init__(self, buscador_usuarios):
        self.buscador_usuarios = buscador_usuarios

    def validar(self, valor):
        if self.buscador_usuarios.buscar(valor) is not None:
            raise ValueError("El correo ya se encuentra registrado.")

        return True


class ValidadorContrasena(Validador):
    def validar(self, valor):
        contrasena = str(valor or "")
        if len(contrasena) < 6:
            raise ValueError("La contrasena es demasiado corta. Debe tener al menos 6 caracteres.")

        return True


class ValidadorConfirmacionContrasena(Validador):
    def validar(self, datos):
        contrasena, confirmar_contrasena = datos
        if contrasena != confirmar_contrasena:
            raise ValueError("Las contrasenas no coinciden. Escribe la misma contrasena en ambos campos.")

        return True
    
class ValidacionesUsuario:

    def __init__(self, buscador_usuarios):

        self.validador_nombre = ValidadorNombre()
        self.validador_apellido = ValidadorApellido()
        self.validador_correo = ValidadorCorreo()
        self.validador_edad = ValidadorEdad()
        self.validador_telefono = ValidadorTelefono()
        self.validador_correo_unico = ValidadorCorreoUnico(buscador_usuarios)
        self.validador_contrasena = ValidadorContrasena()
        self.validador_confirmacion = ValidadorConfirmacionContrasena()
        self.validador_campo_obligatorio = ValidadorSelfie()

    def validar(self, usuario, confirmar_contrasena=None):

        self.validador_nombre.validar(usuario.nombre)
        self.validador_apellido.validar(usuario.apellido)
        self.validador_correo.validar(usuario.correo)
        self.validador_edad.validar(usuario.edad)
        self.validador_telefono.validar(usuario.telefono)
        self.validador_correo_unico.validar(usuario.correo)

        self.validador_contrasena.validar(usuario.contrasena)

        if hasattr(usuario, "direccion"):
            try:
                self.validador_campo_obligatorio.validar(usuario.direccion)
            except ValueError:
                raise ValueError("La direccion es obligatoria.")

        if confirmar_contrasena is not None:
            self.validador_confirmacion.validar(
                (usuario.contrasena, confirmar_contrasena)
            )

class ValidacionesConductor:

    def __init__(self):
        self.validador_patente = ValidadorPatente()
        self.validador_asientos = ValidadorAsientos()
        self.validador_equipaje = ValidadorEquipaje()
        self.validador_numero_licencia = ValidadorNumeroLicencia()
        self.validador_selfie = ValidadorSelfie()

    def validar(self, conductor):

        self.validador_patente.validar(conductor.auto.patente)
        self.validador_asientos.validar(conductor.auto.cantidad_asientos)
        self.validador_equipaje.validar(conductor.auto.peso_equipaje)
        self.validador_numero_licencia.validar(conductor.licencia_conducir)
        self.validador_selfie.validar(conductor.selfie)
