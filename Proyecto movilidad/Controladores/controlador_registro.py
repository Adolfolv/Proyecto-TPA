from dataclasses import dataclass

from Modelos.Usuario.usuario_datos import Pasajero, Conductor, Auto


@dataclass
class ResultadoRegistro:
    usuario: object = None
    error: str = ""

    @property
    def exitoso(self):
        return self.error == ""


class ControladorRegistro:

    def __init__(self, servicio_registro):
        self.servicio_registro = servicio_registro

    def registrar_pasajero(
        self,
        nombre,
        apellido,
        correo,
        edad,
        telefono,
        contrasena,
        confirmar_contrasena,
        direccion,
    ):

        usuario = Pasajero(
            id_usuario=None,
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            edad=edad,
            telefono=telefono,
            contrasena=contrasena,
            direccion=direccion,
        )

        return self._registrar(usuario, confirmar_contrasena)

    def registrar_conductor(
        self,
        nombre,
        apellido,
        correo,
        edad,
        telefono,
        contrasena,
        confirmar_contrasena,
        tipo_licencia,
        licencia_conducir,
        selfie,
        marca,
        modelo,
        ano,
        patente,
        cantidad_asientos,
        peso_equipaje,
    ):
        auto = Auto(
            marca=marca,
            modelo=modelo,
            año=ano,
            patente=patente,
            cantidad_asientos=cantidad_asientos,
            peso_equipaje=peso_equipaje,
        )

        usuario = Conductor(
            id_usuario=None,
            nombre= nombre,
            apellido=apellido,
            correo=correo,
            edad=edad,
            telefono=telefono,
            contrasena=contrasena,
            tipo_licencia=tipo_licencia,
            licencia_conducir=licencia_conducir,
            selfie=selfie,
            auto=auto,
        )

        return self._registrar(usuario, confirmar_contrasena)

    def _registrar(self, usuario, confirmar_contrasena):
        try:
            usuario_registrado = self.servicio_registro.registrar_usuario(
                usuario,
                confirmar_contrasena,
            )
            return ResultadoRegistro(usuario=usuario_registrado)
        except ValueError as error:
            return ResultadoRegistro(error=str(error))
