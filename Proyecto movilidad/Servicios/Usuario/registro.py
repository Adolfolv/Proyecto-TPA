from Modelos.Billetera.datos_billetera import Billetera
from Servicios.Usuario.generador_id import GeneradorID
from Modelos.Usuario.usuario_datos import Conductor
from Validaciones.registro import (
    ValidadorApellido,
    ValidadorAsientos,
    ValidadorConfirmacionContrasena,
    ValidadorContrasena,
    ValidadorCorreo,
    ValidadorCorreoUnico,
    ValidadorEdad,
    ValidadorEquipaje,
    ValidadorNombre,
    ValidadorNumeroLicencia,
    ValidadorPatente,
    ValidadorTelefono,
)


class ServicioRegistro:

    def __init__(self, servicio_usuario):
        self.servicio_usuario = servicio_usuario

        self.validador_correo = ValidadorCorreo()
        self.validador_correo_unico = ValidadorCorreoUnico(servicio_usuario)
        self.validador_edad = ValidadorEdad()
        self.validador_telefono = ValidadorTelefono()
        self.validador_patente = ValidadorPatente()
        self.validador_asientos = ValidadorAsientos()
        self.validador_equipaje = ValidadorEquipaje()
        self.validador_numero_licencia = ValidadorNumeroLicencia()
        self.validador_contrasena = ValidadorContrasena()
        self.validador_confirmacion_contrasena = ValidadorConfirmacionContrasena()
        self.validador_nombre = ValidadorNombre()
        self.validador_apellido = ValidadorApellido()

    def registrar_usuario(self, usuario, confirmar_contrasena=None):

        if not self.validador_nombre.validar(usuario.nombre):
            raise ValueError("El nombre solo puede contener letras.")

        if not self.validador_apellido.validar(usuario.apellido):
            raise ValueError("El apellido solo puede contener letras.")

        if not self.validador_correo.validar(usuario.correo):
            raise ValueError("Correo invalido.")

        if not self.validador_edad.validar(usuario.edad):
            raise ValueError("Edad invalida.")

        if not self.validador_telefono.validar(usuario.telefono):
            raise ValueError("Telefono invalido.")

        if not self.validador_correo_unico.validar(usuario.correo):
            raise ValueError("El correo ya se encuentra registrado.")

        if (
            confirmar_contrasena is not None
            and not self.validador_confirmacion_contrasena.validar(
                (usuario.contrasena, confirmar_contrasena)
            )
        ):
            raise ValueError("Las contrasenas no coinciden.")

        if not self.validador_contrasena.validar(usuario.contrasena):
            raise ValueError("La contrasena es demasiado corta.")

        if isinstance(usuario, Conductor):
            self._validar_conductor(usuario)

        if usuario.id_usuario is None:
            usuario.id_usuario = GeneradorID.generar("USR")

        if usuario.billetera is None:
            usuario.billetera = Billetera()

        return self.servicio_usuario.agregar(usuario)

    def _validar_conductor(self, usuario):
        if not self.validador_patente.validar(usuario.auto.patente):
            raise ValueError("Patente invalida.")

        if not self.validador_asientos.validar(usuario.auto.cantidad_asientos):
            raise ValueError("Cantidad de pasajeros invalida.")

        if not self.validador_equipaje.validar(usuario.auto.peso_equipaje):
            raise ValueError("Peso maximo de equipaje invalido.")

        if not self.validador_numero_licencia.validar(usuario.licencia_conducir):
            raise ValueError("Numero de licencia invalido.")
