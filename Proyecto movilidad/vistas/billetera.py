"""Pantalla de billetera separada por responsabilidades."""

import tkinter as tk
from tkinter import messagebox

from .estilizacion import tema
from .estilizacion.widgets import Moldes


class CabeceraBilletera:
    def __init__(self, panel):
        self.panel = panel
        self.moldes = panel.moldes
        self.callbacks = panel.callbacks

    def crear(self):
        cabecera = self.moldes.crear_frame(self.panel.frame, tema.PANEL, fila=0, columna=0, sticky="ew", margen_y=(0, 12), columnas_peso=((0, 1),))
        self.moldes.crear_label(cabecera, "Billetera virtual", tema.FUENTE_TITULO, tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")
        self.moldes.crear_boton(cabecera, "Volver", False, None, self.callbacks["volver_menu"], metodo="grid", fila=0, columna=1, sticky="e")
        self.moldes.crear_label(cabecera, "Administra tarjetas principales y movimientos entre billetera y tarjetas adjuntas.", tema.FUENTE_TEXTO, tema.TEXTO_SUAVE, tema.PANEL, 880, "left", metodo="grid", fila=1, columna=0, columnas=2, sticky="w", margen_y=(4, 0))

class ResumenBilletera:
    def __init__(self, panel):
        self.panel = panel
        self.moldes = panel.moldes

    def crear(self):
        resumen = self.moldes.crear_frame(self.panel.frame, tema.PANEL, fila=1, columna=0, sticky="ew", margen_y=(0, 10))
        resumen.grid_columnconfigure(0, weight=1, uniform="resumen")
        resumen.grid_columnconfigure(1, weight=1, uniform="resumen")
        saldo_billetera = self.moldes.crear_frame(resumen, tema.PANEL_SUAVE, tema.BORDE, 1, 16, 14, fila=0, columna=0, margen_x=(0, 7))
        self.moldes.crear_label(saldo_billetera, "Saldo de billetera", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE).pack(anchor="w")
        self.label_saldo_billetera = self.moldes.crear_label(saldo_billetera, "$0 CLP", ("Arial", 20, "bold"), tema.PRIMARIO, tema.PANEL_SUAVE)
        self.label_saldo_billetera.pack(anchor="w", pady=(6, 0))
        saldo_tarjetas = self.moldes.crear_frame(resumen, tema.PANEL_SUAVE, tema.BORDE, 1, 16, 14, fila=0, columna=1, margen_x=(7, 0))
        self.moldes.crear_label(saldo_tarjetas, "Saldo total de tarjetas", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE).pack(anchor="w")
        self.label_saldo_tarjetas = self.moldes.crear_label(saldo_tarjetas, "$0 CLP", ("Arial", 20, "bold"), tema.PRIMARIO, tema.PANEL_SUAVE)
        self.label_saldo_tarjetas.pack(anchor="w", pady=(6, 0))

    def actualizar(self, saldo_billetera, saldo_tarjetas):
        self.label_saldo_billetera.config(text=f"${saldo_billetera:.0f} CLP")
        self.label_saldo_tarjetas.config(text=f"${saldo_tarjetas:.0f} CLP")


class PanelTarjetasBilletera:
    def __init__(self, panel):
        self.panel = panel
        self.moldes = panel.moldes
        self.callbacks = panel.callbacks

    def crear(self, padre):
        tarjeta = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, tema.BORDE, 1, 16, 14, fila=0, columna=0, margen_x=(0, 8), columnas_peso=((0, 1), (1, 1)), filas_peso=((9, 1),))
        self.moldes.crear_label(tarjeta, "Agregar tarjeta", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, columnas=2, sticky="w", margen_y=(0, 10))
        self.moldes.crear_label(tarjeta, "Tipo", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=1, columna=0, sticky="w", margen_x=4, margen_y=(0, 4))
        self.moldes.crear_label(tarjeta, "Titular", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=1, columna=1, sticky="w", margen_x=4, margen_y=(0, 4))
        self.selector_tipo_tarjeta = self.moldes.crear_selector(tarjeta, ("Visa", "Mastercard", "American Express"), metodo="grid", fila=2, columna=0, sticky="ew", margen_x=4, margen_y=(0, 8), ipady=4)
        self.entrada_titular = self.moldes.crear_entrada(tarjeta, metodo="grid", fila=2, columna=1, sticky="ew", margen_x=4, margen_y=(0, 8), ipady=4)
        self.moldes.crear_label(tarjeta, "Numero", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=3, columna=0, sticky="w", margen_x=4, margen_y=(0, 4))
        self.moldes.crear_label(tarjeta, "Caducidad (MM/AA)", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=3, columna=1, sticky="w", margen_x=4, margen_y=(0, 4))
        self.entrada_numero = self.moldes.crear_entrada(tarjeta, metodo="grid", fila=4, columna=0, sticky="ew", margen_x=4, margen_y=(0, 8), ipady=4)
        self.entrada_vencimiento = self.moldes.crear_entrada(tarjeta, metodo="grid", fila=4, columna=1, sticky="ew", margen_x=4, margen_y=(0, 8), ipady=4)
        self.moldes.crear_label(tarjeta, "CVV", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=5, columna=0, sticky="w", margen_x=4, margen_y=(0, 4))
        self.entrada_cvv = self.moldes.crear_entrada(tarjeta, metodo="grid", fila=6, columna=0, sticky="ew", margen_x=4, margen_y=(0, 10), ipady=4)
        acciones_tarjeta = self.moldes.crear_frame(tarjeta, tema.PANEL_SUAVE, fila=7, columna=0, columnas=2, sticky="w", margen_y=(0, 8))
        self.moldes.crear_boton(acciones_tarjeta, "Anadir tarjeta", True, None, self.callbacks["agregar_tarjeta"], lado="left", margen_x=(0, 6))
        self.moldes.crear_boton(acciones_tarjeta, "Eliminar tarjeta", False, None, self.callbacks["eliminar_tarjeta"], lado="left")
        self.label_cantidad_tarjetas = self.moldes.crear_label(tarjeta, "Tarjetas agregadas: 0", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=8, columna=0, columnas=2, sticky="w", margen_y=(0, 6))
        self.lista_tarjetas = tk.Listbox(tarjeta, height=8, activestyle="none", relief="solid", bd=1, font=tema.FUENTE_TEXTO, bg=tema.SECUNDARIO, fg=tema.TEXTO, selectbackground=tema.PRIMARIO, selectforeground=tema.PRIMARIO_TEXTO)
        self.lista_tarjetas.insert(tk.END, "Aun no hay tarjetas agregadas.")
        self.moldes.ubicar(self.lista_tarjetas, "grid", fila=9, columna=0, columnas=2, sticky="nsew")

    def datos_tarjeta(self):
        return (self.selector_tipo_tarjeta.get(), self.entrada_titular.get(), self.entrada_numero.get(), self.entrada_vencimiento.get(), self.entrada_cvv.get())

    def numero_tarjeta_seleccionada(self):
        seleccion = self.lista_tarjetas.curselection()
        if not seleccion:
            return ""
        indice = seleccion[0]
        return self.panel.numeros_tarjetas[indice] if indice < len(self.panel.numeros_tarjetas) else ""

    def actualizar(self, tarjetas):
        self.panel.numeros_tarjetas = [tarjeta.numero_tarjeta for tarjeta in tarjetas]
        self.label_cantidad_tarjetas.config(text=f"Tarjetas agregadas: {len(tarjetas)}")
        self.lista_tarjetas.delete(0, tk.END)
        if not tarjetas:
            self.lista_tarjetas.insert(tk.END, "Aun no hay tarjetas agregadas.")
            return
        for tarjeta in tarjetas:
            self.lista_tarjetas.insert(tk.END, f"{tarjeta.titular} - {tarjeta.numero_tarjeta} - ${tarjeta.saldo:.0f}")


