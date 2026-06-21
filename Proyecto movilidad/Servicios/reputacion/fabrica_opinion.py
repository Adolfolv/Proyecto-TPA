from Modelos.Reputacion.opinion import Opinion


class FabricaOpinion:
    def crear(self, conductor, pasajero, estrellas, comentario):
        return Opinion(
            id_opinion=None,
            id_conductor=str(conductor.id_usuario),
            id_pasajero=str(pasajero.id_usuario),
            nombre_pasajero=f"{pasajero.nombre} {pasajero.apellido}".strip(),
            estrellas=int(estrellas),
            comentario=str(comentario).strip(),
        )
