from abstracciones import Validador
from Validaciones.comunes import es_numero


class ValidadorConductorReputacion(Validador):
    def validar(self, conductor):
        if conductor is None or getattr(conductor, "tipo_usuario", "") != "conductor":
            return "Selecciona un conductor valido."
        return ""


class ValidadorPasajeroOpinion(Validador):
    def validar(self, pasajero):
        if getattr(pasajero, "tipo_usuario", "") != "pasajero":
            return "Solo un pasajero puede dejar una opinion."
        return ""


class ValidadorEstrellas(Validador):
    def validar(self, estrellas):
        if not es_numero(estrellas) or not 1 <= int(estrellas) <= 5:
            return "Selecciona una cantidad de estrellas entre 1 y 5."
        return ""


class ValidadorComentario(Validador):
    def validar(self, comentario):
        comentario = str(comentario or "").strip()
        if not comentario:
            return "Escribe una opinion antes de publicarla."
        if len(comentario) > 500:
            return "La opinion no puede superar los 500 caracteres."
        return ""


class ValidadorOpinionUnica(Validador):
    def __init__(self, repositorio_reputacion):
        self.repositorio_reputacion = repositorio_reputacion

    def validar(self, datos):
        conductor, pasajero = datos
        opinion = self.repositorio_reputacion.buscar_del_pasajero(
            conductor.id_usuario,
            pasajero.id_usuario,
        )
        if opinion is not None:
            return "Ya dejaste una opinion para este conductor."
        return ""


class ValidacionesOpinion:
    """Compone las reglas de una opinion como ValidacionesUsuario en registro."""

    def __init__(self, repositorio_reputacion):
        self.validador_conductor = ValidadorConductorReputacion()
        self.validadores = (
            self.validador_conductor,
            ValidadorPasajeroOpinion(),
            ValidadorEstrellas(),
            ValidadorComentario(),
        )
        self.validador_opinion_unica = ValidadorOpinionUnica(repositorio_reputacion)

    def validar_conductor(self, conductor):
        return self.validador_conductor.validar(conductor)

    def validar(self, conductor, pasajero, estrellas, comentario):
        valores = (conductor, pasajero, estrellas, comentario)
        for validador, valor in zip(self.validadores, valores):
            error = validador.validar(valor)
            if error:
                return error
        return self.validador_opinion_unica.validar((conductor, pasajero))
