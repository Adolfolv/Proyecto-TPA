from Modelos.Billetera.datos_billetera import SolicitudOperacionBilletera


#archivo para manejar la lógica de negocio relacionada con la billetera, 
# incluyendo la gestión de tarjetas, movimientos de saldo, pagos y recepciones.  
# realizar pagos, recibir pagos, cargar o retirar fondos, y consultar el saldo a la billetera del usuario..
class ServicioBilletera:

    def __init__(self, repositorio_billetera, operaciones):
        self.repositorio_billetera = repositorio_billetera
        self.operaciones = operaciones

    def obtener_billetera(self, usuario):
        return self.repositorio_billetera.obtener(usuario)

    def ejecutar(self, nombre_operacion, usuario, monto, numero_tarjeta=None):
        operacion = self.operaciones[nombre_operacion]
        solicitud = SolicitudOperacionBilletera(usuario, monto, numero_tarjeta)
        return operacion.ejecutar(solicitud)

    def obtener_resumen(self, usuario):
        billetera = self.obtener_billetera(usuario)
        return {
            "saldo_billetera": billetera.saldo,
            "tarjetas": billetera.tarjetas,
            "transacciones": billetera.transacciones,
        }

    def guardar(self, usuario=None, billetera=None):
        if usuario is None:
            self.repositorio_billetera.guardar()
            return

        billetera = billetera or self.obtener_billetera(usuario)
        self.repositorio_billetera.guardar_por_usuario(usuario.id_usuario, billetera)
