from Modelos.Billetera.tarjetas import (
    TarjetaVisa,
    TarjetaMastercard,
    TarjetaAmericanExpress,
)
from Validaciones.billetera import (
    ValidadorTarjetaEncontrada,
    ValidacionesTarjeta,
)
#_
from Servicios.Billetera.fabrica_tarjeta import FabricaTarjeta
from Servicios.Billetera.servicio_billetera import obtener_o_crear_billetera

class ServicioTarjeta:

    # Patron Strategy simple: el tipo de tarjeta decide que validador/regla se usa.
    TIPOS_TARJETA = {
        "Visa": TarjetaVisa,
        "Mastercard": TarjetaMastercard,
        "American Express": TarjetaAmericanExpress,
    }

    def __init__(
        self,
        repositorio_billetera,
        buscador_tarjeta,
        validaciones_tarjeta=None,
        fabrica_tarjeta=None,
        generador_saldo_tarjeta=None,
    ):
        # Inyeccion de dependencias: recibe repositorio, buscador y fabrica desde afuera.
        self.repositorio_billetera = repositorio_billetera
        self.buscador_tarjeta = buscador_tarjeta
        self.validaciones_tarjeta = (
            validaciones_tarjeta
            or ValidacionesTarjeta(self.TIPOS_TARJETA)
        )
        self.fabrica_tarjeta = fabrica_tarjeta or FabricaTarjeta(
            generador_saldo_tarjeta
        )
        self.validador_tarjeta_encontrada = ValidadorTarjetaEncontrada()

    def _obtener_billetera(self, usuario):
        return obtener_o_crear_billetera(
            self.repositorio_billetera,
            usuario.id_usuario,
        )

    def _buscar_tarjeta(self, billetera, numero_tarjeta):
        tarjeta = self.buscador_tarjeta.buscar(billetera, numero_tarjeta)
        # Si no existe, la validacion lanza ValueError para que la vista lo muestre.
        self.validador_tarjeta_encontrada.validar(tarjeta)
        return tarjeta

    def obtener_tarjetas(self, usuario):
        return self._obtener_billetera(usuario).tarjetas

    def obtener_tarjeta(self, usuario, numero_tarjeta):
        billetera = self._obtener_billetera(usuario)
        return self._buscar_tarjeta(billetera, numero_tarjeta)

    def obtener_tarjeta_de_billetera(self, billetera, numero_tarjeta):
        return self._buscar_tarjeta(billetera, numero_tarjeta)

    def agregar_tarjeta(self, usuario, tipo, titular, numero, vencimiento, cvv):
        billetera = self._obtener_billetera(usuario)

        # El saldo aleatorio solo se genera cuando la tarjeta ya paso validaciones.
        self.validaciones_tarjeta.validar(
            titular,
            billetera,
            tipo,
            numero,
            vencimiento,
            cvv,
        )

        tarjeta = self.fabrica_tarjeta.crear(titular, numero, vencimiento, cvv)
        billetera.tarjetas.append(tarjeta)
        # Se persiste toda la billetera porque las tarjetas viven dentro de ella.
        self.repositorio_billetera.actualizar(usuario.id_usuario, billetera)

        return True

    def eliminar_tarjeta(self, usuario, numero_tarjeta):
        billetera = self._obtener_billetera(usuario)
        tarjeta = self._buscar_tarjeta(billetera, numero_tarjeta)
        billetera.tarjetas.remove(tarjeta)
        # Al eliminar tambien se guarda la billetera completa actualizada.
        self.repositorio_billetera.actualizar(usuario.id_usuario, billetera)
        return True
