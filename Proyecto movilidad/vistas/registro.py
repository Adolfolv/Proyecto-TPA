"""Pantalla de registro."""

import tkinter as tk
from tkinter import filedialog

from .estilizacion import tema
from .estilizacion.constantes_vistas import CATEGORIAS_LICENCIA, MARCAS_MODELOS
from .estilizacion.decoraciones import crear_panel_mensaje_registro
from .estilizacion.widgets import Moldes


PREFIJO_TELEFONO = "+56 9"


class VistaRegistro(tk.Frame):
    def __init__(self, master, navegar, controlador, al_registrar=None):
        self.navegar = navegar
        self.controlador = controlador
        self.al_registrar = al_registrar
        self.moldes = Moldes()
        self.moldes.configurar_selectores(master)
        self.boton_pasajero = None
        self.boton_conductor = None
        self.area_formulario = None
        self.mostrar_mensaje_registro = None
        self.ruta_selfie = ""
        self.tipo_registro = "pasajero"

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

        barra_acciones = self.moldes.crear_frame(contenedor, tema.PANEL, llenar="x", lado="bottom", margen_y=(12, 0))
        self.moldes.crear_boton(barra_acciones,"Registrarse",True,16,self.registrar,lado="right",)
        self.area_formulario = self.moldes.crear_frame(contenedor, tema.PANEL, llenar="both", expandir=True, margen_y=(12, 0))

        self.mostrar_pasajero()

    def limpiar_formulario(self):
        for widget in self.area_formulario.winfo_children():
            widget.destroy()
        self.mostrar_mensaje_registro = None
        self.ruta_selfie = ""

    def alternar_contrasena(self, entradas, boton):
        mostrar = entradas[0].cget("show") == "*"
        caracter = "" if mostrar else "*"
        texto = "Ocultar contrasena" if mostrar else "Mostrar contrasena"

        for entrada in entradas:
            entrada.configure(show=caracter)
        boton.configure(text=texto)

    def seleccionar_selfie(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar selfie",
            filetypes=(
                ("Imagenes", "*.png *.jpg *.jpeg"),
                ("Todos los archivos", "*.*"),
            ),
        )

        if not ruta:
            return

        self.ruta_selfie = ruta
        self.etiqueta_selfie.configure(text="Selfie seleccionada")

    def quitar_selfie(self):
        self.ruta_selfie = ""
        self.etiqueta_selfie.configure(text="Sin selfie seleccionada")

    def configurar_entrada_telefono(self, entrada):
        entrada.insert(0, PREFIJO_TELEFONO)

        def proteger_prefijo(evento=None):
            if not entrada.get().startswith(PREFIJO_TELEFONO):
                entrada.delete(0, tk.END)
                entrada.insert(0, PREFIJO_TELEFONO)

            if entrada.index(tk.INSERT) < len(PREFIJO_TELEFONO):
                entrada.icursor(len(PREFIJO_TELEFONO))

        def bloquear_prefijo(evento):
            posicion = entrada.index(tk.INSERT)
            if evento.keysym in ("BackSpace", "Delete") and posicion <= len(PREFIJO_TELEFONO):
                return "break"
            return None

        entrada.bind("<KeyPress>", bloquear_prefijo)
        entrada.bind("<KeyRelease>", proteger_prefijo)
        entrada.bind("<FocusIn>", proteger_prefijo)
        return entrada

    #activa crear formulario pasajero y cambia el color
    def mostrar_pasajero(self):
        self.tipo_registro = "pasajero"
        self.boton_pasajero.configure(bg=tema.PRIMARIO, fg=tema.PRIMARIO_TEXTO)
        self.boton_conductor.configure(bg=tema.SECUNDARIO, fg=tema.TEXTO)
        self.crear_formulario_pasajero()

    def mostrar_conductor(self):
        self.tipo_registro = "conductor"
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
        self.entrada_nombre = self.moldes.crear_entrada(bloque)
        self.entrada_nombre.grid(row=3, column=0, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.entrada_apellido = self.moldes.crear_entrada(bloque)
        self.entrada_apellido.grid(row=3, column=1, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_label(bloque, "Correo", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=4, column=0, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_label(bloque, "Telefono", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=4, column=1, sticky="w", padx=5, pady=(6, 0))
        self.entrada_correo = self.moldes.crear_entrada(bloque)
        self.entrada_correo.grid(row=5, column=0, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.entrada_telefono = self.configurar_entrada_telefono(self.moldes.crear_entrada(bloque))
        self.entrada_telefono.grid(row=5, column=1, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_label(bloque, "Edad", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=6, column=0, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_label(bloque, "Direccion", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=6, column=1, sticky="w", padx=5, pady=(6, 0))
        self.entrada_edad = self.moldes.crear_entrada(bloque)
        self.entrada_edad.grid(row=7, column=0, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.entrada_direccion = self.moldes.crear_entrada(bloque)
        self.entrada_direccion.grid(row=7, column=1, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_label(bloque, "Datos de la cuenta", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, 780, "center").grid(row=8, column=0, columnspan=2, sticky="ew", pady=(12, 4))
        self.moldes.crear_label(bloque, "Contrasena", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=9, column=0, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_label(bloque, "Confirmar contrasena", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=9, column=1, sticky="w", padx=5, pady=(6, 0))
        self.entrada_contrasena = self.moldes.crear_entrada(bloque, mostrar="*")
        self.entrada_contrasena.grid(row=10, column=0, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.entrada_confirmar = self.moldes.crear_entrada(bloque, mostrar="*")
        self.entrada_confirmar.grid(row=10, column=1, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        boton_mostrar = self.moldes.crear_boton(bloque, "Mostrar contrasena", False, None, None)
        boton_mostrar.configure(
            command=lambda: self.alternar_contrasena(
                (self.entrada_contrasena, self.entrada_confirmar),
                boton_mostrar,
            )
        )
        boton_mostrar.grid(row=11, column=0, sticky="w", padx=5, pady=(0, 4))
        self.mostrar_mensaje_registro = crear_panel_mensaje_registro(contenido)

        # --- DECORACIONES PASAJERO ---
        #lucete jorge deidad

    def crear_formulario_conductor(self):
        self.limpiar_formulario()
        contenido = self.moldes.crear_frame(self.area_formulario, tema.PANEL, llenar="both", expandir=True)
        formularios = self.moldes.crear_frame(contenido, tema.PANEL, llenar="both", expandir=True)
        izquierda = self.moldes.crear_frame(formularios, tema.PANEL, llenar="both", expandir=True, lado="left", margen_x=(0, 6))
        derecha = self.moldes.crear_frame(formularios, tema.PANEL, llenar="both", expandir=True, lado="left", margen_x=(6, 0))

        bloque_personal = self.moldes.crear_frame(izquierda, tema.PANEL_SUAVE, tema.BORDE, 1, 14, 14, llenar="both", expandir=True, margen_x=10, margen_y=8)
        bloque_personal.grid_columnconfigure(0, weight=1)
        bloque_personal.grid_columnconfigure(1, weight=1)
        self.moldes.crear_label(bloque_personal, "Datos personales", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE).grid(row=0, column=0, columnspan=2, pady=(0, 4))
        self.moldes.crear_label(bloque_personal, "Nombre", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=2, column=0, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_label(bloque_personal, "Apellido", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=2, column=1, sticky="w", padx=5, pady=(6, 0))
        self.entrada_conductor_nombre = self.moldes.crear_entrada(bloque_personal)
        self.entrada_conductor_nombre.grid(row=3, column=0, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.entrada_conductor_apellido = self.moldes.crear_entrada(bloque_personal)
        self.entrada_conductor_apellido.grid(row=3, column=1, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_label(bloque_personal, "Correo", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=4, column=0, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_label(bloque_personal, "Telefono", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=4, column=1, sticky="w", padx=5, pady=(6, 0))
        self.entrada_conductor_correo = self.moldes.crear_entrada(bloque_personal)
        self.entrada_conductor_correo.grid(row=5, column=0, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.entrada_conductor_telefono = self.configurar_entrada_telefono(self.moldes.crear_entrada(bloque_personal))
        self.entrada_conductor_telefono.grid(row=5, column=1, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_label(bloque_personal, "Edad", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=6, column=0, sticky="w", padx=5, pady=(6, 0))
        self.entrada_conductor_edad = self.moldes.crear_entrada(bloque_personal)
        self.entrada_conductor_edad.grid(row=7, column=0, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_label(bloque_personal, "Selfie", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=8, column=0, columnspan=2, pady=(6, 0))
        self.etiqueta_selfie = self.moldes.crear_label(
            bloque_personal,
            "Sin selfie seleccionada",
            tema.FUENTE_TEXTO,
            tema.TEXTO_SUAVE,
            tema.PANEL_SUAVE,
        )
        self.etiqueta_selfie.grid(row=9, column=0, columnspan=2, sticky="ew", padx=5, pady=(2, 3))
        self.moldes.crear_boton(bloque_personal, "Seleccionar selfie", False, None, self.seleccionar_selfie).grid(row=10, column=0, sticky="ew", padx=5, pady=(2, 6))
        self.moldes.crear_boton(bloque_personal, "Quitar selfie", False, None, self.quitar_selfie).grid(row=10, column=1, sticky="ew", padx=5, pady=(2, 6))
        self.moldes.crear_label(bloque_personal, "Datos de la cuenta", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, 780, "center").grid(row=11, column=0, columnspan=2, sticky="ew", pady=(12, 4))
        self.moldes.crear_label(bloque_personal, "Contrasena", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=12, column=0, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_label(bloque_personal, "Confirmar contrasena", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=12, column=1, sticky="w", padx=5, pady=(6, 0))
        self.entrada_conductor_contrasena = self.moldes.crear_entrada(bloque_personal, mostrar="*")
        self.entrada_conductor_contrasena.grid(row=13, column=0, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.entrada_conductor_confirmar = self.moldes.crear_entrada(bloque_personal, mostrar="*")
        self.entrada_conductor_confirmar.grid(row=13, column=1, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        boton_mostrar = self.moldes.crear_boton(bloque_personal, "Mostrar contrasena", False, None, None)
        boton_mostrar.configure(command=lambda: self.alternar_contrasena((self.entrada_conductor_contrasena, self.entrada_conductor_confirmar),boton_mostrar,))
        boton_mostrar.grid(row=14, column=0, sticky="w", padx=5, pady=(0, 4))

        bloque_derecho = self.moldes.crear_frame(derecha, tema.PANEL_SUAVE, tema.BORDE, 1, 14, 14, llenar="both", expandir=True, margen_x=10, margen_y=8)
        bloque_derecho.grid_columnconfigure(0, weight=1)
        bloque_derecho.grid_columnconfigure(1, weight=1)
        self.moldes.crear_label(bloque_derecho, "Datos del vehiculo y documentos", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE).grid(row=0, column=0, columnspan=2, pady=(0, 4))
        self.moldes.crear_label(bloque_derecho, "Datos del vehiculo", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, 780, "center").grid(row=2, column=0, columnspan=2, sticky="ew", pady=(12, 4))
        self.moldes.crear_label(bloque_derecho, "Marca", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=3, column=0, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_label(bloque_derecho, "Modelo", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=3, column=1, sticky="w", padx=5, pady=(6, 0))
        self.selector_marca = self.moldes.crear_selector(bloque_derecho, tuple(MARCAS_MODELOS))
        self.selector_marca.grid(row=4, column=0, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.selector_modelo = self.moldes.crear_selector(bloque_derecho, MARCAS_MODELOS[self.selector_marca.get()])
        self.selector_modelo.grid(row=4, column=1, sticky="ew", padx=5, pady=(5, 6), ipady=7)

        def actualizar_modelos(evento=None):
            modelos = MARCAS_MODELOS[self.selector_marca.get()]
            self.selector_modelo.configure(values=modelos)
            self.selector_modelo.current(0)

        self.selector_marca.bind("<<ComboboxSelected>>", actualizar_modelos)
        self.moldes.crear_label(bloque_derecho, "Patente", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=5, column=0, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_label(bloque_derecho, "Ano de creacion", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=5, column=1, sticky="w", padx=5, pady=(6, 0))
        self.entrada_patente = self.moldes.crear_entrada(bloque_derecho)
        self.entrada_patente.grid(row=6, column=0, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.entrada_ano = self.moldes.crear_entrada(bloque_derecho)
        self.entrada_ano.grid(row=6, column=1, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_label(bloque_derecho, "Cantidad de pasajeros", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=7, column=0, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_label(bloque_derecho, "Peso maximo de equipaje", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=7, column=1, sticky="w", padx=5, pady=(6, 0))
        self.entrada_cantidad_asientos = self.moldes.crear_entrada(bloque_derecho)
        self.entrada_cantidad_asientos.grid(row=8, column=0, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.entrada_peso_equipaje = self.moldes.crear_entrada(bloque_derecho)
        self.entrada_peso_equipaje.grid(row=8, column=1, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_label(bloque_derecho, "Documentos", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, 780, "center").grid(row=9, column=0, columnspan=2, sticky="ew", pady=(12, 4))
        self.moldes.crear_label(bloque_derecho, "Categoria", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=10, column=0, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_label(bloque_derecho, "Número de licencia", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=10, column=1, sticky="w", padx=5, pady=(6, 0))
        self.selector_categoria = self.moldes.crear_selector(bloque_derecho, CATEGORIAS_LICENCIA)
        self.selector_categoria.grid(row=11, column=0, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.entrada_licencia = self.moldes.crear_entrada(bloque_derecho)
        self.entrada_licencia.grid(row=11, column=1, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_label(bloque_derecho, "Emisión de licencia", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=12, column=0, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_label(bloque_derecho, "Vencimiento de licencia -> formato(DD-MM-YYYY)", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=12, column=1, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_entrada(bloque_derecho).grid(row=13, column=0, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.moldes.crear_entrada(bloque_derecho).grid(row=13, column=1, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.mostrar_mensaje_registro = crear_panel_mensaje_registro(contenido, compacto=True)


#---Apartado de logica---#


#si en el apartado superior se relleno el formulario de pasajero, al apretar 
#el boton registrar se ejecuta el metodo registrar_pasajero, si se relleno 
#el formulario de conductor se ejecuta el metodo registrar_conductor
    def registrar(self):
        if self.tipo_registro == "conductor":
            self.registrar_conductor()
        else:
            self.registrar_pasajero()

    def registrar_pasajero(self):
        resultado = self.controlador.registrar_pasajero(
                self.entrada_nombre.get(),
                self.entrada_apellido.get(),
                self.entrada_correo.get(),
                self.entrada_edad.get(),
                self.entrada_telefono.get(),
                self.entrada_contrasena.get(),
                self.entrada_confirmar.get(),
                self.entrada_direccion.get(),
            )
        if not resultado.exitoso:
            self.mostrar_mensaje_registro(f"Revisa este dato: {resultado.error}")
            return

        self.mostrar_mensaje_registro("Usuario registrado correctamente.", True)
        if self.al_registrar is not None:
            self.after(700, lambda: self.al_registrar(resultado.usuario))

    def registrar_conductor(self):
        resultado = self.controlador.registrar_conductor(
                self.entrada_conductor_nombre.get(),
                self.entrada_conductor_apellido.get(),
                self.entrada_conductor_correo.get(),
                self.entrada_conductor_edad.get(),
                self.entrada_conductor_telefono.get(),
                self.entrada_conductor_contrasena.get(),
                self.entrada_conductor_confirmar.get(),
                self.selector_categoria.get(),
                self.entrada_licencia.get(),
                self.ruta_selfie,
                self.selector_marca.get(),
                self.selector_modelo.get(),
                self.entrada_ano.get(),
                self.entrada_patente.get(),
                self.entrada_cantidad_asientos.get(),
                self.entrada_peso_equipaje.get(),
            )
        if not resultado.exitoso:
            self.mostrar_mensaje_registro(f"Revisa este dato: {resultado.error}")
            return

        self.mostrar_mensaje_registro("Conductor registrado correctamente.", True)
        if self.al_registrar is not None:
            self.after(700, lambda: self.al_registrar(resultado.usuario))
