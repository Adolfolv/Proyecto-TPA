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
    ValidadorSelfie,
    ValidadorTelefono,
)

#.
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
        self.validador_selfie = ValidadorSelfie()

    def registrar_usuario(self, usuario, confirmar_contrasena=None):

        if not self.validador_nombre.validar(usuario.nombre):
            raise ValueError("El nombre es obligatorio y debe contener letras.")

        if not self.validador_apellido.validar(usuario.apellido):
            raise ValueError("El apellido es obligatorio y debe contener letras.")

        if not self.validador_correo.validar(usuario.correo):
            raise ValueError("Correo invalido. Usa un formato como nombre@correo.com.")

        if not self.validador_edad.validar(usuario.edad):
            raise ValueError("Edad invalida. Debe ser un numero entre 18 y 100.")

        if not self.validador_telefono.validar(usuario.telefono):
            raise ValueError("Telefono invalido. Usa +56 9 seguido de 8 digitos.")

        if not self.validador_correo_unico.validar(usuario.correo):
            raise ValueError("El correo ya se encuentra registrado.")

        if (
            confirmar_contrasena is not None
            and not self.validador_confirmacion_contrasena.validar(
                (usuario.contrasena, confirmar_contrasena)
            )
        ):
            raise ValueError("Las contrasenas no coinciden. Escribe la misma contrasena en ambos campos.")

        if not self.validador_contrasena.validar(usuario.contrasena):
            raise ValueError("La contrasena es demasiado corta. Debe tener al menos 6 caracteres.")

        if isinstance(usuario, Conductor):
            self._validar_conductor(usuario)

        if usuario.id_usuario is None:
            usuario.id_usuario = GeneradorID.generar("USR")

        if usuario.billetera is None:
            usuario.billetera = Billetera()

        return self.servicio_usuario.agregar(usuario)

    def _validar_conductor(self, usuario):
        if not self.validador_patente.validar(usuario.auto.patente):
            raise ValueError("Patente invalida. Usa formato chileno: ABCD12 o AB1234.")

        if not self.validador_asientos.validar(usuario.auto.cantidad_asientos):
            raise ValueError("Cantidad de pasajeros invalida. Debe ser un numero entre 1 y 9.")

        if not self.validador_equipaje.validar(usuario.auto.peso_equipaje):
            raise ValueError("Peso maximo de equipaje invalido. Debe ser un numero entre 0 y 500.")

        if not self.validador_numero_licencia.validar(usuario.licencia_conducir):
            raise ValueError("Numero de licencia invalido. Ingresa un RUT valido, con digito verificador.")

        if not self.validador_selfie.validar(usuario.selfie):
            raise ValueError("Selfie obligatoria. Selecciona una imagen antes de registrarte.")
