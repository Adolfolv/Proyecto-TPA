from Modelos.Billetera.datos_billetera import SolicitudOperacionBilletera
from Validaciones.billetera import normalizar_monto_entero


#archivo para manejar la lógica de negocio relacionada con la billetera, 
# incluyendo la gestión de tarjetas, movimientos de saldo, pagos y recepciones.  
# realizar pagos, recibir pagos, cargar o retirar fondos, y consultar el saldo a la billetera del usuario..
class ServicioBilletera:
    # Patron Service/Fachada: ofrece una entrada simple para operaciones de billetera.

    def __init__(self, repositorio_billetera, operaciones):
        # Inyeccion de dependencias: recibe el repositorio y las operaciones ya armadas.
        self.repositorio_billetera = repositorio_billetera
        self.operaciones = operaciones

    def obtener_billetera(self, usuario):
        return self.repositorio_billetera.obtener(usuario)

    def ejecutar(self, nombre_operacion, usuario, monto, numero_tarjeta=None):
        # Patron Strategy/Command: cada nombre apunta a un objeto operacion distinto.
        # El nombre recibido elige una estrategia concreta: pagar, recibir, cargar o retirar.
        operacion = self.operaciones[nombre_operacion]
        solicitud = SolicitudOperacionBilletera(
            usuario,
            normalizar_monto_entero(monto),
            numero_tarjeta,
        )
        # No es recursion: se delega al ejecutar de la operacion seleccionada.
        return operacion.ejecutar(solicitud)

    def obtener_resumen(self, usuario):
        billetera = self.obtener_billetera(usuario)
        # La vista consume este resumen para refrescar saldos, tarjetas e historial.
        return {
            "saldo_billetera": billetera.saldo,
            "tarjetas": billetera.tarjetas,
            "transacciones": billetera.transacciones,
        }

    def guardar(self, usuario=None, billetera=None):
        if usuario is None:
            # Sin usuario especifico, guarda todas las billeteras cargadas.
            self.repositorio_billetera.guardar()
            return

        # Si no llega una billetera, se usa la billetera actual del usuario.
        billetera = billetera or self.obtener_billetera(usuario)
        self.repositorio_billetera.guardar_por_usuario(usuario.id_usuario, billetera)
