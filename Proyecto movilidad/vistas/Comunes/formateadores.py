class FormateadorMoneda:
    @staticmethod
    def pesos(monto):
        return f"${float(monto or 0):,.0f}".replace(",", ".")
