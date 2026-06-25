"""Pantalla de perfil separada por responsabilidades."""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog

from PIL import Image, ImageOps, ImageTk

from .estilizacion import tema
from .estilizacion.decoraciones import RUTA_IMAGENES, crear_panel_mensaje
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


class FotoPerfil:
    TAMANO = (230, 230)

    def __init__(self, panel):
        self.panel = panel
        self.moldes = panel.moldes
        self.foto = None

    def crear(self, padre):
        self.moldes.crear_label(padre, "Foto de perfil", ("Arial", 20, "bold"), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, sticky="ew", margen_y=(0, 20))
        self.marco_foto = self.moldes.crear_frame(padre, tema.SECUNDARIO, tema.BORDE, 1, fila=1, columna=0, sticky="ew", margen_y=(18, 18), ancho_fijo=258, alto_fijo=258)
        self.marco_foto.grid_propagate(False)
        self.label_foto = tk.Label(self.marco_foto, bg=tema.SECUNDARIO, fg=tema.PRIMARIO, bd=0)
        self.label_foto.pack(fill="both", expand=True, padx=12, pady=12)
        self.boton_cambiar = self.moldes.crear_boton(padre, "Cambiar imagen", False, None, self.panel.acciones["cambiar_imagen"], metodo="grid", fila=2, columna=0, sticky="ew", margen_y=(8, 0))
        self.boton_cambiar.configure(pady=14)
        self.tipo = self.moldes.crear_label(padre, "", ("Arial", 18, "bold"), tema.TEXTO_SUAVE, tema.PANEL_SUAVE, metodo="grid", fila=3, columna=0, sticky="ew", margen_y=(36, 0))
        self.mostrar_boton(False)

    def actualizar(self, datos):
        self.tipo.configure(text=str(datos.get("tipo_usuario", "usuario")).capitalize())
        ruta = self._resolver_ruta(datos.get("imagen", ""))
        if ruta is None or not self._mostrar_imagen(ruta):
            self._mostrar_iniciales(datos)

    def mostrar_boton(self, visible):
        if visible:
            self.boton_cambiar.configure(
                text="Cambiar imagen",
                state="normal",
                bg=tema.SECUNDARIO,
                fg=tema.TEXTO,
                activebackground=tema.SECUNDARIO,
                activeforeground=tema.TEXTO,
                cursor="hand2",
            )
        else:
            self.boton_cambiar.configure(
                text="",
                state="disabled",
                bg=tema.PANEL_SUAVE,
                fg=tema.PANEL_SUAVE,
                activebackground=tema.PANEL_SUAVE,
                activeforeground=tema.PANEL_SUAVE,
                cursor="arrow",
            )

    def _mostrar_imagen(self, ruta):
        try:
            with Image.open(ruta) as imagen:
                imagen = ImageOps.fit(
                    imagen.convert("RGB"),
                    self.TAMANO,
                    method=Image.Resampling.LANCZOS,
                )
            self.foto = ImageTk.PhotoImage(imagen)
            self.label_foto.configure(image=self.foto, text="")
            return True
        except (OSError, ValueError):
            self.foto = None
            return False

    def _mostrar_iniciales(self, datos):
        iniciales = "".join(
            valor[:1].upper()
            for valor in (datos.get("nombre", ""), datos.get("apellido", ""))
            if valor
        ) or "U"
        self.label_foto.configure(
            image="",
            text=iniciales,
            font=("Arial", 46, "bold"),
            fg=tema.TEXTO_SUAVE,
            bg=tema.SECUNDARIO,
        )

    def _resolver_ruta(self, imagen):
        if not imagen:
            return None
        ruta = Path(imagen)
        if ruta.exists():
            return ruta
        if not ruta.is_absolute():
            candidata = Path.cwd() / ruta
            if candidata.exists():
                return candidata
        for carpeta in ("imagenes_usuarios", "imagenes_conductores"):
            candidata = RUTA_IMAGENES / carpeta / imagen
            if candidata.exists():
                return candidata
        return None


