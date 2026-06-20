import tkinter as tk
from datetime import datetime, timedelta

from ..estilizacion import tema
from .constantes import NOMBRES_DIAS


class FormularioSuscripcion:
    """Construye el formulario y entrega sus valores, sin ejecutar casos de uso."""

    def __init__(self, padre, moldes, lugares, accion_previsualizar):
        self.moldes = moldes
        self.variables_dias = []
        self.checks_dias = []
        self.panel = self.moldes.crear_frame(
            padre,
            tema.PANEL_SUAVE,
            tema.BORDE,
            1,
            18,
            18,
            fila=0,
            columna=0,
            sticky="nsew",
            columnas_peso=((0, 1), (1, 1)),
        )
        self.moldes.crear_label(
            self.panel,
            "Nueva suscripcion",
            tema.FUENTE_SUBTITULO,
            tema.TEXTO,
            tema.PANEL_SUAVE,
            metodo="grid",
            fila=0,
            columna=0,
            columnas=2,
            sticky="w",
            margen_y=(0, 10),
        )

        self.origen = self._crear_selector("Origen", lugares, 1, 0)
        self.destino = self._crear_selector("Destino", lugares, 1, 1)
        if len(lugares) > 1:
            self.destino.current(1)

        ahora = datetime.now()
        hora_inicial = (ahora + timedelta(minutes=10)).replace(second=0, microsecond=0)
        self.fecha_inicio = self._crear_entrada(
            "Fecha inicial (AAAA-MM-DD)", 3, 0, ahora.date().isoformat()
        )
        self.fecha_fin = self._crear_entrada(
            "Fecha final (AAAA-MM-DD)",
            3,
            1,
            (ahora.date() + timedelta(days=30)).isoformat(),
        )
        self.hora = self._crear_entrada(
            "Hora (HH:MM)", 5, 0, hora_inicial.strftime("%H:%M")
        )
        self.pasajeros = self._crear_selector(
            "Pasajeros", ("1", "2", "3", "4"), 5, 1
        )
        self._crear_dias(7)
        self.boton_crear = self.moldes.crear_boton(
            self.panel,
            "Crear suscripcion",
            True,
            None,
            accion_previsualizar,
            metodo="grid",
            fila=9,
            columna=0,
            columnas=2,
            sticky="ew",
            margen_y=(14, 0),
        )

    def mostrar(self):
        self.panel.grid()

    def ocultar(self):
        self.panel.grid_remove()

    def habilitar(self, habilitado=True):
        estado_entrada = "normal" if habilitado else "disabled"
        estado_selector = "readonly" if habilitado else "disabled"
        for entrada in (self.fecha_inicio, self.fecha_fin, self.hora):
            entrada.configure(state=estado_entrada)
        for selector in (self.origen, self.destino, self.pasajeros):
            selector.configure(state=estado_selector)
        for check in self.checks_dias:
            check.configure(state=estado_entrada)
        self.boton_crear.configure(
            state=estado_entrada,
            cursor="hand2" if habilitado else "arrow",
        )

    def datos(self):
        return {
            "origen": self.origen.get(),
            "destino": self.destino.get(),
            "fecha_inicio": self.fecha_inicio.get(),
            "fecha_fin": self.fecha_fin.get(),
            "dias_semana": tuple(
                indice
                for indice, variable in enumerate(self.variables_dias)
                if variable.get()
            ),
            "hora": self.hora.get(),
            "cantidad_pasajeros": self.pasajeros.get(),
        }

    def _crear_etiqueta(self, texto, fila, columna):
        self.moldes.crear_label(
            self.panel,
            texto,
            tema.FUENTE_BOTON,
            tema.TEXTO_SUAVE,
            tema.PANEL_SUAVE,
            metodo="grid",
            fila=fila,
            columna=columna,
            sticky="w",
            margen_x=5,
            margen_y=(5, 3),
        )

    def _crear_selector(self, titulo, opciones, fila, columna):
        self._crear_etiqueta(titulo, fila, columna)
        return self.moldes.crear_selector(
            self.panel,
            opciones,
            metodo="grid",
            fila=fila + 1,
            columna=columna,
            sticky="ew",
            margen_x=5,
            margen_y=(0, 5),
        )

    def _crear_entrada(self, titulo, fila, columna, valor):
        self._crear_etiqueta(titulo, fila, columna)
        entrada = self.moldes.crear_entrada(
            self.panel,
            metodo="grid",
            fila=fila + 1,
            columna=columna,
            sticky="ew",
            margen_x=5,
            margen_y=(0, 5),
        )
        entrada.insert(0, valor)
        return entrada

    def _crear_dias(self, fila):
        self.moldes.crear_label(
            self.panel,
            "Dias de la semana",
            tema.FUENTE_BOTON,
            tema.TEXTO_SUAVE,
            tema.PANEL_SUAVE,
            metodo="grid",
            fila=fila,
            columna=0,
            columnas=2,
            sticky="w",
            margen_x=5,
            margen_y=(8, 3),
        )
        contenedor = self.moldes.crear_frame(
            self.panel,
            tema.PANEL_SUAVE,
            fila=fila + 1,
            columna=0,
            columnas=2,
            sticky="ew",
        )
        for indice, nombre in enumerate(NOMBRES_DIAS):
            variable = tk.BooleanVar(value=indice < 5)
            check = tk.Checkbutton(
                contenedor,
                text=nombre,
                variable=variable,
                bg=tema.PANEL_SUAVE,
                fg=tema.TEXTO,
                selectcolor=tema.SECUNDARIO,
                activebackground=tema.PANEL_SUAVE,
                activeforeground=tema.TEXTO,
                disabledforeground=tema.TEXTO_SUAVE,
                font=("Arial", 9),
            )
            check.pack(side="left", expand=True)
            self.variables_dias.append(variable)
            self.checks_dias.append(check)
