"""Vista compacta de reputacion, separada por responsabilidades."""

import tkinter as tk

from .estilizacion import tema
from .estilizacion.widgets import Moldes


class CabeceraReputacion:
    def __init__(self, panel):
        self.panel = panel

    def crear(self):
        cabecera = self.panel.moldes.crear_frame(self.panel.principal, tema.PANEL, fila=0, columna=0, sticky="ew", margen_y=(0, 16), columnas_peso=((0, 1),))
        self.panel.moldes.crear_label(cabecera, "Tarjeta social", tema.FUENTE_TITULO, tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")
        acciones = self.panel.moldes.crear_frame(cabecera, tema.PANEL, fila=0, columna=1, sticky="e")
        self.panel.moldes.crear_boton(acciones, tema.texto_boton(), comando=self.panel.acciones["tema"], lado="left", margen_x=(0, 8))
        self.panel.moldes.crear_boton(acciones, "Volver", comando=self.panel.acciones["volver"], lado="left")


class FormularioOpinion:
    def __init__(self, panel):
        self.panel = panel
        self.moldes = panel.moldes

    def crear(self, padre):
        bloque = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, fila=4, columna=0, sticky="ew", margen_y=(22, 0), columnas_peso=((0, 1),))
        self.moldes.crear_label(bloque, "Deja tu opinion", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, sticky="w")
        self.estrellas = self.moldes.crear_selector(bloque, ("5 estrellas", "4 estrellas", "3 estrellas", "2 estrellas", "1 estrella"), metodo="grid", fila=1, columna=0, sticky="ew", margen_y=(10, 8))
        self.comentario = tk.Text(bloque, height=4, font=tema.FUENTE_TEXTO, bg=tema.SECUNDARIO, fg=tema.TEXTO, insertbackground=tema.TEXTO, relief="flat", bd=0, wrap="word")
        self.comentario.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        self.moldes.crear_boton(bloque, "Publicar opinion", True, comando=self.panel.acciones["publicar"], metodo="grid", fila=3, columna=0, sticky="ew")

    def datos(self):
        return self.estrellas.get().split()[0], self.comentario.get("1.0", "end").strip()

    def limpiar(self):
        self.comentario.delete("1.0", "end")


class PanelReputacion:
    def __init__(self, padre, moldes, acciones, es_pasajero):
        self.padre = padre
        self.moldes = moldes
        self.acciones = acciones
        self.es_pasajero = es_pasajero
        self.formulario = None

    def crear(self):
        self.principal = self.moldes.crear_frame(self.padre, tema.PANEL, tema.BORDE, 1, 20, 20, llenar="both", expandir=True, margen_x=24, margen_y=24, columnas_peso=((0, 1),), filas_peso=((1, 1),))
        CabeceraReputacion(self).crear()
        cuerpo = self.moldes.crear_frame(self.principal, tema.PANEL, fila=1, columna=0, sticky="nsew", columnas_peso=((0, 1), (1, 2)), filas_peso=((0, 1),))
        self.lateral = self.moldes.crear_frame(cuerpo, tema.PANEL_SUAVE, tema.BORDE, 1, 22, 22, fila=0, columna=0, sticky="nsew", margen_x=(0, 10), columnas_peso=((0, 1),))
        detalle = self.moldes.crear_frame(cuerpo, tema.PANEL_SUAVE, tema.BORDE, 1, 18, 18, fila=0, columna=1, sticky="nsew", margen_x=(10, 0), columnas_peso=((0, 1),), filas_peso=((1, 1),))
        self.crear_resumen()
        self.crear_opiniones(detalle)
        if self.es_pasajero:
            self.formulario = FormularioOpinion(self)
            self.formulario.crear(self.lateral)

    def crear_resumen(self):
        self.moldes.crear_label(self.lateral, "Conductor", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, sticky="w")
        self.selector = self.moldes.crear_selector(self.lateral, ("Cargando...",), metodo="grid", fila=1, columna=0, sticky="ew", margen_y=(8, 20))
        self.selector.bind("<<ComboboxSelected>>", self.acciones["seleccionar"])
        self.nombre = self.moldes.crear_label(self.lateral, "", ("Arial", 20, "bold"), tema.TEXTO, tema.PANEL_SUAVE, 300, "center", metodo="grid", fila=2, columna=0, sticky="ew")
        self.resumen = self.moldes.crear_label(self.lateral, "Sin calificaciones", ("Arial", 18, "bold"), tema.ADMIN_CONDUCTOR, tema.PANEL_SUAVE, metodo="grid", fila=3, columna=0, sticky="", margen_y=(12, 0))

    def crear_opiniones(self, padre):
        self.moldes.crear_label(padre, "Opiniones de pasajeros", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, sticky="w", margen_y=(0, 12))
        self.tabla = self.moldes.crear_tabla(padre, (("autor", "Pasajero", 140), ("estrellas", "Estrellas", 100), ("comentario", "Opinion", 420)), alto=12, metodo="grid", fila=1, columna=0, sticky="nsew")
        self.mensaje = self.moldes.crear_label(padre, "", tema.FUENTE_TEXTO, tema.TEXTO_SUAVE, tema.PANEL_SUAVE, metodo="grid", fila=2, columna=0, sticky="ew", margen_y=(10, 0))

    def configurar_conductores(self, conductores, conductor_actual=None):
        nombres = [f"{item.nombre} {item.apellido}" for item in conductores]
        if conductor_actual is not None:
            nombres = [f"{conductor_actual.nombre} {conductor_actual.apellido}"]
        self.selector.configure(values=nombres or ["No hay conductores"], state="readonly" if conductores else "disabled")
        self.selector.current(0)

    def actualizar(self, datos):
        promedio = datos["promedio"]
        llenas = int(round(promedio))
        conductor = datos["conductor"]
        opiniones = datos["opiniones"]
        self.nombre.configure(text=f"{conductor.nombre} {conductor.apellido}")
        self.resumen.configure(text=f"{'★' * llenas}{'☆' * (5 - llenas)}  {promedio:.1f} | {len(opiniones)} opiniones")
        filas = {f"opinion-{i}": (opinion.nombre_pasajero, "★" * opinion.estrellas, opinion.comentario) for i, opinion in enumerate(opiniones)}
        self.moldes.sincronizar_tabla(self.tabla, filas)
        self.mostrar_mensaje("" if filas else "Este conductor aun no tiene opiniones.")

    def mostrar_mensaje(self, texto, exito=False):
        self.mensaje.configure(text=texto, fg=tema.EXITO if exito else tema.TEXTO_SUAVE)


