"""Strategy de selección aleatoria para ofertas simuladas."""

from random import Random


class SelectorOfertasAleatorias:
    def __init__(self, minimo=3, maximo=5, randomizador=None):
        self.minimo = minimo
        self.maximo = maximo
        self.randomizador = randomizador or Random()

    def seleccionar_ids(self, catalogo):
        cantidad = min(len(catalogo), self.randomizador.randint(self.minimo, self.maximo))
        return self.randomizador.sample(tuple(catalogo), cantidad)