class PanelMovimientoBilletera:
    def __init__(self, panel):
        self.panel = panel
        self.moldes = panel.moldes
        self.callbacks = panel.callbacks

    def crear(self, padre):
        movimiento = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, tema.BORDE, 1, 16, 14, fila=0, columna=1, margen_x=(8, 0), columnas_peso=((0, 1), (1, 1)), filas_peso=((9, 1),))
        self.moldes.crear_label(movimiento, "Mover saldo", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, columnas=2, sticky="w", margen_y=(0, 10))
        self.moldes.crear_label(movimiento, "Tarjeta", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=1, columna=0, sticky="w", margen_x=4, margen_y=(0, 4))
        self.moldes.crear_label(movimiento, "Direccion", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=1, columna=1, sticky="w", margen_x=4, margen_y=(0, 4))
        self.selector_tarjeta_movimiento = self.moldes.crear_selector(movimiento, ("Sin tarjetas",), metodo="grid", fila=2, columna=0, sticky="ew", margen_x=4, margen_y=(0, 8), ipady=4)
        self.selector_direccion = self.moldes.crear_selector(movimiento, ("Tarjeta a billetera", "Billetera a tarjeta"), metodo="grid", fila=2, columna=1, sticky="ew", margen_x=4, margen_y=(0, 8), ipady=4)
        self.moldes.crear_label(movimiento, "Monto", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=3, columna=0, sticky="w", margen_x=4, margen_y=(0, 4))
        self.entrada_monto = self.moldes.crear_entrada(movimiento, metodo="grid", fila=4, columna=0, sticky="ew", margen_x=4, margen_y=(0, 10), ipady=4)
        self.moldes.crear_label(movimiento, "Puedes mover saldo desde una tarjeta hacia la billetera o devolver saldo a una tarjeta.", tema.FUENTE_TEXTO, tema.TEXTO_SUAVE, tema.PANEL_SUAVE, 420, "left", metodo="grid", fila=5, columna=0, columnas=2, sticky="w", margen_y=(0, 12))
        self.moldes.crear_boton(movimiento, "Mover saldo", True, None, self.callbacks["mover_saldo"], metodo="grid", fila=6, columna=0, sticky="w")
        self.moldes.crear_label(movimiento, "Historial de transacciones", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=8, columna=0, columnas=2, sticky="w", margen_y=(14, 6))
        self.lista_historial = tk.Listbox(movimiento, height=8, activestyle="none", relief="solid", bd=1, font=tema.FUENTE_TEXTO, bg=tema.SECUNDARIO, fg=tema.TEXTO, selectbackground=tema.PRIMARIO, selectforeground=tema.PRIMARIO_TEXTO)
        self.lista_historial.insert(tk.END, "Aun no hay transacciones registradas.")
        self.moldes.ubicar(self.lista_historial, "grid", fila=9, columna=0, columnas=2, sticky="nsew")

    def datos_movimiento(self):
        return (self.numero_tarjeta_movimiento(), self.selector_direccion.get(), self.entrada_monto.get())

    def numero_tarjeta_movimiento(self):
        valor = self.selector_tarjeta_movimiento.get()
        return "" if valor == "Sin tarjetas" else valor.split(" - ")[0]

    def actualizar_tarjetas(self, tarjetas):
        if not tarjetas:
            self.selector_tarjeta_movimiento.configure(values=("Sin tarjetas",))
            self.selector_tarjeta_movimiento.current(0)
            return
        opciones = tuple(f"{tarjeta.numero_tarjeta} - ${tarjeta.saldo:.0f}" for tarjeta in tarjetas)
        self.selector_tarjeta_movimiento.configure(values=opciones)
        self.selector_tarjeta_movimiento.current(0)

    def actualizar_historial(self, transacciones):
        self.lista_historial.delete(0, tk.END)
        if not transacciones:
            self.lista_historial.insert(tk.END, "Aun no hay transacciones registradas.")
            return
        for transaccion in transacciones:
            self.lista_historial.insert(tk.END, f"{transaccion.id_transaccion} - {transaccion.tipo} - ${transaccion.monto:.0f} - {transaccion.fecha}")


