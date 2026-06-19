from dataclasses import dataclass


@dataclass
class ResultadoAyuda:
    texto: str = ""
    error: str = ""

    @property
    def exitoso(self):
        return self.error == ""


class ControladorAyuda:
    """Adapta la vista de ayuda al servicio sin exponer detalles de IA."""

    def __init__(self, servicio_ayuda):
        self.servicio_ayuda = servicio_ayuda

    def listar_secciones(self, usuario=None):
        return self.servicio_ayuda.listar_secciones(usuario)

    def listar_sugerencias(self, usuario=None):
        return self.servicio_ayuda.listar_sugerencias(usuario)

    def consultar_asistente(self, pregunta, usuario=None):
        try:
            return ResultadoAyuda(texto=self.servicio_ayuda.consultar_asistente(pregunta, usuario))
        except Exception as error:
            return ResultadoAyuda(error=str(error))
