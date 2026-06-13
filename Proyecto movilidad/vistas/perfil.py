"""Pantalla de perfil separada por responsabilidades."""

import tkinter as tk
from tkinter import messagebox

from .estilizacion import tema
from .estilizacion.decoraciones import crear_panel_mensaje_registro
from .estilizacion.widgets import Moldes


class CabeceraPerfil:
    def __init__(self, panel):
        self.panel = panel
        self.moldes = panel.moldes
        self.acciones = panel.acciones

    def crear(self):
        cabecera = self.moldes.crear_frame(self.panel.panel_principal, tema.PANEL, fila=0, columna=0, sticky="ew", margen_y=(0, 18), columnas_peso=((0, 1),))
        self.moldes.crear_label(cabecera, "Perfil", tema.FUENTE_TITULO, tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")
        self.moldes.crear_boton(cabecera, "Volver", False, None, self.acciones["volver_menu"], metodo="grid", fila=0, columna=1, sticky="e")


class FormularioPerfil:
    CAMPOS = (
        ("Nombre", "nombre", True),
        ("Apellido", "apellido", True),
        ("Correo", "correo", True),
        ("Telefono", "telefono", True),
        ("Tipo de usuario", "tipo_usuario", False),
    )

    def __init__(self, panel):
        self.panel = panel
        self.moldes = panel.moldes
        self.campos = {}

    def crear(self, padre):
        self.moldes.crear_label(padre, "\U0001F464", ("Arial", 82, "bold"), tema.PRIMARIO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, sticky="", margen_y=(0, 6))
        self.moldes.crear_label(padre, "Perfil", ("Arial", 28, "bold"), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=1, columna=0, sticky="", margen_y=(0, 18))
        for indice, (titulo, clave, editable) in enumerate(self.CAMPOS):
            self.crear_dato(padre, titulo, self.panel.datos.get(clave, ""), indice + 2, clave, editable)
        self.moldes.crear_boton(padre, "Actualizar informacion", True, None, self.panel.acciones["actualizar"], metodo="grid", fila=14, columna=0, sticky="ew", margen_y=(20, 8))

    def crear_dato(self, padre, titulo, valor, fila, clave, editable=True):
        self.moldes.crear_label(padre, titulo, ("Arial", 13, "bold"), tema.TEXTO_SUAVE, tema.PANEL_SUAVE, metodo="grid", fila=fila * 2, columna=0, sticky="", margen_y=(0 if fila == 2 else 12, 4))
        entrada = tk.Entry(padre, font=("Arial", 16, "bold"), bg=tema.SECUNDARIO, fg=tema.TEXTO, insertbackground=tema.TEXTO, relief="flat", bd=0, justify="center", width=32)
        entrada.insert(0, valor)
        if not editable:
            entrada.configure(state="readonly", readonlybackground=tema.SECUNDARIO)
        entrada.grid(row=fila * 2 + 1, column=0, sticky="ew", ipady=6)
        self.campos[clave] = entrada

    def datos_formulario(self):
        return {
            "nombre": self.campos["nombre"].get(),
            "apellido": self.campos["apellido"].get(),
            "correo": self.campos["correo"].get(),
            "telefono": self.campos["telefono"].get(),
        }

    def actualizar(self, datos):
        for clave, valor in datos.items():
            campo = self.campos.get(clave)
            if campo is None:
                continue
            estado = campo.cget("state")
            campo.configure(state="normal")
            campo.delete(0, tk.END)
            campo.insert(0, valor)
            campo.configure(state=estado)


class PanelPerfil:
    def __init__(self, padre, moldes, acciones):
        self.padre = padre
        self.moldes = moldes
        self.acciones = acciones
        self.datos = {}
        self.mostrar_mensaje = None

    def crear(self):
        self.panel_principal = self.moldes.crear_frame(self.padre, tema.PANEL, tema.BORDE, 1, 22, 22, llenar="both", expandir=True, margen_x=24, margen_y=24, columnas_peso=((0, 1),), filas_peso=((1, 1),))
        self.cabecera = CabeceraPerfil(self)
        self.formulario = FormularioPerfil(self)
        self.cabecera.crear()
        self.crear_contenido()

    def crear_contenido(self):
        cuerpo = self.moldes.crear_frame(self.panel_principal, tema.PANEL, fila=1, columna=0, sticky="nsew", columnas_peso=((0, 1), (1, 0), (2, 1)), filas_peso=((0, 1), (1, 0), (2, 1)))
        contenido = self.moldes.crear_frame(cuerpo, tema.PANEL_SUAVE, tema.BORDE, 1, 36, 28, fila=1, columna=1, sticky="", columnas_peso=((0, 1),))
        self.formulario.crear(contenido)
        self.crear_mensaje(contenido)

    def crear_mensaje(self, padre):
        area_mensaje = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, fila=15, columna=0, sticky="ew")
        self.mostrar_mensaje = crear_panel_mensaje_registro(area_mensaje, compacto=True)

    def actualizar(self, datos):
        self.datos = datos
        if hasattr(self, "formulario"):
            self.formulario.actualizar(datos)


class VistaPerfil(tk.Frame):
    """Coordina la pantalla de perfil y delega acciones al controlador."""

    def __init__(self, padre, navegar, controlador_perfil, usuario_actual):
        self.navegar = navegar
        self.controlador_perfil = controlador_perfil
        self.usuario_actual = usuario_actual
        self.moldes = Moldes()

        super().__init__(padre, bg=tema.FONDO)
        self.pack(fill="both", expand=True)
        self.crear_widgets()
        self.actualizar_vista()

    def crear_widgets(self):
        acciones = {
            "volver_menu": lambda: self.navegar("menu"),
            "actualizar": self.actualizar_perfil,
        }
        self.panel = PanelPerfil(self, self.moldes, acciones)
        self.panel.crear()

    def actualizar_perfil(self):
        if not messagebox.askyesno("Confirmar cambios", "Estas seguro de cambiar los datos del perfil?"):
            return

        datos = self.panel.formulario.datos_formulario()
        resultado = self.controlador_perfil.actualizar_perfil(
            self.usuario_actual,
            datos["nombre"],
            datos["apellido"],
            datos["correo"],
            datos["telefono"],
        )
        if not resultado.exitoso:
            self.panel.mostrar_mensaje(f"Revisa este dato: {resultado.error}")
            return

        self.panel.actualizar(resultado.datos)
        self.panel.mostrar_mensaje("Perfil actualizado correctamente.", True)

    def actualizar_vista(self):
        resultado = self.controlador_perfil.obtener_perfil(self.usuario_actual)
        if not resultado.exitoso:
            self.panel.mostrar_mensaje(f"Revisa este dato: {resultado.error}")
            return
        self.panel.actualizar(resultado.datos)
