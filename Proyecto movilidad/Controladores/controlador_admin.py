class ControladorAdmin:
    """Adapta las acciones de la vista admin hacia ServicioAdmin."""

    def __init__(self, servicio_admin):
        self.servicio_admin = servicio_admin

    def contar_por_tipo(self):
        # La vista pide datos listos para pintar; el servicio decide de donde salen.
        return self.servicio_admin.contar_por_tipo()

    def listar_por_tipo(self, tipo_usuario):
        # Mantiene a la vista separada del repositorio y del formato JSON.
        return self.servicio_admin.listar_por_tipo(tipo_usuario)

    def congelar_cuenta(self, id_usuario):
        # Accion administrativa real: el servicio valida y persiste el cambio.
        return self.servicio_admin.congelar_cuenta(id_usuario)

    def descongelar_cuenta(self, id_usuario):
        # Accion administrativa real: vuelve a habilitar una cuenta congelada.
        return self.servicio_admin.descongelar_cuenta(id_usuario)

    def eliminar_cuenta(self, id_usuario):
        # Accion administrativa real: el servicio valida antes de eliminar.
        return self.servicio_admin.eliminar_cuenta(id_usuario)
