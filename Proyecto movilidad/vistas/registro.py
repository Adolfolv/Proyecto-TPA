"""Pantalla de registro visual sin navegacion real."""

import tkinter as tk

from .estilizacion import tema
from .estilizacion.constantes_vistas import CATEGORIAS_LICENCIA, MARCAS_MODELOS
from .estilizacion.widgets import Moldes


PREFIJO_TELEFONO = "+56 9"


class VistaRegistro(tk.Frame):
    def __init__(self, master, navegar):
        self.navegar = navegar
        self.moldes = Moldes()
        self.moldes.configurar_selectores(master)
        self.boton_pasajero = None
        self.boton_conductor = None
        self.area_formulario = None

        super().__init__(master, bg=tema.FONDO)
        self.pack(fill="both", expand=True)
        self.crear_widgets()

    #activa mostrar pasajero
    def crear_widgets(self):
        contenedor = self.moldes.crear_frame(self, tema.PANEL, tema.BORDE, 1, 18, 18, llenar="both", expandir=True, margen_x=24, margen_y=24)
        cabecera = self.moldes.crear_frame(contenedor, tema.PANEL, llenar="x")
        self.moldes.crear_label(cabecera, "Registro", tema.FUENTE_TITULO, tema.TEXTO, tema.PANEL, lado="left")
        self.moldes.crear_boton(cabecera, "Volver", False, None, lambda: self.navegar("pantalla_inicial"), lado="right")

        selector = self.moldes.crear_frame(contenedor, tema.PANEL, llenar="x", margen_y=(18, 0))
        self.boton_pasajero = self.moldes.crear_boton(selector, "Pasajero", True, None, self.mostrar_pasajero, llenar="x", expandir=True, lado="left", margen_x=(5, 0))
        self.moldes.crear_frame(selector, tema.TEXTO_SUAVE, llenar="y", lado="left", margen_x=4, ancho_fijo=1)
        self.boton_conductor = self.moldes.crear_boton(selector, "Conductor", False, None, self.mostrar_conductor, llenar="x", expandir=True, lado="left", margen_x=(0, 5))

        self.area_formulario = self.moldes.crear_frame(contenedor, tema.PANEL, llenar="both", expandir=True, margen_y=(12, 0))
        self.moldes.crear_boton(contenedor, "Registrarse", True, 16, lambda: self.navegar("menu"), margen_x=5, margen_y=(14, 0))

        self.mostrar_pasajero()

    def limpiar_formulario(self):
        for widget in self.area_formulario.winfo_children():
            widget.destroy()

    def configurar_entrada_telefono(self, entrada):
        entrada.insert(0, PREFIJO_TELEFONO)

        def mantener_prefijo(evento=None):
            texto = entrada.get()
            if not texto.startswith(PREFIJO_TELEFONO):
                if PREFIJO_TELEFONO.startswith(texto):
                    texto = ""
                else:
                    for cantidad in range(len(PREFIJO_TELEFONO), 0, -1):
                        if texto.startswith(PREFIJO_TELEFONO[:cantidad]):
                            texto = texto[cantidad:]
                            break
                entrada.delete(0, tk.END)
                entrada.insert(0, PREFIJO_TELEFONO + texto)

            if entrada.index(tk.INSERT) < len(PREFIJO_TELEFONO):
                entrada.icursor(len(PREFIJO_TELEFONO))

        def bloquear_borrado_prefijo(evento):
            posicion = entrada.index(tk.INSERT)
            if evento.keysym == "BackSpace" and posicion <= len(PREFIJO_TELEFONO):
                entrada.icursor(len(PREFIJO_TELEFONO))
                return "break"
            if evento.keysym == "Delete" and posicion < len(PREFIJO_TELEFONO):
                entrada.icursor(len(PREFIJO_TELEFONO))
                return "break"
            return None

        entrada.bind("<KeyPress>", bloquear_borrado_prefijo)
        entrada.bind("<KeyRelease>", mantener_prefijo)
        entrada.bind("<ButtonRelease-1>", mantener_prefijo)
        entrada.bind("<FocusIn>", mantener_prefijo)
        return entrada

    #activa crear formulario pasajero y cambia el color
    def mostrar_pasajero(self):
        self.boton_pasajero.configure(bg=tema.PRIMARIO, fg=tema.PRIMARIO_TEXTO)
        self.boton_conductor.configure(bg=tema.SECUNDARIO, fg=tema.TEXTO)
        self.crear_formulario_pasajero()

    def mostrar_conductor(self):
        self.boton_pasajero.configure(bg=tema.SECUNDARIO, fg=tema.TEXTO)
        self.boton_conductor.configure(bg=tema.PRIMARIO, fg=tema.PRIMARIO_TEXTO)
        self.crear_formulario_conductor()

    def crear_formulario_pasajero(self):
        self.limpiar_formulario()
        contenido = self.moldes.crear_frame(self.area_formulario, tema.PANEL, llenar="both", expandir=True)
        bloque = self.moldes.crear_frame(contenido, tema.PANEL_SUAVE, tema.BORDE, 1, 14, 14, llenar="x", margen_x=10, margen_y=8)
        bloque.grid_columnconfigure(0, weight=1)
        bloque.grid_columnconfigure(1, weight=1)
        self.moldes.crear_label(bloque, "Datos del pasajero", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE).grid(row=0, column=0, columnspan=2, pady=(0, 4))
        self.moldes.crear_label(bloque, "Nombre", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=2, column=0, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_label(bloque, "Apellido", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=2, column=1, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_entrada(bloque).grid(row=3, column=0, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_entrada(bloque).grid(row=3, column=1, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_label(bloque, "Correo", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=4, column=0, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_label(bloque, "Telefono", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=4, column=1, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_entrada(bloque).grid(row=5, column=0, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        entrada_telefono = self.configurar_entrada_telefono(self.moldes.crear_entrada(bloque))
        entrada_telefono.grid(row=5, column=1, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_label(bloque, "Datos de la cuenta", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, 780, "center").grid(row=6, column=0, columnspan=2, sticky="ew", pady=(12, 4))
        self.moldes.crear_label(bloque, "Contrasena", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=7, column=0, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_label(bloque, "Confirmar contrasena", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=7, column=1, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_entrada(bloque, mostrar="*").grid(row=8, column=0, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_entrada(bloque, mostrar="*").grid(row=8, column=1, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_boton(bloque, "Mostrar contrasena", False, None, None).grid(row=9, column=0, sticky="w", padx=5, pady=(0, 4))

        # --- DECORACIONES PASAJERO ---
        #lucete jorge deidad

    def crear_formulario_conductor(self):
        self.limpiar_formulario()
        contenido = self.moldes.crear_frame(self.area_formulario, tema.PANEL, llenar="both", expandir=True)
        izquierda = self.moldes.crear_frame(contenido, tema.PANEL, llenar="both", expandir=True, lado="left", margen_x=(0, 6))
        derecha = self.moldes.crear_frame(contenido, tema.PANEL, llenar="both", expandir=True, lado="left", margen_x=(6, 0))

        bloque_personal = self.moldes.crear_frame(izquierda, tema.PANEL_SUAVE, tema.BORDE, 1, 14, 14, llenar="both", expandir=True, margen_x=10, margen_y=8)
        bloque_personal.grid_columnconfigure(0, weight=1)
        bloque_personal.grid_columnconfigure(1, weight=1)
        self.moldes.crear_label(bloque_personal, "Datos personales", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE).grid(row=0, column=0, columnspan=2, pady=(0, 4))
        self.moldes.crear_label(bloque_personal, "Nombre", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=2, column=0, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_label(bloque_personal, "Apellido", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=2, column=1, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_entrada(bloque_personal).grid(row=3, column=0, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_entrada(bloque_personal).grid(row=3, column=1, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_label(bloque_personal, "Correo", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=4, column=0, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_label(bloque_personal, "Telefono", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=4, column=1, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_entrada(bloque_personal).grid(row=5, column=0, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        entrada_telefono = self.configurar_entrada_telefono(self.moldes.crear_entrada(bloque_personal))
        entrada_telefono.grid(row=5, column=1, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_label(bloque_personal, "Selfie", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=6, column=0, columnspan=2, pady=(6, 0))
        self.moldes.crear_boton(bloque_personal, "Seleccionar selfie", False, None, None).grid(row=7, column=0, columnspan=2, sticky="ew", padx=5, pady=(5, 4))
        self.moldes.crear_boton(bloque_personal, "Quitar selfie", False, None, None).grid(row=8, column=0, columnspan=2, sticky="ew", padx=5, pady=(0, 6))
        self.moldes.crear_label(bloque_personal, "Datos de la cuenta", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, 780, "center").grid(row=9, column=0, columnspan=2, sticky="ew", pady=(12, 4))
        self.moldes.crear_label(bloque_personal, "Contrasena", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=10, column=0, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_label(bloque_personal, "Confirmar contrasena", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=10, column=1, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_entrada(bloque_personal, mostrar="*").grid(row=11, column=0, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_entrada(bloque_personal, mostrar="*").grid(row=11, column=1, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_boton(bloque_personal, "Mostrar contrasena", False, None, None).grid(row=12, column=0, sticky="w", padx=5, pady=(0, 4))

        bloque_derecho = self.moldes.crear_frame(derecha, tema.PANEL_SUAVE, tema.BORDE, 1, 14, 14, llenar="both", expandir=True, margen_x=10, margen_y=8)
        bloque_derecho.grid_columnconfigure(0, weight=1)
        bloque_derecho.grid_columnconfigure(1, weight=1)
        self.moldes.crear_label(bloque_derecho, "Datos del vehiculo y documentos", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE).grid(row=0, column=0, columnspan=2, pady=(0, 4))
        self.moldes.crear_label(bloque_derecho, "Datos del vehiculo", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, 780, "center").grid(row=2, column=0, columnspan=2, sticky="ew", pady=(12, 4))
        self.moldes.crear_label(bloque_derecho, "Marca", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=3, column=0, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_label(bloque_derecho, "Modelo", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=3, column=1, sticky="w", padx=5, pady=(6, 0))
        selector_marca = self.moldes.crear_selector(bloque_derecho, tuple(MARCAS_MODELOS))
        selector_marca.grid(row=4, column=0, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        selector_modelo = self.moldes.crear_selector(bloque_derecho, MARCAS_MODELOS[selector_marca.get()])
        selector_modelo.grid(row=4, column=1, sticky="ew", padx=5, pady=(5, 6), ipady=7)

        def actualizar_modelos(evento=None):
            modelos = MARCAS_MODELOS[selector_marca.get()]
            selector_modelo.configure(values=modelos)
            selector_modelo.current(0)

        selector_marca.bind("<<ComboboxSelected>>", actualizar_modelos)
        self.moldes.crear_label(bloque_derecho, "Patente", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=5, column=0, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_label(bloque_derecho, "Ano de creacion", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=5, column=1, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_entrada(bloque_derecho).grid(row=6, column=0, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_entrada(bloque_derecho).grid(row=6, column=1, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_label(bloque_derecho, "Cantidad de pasajeros", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=7, column=0, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_label(bloque_derecho, "Peso maximo de equipaje", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=7, column=1, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_entrada(bloque_derecho).grid(row=8, column=0, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_entrada(bloque_derecho).grid(row=8, column=1, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_label(bloque_derecho, "Documentos", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, 780, "center").grid(row=9, column=0, columnspan=2, sticky="ew", pady=(12, 4))
        self.moldes.crear_label(bloque_derecho, "Categoria", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=10, column=0, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_label(bloque_derecho, "Número de licencia", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=10, column=1, sticky="w", padx=5, pady=(6, 0))
        selector_categoria = self.moldes.crear_selector(bloque_derecho, CATEGORIAS_LICENCIA)
        selector_categoria.grid(row=11, column=0, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_entrada(bloque_derecho).grid(row=11, column=1, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_label(bloque_derecho, "Emisión de licencia", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=12, column=0, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_label(bloque_derecho, "Vencimiento de licencia -> formato(DD-MM-YYYY)", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=12, column=1, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_entrada(bloque_derecho).grid(row=13, column=0, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_entrada(bloque_derecho).grid(row=13, column=1, sticky="ew", padx=5, pady=(5, 6), ipady=7)
