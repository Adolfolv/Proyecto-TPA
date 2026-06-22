# Interfaz base: obliga a que las operaciones de billetera tengan un ejecutar().
from abstracciones import OperacionBilletera

# Clases de dominio que hacen el trabajo concreto: historial, movimiento y pago.
from Modelos.Billetera.movimiento import HistorialTransacciones, MoverSaldo, Pago
from Servicios.Billetera.servicio_billetera import obtener_o_crear_billetera


class OperacionMovimiento(OperacionBilletera):
    # Esta clase base representa lo comun a cualquier operacion de saldo.
    # Clase base de operaciones: comparte obtencion, historial y guardado.

    def __init__(self, repositorio_billetera, tipo_transaccion, historial=None):
        # Inyeccion de dependencias: permite cambiar repositorio o historial.
        # El repositorio se usa para obtener y guardar la billetera del usuario.
        self.repositorio_billetera = repositorio_billetera
        # El tipo se guarda despues en el historial: "Pago", "Retiro a tarjeta", etc.
        self.tipo_transaccion = tipo_transaccion
        # Si no se entrega un historial externo, se crea el historial normal.
        self.historial = historial or HistorialTransacciones()

    def _completar(self, usuario, billetera, monto):
        # Template Method parcial: las subclases cambian saldo y luego usan este cierre comun.
        # Toda operacion que cambia saldo termina registrando historial y guardando JSON.
        # Primero se agrega una transaccion a la lista de la billetera.
        self.historial.crear_transaccion(billetera, self.tipo_transaccion, monto)
        # Luego se persiste la billetera completa asociada al usuario.
        self.repositorio_billetera.actualizar(usuario.id_usuario, billetera)
        # Se devuelve True para indicar que la operacion termino correctamente.
        return True

    def _obtener_billetera(self, usuario):
        # Centraliza la forma de recuperar la billetera del usuario actual.
        return obtener_o_crear_billetera(
            self.repositorio_billetera,
            usuario.id_usuario,
        )


class OperacionPago(OperacionMovimiento):
    # Esta clase sirve para operaciones que solo usan la billetera, no una tarjeta.
    # Patron Command/Strategy: encapsula una operacion concreta de pago o recepcion.

    def __init__(
        self,
        # Repositorio donde se obtiene y guarda la billetera.
        repositorio_billetera,
        # Nombre que se vera en el historial de transacciones.
        tipo_transaccion,
        # Nombre del metodo que se llamara en Pago: "pagar" o "recibir_pago".
        metodo_pago,
        # Objeto opcional para hacer el pago; si no llega, se crea Pago().
        pago=None,
        # Historial opcional, util si se quisiera reemplazar en pruebas.
        historial=None,
    ):
        # Reutiliza la inicializacion comun: repositorio, tipo e historial.
        super().__init__(repositorio_billetera, tipo_transaccion, historial)
        # Guarda el nombre del metodo que se ejecutara dinamicamente.
        self.metodo_pago = metodo_pago
        # Si no se inyecta un objeto Pago, usa la implementacion por defecto.
        self.pago = pago or Pago()

    def ejecutar(self, solicitud):
        # La solicitud trae usuario, monto y opcionalmente numero de tarjeta.
        # Para pagar o recibir solo se necesita la billetera del usuario.
        billetera = self._obtener_billetera(solicitud.usuario)
        # Dynamic dispatch: el texto del metodo selecciona pagar o recibir_pago.
        # metodo_pago contiene el nombre del metodo real: pagar o recibir_pago.
        # getattr busca el metodo por nombre y lo ejecuta con billetera y monto.
        getattr(self.pago, self.metodo_pago)(billetera, solicitud.monto)
        # Despues de modificar saldo, registra historial y guarda.
        return self._completar(solicitud.usuario, billetera, solicitud.monto)


class OperacionMovimientoTarjeta(OperacionMovimiento):
    # Esta clase sirve para operaciones que mueven dinero entre billetera y tarjeta.
    # Patron Command/Strategy: encapsula cargar o retirar saldo usando una tarjeta.

    def __init__(
        self,
        # Repositorio donde se obtiene y guarda la billetera.
        repositorio_billetera,
        # Servicio usado para encontrar la tarjeta dentro de la billetera.
        servicio_tarjeta,
        # Nombre que aparecera en el historial.
        tipo_transaccion,
        # False: tarjeta a billetera. True: billetera a tarjeta.
        origen_es_billetera=False,
        # Objeto opcional que sabe mover saldo entre dos objetos.
        mover=None,
        # Historial opcional, igual que en la clase padre.
        historial=None,
    ):
        # Inicializa los datos comunes de cualquier operacion.
        super().__init__(repositorio_billetera, tipo_transaccion, historial)
        # Se guarda el servicio de tarjetas para buscar la tarjeta indicada.
        self.servicio_tarjeta = servicio_tarjeta
        # Define el sentido del movimiento sin usar otra clase distinta.
        self.origen_es_billetera = origen_es_billetera
        # Si no se inyecta un MoverSaldo, se usa el normal.
        self.mover = mover or MoverSaldo()

    def ejecutar(self, solicitud):
        # Primero se obtiene la billetera del usuario.
        billetera = self._obtener_billetera(solicitud.usuario)
        # Luego se busca la tarjeta indicada en la solicitud.
        tarjeta = self.servicio_tarjeta.obtener_tarjeta_de_billetera(
            billetera,
            solicitud.numero_tarjeta,
        )
        # Strategy por configuracion: origen_es_billetera cambia la direccion del flujo.
        # Cambia el sentido del movimiento segun si el origen es la billetera o la tarjeta.
        # Si origen_es_billetera es True: se retira desde billetera hacia tarjeta.
        # Si es False: se carga desde tarjeta hacia billetera.
        origen, destino = (
            (billetera, tarjeta)
            if self.origen_es_billetera
            else (tarjeta, billetera)
        )
        # Ejecuta el movimiento real: quitar saldo al origen y sumarlo al destino.
        self.mover.mover_saldo(origen, destino, solicitud.monto)
        # Despues de mover saldo, registra historial y guarda.
        return self._completar(solicitud.usuario, billetera, solicitud.monto)
