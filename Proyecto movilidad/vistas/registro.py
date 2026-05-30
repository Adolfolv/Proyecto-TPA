"""Pantalla de registro visual sin navegacion real."""

import tkinter as tk

from Comunes import tema
from Comunes.widgets import Moldes


class VistaRegistro(tk.Frame):
    def __init__(self):
        ventana = tk.Tk()
        ventana.title("Registro")
        ventana.geometry("900x700")
        ventana.minsize(760, 620)
        ventana.attributes("-fullscreen", False)

        self.moldes = Moldes()
        self.boton_pasajero = None
        self.boton_conductor = None
        self.area_formulario = None
        self.canvas_scroll = None
        self.ventana_scroll = None

        super().__init__(ventana, bg=tema.FONDO)
        self.pack(fill="both", expand=True)
        self.crear_widgets()

    def crear_widgets(self):
        contenedor = self.moldes.crear_frame(self, tema.PANEL, tema.BORDE, 1, 18, 18, llenar="both", expandir=True, margen_x=24, margen_y=24)
        cabecera = self.moldes.crear_frame(contenedor, tema.PANEL, llenar="x")
        self.moldes.crear_label(cabecera, "Registro", tema.FUENTE_TITULO, tema.TEXTO, tema.PANEL, lado="left")
        self.moldes.crear_boton(cabecera, "Volver", False, None, None, lado="right")

        selector = self.moldes.crear_frame(contenedor, tema.PANEL, llenar="x", margen_y=(18, 0))
        self.boton_pasajero = self.moldes.crear_boton(selector, "Pasajero", True, None, self.mostrar_pasajero, llenar="x", expandir=True, lado="left", margen_x=(5, 0))
        self.moldes.crear_frame(selector, tema.TEXTO_SUAVE, llenar="y", lado="left", margen_x=4, ancho_fijo=1)
        self.boton_conductor = self.moldes.crear_boton(selector, "Conductor", False, None, self.mostrar_conductor, llenar="x", expandir=True, lado="left", margen_x=(0, 5))

        self.area_formulario = self.moldes.crear_frame(contenedor, tema.PANEL, llenar="both", expandir=True, margen_y=(12, 0))
        acciones = self.moldes.crear_frame(contenedor, tema.PANEL, margen_y=(14, 0))
        self.moldes.crear_boton(acciones, "Registrarse", True, 16, None, margen_x=5)
        self.moldes.crear_label(contenedor, "Completa los datos para crear tu cuenta.", tema.FUENTE_TEXTO, tema.TEXTO_SUAVE, tema.PANEL, 780, "center", margen_y=(10, 0))

        self.mostrar_pasajero()

    def limpiar_formulario(self):
        for widget in self.area_formulario.winfo_children():
            widget.destroy()
        self.canvas_scroll = None
        self.ventana_scroll = None

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
        bloque = self.crear_bloque(contenido, "Datos del pasajero", "Informacion principal para crear la cuenta.")
        self.crear_fila_campos(bloque, "Nombre", "Apellido")
        self.crear_fila_campos(bloque, "Correo", "Telefono")
        self.crear_fila_campos(bloque, "Direccion", "")
        self.crear_fila_campos(bloque, "Contrasena", "Confirmar contrasena", "*", "*")
        self.moldes.crear_boton(bloque, "Mostrar contrasena", False, None, None, lado="left", margen_x=5, margen_y=(0, 4))

    def crear_formulario_conductor(self):
        self.limpiar_formulario()
        fila_scroll = self.moldes.crear_frame(self.area_formulario, tema.PANEL, llenar="both", expandir=True)
        self.canvas_scroll = self.moldes.crear_canvas(fila_scroll, tema.PANEL, llenar="both", expandir=True, lado="left")
        barra = self.moldes.crear_scroll_vertical(fila_scroll, self.canvas_scroll.yview, llenar="y", lado="right")
        self.canvas_scroll.configure(yscrollcommand=barra.set)

        contenido = self.moldes.crear_frame(self.canvas_scroll, tema.PANEL)
        self.ventana_scroll = self.canvas_scroll.create_window((0, 0), window=contenido, anchor="nw")
        contenido.bind("<Configure>", self.actualizar_scroll)
        self.canvas_scroll.bind("<Configure>", self.ajustar_ancho_scroll)

        bloque_personal = self.crear_bloque(contenido, "Datos personales", "Informacion principal del conductor.")
        self.crear_fila_campos(bloque_personal, "Telefono", "Nombre")
        self.crear_fila_campos(bloque_personal, "Apellido", "Correo")
        fila_seguridad = self.moldes.crear_frame(bloque_personal, tema.PANEL_SUAVE, llenar="x")
        lado_selfie = self.moldes.crear_frame(fila_seguridad, tema.PANEL_SUAVE, llenar="both", expandir=True, lado="left", margen_x=(5, 5))
        lado_claves = self.moldes.crear_frame(fila_seguridad, tema.PANEL_SUAVE, llenar="both", expandir=True, lado="left", margen_x=(5, 5))
        self.moldes.crear_label(lado_selfie, "Selfie", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, margen_y=(8, 2))
        self.moldes.crear_boton(lado_selfie, "Seleccionar selfie", False, None, None, llenar="x", margen_y=(5, 8))
        self.crear_campo(lado_claves, "Contrasena", "*")
        self.crear_campo(lado_claves, "Confirmar contrasena", "*")
        self.moldes.crear_boton(lado_claves, "Mostrar contrasena", False, None, None, lado="left", margen_x=5, margen_y=(0, 4))

        bloque_vehiculo = self.crear_bloque(contenido, "Datos del vehiculo", "Informacion del auto asociado al conductor.")
        self.crear_fila_campos(bloque_vehiculo, "Licencia de conducir", "Marca del vehiculo")
        self.crear_fila_campos(bloque_vehiculo, "Modelo del vehiculo", "Patente")
        self.moldes.crear_boton(bloque_vehiculo, "Seleccionar documento", False, None, None, llenar="x", margen_x=5, margen_y=(8, 8))
        self.vincular_rueda_scroll(contenido)

    def crear_bloque(self, padre, titulo, descripcion):
        bloque = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, tema.BORDE, 1, 14, 14, llenar="x", margen_x=10, margen_y=8)
        self.moldes.crear_label(bloque, titulo, tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, margen_y=(0, 4))
        self.moldes.crear_label(bloque, descripcion, tema.FUENTE_TEXTO, tema.TEXTO_SUAVE, tema.PANEL_SUAVE, 780, "left", margen_y=(0, 10))
        return bloque

    def crear_fila_campos(self, padre, texto_izquierda, texto_derecha, mostrar_izquierda="", mostrar_derecha=""):
        fila = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, llenar="x")
        izquierda = self.moldes.crear_frame(fila, tema.PANEL_SUAVE, llenar="x", expandir=True, lado="left", margen_x=5)
        derecha = self.moldes.crear_frame(fila, tema.PANEL_SUAVE, llenar="x", expandir=True, lado="left", margen_x=5)
        self.crear_campo(izquierda, texto_izquierda, mostrar_izquierda)
        if texto_derecha:
            self.crear_campo(derecha, texto_derecha, mostrar_derecha)

    def crear_campo(self, padre, texto, mostrar=""):
        self.moldes.crear_label(padre, texto, tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, margen_y=(6, 0))
        self.moldes.crear_entrada(padre, mostrar=mostrar, llenar="x", margen_y=(5, 6))

    def actualizar_scroll(self, evento=None):
        if self.canvas_scroll is not None:
            self.canvas_scroll.configure(scrollregion=self.canvas_scroll.bbox("all"))

    def ajustar_ancho_scroll(self, evento=None):
        if self.canvas_scroll is not None and self.ventana_scroll is not None:
            self.canvas_scroll.itemconfigure(self.ventana_scroll, width=max(1, evento.width - 4))

    def vincular_rueda_scroll(self, widget):
        widget.bind("<MouseWheel>", self.mover_scroll_rueda, add="+")
        for hijo in widget.winfo_children():
            self.vincular_rueda_scroll(hijo)

    def mover_scroll_rueda(self, evento):
        if self.canvas_scroll is not None:
            self.canvas_scroll.yview_scroll(-int(evento.delta / 120) * 3, "units")
            return "break"

    def ejecutar(self):
        self.master.mainloop()


if __name__ == "__main__":
    VistaRegistro().ejecutar()