class PanelBilletera:
    def __init__(self, padre, moldes, callbacks):
        self.padre = padre
        self.moldes = moldes
        self.callbacks = callbacks
        self.numeros_tarjetas = []

    def crear(self):
        self.frame = self.moldes.crear_frame(self.padre, tema.PANEL, tema.BORDE, 1, 22, 22, llenar="both", expandir=True, margen_x=24, margen_y=24, columnas_peso=((0, 1),), filas_peso=((2, 1),))
        self.cabecera = CabeceraBilletera(self)
        self.resumen = ResumenBilletera(self)
        self.tarjetas = PanelTarjetasBilletera(self)
        self.movimiento = PanelMovimientoBilletera(self)
        self.cabecera.crear()
        self.resumen.crear()
        self.crear_gestion()

    def crear_gestion(self):
        gestion = self.moldes.crear_frame(self.frame, tema.PANEL, fila=2, columna=0, sticky="nsew", margen_y=(0, 8), columnas_peso=((0, 1), (1, 1)), filas_peso=((0, 1),))
        gestion.grid_columnconfigure(0, weight=1, uniform="gestion")
        gestion.grid_columnconfigure(1, weight=1, uniform="gestion")
        self.tarjetas.crear(gestion)
        self.movimiento.crear(gestion)

    def actualizar(self, saldo_billetera, tarjetas, transacciones):
        saldo_tarjetas = sum(float(tarjeta.saldo or 0) for tarjeta in tarjetas)
        self.resumen.actualizar(saldo_billetera, saldo_tarjetas)
        self.tarjetas.actualizar(tarjetas)
        self.movimiento.actualizar_tarjetas(tarjetas)
        self.movimiento.actualizar_historial(transacciones)


