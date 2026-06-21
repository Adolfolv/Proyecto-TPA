class CalculoReputacion:

    def calcular_promedio(self, total_estrellas, cantidad_opiniones):
        if cantidad_opiniones == 0:
            return 0

        return total_estrellas / cantidad_opiniones