"""Pantalla de perfil compacta."""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog

from PIL import Image, ImageOps, ImageTk

from .estilizacion import tema
from .estilizacion.decoraciones import crear_panel_mensaje
from .estilizacion.widgets import Moldes


class WidgetsPerfil:
    def __init__(self, entradas, botones, foto, tipo):
        self.entradas, self.botones, self.foto_label, self.tipo_label = entradas, botones, foto, tipo
        self.foto = None

    def datos(self):
        return {clave: entrada.get() for clave, entrada in self.entradas.items()}

    def cargar(self, datos):
        for clave, entrada in self.entradas.items():
            estado = entrada.cget("state"); entrada.configure(state="normal")
            entrada.delete(0, tk.END); entrada.insert(0, datos.get(clave, "")); entrada.configure(state=estado)
        self.tipo_label.configure(text=str(datos.get("tipo_usuario", "usuario")).capitalize())
        self.cargar_foto(datos)

    def editar(self, activo):
        for entrada in self.entradas.values():
            entrada.configure(state="normal" if activo else "readonly", readonlybackground=tema.SECUNDARIO)
        self.botones["editar"].configure(state="disabled" if activo else "normal")
        for clave in ("confirmar", "cancelar", "imagen"):
            self.botones[clave].grid() if activo else self.botones[clave].grid_remove()

    def cargar_foto(self, datos):
        ruta = Path(str(datos.get("imagen", "") or ""))
        if ruta.exists():
            try:
                with Image.open(ruta) as archivo:
                    imagen = ImageOps.fit(archivo.convert("RGB"), (150, 150), method=Image.Resampling.LANCZOS)
                self.foto = ImageTk.PhotoImage(imagen); self.foto_label.configure(image=self.foto, text="")
                return
            except (OSError, ValueError):
                pass
        iniciales = "".join(valor[:1].upper() for valor in (datos.get("nombre", ""), datos.get("apellido", "")) if valor) or "U"
        self.foto = None; self.foto_label.configure(image="", text=iniciales, font=("Arial", 42, "bold"), fg=tema.PRIMARIO)


