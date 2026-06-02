from abc import ABC, abstractmethod

#archivo para almacenar clases abstractas.
class TarjetaBase(ABC):
    
    @abstractmethod
    def numero_valido(self, numero):
        pass

class Validador(ABC):
    @abstractmethod
    def validar(self, datos):
        pass

class NavegadorAbstracto(ABC):
    @abstractmethod
    def navegar(self, destino):
        pass


class RutaNavegacion(ABC):
    rutas_registradas = []
    destino = ""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.destino:
            RutaNavegacion.rutas_registradas.append(cls)

    def __init__(self, navegacion):
        self.navegacion = navegacion

    def limpiar_pantalla(self):
        for widget in self.navegacion.ventana.winfo_children():
            widget.destroy()

    def mostrar(self, vista, titulo):
        self.limpiar_pantalla()
        self.navegacion.ventana.title(titulo)
        vista(self.navegacion.ventana, self.navegacion.navegar)

    @abstractmethod
    def ejecutar(self):
        pass