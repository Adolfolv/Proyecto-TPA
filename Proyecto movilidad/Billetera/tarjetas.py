import abstracciones

TarjetaBase = abstracciones.TarjetaBase

class TarjetaVisa(TarjetaBase):

    longitud_cvv = 3
    def numero_valido(self, numero):
        return (numero.startswith("4") and 13 <= len(numero) <= 19)

class TarjetaMastercard(TarjetaBase):

    longitud_cvv = 3
    def numero_valido(self, numero):
        if len(numero) != 16:
            return False

        dos = int(numero[:2])
        cuatro = int(numero[:4])
        return (51 <= dos <= 55 or 2221 <= cuatro <= 2720)

class TarjetaAmericanExpress(TarjetaBase):

    longitud_cvv = 4
    def numero_valido(self, numero):
        return (len(numero) == 15 and numero.startswith(("34", "37")))
    

agregar_algo = abstracciones.agregar_algo

class ServicioTarjeta(agregar_algo):

    def agregar_tarjeta(self, usuario, tarjeta):

        for tarjeta_existente in usuario.billetera.tarjetas:

            if (
                tarjeta_existente.numero_tarjeta
                == tarjeta.numero_tarjeta
            ):

                print("La tarjeta ya existe")
                return False

        usuario.billetera.tarjetas.append(tarjeta)
        print("Tarjeta agregada correctamente")
        return True








    
#