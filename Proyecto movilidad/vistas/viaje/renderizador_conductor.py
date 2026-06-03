import tkinter as tk

from PIL import Image, ImageTk

from ..estilizacion import tema
from .renderizador_base import RenderizadorViajeBase


class RenderizadorConductor(RenderizadorViajeBase):
    """Pinta resultados propios del flujo del conductor."""

    def actualizar_cronometro_busqueda(self, segundos_transcurridos=0):
        # El cronometro simula la espera hasta encontrar un pasajero.
        duracion_busqueda = self.vista.info_pasajero_busqueda.duracion_busqueda
        self.vista.label_cronometro.config(text=f"00:{segundos_transcurridos:02d}")
        if segundos_transcurridos < duracion_busqueda:
            self.vista.label_cronometro.after(
                1000,
                lambda: self.actualizar_cronometro_busqueda(segundos_transcurridos + 1),
            )
            return
        # Al terminar el conteo, se pinta el pasajero y se cambia el estado visual.
        self.mostrar_pasajero_encontrado()
        self.vista.estado_visual.pasajero_encontrado()

    def mostrar_pasajero_encontrado(self):
        # Construye el panel con los datos del pasajero elegido por el servicio.
        pasajero = self.vista.info_pasajero_busqueda
        imagen = Image.open(self.vista.ruta_imagenes_usuarios / pasajero.imagen)
        imagen.thumbnail((64, 64))
        self.vista.imagen_pasajero = ImageTk.PhotoImage(imagen)
        tk.Label(
            self.vista.frame_pasajero,
            image=self.vista.imagen_pasajero,
            bg=tema.PANEL_SUAVE,
        ).grid(row=0, column=0, rowspan=4, sticky="nw", padx=10, pady=10)

        llegada = (
            f"Llegar: {pasajero.km_para_llegar} km | "
            f"{pasajero.tiempo_para_llegar} s"
        )
        traslado = (
            f"Traslado: {pasajero.km_transportando} km | "
            f"{pasajero.tiempo_transportando} s"
        )
        # Cada label pertenece al panel visual del pasajero encontrado.
        self.vista.moldes.crear_label(
            self.vista.frame_pasajero,
            pasajero.nombre_completo,
            ("Arial", 12, "bold"),
            tema.TEXTO,
            tema.PANEL_SUAVE,
            metodo="grid",
            fila=0,
            columna=1,
            sticky="w",
            margen_x=8,
            margen_y=(10, 2),
        )
        self.vista.moldes.crear_label(
            self.vista.frame_pasajero,
            pasajero.trayecto,
            ("Arial", 9),
            tema.TEXTO,
            tema.PANEL_SUAVE,
            300,
            "left",
            metodo="grid",
            fila=1,
            columna=1,
            sticky="w",
            margen_x=8,
        )
        self.vista.moldes.crear_label(
            self.vista.frame_pasajero,
            f"Vehiculo: {pasajero.vehiculo}",
            ("Arial", 9),
            tema.TEXTO_SUAVE,
            tema.PANEL_SUAVE,
            metodo="grid",
            fila=2,
            columna=1,
            sticky="w",
            margen_x=8,
        )
        self.vista.moldes.crear_label(
            self.vista.frame_pasajero,
            f"Pago: ${pasajero.precio}",
            ("Arial", 9, "bold"),
            tema.PRIMARIO,
            tema.PANEL_SUAVE,
            metodo="grid",
            fila=3,
            columna=1,
            sticky="w",
            margen_x=8,
            margen_y=(0, 10),
        )
        self.vista.moldes.crear_label(
            self.vista.frame_pasajero,
            llegada,
            ("Arial", 9),
            tema.TEXTO,
            tema.PANEL_SUAVE,
            metodo="grid",
            fila=4,
            columna=0,
            columnas=2,
            sticky="w",
            margen_x=10,
            margen_y=(0, 2),
        )
        self.vista.moldes.crear_label(
            self.vista.frame_pasajero,
            traslado,
            ("Arial", 9),
            tema.TEXTO,
            tema.PANEL_SUAVE,
            metodo="grid",
            fila=5,
            columna=0,
            columnas=2,
            sticky="w",
            margen_x=10,
            margen_y=(0, 10),
        )

        ruta_pasajero = self.vista.controlador_conductor.formar_ruta_pasajero_conductor(
            pasajero
        )
        # La ruta la calcula el controlador/servicio; el renderizador solo la dibuja.
        self.dibujar_trayecto_en_mapa(ruta_pasajero)
