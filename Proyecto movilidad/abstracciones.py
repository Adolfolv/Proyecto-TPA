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
