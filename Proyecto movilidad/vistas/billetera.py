"""Pantalla de billetera visual sin navegacion real."""

import tkinter as tk

from estilizacion import tema
from estilizacion.widgets import Moldes


class VistaBilletera(tk.Frame):
    def __init__(self):
        ventana = tk.Tk()
        ventana.title("Billetera virtual")
        ventana.geometry("1000x720")
        ventana.minsize(860, 620)
        ventana.attributes("-fullscreen", True)

        self.moldes = Moldes()
        self.moldes.configurar_selectores(ventana)

        super().__init__(ventana, bg=tema.FONDO)
        self.pack(fill="both", expand=True)
        self.crear_widgets()

    def crear_widgets(self):
        panel = self.moldes.crear_frame(self, tema.PANEL, tema.BORDE, 1, 22, 22, llenar="both", expandir=True, margen_x=24, margen_y=24, columnas_peso=((0, 1),), filas_peso=((2, 1),))

        cabecera = self.moldes.crear_frame(panel, tema.PANEL, fila=0, columna=0, sticky="ew", margen_y=(0, 12), columnas_peso=((0, 1),))
        self.moldes.crear_label(cabecera, "Billetera virtual", tema.FUENTE_TITULO, tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")
        self.moldes.crear_boton(cabecera, "Volver", False, None, None, metodo="grid", fila=0, columna=1, sticky="e")
        self.moldes.crear_label(cabecera, "Administra tarjetas principales y movimientos entre billetera y tarjetas adjuntas.", tema.FUENTE_TEXTO, tema.TEXTO_SUAVE, tema.PANEL, 880, "left", metodo="grid", fila=1, columna=0, columnas=2, sticky="w", margen_y=(4, 0))

        resumen = self.moldes.crear_frame(panel, tema.PANEL, fila=1, columna=0, sticky="ew", margen_y=(0, 10))
        resumen.grid_columnconfigure(0, weight=1, uniform="resumen")
        resumen.grid_columnconfigure(1, weight=1, uniform="resumen")
        saldo_billetera = self.moldes.crear_frame(resumen, tema.PANEL_SUAVE, tema.BORDE, 1, 16, 14, fila=0, columna=0, margen_x=(0, 7))
        self.moldes.crear_label(saldo_billetera, "Saldo de billetera", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE).pack(anchor="w")
        self.moldes.crear_label(saldo_billetera, "$0 CLP", ("Arial", 20, "bold"), tema.PRIMARIO, tema.PANEL_SUAVE).pack(anchor="w", pady=(6, 0))
        saldo_tarjetas = self.moldes.crear_frame(resumen, tema.PANEL_SUAVE, tema.BORDE, 1, 16, 14, fila=0, columna=1, margen_x=(7, 0))
        self.moldes.crear_label(saldo_tarjetas, "Saldo total de tarjetas", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE).pack(anchor="w")
        self.moldes.crear_label(saldo_tarjetas, "$0 CLP", ("Arial", 20, "bold"), tema.PRIMARIO, tema.PANEL_SUAVE).pack(anchor="w", pady=(6, 0))

        gestion = self.moldes.crear_frame(panel, tema.PANEL, fila=2, columna=0, sticky="nsew", margen_y=(0, 8), columnas_peso=((0, 1), (1, 1)), filas_peso=((0, 1),))
        gestion.grid_columnconfigure(0, weight=1, uniform="gestion")
        gestion.grid_columnconfigure(1, weight=1, uniform="gestion")
        
        tarjeta = self.moldes.crear_frame(gestion, tema.PANEL_SUAVE, tema.BORDE, 1, 16, 14, fila=0, columna=0, margen_x=(0, 8), columnas_peso=((0, 1), (1, 1)), filas_peso=((9, 1),))
        self.moldes.crear_label(tarjeta, "Agregar tarjeta", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, columnas=2, sticky="w", margen_y=(0, 10))
        self.moldes.crear_label(tarjeta, "Tipo", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=1, columna=0, sticky="w", margen_x=4, margen_y=(0, 4))
        self.moldes.crear_label(tarjeta, "Titular", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=1, columna=1, sticky="w", margen_x=4, margen_y=(0, 4))
        self.moldes.crear_selector(tarjeta, ("Visa", "Mastercard", "American Express"), metodo="grid", fila=2, columna=0, sticky="ew", margen_x=4, margen_y=(0, 8), ipady=4)
        self.moldes.crear_entrada(tarjeta, metodo="grid", fila=2, columna=1, sticky="ew", margen_x=4, margen_y=(0, 8), ipady=4)
        self.moldes.crear_label(tarjeta, "Numero", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=3, columna=0, sticky="w", margen_x=4, margen_y=(0, 4))
        self.moldes.crear_label(tarjeta, "Caducidad (MM/AA)", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=3, columna=1, sticky="w", margen_x=4, margen_y=(0, 4))
        self.moldes.crear_entrada(tarjeta, metodo="grid", fila=4, columna=0, sticky="ew", margen_x=4, margen_y=(0, 8), ipady=4)
        self.moldes.crear_entrada(tarjeta, metodo="grid", fila=4, columna=1, sticky="ew", margen_x=4, margen_y=(0, 8), ipady=4)
        self.moldes.crear_label(tarjeta, "CVV", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=5, columna=0, sticky="w", margen_x=4, margen_y=(0, 4))
        self.moldes.crear_entrada(tarjeta, metodo="grid", fila=6, columna=0, sticky="ew", margen_x=4, margen_y=(0, 10), ipady=4)
        acciones_tarjeta = self.moldes.crear_frame(tarjeta, tema.PANEL_SUAVE, fila=7, columna=0, columnas=2, sticky="w", margen_y=(0, 8))
        self.moldes.crear_boton(acciones_tarjeta, "Anadir tarjeta", True, None, None, lado="left", margen_x=(0, 6))
        self.moldes.crear_boton(acciones_tarjeta, "Eliminar tarjeta", False, None, None, lado="left")
        self.moldes.crear_label(tarjeta, "Tarjetas agregadas: 0", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=8, columna=0, columnas=2, sticky="w", margen_y=(0, 6))
        lista_tarjetas = tk.Listbox(tarjeta, height=8, activestyle="none", relief="solid", bd=1, font=tema.FUENTE_TEXTO, bg=tema.SECUNDARIO, fg=tema.TEXTO, selectbackground=tema.PRIMARIO, selectforeground=tema.PRIMARIO_TEXTO)
        lista_tarjetas.insert(tk.END, "Aun no hay tarjetas agregadas.")
        self.moldes.ubicar(lista_tarjetas, "grid", fila=9, columna=0, columnas=2, sticky="nsew")

        movimiento = self.moldes.crear_frame(gestion, tema.PANEL_SUAVE, tema.BORDE, 1, 16, 14, fila=0, columna=1, margen_x=(8, 0), columnas_peso=((0, 1), (1, 1)), filas_peso=((9, 1),))
        self.moldes.crear_label(movimiento, "Mover saldo", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, columnas=2, sticky="w", margen_y=(0, 10))
        self.moldes.crear_label(movimiento, "Tarjeta", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=1, columna=0, sticky="w", margen_x=4, margen_y=(0, 4))
        self.moldes.crear_label(movimiento, "Direccion", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=1, columna=1, sticky="w", margen_x=4, margen_y=(0, 4))
        self.moldes.crear_selector(movimiento, ("Sin tarjetas",), metodo="grid", fila=2, columna=0, sticky="ew", margen_x=4, margen_y=(0, 8), ipady=4)
        self.moldes.crear_selector(movimiento, ("Tarjeta a billetera", "Billetera a tarjeta"), metodo="grid", fila=2, columna=1, sticky="ew", margen_x=4, margen_y=(0, 8), ipady=4)
        self.moldes.crear_label(movimiento, "Monto", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=3, columna=0, sticky="w", margen_x=4, margen_y=(0, 4))
        self.moldes.crear_entrada(movimiento, metodo="grid", fila=4, columna=0, sticky="ew", margen_x=4, margen_y=(0, 10), ipady=4)
        self.moldes.crear_label(movimiento, "Puedes mover saldo desde una tarjeta hacia la billetera o devolver saldo a una tarjeta.", tema.FUENTE_TEXTO, tema.TEXTO_SUAVE, tema.PANEL_SUAVE, 420, "left", metodo="grid", fila=5, columna=0, columnas=2, sticky="w", margen_y=(0, 12))
        self.moldes.crear_boton(movimiento, "Mover saldo", True, None, None, metodo="grid", fila=6, columna=0, sticky="w")
        self.moldes.crear_label(movimiento, "Historial de transacciones", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=8, columna=0, columnas=2, sticky="w", margen_y=(14, 6))
        lista_historial = tk.Listbox(movimiento, height=8, activestyle="none", relief="solid", bd=1, font=tema.FUENTE_TEXTO, bg=tema.SECUNDARIO, fg=tema.TEXTO, selectbackground=tema.PRIMARIO, selectforeground=tema.PRIMARIO_TEXTO)
        lista_historial.insert(tk.END, "Aun no hay transacciones registradas.")
        self.moldes.ubicar(lista_historial, "grid", fila=9, columna=0, columnas=2, sticky="nsew")


    def ejecutar(self):
        self.master.mainloop()


if __name__ == "__main__":
    VistaBilletera().ejecutar()
