from Servicios.Viajes.datos_viaje import LUGARES_OSORNO


class ValidacionesViaje:
    """Reglas de entrada del formulario de busqueda de viajes.."""

    def validar_busqueda_vehiculos(self, cantidad_usuarios, ubicacion_inicial, ubicacion_final):
        try:
            cantidad = int(cantidad_usuarios)
        except (TypeError, ValueError):
            return False, "La cantidad de usuarios debe ser un numero entero."

        if cantidad <= 0:
            return False, "La cantidad de usuarios debe ser mayor a 0."

        if cantidad > 4:
            return False, "La cantidad maxima de usuarios es 4."

        if ubicacion_inicial == ubicacion_final:
            return False, "La ubicacion inicial y final deben ser distintas."

        return True, ""

    def validar_pago_pasajero(self, servicio_billetera, usuario):
        if servicio_billetera is None:
            raise ValueError("No se pudo realizar el pago del viaje.")

        if getattr(usuario, "tipo_usuario", "") != "pasajero":
            raise ValueError("No se pudo realizar el pago del viaje.")

        return True

    def validar_abono_conductor(self, servicio_billetera, usuario):
        if servicio_billetera is None:
            raise ValueError("No se pudo abonar el pago al conductor.")

        if getattr(usuario, "tipo_usuario", "") != "conductor":
            raise ValueError("No se pudo abonar el pago al conductor.")

        return True
