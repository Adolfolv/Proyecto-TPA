class ServicioAyuda:
    """Fachada entre la ayuda fija y el proveedor de IA."""

    def __init__(self, contenido_ayuda, cliente_ia):
        self.contenido_ayuda = contenido_ayuda
        self.cliente_ia = cliente_ia

    def pedir_solicitud(self, solicitud=None, usuario=None):
        if solicitud is None:
            return self._crear_contenido(usuario)
        pregunta = solicitud.strip()
        if not pregunta:
            raise ValueError("Escribe una consulta antes de enviar.")
        return self.cliente_ia.generar_respuesta(self._crear_instruccion(usuario), pregunta)

    def _crear_contenido(self, usuario=None):
        return {
            "rol": self.contenido_ayuda.nombre_rol(usuario),
            "secciones": self.contenido_ayuda.listar(usuario),
            "sugerencias": self.contenido_ayuda.listar_sugerencias(usuario),
        }

    def _crear_instruccion(self, usuario):
        tipo_usuario = getattr(usuario, "tipo_usuario", "visitante") if usuario is not None else "visitante"
        return (
            "Eres el asistente de ayuda de la aplicacion Movilidad. "
            "Responde en espanol, con tono claro y breve. "
            "Usa principalmente esta informacion de la aplicacion y no inventes funciones no presentes. "
            "Usa texto plano, sin tablas ni sintaxis Markdown. "
            f"Tipo de usuario actual: {tipo_usuario}.\n"
            "Entrega la respuesta completa, sin dejar frases inconclusas. "
            f"Informacion disponible:\n{self.contenido_ayuda.como_contexto(usuario)}"
        )
