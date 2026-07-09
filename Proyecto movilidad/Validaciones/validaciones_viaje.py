from math import isfinite

from Servicios.Viajes.datos_viaje import LUGARES_OSORNO, TIPOS_MATERIAL


class ValidacionesViaje:
    """Reglas de entrada del formulario de busqueda de viajes.."""

    VOLUMEN_MINIMO_M3 = 0.01
    VOLUMEN_MAXIMO_M3 = 2.0
    PESO_MINIMO_KG = 0.1
    PESO_MAXIMO_KG = 500.0

    def validar_busqueda_vehiculos(
        self,
        cantidad_usuarios,
        ubicacion_inicial,
        ubicacion_final,
        tipo_viaje="normal",
        volumen=None,
        peso=None,
        tipo_material=None,
    ):
        try:
            cantidad = int(cantidad_usuarios)
        except (TypeError, ValueError):
            return False, "La cantidad de usuarios debe ser un número entero."

        if cantidad <= 0:
            return False, "La cantidad de usuarios debe ser mayor a 0."

        if cantidad > 4:
            return False, "La cantidad máxima de usuarios es 4."

        if ubicacion_inicial == ubicacion_final:
            return False, "La ubicación inicial y final deben ser distintas."

        if tipo_viaje == "material":
            try:
                volumen_numero = float(str(volumen).replace(",", "."))
                peso_numero = float(str(peso).replace(",", "."))
            except (TypeError, ValueError):
                return False, "El volumen y el peso deben ser números válidos."

            if not isfinite(volumen_numero) or not isfinite(peso_numero):
                return False, "El volumen y el peso deben ser números válidos."

            if not self.VOLUMEN_MINIMO_M3 <= volumen_numero <= self.VOLUMEN_MAXIMO_M3:
                return False, "El volumen debe estar entre 0,01 y 2 m3."

            if not self.PESO_MINIMO_KG <= peso_numero <= self.PESO_MAXIMO_KG:
                return False, "El peso debe estar entre 0,1 y 500 kg."

            if tipo_material not in TIPOS_MATERIAL:
                return False, "Debe seleccionar un tipo de material válido."

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
