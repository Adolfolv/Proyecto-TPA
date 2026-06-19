class ServicioAyuda:
    """Coordina contenido fijo de ayuda y consultas al proveedor de IA."""

    def __init__(self, contenido_ayuda, cliente_ia):
        self.contenido_ayuda = contenido_ayuda
        self.cliente_ia = cliente_ia

    def listar_secciones(self, usuario=None):
        return self.contenido_ayuda.listar(usuario)

    def listar_sugerencias(self, usuario=None):
        return self.contenido_ayuda.listar_sugerencias(usuario)

    def consultar_asistente(self, pregunta, usuario=None):
        pregunta = pregunta.strip()
        if not pregunta:
            raise ValueError("Escribe una consulta antes de enviar.")
        return self.cliente_ia.generar_respuesta(self._crear_instruccion(usuario), pregunta)

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
