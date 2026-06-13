class ServicioAdmin:
    """Agrupa las consultas administrativas sin exponer el repositorio a la vista."""

    def __init__(self, repositorio_usuario):
        self.repositorio_usuario = repositorio_usuario

    def listar_usuarios(self):
        # El panel administrador necesita revisar usuarios registrados.
        # Se usa el repositorio existente para no duplicar la lectura de usuarios.json.
        return self.repositorio_usuario.listar()

    def listar_por_tipo(self, tipo_usuario):
        # Filtra usuarios para cada seccion del panel administrador sin cambiar
        # la estructura del repositorio ni el formato actual de usuarios.json.
        return [
            usuario
            for usuario in self.listar_usuarios()
            if getattr(usuario, "tipo_usuario", "usuario") == tipo_usuario
        ]

    def contar_por_tipo(self):
        # Entrega un resumen para el panel administrador sin mezclar esta logica
        # con las vistas normales de pasajero o conductor.
        conteo = {
            "pasajero": 0,
            "conductor": 0,
            "administrador": 0,
        }

        for usuario in self.listar_usuarios():
            tipo = getattr(usuario, "tipo_usuario", "usuario")
            conteo[tipo] = conteo.get(tipo, 0) + 1

        return conteo

    def congelar_cuenta(self, id_usuario):
        # La regla de negocio queda aqui: el panel solo puede congelar cuentas
        # operativas, no cuentas administradoras.
        usuario = self._buscar_usuario_gestionable(id_usuario)
        if usuario is None:
            return False

        usuario.cuenta_congelada = True
        self.repositorio_usuario.guardar_usuario(usuario)
        return True

    def descongelar_cuenta(self, id_usuario):
        # Descongelar usa la misma validacion que congelar para mantener
        # protegidas las cuentas administradoras.
        usuario = self._buscar_usuario_gestionable(id_usuario)
        if usuario is None:
            return False

        usuario.cuenta_congelada = False
        self.repositorio_usuario.guardar_usuario(usuario)
        return True

    def eliminar_cuenta(self, id_usuario):
        # El borrado tambien pasa por el servicio para proteger cuentas admin
        # y mantener el repositorio como detalle de persistencia.
        usuario = self._buscar_usuario_gestionable(id_usuario)
        if usuario is None:
            return False

        return self.repositorio_usuario.eliminar_por_id(id_usuario)

    def _buscar_usuario_gestionable(self, id_usuario):
        # Solo pasajeros y conductores aparecen en el panel gestionable.
        for usuario in self.listar_usuarios():
            if str(usuario.id_usuario) == str(id_usuario) and getattr(usuario, "tipo_usuario", "") in ("pasajero", "conductor"):
                return usuario

        return None
