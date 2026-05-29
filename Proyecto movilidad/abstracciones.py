from abc import ABC, abstractmethod

class TarjetaBase(ABC):
    
    @abstractmethod
    def numero_valido(self, numero):
        pass
