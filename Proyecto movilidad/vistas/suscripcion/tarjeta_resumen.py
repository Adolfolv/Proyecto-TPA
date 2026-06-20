from ..estilizacion import tema
from .constantes import NOMBRES_DIAS


class TarjetaResumenSuscripcion:
    """Representa la cotizacion pendiente y sus controles de pago."""

    def __init__(self, padre, moldes, acciones):
        self.moldes = moldes
        self.valores = {}
        self.panel = self.moldes.crear_frame(
            padre,
            tema.PANEL_SUAVE,
            tema.BORDE,
            1,
            22,
            22,
            fila=0,
            columna=0,
            sticky="nsew",
            columnas_peso=((0, 1), (1, 2)),
        )
        self.moldes.crear_label(
            self.panel,
            "Resumen de la suscripcion",
            tema.FUENTE_SUBTITULO,
            tema.TEXTO,
            tema.PANEL_SUAVE,
            metodo="grid",
            fila=0,
            columna=0,
            columnas=2,
            sticky="w",
            margen_y=(0, 14),
        )
        campos = (
            ("Ruta", "ruta"),
            ("Periodo", "periodo"),
            ("Dias de viaje", "dias"),
            ("Hora", "hora"),
            ("Cantidad de dias de viaje", "cantidad_viajes"),
            ("Pasajeros", "pasajeros"),
            ("Precio por viaje", "precio_viaje"),
            ("Total a pagar", "precio_total"),
        )
        for fila, (titulo, clave) in enumerate(campos, start=1):
            self.moldes.crear_label(
                self.panel,
                titulo,
                tema.FUENTE_BOTON,
                tema.TEXTO_SUAVE,
                tema.PANEL_SUAVE,
                metodo="grid",
                fila=fila,
                columna=0,
                sticky="w",
                margen_y=5,
            )
            fuente = tema.FUENTE_SUBTITULO if clave == "precio_total" else tema.FUENTE_TEXTO
            color = tema.PRIMARIO if clave == "precio_total" else tema.TEXTO
            self.valores[clave] = self.moldes.crear_label(
                self.panel,
                "-",
                fuente,
                color,
                tema.PANEL_SUAVE,
                300,
                "right",
                metodo="grid",
                fila=fila,
                columna=1,
                sticky="e",
                margen_y=5,
            )

        self.area_acciones = self.moldes.crear_frame(
            self.panel,
            tema.PANEL_SUAVE,
            fila=len(campos) + 1,
            columna=0,
            columnas=2,
            sticky="ew",
            margen_y=(18, 0),
        )
        self.boton_editar = self.moldes.crear_boton(
            self.area_acciones,
            "Editar datos",
            False,
            None,
            acciones["editar"],
            lado="left",
            margen_x=(0, 5),
        )
        self.boton_pagar = self.moldes.crear_boton(
            self.area_acciones,
            "Pagar",
            True,
            None,
            acciones["pagar"],
            lado="right",
            margen_x=(5, 0),
        )
        self.boton_confirmar = self.moldes.crear_boton(
            self.area_acciones,
            "Confirmar",
            True,
            None,
            acciones["confirmar"],
        )
        self.boton_cancelar = self.moldes.crear_boton(
            self.area_acciones,
            "Cancelar suscripcion",
            False,
            None,
            acciones["cancelar"],
        )
        self.panel.grid_remove()

    def actualizar(self, resumen):
        dias = ", ".join(NOMBRES_DIAS[dia] for dia in resumen.dias_semana)
        valores = {
            "ruta": f"{resumen.origen} -> {resumen.destino}",
            "periodo": f"{resumen.fecha_inicio} al {resumen.fecha_fin}",
            "dias": dias,
            "hora": resumen.hora,
            "cantidad_viajes": str(resumen.cantidad_viajes),
            "pasajeros": str(resumen.cantidad_pasajeros),
            "precio_viaje": f"${resumen.precio_por_viaje:,.0f}",
            "precio_total": f"${resumen.precio_total:,.0f}",
        }
        for clave, valor in valores.items():
            self.valores[clave].configure(text=valor)

    def mostrar(self):
        self.panel.grid()

    def ocultar(self):
        self.panel.grid_remove()

    def mostrar_cotizacion(self):
        self._ocultar_botones()
        self.boton_editar.pack(side="left", padx=(0, 5))
        self.boton_pagar.pack(side="right", padx=(5, 0))

    def mostrar_confirmacion(self):
        self._ocultar_botones()
        self.boton_cancelar.pack(side="left", padx=(0, 5))
        self.boton_confirmar.pack(side="right", padx=(5, 0))

    def bloquear_confirmacion(self, bloquear=True):
        estado = "disabled" if bloquear else "normal"
        cursor = "arrow" if bloquear else "hand2"
        self.boton_confirmar.configure(state=estado, cursor=cursor)
        self.boton_cancelar.configure(state=estado, cursor=cursor)

    def _ocultar_botones(self):
        for boton in (
            self.boton_editar,
            self.boton_pagar,
            self.boton_confirmar,
            self.boton_cancelar,
        ):
            boton.pack_forget()
