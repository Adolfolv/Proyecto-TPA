from dataclasses import dataclass


@dataclass
class ResultadoOperacion:
    """Resultado comun que los controladores entregan a las vistas."""

    datos: object = None
    error: str = ""

    @property
    def exitoso(self):
        return not self.error
