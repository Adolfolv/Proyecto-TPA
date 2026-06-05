"""Pantalla de menu principal visual sin navegacion real.."""

import tkinter as tk

from .estilizacion import tema
from .estilizacion.decoraciones import crear_decoracion_menu_viaje
from .estilizacion.widgets import Moldes


class VistaMenu(tk.Frame):
    def __init__(self, padre, navegar):
        self.navegar = navegar
        self.moldes = Moldes()

        super().__init__(padre, bg=tema.FONDO)
        self.pack(fill="both", expand=True)
        self.crear_widgets()

    def crear_widgets(self):
        panel = self.moldes.crear_frame(self, tema.PANEL, tema.BORDE, 1, 22, 22, llenar="both", expandir=True, margen_x=24, margen_y=24, columnas_peso=((0, 1),), filas_peso=((1, 1),))

        cabecera = self.moldes.crear_frame(panel, tema.PANEL, fila=0, columna=0, sticky="ew", margen_y=(0, 16), columnas_peso=((0, 1), (1, 2), (2, 1)))

        self.moldes.crear_boton(cabecera, "Perfil", False, None, None, metodo="grid", fila=0, columna=0, sticky="w")
        textos = self.moldes.crear_frame(cabecera, tema.PANEL, fila=0, columna=1, sticky="")
        self.moldes.crear_label(textos, "Menu principal", tema.FUENTE_TITULO, tema.TEXTO, tema.PANEL).pack()
        self.moldes.crear_boton(cabecera, "Cerrar sesion", False, None, lambda: self.navegar("pantalla_inicial"), metodo="grid", fila=0, columna=2, sticky="e")

        contenido = self.moldes.crear_frame(panel, tema.PANEL, fila=1, columna=0, columnas_peso=((0, 1), (1, 2), (2, 1)), filas_peso=((0, 1),))
        contenido.grid_columnconfigure(0, uniform="menu")
        contenido.grid_columnconfigure(1, uniform="menu")
        contenido.grid_columnconfigure(2, uniform="menu")

        izquierda = self.moldes.crear_frame(contenido, tema.PANEL, fila=0, columna=0, margen_x=(0, 16), columnas_peso=((0, 1),), filas_peso=((0, 1), (1, 1)))

        self.moldes.crear_tarjeta_acceso_menu(izquierda, "Servicios", "Gestiona solicitudes y opciones disponibles.", metodo="grid", fila=0, columna=0, sticky="nsew", margen_y=(0, 8))
        self.moldes.crear_tarjeta_acceso_menu(izquierda, "Billetera", "Revisa saldo, pagos y movimientos recientes.", comando=lambda: self.navegar("billetera"), metodo="grid", fila=1, columna=0, sticky="nsew", margen_y=(8, 0))

        centro = self.moldes.crear_frame(contenido, tema.PANEL, fila=0, columna=1, columnas_peso=((0, 1),), filas_peso=((0, 1),))
        crear_decoracion_menu_viaje(centro, comando=lambda: self.navegar("viaje"), metodo="grid", row=0, column=0, sticky="nsew")

        derecha = self.moldes.crear_frame(contenido, tema.PANEL, fila=0, columna=2, margen_x=(16, 0), columnas_peso=((0, 1),), filas_peso=((0, 1), (1, 1)))

        self.moldes.crear_tarjeta_acceso_menu(derecha, "Historial", "Consulta viajes realizados y actividad anterior.", metodo="grid", fila=0, columna=0, sticky="nsew", margen_y=(0, 8))
        self.moldes.crear_tarjeta_acceso_menu(derecha, "Tarjeta social", "Accede a beneficios, perfil publico y comunidad.", metodo="grid", fila=1, columna=0, sticky="nsew", margen_y=(8, 0))

        pie = self.moldes.crear_frame(panel, tema.PANEL, fila=2, columna=0, sticky="ew", margen_y=(16, 0), columnas_peso=((0, 1),))
        acciones = self.moldes.crear_frame(pie, tema.PANEL, fila=0, columna=0, sticky="")
        self.moldes.crear_boton(acciones, "Ayuda", False, None, None, lado="left", margen_x=5)
        self.moldes.crear_boton(acciones, "Cambiar modo", False, None, None, lado="left", margen_x=5)
        self.moldes.crear_label(pie, "Selecciona una opcion para continuar.", tema.FUENTE_TEXTO, tema.TEXTO_SUAVE, tema.PANEL, 900, "center", metodo="grid", fila=1, columna=0, margen_y=(10, 0))