class VistaPerfil(tk.Frame):
    CAMPOS = (("Nombre", "nombre"), ("Apellido", "apellido"), ("Correo", "correo"), ("Telefono", "telefono"))

    def __init__(self, padre, navegar, controlador_perfil, usuario_actual):
        self.navegar, self.controlador_perfil, self.usuario_actual = navegar, controlador_perfil, usuario_actual
        self.moldes, self.datos, self.imagen_temporal = Moldes(), {}, ""
        super().__init__(padre, bg=tema.FONDO); self.pack(fill="both", expand=True)
        self.crear_widgets(); self.actualizar_vista()

    def crear_widgets(self):
        panel = self.moldes.crear_frame(self, tema.PANEL, tema.BORDE, 1, 22, 22, llenar="both", expandir=True, margen_x=24, margen_y=24, columnas_peso=((0, 1),), filas_peso=((1, 1),))
        cabecera = self.moldes.crear_frame(panel, tema.PANEL, fila=0, columna=0, sticky="ew", margen_y=(0, 18), columnas_peso=((0, 1),))
        self.moldes.crear_label(cabecera, "Perfil", tema.FUENTE_TITULO, tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")
        self.moldes.crear_boton(cabecera, "Volver", False, None, lambda: self.navegar("menu"), metodo="grid", fila=0, columna=1, sticky="e")
        cuerpo = self.moldes.crear_frame(panel, tema.PANEL, fila=1, columna=0, sticky="nsew", columnas_peso=((0, 1),), filas_peso=((0, 1),))
        tarjeta = self.moldes.crear_frame(cuerpo, tema.PANEL_SUAVE, tema.BORDE, 1, 34, 30, fila=0, columna=0, sticky="", columnas_peso=((0, 0), (1, 1)))
        foto, tipo, boton_imagen = self.crear_foto(tarjeta); entradas = self.crear_entradas(tarjeta); botones = self.crear_botones(tarjeta, boton_imagen)
        self.widgets = WidgetsPerfil(entradas, botones, foto, tipo); self.widgets.editar(False)
        self.mostrar_mensaje = crear_panel_mensaje(self.moldes.crear_frame(cuerpo, tema.PANEL, fila=1, columna=0, sticky="ew", margen_y=(12, 0)), compacto=True)

    def crear_foto(self, padre):
        lateral = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, fila=0, columna=0, sticky="n", margen_x=(0, 34), columnas_peso=((0, 1),))
        self.moldes.crear_label(lateral, "Foto", ("Arial", 18, "bold"), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, sticky="ew", margen_y=(0, 12))
        marco = self.moldes.crear_frame(lateral, tema.SECUNDARIO, tema.BORDE, 1, fila=1, columna=0, ancho_fijo=180, alto_fijo=180); marco.grid_propagate(False)
        foto = tk.Label(marco, bg=tema.SECUNDARIO, fg=tema.PRIMARIO, bd=0); foto.pack(fill="both", expand=True, padx=12, pady=12)
        boton = self.moldes.crear_boton(lateral, "Cambiar foto", False, None, self.seleccionar_imagen, metodo="grid", fila=2, columna=0, sticky="ew", margen_y=(12, 0))
        tipo = self.moldes.crear_label(lateral, "", ("Arial", 14, "bold"), tema.TEXTO_SUAVE, tema.PANEL_SUAVE, metodo="grid", fila=3, columna=0, sticky="ew", margen_y=(18, 0))
        return foto, tipo, boton

    def crear_entradas(self, padre):
        formulario = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, fila=0, columna=1, sticky="nsew", columnas_peso=((0, 1), (1, 1)))
        self.moldes.crear_label(formulario, "Datos personales", ("Arial", 20, "bold"), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, columnas=2, sticky="ew", margen_y=(0, 20))
        entradas = {}
        for i, (titulo, clave) in enumerate(self.CAMPOS):
            fila, col = (i // 2) * 2 + 1, i % 2
            self.moldes.crear_label(formulario, titulo, ("Arial", 13, "bold"), tema.TEXTO_SUAVE, tema.PANEL_SUAVE, metodo="grid", fila=fila, columna=col, sticky="w", margen_y=(0, 6))
            entrada = tk.Entry(formulario, font=("Arial", 16, "bold"), bg=tema.SECUNDARIO, fg=tema.TEXTO, insertbackground=tema.TEXTO, relief="flat", bd=0, width=24)
            entrada.grid(row=fila + 1, column=col, sticky="ew", padx=(0, 18 if col == 0 else 0), pady=(0, 18), ipady=9); entradas[clave] = entrada
        self.formulario = formulario; return entradas

    def crear_botones(self, padre, boton_imagen):
        botones = {
            "editar": self.moldes.crear_boton(self.formulario, "Actualizar", True, None, self.iniciar_edicion, metodo="grid", fila=5, columna=0, columnas=2, sticky="ew"),
            "confirmar": self.moldes.crear_boton(self.formulario, "Confirmar", True, None, self.confirmar_cambios, metodo="grid", fila=6, columna=0, sticky="ew", margen_x=(0, 6), margen_y=(10, 0)),
            "cancelar": self.moldes.crear_boton(self.formulario, "Cancelar", False, None, self.cancelar_edicion, metodo="grid", fila=6, columna=1, sticky="ew", margen_x=(6, 0), margen_y=(10, 0)),
            "imagen": boton_imagen,
        }
        for boton in botones.values(): boton.configure(pady=12)
        return botones

    def iniciar_edicion(self):
        self.imagen_temporal = self.datos.get("imagen", ""); self.widgets.editar(True); self.mostrar_mensaje("")

    def cancelar_edicion(self):
        self.imagen_temporal = self.datos.get("imagen", ""); self.widgets.cargar(self.datos); self.widgets.editar(False); self.mostrar_mensaje("")

    def seleccionar_imagen(self):
        ruta = filedialog.askopenfilename(title="Cambiar foto", filetypes=(("Imagenes", "*.png *.jpg *.jpeg"), ("Todos", "*.*")))
        if ruta:
            self.imagen_temporal = ruta; self.widgets.cargar_foto(dict(self.datos, **self.widgets.datos(), imagen=ruta))

    def confirmar_cambios(self):
        datos = dict(self.widgets.datos(), imagen=self.imagen_temporal)
        resultado = self.controlador_perfil.actualizar_perfil(self.usuario_actual, datos["nombre"], datos["apellido"], datos["correo"], datos["telefono"], datos["imagen"])
        if not resultado.exitoso:
            self.mostrar_mensaje(f"Revisa este dato: {resultado.error}"); return
        self.datos = resultado.datos; self.widgets.cargar(self.datos); self.widgets.editar(False); self.mostrar_mensaje("Perfil actualizado correctamente.", True)

    def actualizar_vista(self):
        resultado = self.controlador_perfil.obtener_perfil(self.usuario_actual)
        if not resultado.exitoso:
            self.mostrar_mensaje(f"Revisa este dato: {resultado.error}"); return
        self.datos = resultado.datos; self.imagen_temporal = self.datos.get("imagen", ""); self.widgets.cargar(self.datos)
