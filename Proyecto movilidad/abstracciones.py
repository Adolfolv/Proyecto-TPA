from abc import ABC, abstractmethod

class TarjetaBase(ABC):
    
    @abstractmethod
    def numero_valido(self, numero):
        pass

class agregar_algo(ABC):
    @abstractmethod
    def agregar(self, algo):
        pass