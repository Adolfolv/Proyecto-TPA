"""Pantalla de registro.."""

import tkinter as tk
from tkinter import filedialog

from .estilizacion import tema
from .estilizacion.constantes_vistas import CATEGORIAS_LICENCIA, MARCAS_MODELOS
from .estilizacion.decoraciones import crear_panel_mensaje
from .estilizacion.widgets import Moldes


PREFIJO_TELEFONO = "+56 9"


class EntradaTelefono:
    def configurar(self, entrada):
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


class FormularioRegistroBase:
    def __init__(self, area_formulario, moldes):
        self.area_formulario = area_formulario
        self.moldes = moldes
        self.telefono = EntradaTelefono()
        self.mostrar_mensaje = None

    def crear_contenido(self, compacto=False):
        self.limpiar()
        contenido = self.moldes.crear_frame(self.area_formulario, tema.PANEL, llenar="both", expandir=True)
        self.mostrar_mensaje = crear_panel_mensaje(contenido, compacto=compacto)
        return contenido

    def limpiar(self):
        for widget in self.area_formulario.winfo_children():
            widget.destroy()

    def crear_bloque(self, padre, titulo, llenar="x", expandir=False):
        bloque = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, tema.BORDE, 1, 14, 14, llenar=llenar, expandir=expandir, margen_x=10, margen_y=8)
        bloque.grid_columnconfigure(0, weight=1)
        bloque.grid_columnconfigure(1, weight=1)
        self.moldes.crear_label(bloque, titulo, tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE).grid(row=0, column=0, columnspan=2, pady=(0, 4))
        return bloque

    def crear_entrada(self, bloque, texto, fila, columna, mostrar="", telefono=False):
        self.moldes.crear_label(bloque, texto, tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=fila, column=columna, sticky="w", padx=5, pady=(6, 0))
        entrada = self.moldes.crear_entrada(bloque, mostrar=mostrar)
        if telefono:
            entrada = self.telefono.configurar(entrada)
        entrada.grid(row=fila + 1, column=columna, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        return entrada

    def crear_subtitulo(self, bloque, texto, fila):
        self.moldes.crear_label(bloque, texto, tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, 780, "center").grid(row=fila, column=0, columnspan=2, sticky="ew", pady=(12, 4))

    def alternar_contrasena(self, entradas, boton):
        mostrar = entradas[0].cget("show") == "*"
        caracter = "" if mostrar else "*"
        texto = "Ocultar contraseña" if mostrar else "Mostrar contraseña"
        for entrada in entradas:
            entrada.configure(show=caracter)
        boton.configure(text=texto)

    def crear_boton_mostrar_contrasena(self, bloque, fila, entradas):
        boton = self.moldes.crear_boton(bloque, "Mostrar contraseña", False, None, None)
        boton.configure(command=lambda: self.alternar_contrasena(entradas, boton))
        boton.grid(row=fila, column=0, sticky="w", padx=5, pady=(0, 4))


class FormularioPasajero(FormularioRegistroBase):
    def crear(self):
        contenido = self.crear_contenido()
        bloque = self.crear_bloque(contenido, "Datos del pasajero")
        self.entrada_nombre = self.crear_entrada(bloque, "Nombre", 2, 0)
        self.entrada_apellido = self.crear_entrada(bloque, "Apellido", 2, 1)
        self.entrada_correo = self.crear_entrada(bloque, "Correo", 4, 0)
        self.entrada_telefono = self.crear_entrada(bloque, "Teléfono", 4, 1, telefono=True)
        self.entrada_edad = self.crear_entrada(bloque, "Edad", 6, 0)
        self.entrada_direccion = self.crear_entrada(bloque, "Dirección", 6, 1)
        self.crear_subtitulo(bloque, "Datos de la cuenta", 8)
        self.entrada_contrasena = self.crear_entrada(bloque, "Contraseña", 9, 0, mostrar="*")
        self.entrada_confirmar = self.crear_entrada(bloque, "Confirmar contraseña", 9, 1, mostrar="*")
        self.crear_boton_mostrar_contrasena(bloque, 11, (self.entrada_contrasena, self.entrada_confirmar))

    def datos(self):
        return {
            "nombre": self.entrada_nombre.get(),
            "apellido": self.entrada_apellido.get(),
            "correo": self.entrada_correo.get(),
            "edad": self.entrada_edad.get(),
            "telefono": self.entrada_telefono.get(),
            "contrasena": self.entrada_contrasena.get(),
            "confirmar_contrasena": self.entrada_confirmar.get(),
            "direccion": self.entrada_direccion.get(),
        }


class FormularioConductor(FormularioRegistroBase):
    def __init__(self, area_formulario, moldes):
        super().__init__(area_formulario, moldes)
        self.ruta_selfie = ""

    def crear(self):
        contenido = self.crear_contenido(compacto=True)
        formularios = self.moldes.crear_frame(contenido, tema.PANEL, llenar="both", expandir=True)
        izquierda = self.moldes.crear_frame(formularios, tema.PANEL, llenar="both", expandir=True, lado="left", margen_x=(0, 6))
        derecha = self.moldes.crear_frame(formularios, tema.PANEL, llenar="both", expandir=True, lado="left", margen_x=(6, 0))
        self.crear_datos_personales(izquierda)
        self.crear_datos_vehiculo(derecha)

    def crear_datos_personales(self, padre):
        bloque = self.crear_bloque(padre, "Datos personales", llenar="both", expandir=True)
        self.entrada_nombre = self.crear_entrada(bloque, "Nombre", 2, 0)
        self.entrada_apellido = self.crear_entrada(bloque, "Apellido", 2, 1)
        self.entrada_correo = self.crear_entrada(bloque, "Correo", 4, 0)
        self.entrada_telefono = self.crear_entrada(bloque, "Teléfono", 4, 1, telefono=True)
        self.entrada_edad = self.crear_entrada(bloque, "Edad", 6, 0)
        self.crear_selfie(bloque)
        self.crear_subtitulo(bloque, "Datos de la cuenta", 11)
        self.entrada_contrasena = self.crear_entrada(bloque, "Contraseña", 12, 0, mostrar="*")
        self.entrada_confirmar = self.crear_entrada(bloque, "Confirmar contraseña", 12, 1, mostrar="*")
        self.crear_boton_mostrar_contrasena(bloque, 14, (self.entrada_contrasena, self.entrada_confirmar))

    def crear_selfie(self, bloque):
        self.moldes.crear_label(bloque, "Selfie", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=8, column=0, columnspan=2, pady=(6, 0))
        self.etiqueta_selfie = self.moldes.crear_label(bloque, "Sin selfie seleccionada", tema.FUENTE_TEXTO, tema.TEXTO_SUAVE, tema.PANEL_SUAVE)
        self.etiqueta_selfie.grid(row=9, column=0, columnspan=2, sticky="ew", padx=5, pady=(2, 3))
        self.moldes.crear_boton(bloque, "Seleccionar selfie", False, None, self.seleccionar_selfie).grid(row=10, column=0, sticky="ew", padx=5, pady=(2, 6))
        self.moldes.crear_boton(bloque, "Quitar selfie", False, None, self.quitar_selfie).grid(row=10, column=1, sticky="ew", padx=5, pady=(2, 6))

    def crear_datos_vehiculo(self, padre):
        bloque = self.crear_bloque(padre, "Datos del vehículo y documentos", llenar="both", expandir=True)
        self.crear_subtitulo(bloque, "Datos del vehículo", 2)
        self.crear_selectores_vehiculo(bloque)
        self.entrada_patente = self.crear_entrada(bloque, "Patente", 5, 0)
        self.entrada_ano = self.crear_entrada(bloque, "Año de creación", 5, 1)
        self.entrada_cantidad_asientos = self.crear_entrada(bloque, "Cantidad de pasajeros", 7, 0)
        self.entrada_peso_equipaje = self.crear_entrada(bloque, "Peso máximo de equipaje", 7, 1)
        self.crear_subtitulo(bloque, "Documentos", 9)
        self.crear_documentos(bloque)

    def crear_selectores_vehiculo(self, bloque):
        self.moldes.crear_label(bloque, "Marca", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=3, column=0, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_label(bloque, "Modelo", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=3, column=1, sticky="w", padx=5, pady=(6, 0))
        self.selector_marca = self.moldes.crear_selector(bloque, tuple(MARCAS_MODELOS))
        self.selector_marca.grid(row=4, column=0, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.selector_modelo = self.moldes.crear_selector(bloque, MARCAS_MODELOS[self.selector_marca.get()])
        self.selector_modelo.grid(row=4, column=1, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.selector_marca.bind("<<ComboboxSelected>>", self.actualizar_modelos)

    def crear_documentos(self, bloque):
        self.moldes.crear_label(bloque, "Categoría", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=10, column=0, sticky="w", padx=5, pady=(6, 0))
        self.moldes.crear_label(bloque, "Número de licencia", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE).grid(row=10, column=1, sticky="w", padx=5, pady=(6, 0))
        self.selector_categoria = self.moldes.crear_selector(bloque, CATEGORIAS_LICENCIA)
        self.selector_categoria.grid(row=11, column=0, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.entrada_licencia = self.moldes.crear_entrada(bloque)
        self.entrada_licencia.grid(row=11, column=1, sticky="ew", padx=5, pady=(5, 6), ipady=7)
        self.crear_entrada(bloque, "Emisión de licencia", 12, 0)
        self.crear_entrada(bloque, "Vencimiento de licencia -> formato(DD-MM-YYYY)", 12, 1)

    def actualizar_modelos(self, evento=None):
        modelos = MARCAS_MODELOS[self.selector_marca.get()]
        self.selector_modelo.configure(values=modelos)
        self.selector_modelo.current(0)

    def seleccionar_selfie(self):
        ruta = filedialog.askopenfilename(title="Seleccionar selfie", filetypes=(("Imágenes", "*.png *.jpg *.jpeg"), ("Todos los archivos", "*.*")))
        if not ruta:
            return
        self.ruta_selfie = ruta
        self.etiqueta_selfie.configure(text="Selfie seleccionada")

    def quitar_selfie(self):
        self.ruta_selfie = ""
        self.etiqueta_selfie.configure(text="Sin selfie seleccionada")

    def datos(self):
        return {
            "nombre": self.entrada_nombre.get(),
            "apellido": self.entrada_apellido.get(),
            "correo": self.entrada_correo.get(),
            "edad": self.entrada_edad.get(),
            "telefono": self.entrada_telefono.get(),
            "contrasena": self.entrada_contrasena.get(),
            "confirmar_contrasena": self.entrada_confirmar.get(),
            "tipo_licencia": self.selector_categoria.get(),
            "licencia_conducir": self.entrada_licencia.get(),
            "selfie": self.ruta_selfie,
            "marca": self.selector_marca.get(),
            "modelo": self.selector_modelo.get(),
            "ano": self.entrada_ano.get(),
            "patente": self.entrada_patente.get(),
            "cantidad_asientos": self.entrada_cantidad_asientos.get(),
            "peso_equipaje": self.entrada_peso_equipaje.get(),
        }


class SelectorTipoRegistro:
    def __init__(self, padre, moldes, mostrar_pasajero, mostrar_conductor):
        self.moldes = moldes
        selector = self.moldes.crear_frame(padre, tema.PANEL, llenar="x", margen_y=(18, 0))
        self.boton_pasajero = self.moldes.crear_boton(selector, "Pasajero", True, None, mostrar_pasajero, llenar="x", expandir=True, lado="left", margen_x=(5, 0))
        self.moldes.crear_frame(selector, tema.TEXTO_SUAVE, llenar="y", lado="left", margen_x=4, ancho_fijo=1)
        self.boton_conductor = self.moldes.crear_boton(selector, "Conductor", False, None, mostrar_conductor, llenar="x", expandir=True, lado="left", margen_x=(0, 5))

    def seleccionar(self, tipo):
        pasajero = tipo == "pasajero"
        self.boton_pasajero.configure(bg=tema.PRIMARIO if pasajero else tema.SECUNDARIO, fg=tema.PRIMARIO_TEXTO if pasajero else tema.TEXTO)
        self.boton_conductor.configure(bg=tema.SECUNDARIO if pasajero else tema.PRIMARIO, fg=tema.TEXTO if pasajero else tema.PRIMARIO_TEXTO)


class FlujoRegistro:
    def __init__(self, vista):
        self.vista = vista

    def registrar(self):
        if self.vista.tipo_registro == "conductor":
            resultado = self.registrar_conductor()
            mensaje_exito = "Conductor registrado correctamente."
        else:
            resultado = self.registrar_pasajero()
            mensaje_exito = "Usuario registrado correctamente."
        self.mostrar_resultado(resultado, mensaje_exito)

    def registrar_pasajero(self):
        datos = self.vista.formulario_actual.datos()
        return self.vista.controlador.registrar_pasajero(**datos)

    def registrar_conductor(self):
        datos = self.vista.formulario_actual.datos()
        return self.vista.controlador.registrar_conductor(**datos)

    def mostrar_resultado(self, resultado, mensaje_exito):
        if not resultado.exitoso:
            self.vista.formulario_actual.mostrar_mensaje(f"Revisa este dato: {resultado.error}")
            return
        self.vista.formulario_actual.mostrar_mensaje(mensaje_exito, True)
        if self.vista.al_registrar is not None:
            self.vista.after(700, lambda: self.vista.al_registrar(resultado.datos))


class VistaRegistro(tk.Frame):
    def __init__(self, padre, navegar, controlador, al_registrar=None):
        self.navegar = navegar
        self.controlador = controlador
        self.al_registrar = al_registrar
        self.moldes = Moldes()
        self.moldes.configurar_selectores(padre)
        self.tipo_registro = "pasajero"
        self.formulario_actual = None
        super().__init__(padre, bg=tema.FONDO)
        self.pack(fill="both", expand=True)
        self.crear_widgets()

    def crear_widgets(self):
        contenedor = self.moldes.crear_frame(self, tema.PANEL, tema.BORDE, 1, 18, 18, llenar="both", expandir=True, margen_x=24, margen_y=24)
        self.crear_cabecera(contenedor)
        self.selector_tipo = SelectorTipoRegistro(contenedor, self.moldes, self.mostrar_pasajero, self.mostrar_conductor)
        barra_acciones = self.moldes.crear_frame(contenedor, tema.PANEL, llenar="x", lado="bottom", margen_y=(12, 0))
        self.moldes.crear_boton(barra_acciones, "Registrarse", True, 16, self.registrar, lado="right")
        self.area_formulario = self.moldes.crear_frame(contenedor, tema.PANEL, llenar="both", expandir=True, margen_y=(12, 0))
        self.flujo = FlujoRegistro(self)
        self.mostrar_pasajero()

    def crear_cabecera(self, contenedor):
        cabecera = self.moldes.crear_frame(contenedor, tema.PANEL, llenar="x")
        self.moldes.crear_label(cabecera, "Registro", tema.FUENTE_TITULO, tema.TEXTO, tema.PANEL, lado="left")
        self.moldes.crear_boton(cabecera, "Volver", False, None, lambda: self.navegar("pantalla_inicial"), lado="right")

    def mostrar_pasajero(self):
        self.tipo_registro = "pasajero"
        self.selector_tipo.seleccionar("pasajero")
        self.formulario_actual = FormularioPasajero(self.area_formulario, self.moldes)
        self.formulario_actual.crear()

    def mostrar_conductor(self):
        self.tipo_registro = "conductor"
        self.selector_tipo.seleccionar("conductor")
        self.formulario_actual = FormularioConductor(self.area_formulario, self.moldes)
        self.formulario_actual.crear()

    def registrar(self):
        self.flujo.registrar()