class FormularioPerfil:
    CAMPOS = (
        ("Nombre", "nombre"),
        ("Apellido", "apellido"),
        ("Correo", "correo"),
        ("Telefono", "telefono"),
    )

    def __init__(self, panel):
        self.panel = panel
        self.moldes = panel.moldes
        self.campos = {}

    def crear(self, padre):
        self.moldes.crear_label(padre, "Datos personales", ("Arial", 20, "bold"), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, columnas=2, sticky="ew", margen_y=(0, 20))
        for indice, (titulo, clave) in enumerate(self.CAMPOS):
            self.crear_dato(padre, titulo, self.panel.datos.get(clave, ""), indice + 1, clave)
        self.crear_acciones(padre, 7)
        self.set_editable(False)

    def crear_dato(self, padre, titulo, valor, indice, clave):
        columna = (indice - 1) % 2
        fila = ((indice - 1) // 2) * 3 + 1
        self.moldes.crear_label(padre, titulo, ("Arial", 13, "bold"), tema.TEXTO_SUAVE, tema.PANEL_SUAVE, metodo="grid", fila=fila, columna=columna, sticky="w", margen_x=(0, 16), margen_y=(0, 7))
        entrada = tk.Entry(padre, font=("Arial", 17, "bold"), bg=tema.SECUNDARIO, fg=tema.TEXTO, insertbackground=tema.TEXTO, relief="flat", bd=0, width=28)
        entrada.insert(0, valor)
        entrada.grid(row=fila + 1, column=columna, sticky="ew", padx=(0, 18 if columna == 0 else 0), pady=(0, 20), ipady=11)
        self.campos[clave] = entrada

    def crear_acciones(self, padre, fila):
        acciones = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, fila=fila, columna=0, columnas=2, sticky="ew", margen_y=(14, 0), columnas_peso=((0, 1), (1, 1)))
        self.boton_editar = self.moldes.crear_boton(acciones, "Actualizar", True, None, self.panel.acciones["editar"], metodo="grid", fila=0, columna=0, columnas=2, sticky="ew")
        self.boton_confirmar = self.moldes.crear_boton(acciones, "Confirmar", True, None, self.panel.acciones["confirmar"], metodo="grid", fila=1, columna=0, sticky="ew", margen_x=(0, 6), margen_y=(10, 0))
        self.boton_cancelar = self.moldes.crear_boton(acciones, "Cancelar cambios", False, None, self.panel.acciones["cancelar"], metodo="grid", fila=1, columna=1, sticky="ew", margen_x=(6, 0), margen_y=(10, 0))
        for boton in (self.boton_editar, self.boton_confirmar, self.boton_cancelar):
            boton.configure(pady=14)
        self._mostrar_boton_accion(self.boton_confirmar, False, "Confirmar", True)
        self._mostrar_boton_accion(self.boton_cancelar, False, "Cancelar cambios", False)

    def set_editable(self, editable):
        estado = "normal" if editable else "readonly"
        for campo in self.campos.values():
            campo.configure(state=estado, readonlybackground=tema.SECUNDARIO)
        if editable:
            self.boton_editar.configure(state="disabled")
            self._mostrar_boton_accion(self.boton_confirmar, True, "Confirmar", True)
            self._mostrar_boton_accion(self.boton_cancelar, True, "Cancelar cambios", False)
        else:
            self.boton_editar.configure(state="normal")
            self._mostrar_boton_accion(self.boton_confirmar, False, "Confirmar", True)
            self._mostrar_boton_accion(self.boton_cancelar, False, "Cancelar cambios", False)

    def _mostrar_boton_accion(self, boton, visible, texto, principal):
        if visible:
            fondo = tema.PRIMARIO if principal else tema.SECUNDARIO
            color = tema.PRIMARIO_TEXTO if principal else tema.TEXTO
            boton.configure(
                text=texto,
                state="normal",
                bg=fondo,
                fg=color,
                activebackground=fondo,
                activeforeground=color,
                cursor="hand2",
            )
            return

        boton.configure(
            text="",
            state="disabled",
            bg=tema.PANEL_SUAVE,
            fg=tema.PANEL_SUAVE,
            activebackground=tema.PANEL_SUAVE,
            activeforeground=tema.PANEL_SUAVE,
            cursor="arrow",
        )

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
        self.imagen_temporal = ""
        self.mostrar_mensaje = None
        self.modo_edicion = False

    def crear(self):
        self.panel_principal = self.moldes.crear_frame(self.padre, tema.PANEL, tema.BORDE, 1, 22, 22, llenar="both", expandir=True, margen_x=24, margen_y=24, columnas_peso=((0, 1),), filas_peso=((1, 1),))
        self.cabecera = CabeceraPerfil(self)
        self.formulario = FormularioPerfil(self)
        self.foto = FotoPerfil(self)
        self.cabecera.crear()
        self.crear_contenido()

    def crear_contenido(self):
        cuerpo = self.moldes.crear_frame(self.panel_principal, tema.PANEL, fila=1, columna=0, sticky="nsew", columnas_peso=((0, 1),), filas_peso=((2, 1),))
        contenido = self.moldes.crear_frame(cuerpo, tema.PANEL_SUAVE, tema.BORDE, 1, 42, 38, fila=0, columna=0, sticky="ew", columnas_peso=((0, 0), (1, 0), (2, 1)))
        lateral = self.moldes.crear_frame(contenido, tema.PANEL_SUAVE, fila=0, columna=0, sticky="nsew", columnas_peso=((0, 1),), filas_peso=((5, 1),), ancho_fijo=310)
        lateral.grid_propagate(False)
        self.moldes.crear_frame(contenido, tema.BORDE, fila=0, columna=1, sticky="ns", margen_x=34, ancho_fijo=1)
        formulario = self.moldes.crear_frame(contenido, tema.PANEL_SUAVE, fila=0, columna=2, sticky="nsew", columnas_peso=((0, 1), (1, 1)))
        self.foto.crear(lateral)
        self.formulario.crear(formulario)
        self.crear_mensaje(cuerpo)

    def crear_mensaje(self, padre):
        area_mensaje = self.moldes.crear_frame(padre, tema.PANEL, fila=1, columna=0, sticky="ew", margen_y=(12, 0))
        self.mostrar_mensaje = crear_panel_mensaje(area_mensaje, compacto=True)

    def iniciar_edicion(self):
        self.modo_edicion = True
        self.imagen_temporal = self.datos.get("imagen", "")
        self.formulario.set_editable(True)
        self.foto.mostrar_boton(True)
        self.mostrar_mensaje("")

    def cancelar_edicion(self):
        self.modo_edicion = False
        self.imagen_temporal = self.datos.get("imagen", "")
        self.formulario.actualizar(self.datos)
        self.foto.actualizar(self.datos)
        self.formulario.set_editable(False)
        self.foto.mostrar_boton(False)
        self.mostrar_mensaje("")

    def seleccionar_imagen(self):
        ruta = filedialog.askopenfilename(
            title="Cambiar foto de perfil",
            filetypes=(("Imagenes", "*.png *.jpg *.jpeg"), ("Todos los archivos", "*.*")),
        )
        if not ruta:
            return
        self.imagen_temporal = ruta
        datos_vista = dict(self.datos)
        datos_vista.update(self.formulario.datos_formulario())
        datos_vista["imagen"] = ruta
        self.foto.actualizar(datos_vista)

    def datos_formulario(self):
        datos = self.formulario.datos_formulario()
        datos["imagen"] = self.imagen_temporal
        return datos

    def actualizar(self, datos):
        self.datos = datos
        self.imagen_temporal = datos.get("imagen", "")
        if hasattr(self, "formulario"):
            self.formulario.actualizar(datos)
        if hasattr(self, "foto"):
            self.foto.actualizar(datos)

    def finalizar_edicion(self):
        self.modo_edicion = False
        self.formulario.set_editable(False)
        self.foto.mostrar_boton(False)


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
            "editar": self.editar_perfil,
            "confirmar": self.confirmar_cambios,
            "cancelar": self.cancelar_cambios,
            "cambiar_imagen": self.cambiar_imagen,
        }
        self.panel = PanelPerfil(self, self.moldes, acciones)
        self.panel.crear()

    def editar_perfil(self):
        self.panel.iniciar_edicion()

    def cancelar_cambios(self):
        self.panel.cancelar_edicion()

    def cambiar_imagen(self):
        self.panel.seleccionar_imagen()

    def confirmar_cambios(self):
        datos = self.panel.datos_formulario()
        resultado = self.controlador_perfil.actualizar_perfil(
            self.usuario_actual,
            datos["nombre"],
            datos["apellido"],
            datos["correo"],
            datos["telefono"],
            datos["imagen"],
        )
        if not resultado.exitoso:
            self.panel.mostrar_mensaje(f"Revisa este dato: {resultado.error}")
            return

        self.panel.actualizar(resultado.datos)
        self.panel.finalizar_edicion()
        self.panel.mostrar_mensaje("Perfil actualizado correctamente.", True)

    def actualizar_vista(self):
        resultado = self.controlador_perfil.obtener_perfil(self.usuario_actual)
        if not resultado.exitoso:
            self.panel.mostrar_mensaje(f"Revisa este dato: {resultado.error}")
            return
        self.panel.actualizar(resultado.datos)
