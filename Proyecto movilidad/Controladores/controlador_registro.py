from Modelos.modelo_Usuario.usuario_datos import Pasajero, Conductor, Auto


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
    ):
        usuario = Pasajero(
            id_usuario=None,
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            edad=edad,
            telefono=telefono,
            contrasena=contrasena,
            direccion=""
        )

        return self.servicio_registro.registrar_usuario(
            usuario,
            confirmar_contrasena,
        )

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
            auto=auto,
        )

        return self.servicio_registro.registrar_usuario(
            usuario,
            confirmar_contrasena,
        )
