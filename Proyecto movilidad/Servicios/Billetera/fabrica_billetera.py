from Modelos.Billetera.datos_billetera import Billetera, Tarjetas, Transaccion
from Validaciones.billetera import normalizar_saldo_entero


class FabricaBilletera:
    # Patron Factory: reconstruye objetos de dominio desde datos del JSON.
    """Reconstruye billeteras y sus modelos anidados desde datos persistidos.."""

    def crear_desde_dict(self, datos):
        return Billetera(
            saldo=normalizar_saldo_entero(datos.get("saldo", 0)),
            tarjetas=[
                self._crear_tarjeta(tarjeta)
                for tarjeta in datos.get("tarjetas", [])
            ],
            transacciones=[
                self._crear_transaccion(transaccion)
                for transaccion in datos.get("transacciones", [])
            ],
        )

    def _crear_tarjeta(self, datos):
        return Tarjetas(
            titular=datos["titular"],
            numero_tarjeta=str(datos["numero_tarjeta"]).strip(),
            vencimiento=str(datos["vencimiento"]).strip(),
            cvv="",
            saldo=normalizar_saldo_entero(datos.get("saldo", 0)),
        )

    def _crear_transaccion(self, datos):
        return Transaccion(
            id_transaccion=str(datos["id_transaccion"]),
            tipo=str(datos["tipo"]),
            monto=normalizar_saldo_entero(datos.get("monto", 0)),
            fecha=str(datos["fecha"]),
        )
