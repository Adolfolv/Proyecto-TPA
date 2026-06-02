class ValidacionesViaje:
    def validar_busqueda_vehiculos(self, cantidad_usuarios, ubicacion_inicial, ubicacion_final):
        try:
            cantidad = int(cantidad_usuarios)
        except ValueError:
            return False, "La cantidad de usuarios debe ser un numero entero."

        if cantidad <= 0:
            return False, "La cantidad de usuarios debe ser mayor a 0."

        if cantidad > 4:
            return False, "La cantidad maxima de usuarios es 4."

        if ubicacion_inicial == ubicacion_final:
            return False, "La ubicacion inicial y final deben ser distintas."

        return True, ""
