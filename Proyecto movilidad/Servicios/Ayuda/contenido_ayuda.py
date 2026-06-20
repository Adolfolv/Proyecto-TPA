class ContenidoAyuda:
    """Entrega informacion y sugerencias segun el tipo de cuenta."""

    SECCIONES_VISITANTE = (
        ("Inicio de sesion y registro", "Ingresa con tu correo y contrasena o crea una cuenta desde Registrarse."),
        ("Tipos de cuenta", "Elige pasajero para solicitar viajes o conductor para recibir solicitudes."),
        ("Acceso a ayuda", "Al iniciar sesion, esta guia se adapta automaticamente a tu cuenta."),
    )

    SECCIONES_COMUNES = (
        ("Perfil y datos personales", "Revisa y actualiza tus datos desde Perfil."),
        ("Billetera", "Consulta saldo, tarjetas y movimientos de dinero."),
        ("Cuenta congelada", "Un administrador debe reactivar una cuenta congelada."),
    )

    SECCIONES_POR_TIPO = {
        "pasajero": (
            ("Solicitar un viaje", "Indica pasajeros, origen y destino; luego busca un vehiculo."),
            ("Elegir y pagar", "Selecciona un vehiculo y confirma el pago desde tu billetera."),
            ("Seguir el trayecto", "Sigue el mapa y el progreso hasta completar el viaje."),
        ),
        "conductor": (
            ("Buscar pasajeros", "Indica tu ubicacion y busca una solicitud disponible."),
            ("Revisar una solicitud", "Comprueba pasajero, trayecto, pago y tiempos estimados."),
            ("Aceptar y completar", "Confirma el viaje, sigue el mapa y recibe el pago."),
        ),
        "administrador": (
            ("Gestion de pasajeros", "Revisa, congela, descongela o elimina cuentas de pasajeros."),
            ("Gestion de conductores", "Cambia al listado de conductores para gestionar sus cuentas."),
        ),
    }

    SUGERENCIAS_POR_TIPO = {
        "visitante": ("Como creo una cuenta?", "Pasajero o conductor?", "Como inicio sesion?", "Que ofrece la aplicacion?"),
        "pasajero": ("Como solicito un viaje?", "Como pago un viaje?", "Como uso mi billetera?", "Como actualizo mi perfil?"),
        "conductor": ("Como busco pasajeros?", "Como acepto un viaje?", "Como recibo el pago?", "Como actualizo mi perfil?"),
        "administrador": ("Como congelo una cuenta?", "Como descongelo una cuenta?", "Como elimino una cuenta?", "Como cambio de listado?"),
    }

    def listar(self, usuario=None):
        tipo_usuario = self._obtener_tipo_usuario(usuario)
        if tipo_usuario == "visitante":
            return self.SECCIONES_VISITANTE
        return self.SECCIONES_POR_TIPO.get(tipo_usuario, ()) + self.SECCIONES_COMUNES

    def listar_sugerencias(self, usuario=None):
        return self.SUGERENCIAS_POR_TIPO.get(self._obtener_tipo_usuario(usuario), self.SUGERENCIAS_POR_TIPO["visitante"])

    def como_contexto(self, usuario=None):
        return "\n".join(f"- {titulo}: {descripcion}" for titulo, descripcion in self.listar(usuario))

    @staticmethod
    def _obtener_tipo_usuario(usuario):
        if usuario is None:
            return "visitante"
        if isinstance(usuario, str):
            return usuario.lower()
        return str(getattr(usuario, "tipo_usuario", "visitante")).lower()
