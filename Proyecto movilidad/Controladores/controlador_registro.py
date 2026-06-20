from dataclasses import dataclass

# PATRÓN DE DISEÑO: DTO
# Usamos esta clase pura para empaquetar y transportar la respuesta
# de forma estandarizada hacia la interfaz gráfica, separando los datos de la lógica.
@dataclass
class ResultadoRegistro:
    usuario: object = None
    error: str = ""

    @property
    def exitoso(self):
        return self.error == ""


class ControladorRegistro:
    # PRINCIPIO SOLID: DIP 
    # No instanciamos el Servicio aquí adentro. Lo inyectamos por parámetro 
    # para no depender de una implementación rígida y evitar el acoplamiento fuerte
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
        direccion,
        confirmar_contrasena
    ):
        
        datos = {
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "edad": edad,
            "telefono": telefono,
            "contrasena": contrasena,
            "direccion": direccion,
        }
        return self._registrar(
            self.servicio_registro.registrar_pasajero,
            datos,
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
        tipo_licencia,
        licencia_conducir,
        selfie,
        marca,
        modelo,
        ano,
        patente,
        cantidad_asientos,
        peso_equipaje,
        confirmar_contrasena
    ):
        datos = {
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "edad": edad,
            "telefono": telefono,
            "contrasena": contrasena,
            "tipo_licencia": tipo_licencia,
            "licencia_conducir": licencia_conducir,
            "selfie": selfie,
            "marca": marca,
            "modelo": modelo,
            "ano": ano,
            "patente": patente,
            "cantidad_asientos": cantidad_asientos,
            "peso_equipaje": peso_equipaje,
        }
        return self._registrar(
            self.servicio_registro.registrar_conductor,
            datos,
            confirmar_contrasena,
        )
    def _registrar(self, registrar, datos, confirmar_contrasena):
        try:
            usuario_registrado = registrar(datos, confirmar_contrasena)
            return ResultadoRegistro(usuario=usuario_registrado)
        except ValueError as error:
            return ResultadoRegistro(error=str(error))
    def _registrar(self, registrar, datos, confirmar_contrasena):
        try:
            usuario_registrado = registrar(
                datos,
                confirmar_contrasena,
            )
            return ResultadoRegistro(usuario=usuario_registrado)
        except ValueError as error:
            return ResultadoRegistro(error=str(error))