class FlujoBilletera:
    def __init__(self, vista, panel):
        self.vista = vista
        self.panel = panel

    def agregar_tarjeta(self):
        tipo, titular, numero, vencimiento, cvv = self.panel.tarjetas.datos_tarjeta()
        self.ejecutar_accion(lambda: self.vista.controlador.agregar_tarjeta(self.vista.usuario, tipo, titular, numero, vencimiento, cvv), "Tarjeta agregada correctamente.")

    def eliminar_tarjeta(self):
        numero = self.panel.tarjetas.numero_tarjeta_seleccionada()
        self.ejecutar_accion(lambda: self.vista.controlador.eliminar_tarjeta(self.vista.usuario, numero), "Tarjeta eliminada correctamente.")

    def mover_saldo(self):
        numero, direccion, monto = self.panel.movimiento.datos_movimiento()
        if direccion == "Tarjeta a billetera":
            accion = lambda: self.vista.controlador.cargar_desde_tarjeta(self.vista.usuario, numero, monto)
        else:
            accion = lambda: self.vista.controlador.retirar_a_tarjeta(self.vista.usuario, numero, monto)
        self.ejecutar_accion(accion, "Saldo movido correctamente.")

    def ejecutar_accion(self, accion, mensaje_exito):
        try:
            accion()
            self.vista.actualizar_vista()
            messagebox.showinfo("Billetera", mensaje_exito)
        except ValueError as error:
            messagebox.showerror("Billetera", f"Revisa este dato: {error}")


class VistaBilletera(tk.Frame):
    def __init__(self, master, navegar):
        self.navegar = navegar
        self.controlador = None
        self.usuario = None
        self.moldes = Moldes()
        self.moldes.configurar_selectores(master)
        super().__init__(master, bg=tema.FONDO)
        self.pack(fill="both", expand=True)
        self.crear_widgets()

    def crear_widgets(self):
        callbacks = {"volver_menu": lambda: self.navegar("menu"), "agregar_tarjeta": self.agregar_tarjeta, "eliminar_tarjeta": self.eliminar_tarjeta, "mover_saldo": self.mover_saldo}
        self.panel = PanelBilletera(self, self.moldes, callbacks)
        self.panel.crear()
        self.flujo = FlujoBilletera(self, self.panel)

    def conectar_controlador(self, controlador, usuario):
        self.controlador = controlador
        self.usuario = usuario
        self.actualizar_vista()

    def agregar_tarjeta(self):
        self.flujo.agregar_tarjeta()

    def eliminar_tarjeta(self):
        self.flujo.eliminar_tarjeta()

    def mover_saldo(self):
        self.flujo.mover_saldo()

    def actualizar_vista(self):
        if self.usuario is None or self.controlador is None:
            return
        resumen = self.controlador.obtener_resumen(self.usuario)
        self.panel.actualizar(
            resumen["saldo_billetera"],
            resumen["tarjetas"],
            resumen["transacciones"],
        )
