"""Fachada del módulo de suscripciones.

Mantiene una entrada simple para los controladores y delega la lógica real en
servicios especializados: pasajero, conductor, pagos y operaciones comunes.
"""

class ServicioSuscripcion:
    """Fachada pública del módulo de suscripciones."""

    def __init__(self, alta_pasajero, consultas_pasajero, viajes_pasajero,
                 cancelacion_pasajero, ofertas_conductor, agenda_conductor,
                 asignacion_conductor, viajes_conductor, procesador, pagos):
        self.alta_pasajero = alta_pasajero
        self.consultas_pasajero = consultas_pasajero
        self.viajes_pasajero = viajes_pasajero
        self.cancelacion_pasajero = cancelacion_pasajero
        self.ofertas_conductor = ofertas_conductor
        self.agenda_conductor = agenda_conductor
        self.asignacion_conductor = asignacion_conductor
        self.viajes_conductor = viajes_conductor
        self.procesador = procesador
        self.pagos = pagos


    # --- Casos de uso del pasajero ---


    def previsualizar(self, *args):
        return self.alta_pasajero.previsualizar(*args)

    def confirmar(self, *args):
        return self.alta_pasajero.confirmar(*args)

    def buscar_conductores(self, *args):
        return self.alta_pasajero.buscar_conductores(*args)

    def obtener_lugares_disponibles(self):
        return self.alta_pasajero.obtener_lugares_disponibles()

    def listar_suscripciones(self, *args):
        return self.consultas_pasajero.listar_suscripciones(*args)

    def listar_viajes(self, *args, **kwargs):
        return self.consultas_pasajero.listar_viajes(*args, **kwargs)

    def confirmar_inicio(self, *args):
        return self.viajes_pasajero.confirmar_inicio(*args)

    def completar_viaje_pasajero(self, *args):
        return self.viajes_pasajero.completar_viaje_pasajero(*args)

    def cancelar_viaje(self, *args):
        return self.viajes_pasajero.cancelar_viaje(*args)

    def cancelar_suscripcion_pasajero(self, *args):
        return self.cancelacion_pasajero.cancelar_suscripcion(*args)

    # --- Casos de uso del conductor ---
    def listar_disponibles_conductor(self, *args):
        return self.ofertas_conductor.listar_disponibles_conductor(*args)

    def buscar_ofertas_conductor(self, *args):
        return self.ofertas_conductor.buscar_ofertas_conductor(*args)

    def listar_actuales_conductor(self, *args):
        return self.agenda_conductor.listar_actuales_conductor(*args)

    def obtener_agenda_conductor(self, *args):
        return self.agenda_conductor.obtener_agenda_conductor(*args)

    def agregar_suscripcion_conductor(self, *args):
        return self.asignacion_conductor.agregar_suscripcion_conductor(*args)

    def listar_viajes_suscripcion_conductor(self, *args):
        return self.agenda_conductor.listar_viajes_suscripcion_conductor(*args)

    def cancelar_suscripcion_conductor(self, *args):
        return self.asignacion_conductor.cancelar_suscripcion_conductor(*args)

    def confirmar_pasajero_abordo_conductor(self, *args):
        return self.viajes_conductor.confirmar_pasajero_abordo_conductor(*args)

    def finalizar_viaje_conductor(self, *args):
        return self.viajes_conductor.finalizar_viaje_conductor(*args)

    def cancelar_viaje_conductor(self, *args):
        return self.viajes_conductor.cancelar_viaje_conductor(*args)



    # --- Operaciones de pagos ---



    def cobrar_suscripcion(self, *args):
        return self.pagos.cobrar_suscripcion(*args)

    def reembolsar_suscripcion(self, *args):
        return self.pagos.reembolsar_suscripcion(*args)

    def abonar_conductor_suscripcion(self, *args):
        return self.pagos.abonar_conductor(*args)

    # --- Tareas periódicas ---
    def procesar_pendientes(self, ahora=None):
        """Procesa viajes vencidos y finaliza suscripciones expiradas."""
        return self.procesador.procesar(ahora)
