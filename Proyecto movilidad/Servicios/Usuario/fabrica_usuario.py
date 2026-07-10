from Modelos.Usuario.usuario_datos import Auto, Conductor, Pasajero


class FabricaUsuario:
    """Construye usuarios nuevos."""

    def crear_pasajero(self, datos):
        return Pasajero(id_usuario=None, **datos)

    def crear_conductor(self, datos):
        datos_conductor = dict(datos)
        datos_auto = {
            clave: datos_conductor.pop(clave)
            for clave in (
                "marca",
                "modelo",
                "ano",
                "patente",
                "cantidad_asientos",
                "peso_equipaje",
            )
        }
        return Conductor(
            id_usuario=None,
            auto=Auto(**datos_auto),
            **datos_conductor,
        )