class VistaReputacion(tk.Frame):
    def __init__(self, padre, navegar, controlador_reputacion, usuario_actual):
        self.navegar = navegar
        self.controlador = controlador_reputacion
        self.usuario_actual = usuario_actual
        self.moldes = Moldes()
        self.conductores = []
        self.id_conductor = None
        super().__init__(padre, bg=tema.FONDO)
        self.pack(fill="both", expand=True)
        acciones = {"volver": lambda: navegar("menu"), "tema": self.cambiar_tema, "seleccionar": self.seleccionar_conductor, "publicar": self.publicar_opinion}
        self.panel = PanelReputacion(self, self.moldes, acciones, self.es_pasajero)
        self.panel.crear()
        self.iniciar()

    @property
    def es_pasajero(self):
        return getattr(self.usuario_actual, "tipo_usuario", "") == "pasajero"

    def iniciar(self):
        if self.es_pasajero:
            self.conductores = self.controlador.listar_conductores()
            self.panel.configurar_conductores(self.conductores)
            if not self.conductores:
                self.panel.mostrar_mensaje("Aun no hay conductores disponibles.")
                return
            self.id_conductor = self.conductores[0].id_usuario
        else:
            self.id_conductor = self.usuario_actual.id_usuario
            self.panel.configurar_conductores([], self.usuario_actual)
        self.cargar_reputacion()

    def seleccionar_conductor(self, _evento=None):
        indice = self.panel.selector.current()
        if 0 <= indice < len(self.conductores):
            self.id_conductor = self.conductores[indice].id_usuario
            self.cargar_reputacion()

    def cargar_reputacion(self):
        resultado = self.controlador.cargar_reputacion(self.id_conductor)
        if resultado.exitoso:
            self.panel.actualizar(resultado.datos)
        else:
            self.panel.mostrar_mensaje(resultado.error)

    def publicar_opinion(self):
        estrellas, comentario = self.panel.formulario.datos()
        resultado = self.controlador.agregar_opinion(self.id_conductor, self.usuario_actual, estrellas, comentario)
        if not resultado.exitoso:
            self.panel.mostrar_mensaje(resultado.error)
            return
        self.panel.formulario.limpiar()
        self.panel.actualizar(resultado.datos)
        self.panel.mostrar_mensaje("Opinion publicada correctamente.", True)

    def cambiar_tema(self):
        tema.alternar_tema()
        self.navegar("reputacion")
