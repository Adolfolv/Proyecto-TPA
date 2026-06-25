from dataclasses import dataclass


@dataclass(frozen=True)
class PerfilAyuda:
    secciones: tuple
    sugerencias: tuple
    incluir_comunes: bool = True

    def secciones_completas(self, comunes):
        return self.secciones + (comunes if self.incluir_comunes else ())


class ContenidoAyuda:
    """Entrega informacion y sugerencias segun el tipo de cuenta."""

    NOMBRES_ROL = {
        "pasajero": "Pasajero",
        "conductor": "Conductor",
        "administrador": "Administrador",
        "visitante": "Visitante",
    }

    SECCIONES_COMUNES = (
        ("Perfil y datos personales", "Revisa y actualiza tus datos desde Perfil."),
        ("Billetera", "Consulta saldo, tarjetas y movimientos de dinero."),
        ("Cuenta congelada", "Un administrador debe reactivar una cuenta congelada."),
    )

    PERFILES = {
        "visitante": PerfilAyuda(
            (
                ("Inicio de sesion y registro", "Ingresa con tu correo y contrasena o crea una cuenta desde Registrarse."),
                ("Tipos de cuenta", "Elige pasajero para solicitar viajes o conductor para recibir solicitudes."),
                ("Acceso a ayuda", "Al iniciar sesion, esta guia se adapta automaticamente a tu cuenta."),
            ),
            ("Como creo una cuenta?", "Pasajero o conductor?", "Como inicio sesion?", "Que ofrece la aplicacion?"),
            incluir_comunes=False,
        ),
        "pasajero": PerfilAyuda(
            (
                ("Solicitar un viaje", "Indica pasajeros, origen y destino; luego busca un vehiculo."),
                ("Elegir y pagar", "Selecciona un vehiculo y confirma el pago desde tu billetera."),
                ("Seguir el trayecto", "Sigue el mapa y el progreso hasta completar el viaje."),
            ),
            ("Como solicito un viaje?", "Como pago un viaje?", "Como uso mi billetera?", "Como actualizo mi perfil?"),
        ),
        "conductor": PerfilAyuda(
            (
                ("Buscar pasajeros", "Indica tu ubicacion y busca una solicitud disponible."),
                ("Revisar una solicitud", "Comprueba pasajero, trayecto, pago y tiempos estimados."),
                ("Aceptar y completar", "Confirma el viaje, sigue el mapa y recibe el pago."),
            ),
            ("Como busco pasajeros?", "Como acepto un viaje?", "Como recibo el pago?", "Como actualizo mi perfil?"),
        ),
        "administrador": PerfilAyuda(
            (
                ("Gestion de pasajeros", "Revisa, congela, descongela o elimina cuentas de pasajeros."),
                ("Gestion de conductores", "Cambia al listado de conductores para gestionar sus cuentas."),
            ),
            ("Como congelo una cuenta?", "Como descongelo una cuenta?", "Como elimino una cuenta?", "Como cambio de listado?"),
        ),
    }

    def listar(self, usuario=None):
        return self._perfil(usuario).secciones_completas(self.SECCIONES_COMUNES)

    def listar_sugerencias(self, usuario=None):
        return self._perfil(usuario).sugerencias

    def nombre_rol(self, usuario=None):
        return self.NOMBRES_ROL.get(self._obtener_tipo_usuario(usuario), "Visitante")

    def como_contexto(self, usuario=None):
        return "\n".join(f"- {titulo}: {descripcion}" for titulo, descripcion in self.listar(usuario))

    def _perfil(self, usuario):
        return self.PERFILES.get(self._obtener_tipo_usuario(usuario), self.PERFILES["visitante"])

    @staticmethod
    def _obtener_tipo_usuario(usuario):
        if usuario is None:
            return "visitante"
        if isinstance(usuario, str):
            return usuario.lower()
        return str(getattr(usuario, "tipo_usuario", "visitante")).lower()
