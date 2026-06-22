from Servicios.Usuario.buscador import BuscadorUsuario
from Servicios.reputacion.calculo_repu import CalculoReputacion
from Servicios.reputacion.fabrica_opinion import FabricaOpinion
from Validaciones.reputacion import ValidacionesOpinion


class ServicioReputacion:
    def __init__(self, repositorio_reputacion, repositorio_usuario):
        self.repositorio_reputacion = repositorio_reputacion
        self.repositorio_usuario = repositorio_usuario
        self.validaciones = ValidacionesOpinion(repositorio_reputacion)

    def listar_conductores(self):
        return [
            usuario
            for usuario in self.repositorio_usuario.listar()
            if getattr(usuario, "tipo_usuario", "") == "conductor"
            and not getattr(usuario, "cuenta_congelada", False)
        ]

    def obtener_reputacion(self, referencia):
        conductor = self._buscar_conductor(referencia)
        self.validaciones.validar_conductor(conductor)
        return self._resultado(conductor)

    def agregar_opinion(self, referencia, pasajero, estrellas, comentario):
        conductor = self._buscar_conductor(referencia)
        self.validaciones.validar(conductor, pasajero, estrellas, comentario)
        opinion = FabricaOpinion().crear(
            conductor,
            pasajero,
            estrellas,
            comentario,
        )
        opinion.id_opinion = self._siguiente_id_opinion()
        self.repositorio_reputacion.agregar(opinion)
        return self._resultado(conductor)

    def _siguiente_id_opinion(self):
        numeros = [
            int(opinion.id_opinion[3:])
            for opinion in self.repositorio_reputacion.listar()
        ]
        return f"OPI{max(numeros, default=0) + 1:04d}"

    def _buscar_conductor(self, referencia):
        if getattr(referencia, "tipo_usuario", "") == "conductor":
            return referencia
        return BuscadorUsuario(self.repositorio_usuario).buscar(referencia)

    def _resultado(self, conductor):
        opiniones = self.repositorio_reputacion.listar_por_conductor(conductor.id_usuario)
        promedio = CalculoReputacion().calcular_promedio(
            sum(item.estrellas for item in opiniones), len(opiniones)
        )
        return {
            "conductor": conductor,
            "promedio": round(promedio, 1),
            "opiniones": list(reversed(opiniones)),
        }
