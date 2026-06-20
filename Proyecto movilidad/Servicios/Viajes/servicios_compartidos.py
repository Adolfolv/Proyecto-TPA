from Servicios.Viajes.calculadora_viaje import CalculadoraViaje
from Servicios.Viajes.datos_viaje import LUGARES_OSORNO
from Servicios.Viajes.fabrica_viaje import FabricaViaje
from Servicios.Viajes.trayectoria import Trayectoria
from Validaciones.validaciones_viaje import ValidacionesViaje


class ServicioViajeComun:
    """Operaciones compartidas por pasajero y conductor."""

    def __init__(self, trayectoria=None):
        self.viajes = []
        self.trayectoria = trayectoria or Trayectoria()
        self.calculadora = CalculadoraViaje(self.trayectoria)
        self.fabrica = FabricaViaje(self.trayectoria, self.calculadora)

    def obtener_lugares_disponibles(self):
        return tuple(LUGARES_OSORNO)

    def obtener_punto_lugar(self, nombre_lugar):
        return LUGARES_OSORNO[nombre_lugar]

    def formar_trayectoria(self, ubicacion_inicial, ubicacion_final):
        inicio = self.obtener_punto_lugar(ubicacion_inicial)
        destino = self.obtener_punto_lugar(ubicacion_final)
        return self.formar_trayectoria_por_puntos(inicio, destino)

    def formar_trayectoria_por_puntos(self, inicio, destino):
        ruta_relativa = self.trayectoria.calcular_trayectoria(inicio, destino)
        return [self.trayectoria.coordenada_real(punto) for punto in ruta_relativa]

    def iniciar_viaje(self, viaje):
        self.viajes.append(viaje)
        return viaje

    def calcular_tiempo_por_km(self, distancia):
        return self.calculadora.calcular_tiempo_por_km(distancia)

    def calcular_km_trayectoria(self, ruta_relativa):
        return self.calculadora.calcular_km_trayectoria(ruta_relativa)

    def calcular_km_entre_coordenadas(self, inicio, destino):
        return self.calculadora.calcular_km_entre_coordenadas(inicio, destino)

    def calcular_tiempos_viaje(self, km_para_llegar, km_transportando):
        return self.calculadora.calcular_tiempos_viaje(
            km_para_llegar,
            km_transportando,
        )


class ServicioPagoViaje:
    """Reglas de pago propias del flujo de viajes."""

    def __init__(self, servicio_billetera=None):
        self.servicio_billetera = servicio_billetera
        self.validaciones = ValidacionesViaje()

    def cobrar_pasajero(self, usuario, monto):
        self.validaciones.validar_pago_pasajero(self.servicio_billetera, usuario)
        self.servicio_billetera.ejecutar("pagar", usuario, monto)
        return True

    def abonar_conductor(self, usuario, monto):
        self.validaciones.validar_abono_conductor(self.servicio_billetera, usuario)
        self.servicio_billetera.ejecutar("recibir", usuario, monto)
        return True
