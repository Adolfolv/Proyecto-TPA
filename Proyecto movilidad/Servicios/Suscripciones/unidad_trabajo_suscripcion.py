"""Unidad de trabajo para guardar juntas una suscripcion y sus viajes."""


class UnidadTrabajoSuscripcion:
    """Guarda todos los cambios o los deshace todos."""

    def __init__(self, repositorio):
        self.repositorio = repositorio
        self.snapshot = None
        self.debe_guardar = False

    def __enter__(self):
        # Se ejecuta automaticamente al entrar al `with`.
        self.snapshot = self.repositorio.crear_snapshot()
        self.debe_guardar = False
        return self

    def confirmar(self):
        # Autoriza el guardado cuando termine correctamente el `with`.
        self.debe_guardar = True

    def __exit__(self, tipo_error, *_):
        # Python siempre llama este metodo al salir del `with`.
        # `tipo_error` es None si no hubo error; `*_` recibe los otros dos
        # parametros obligatorios (error y traceback), que aqui no necesitamos.
        if tipo_error is not None or not self.debe_guardar:
            self.repositorio.restaurar_snapshot(self.snapshot)
            return False

        try:
            self.repositorio.guardar_cambios()
        except Exception:
            self.repositorio.restaurar_snapshot(self.snapshot)
            raise

        return False
