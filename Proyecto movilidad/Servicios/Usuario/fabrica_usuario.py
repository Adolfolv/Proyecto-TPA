from Modelos.Usuario.usuario_datos import Auto, Conductor, Pasajero, Usuario


class FabricaUsuario:
    """Construye usuarios nuevos y reconstruye usuarios persistidos.."""

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

    def crear_desde_dict(self, datos):
        tipo = datos.get("tipo_usuario", "usuario")
        datos_usuario = {
            clave: valor
            for clave, valor in datos.items()
            if clave not in ("billetera", "tipo_usuario")
        }

        if tipo == "conductor":
            datos_usuario["auto"] = Auto(**datos_usuario["auto"])
            return Conductor(**datos_usuario)

        if tipo == "pasajero":
            return Pasajero(**datos_usuario)

        return Usuario(**datos_usuario)
