import tkinter as tk
from datetime import datetime

from .estilizacion import tema
from .estilizacion.decoraciones import crear_logo_suscripcion_pasajero
from .estilizacion.widgets import Moldes


class VistaHistorial(tk.Frame):
    """Ensambla los componentes de la pantalla de historial."""

    def __init__(self, padre, navegar, controlador, usuario_actual):
        super().__init__(padre, bg=tema.FONDO)
        self.pack(fill="both", expand=True)
        self.navegar = navegar
        self.controlador = controlador
        self.usuario_actual = usuario_actual
        self.moldes = Moldes()
        self.viajes = ()
        self.transacciones = ()
        self.viajes_por_item = {}
        self.transacciones_por_item = {}
        self.renderizador = RenderizadorHistorial(self)
        self.acciones = AccionesHistorial(self)
        ConstructorHistorial(self).crear()
        self.acciones.cargar()


class ConstructorHistorial:
    """Crea y ubica widgets sin consultar ni transformar datos."""

    def __init__(self, vista):
        self.vista = vista
        self.moldes = vista.moldes

    def crear(self):
        vista = self.vista
        principal = self.moldes.crear_frame(
            vista, tema.PANEL, tema.BORDE, 1, 14, 14,
            llenar="both", expandir=True, margen_x=20, margen_y=20,
            columnas_peso=((0, 1), (1, 2)), filas_peso=((1, 1),),
        )
        principal.grid_columnconfigure(0, weight=1, uniform="historial")
        principal.grid_columnconfigure(1, weight=2, uniform="historial")
        self._crear_cabecera(principal)
        self._crear_informacion(principal)
        self._crear_contenido(principal)

    def _crear_cabecera(self, padre):
        vista = self.vista
        cabecera = self.moldes.crear_frame(padre, tema.PANEL, fila=0, columna=0, columnas=2, sticky="ew", margen_y=(0, 14), columnas_peso=((0, 1),))
        self.moldes.crear_label(cabecera, "Historial general", tema.FUENTE_TITULO, tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")
        self.moldes.crear_boton(cabecera, "Volver", False, None, lambda: vista.navegar("menu"), metodo="grid", fila=0, columna=1, sticky="e")

    def _crear_informacion(self, padre):
        vista = self.vista
        panel = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, tema.BORDE, 1, 14, 14, fila=1, columna=0, sticky="nsew", margen_x=(0, 10), columnas_peso=((0, 1),), filas_peso=((9, 1),))
        self.moldes.crear_label(panel, "Informacion", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, sticky="w", margen_y=(0, 10))
        self.moldes.crear_label(panel, "Procedencia", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=1, columna=0, sticky="w")
        vista.selector_modalidad = self.moldes.crear_selector(panel, ("Todos", "Viaje normal", "Suscripcion"), metodo="grid", fila=2, columna=0, sticky="ew", margen_y=(4, 10), ipady=4)
        self.moldes.crear_label(panel, "Tipo de viaje", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=3, columna=0, sticky="w")
        vista.selector_tipo = self.moldes.crear_selector(panel, ("Todos", "Normal", "Material"), metodo="grid", fila=4, columna=0, sticky="ew", margen_y=(4, 14), ipady=4)
        vista.selector_modalidad.bind("<<ComboboxSelected>>", vista.acciones.aplicar_filtros)
        vista.selector_tipo.bind("<<ComboboxSelected>>", vista.acciones.aplicar_filtros)

        resumen = self.moldes.crear_frame(panel, tema.PANEL, tema.BORDE, 1, 10, 10, fila=5, columna=0, sticky="ew", columnas_peso=((0, 1),))
        vista.label_total = self.moldes.crear_label(resumen, "Viajes: 0", tema.FUENTE_BOTON, tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")
        vista.label_distancia = self.moldes.crear_label(resumen, "Distancia: 0 km", tema.FUENTE_TEXTO, tema.TEXTO_SUAVE, tema.PANEL, metodo="grid", fila=1, columna=0, sticky="w", margen_y=(5, 0))
        vista.label_monto = self.moldes.crear_label(resumen, "Monto: $0", tema.FUENTE_TEXTO, tema.PRIMARIO, tema.PANEL, metodo="grid", fila=2, columna=0, sticky="w", margen_y=(5, 0))
        vista.label_transacciones = self.moldes.crear_label(resumen, "Transacciones: 0", tema.FUENTE_TEXTO, tema.TEXTO_SUAVE, tema.PANEL, metodo="grid", fila=3, columna=0, sticky="w", margen_y=(5, 0))
        self.moldes.crear_label(panel, "Detalle seleccionado", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=6, columna=0, sticky="w", margen_y=(18, 8))
        vista.label_detalle = self.moldes.crear_label(panel, "Selecciona un viaje o una transaccion.", tema.FUENTE_TEXTO, tema.TEXTO_SUAVE, tema.PANEL_SUAVE, 250, "left", metodo="grid", fila=7, columna=0, sticky="nw")
        vista.logo_suscripcion = crear_logo_suscripcion_pasajero(panel, (520, 248))
        vista.logo_suscripcion.grid(row=9, column=0, sticky="s", pady=(16, 2))

    def _crear_contenido(self, padre):
        vista = self.vista
        panel = self.moldes.crear_frame(padre, tema.PANEL, fila=1, columna=1, sticky="nsew", columnas_peso=((0, 1),), filas_peso=((1, 2), (4, 1), (7, 2)))
        self.moldes.crear_label(panel, "Viajes realizados", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w", margen_y=(0, 8))
        vista.tabla_viajes = self.moldes.crear_tabla(panel, (("fecha", "Fecha", 110), ("ruta", "Ruta", 200), ("modalidad", "Procedencia", 95), ("tipo", "Tipo", 70), ("monto", "Monto", 75)), alto=5, metodo="grid", fila=1, columna=0, sticky="nsew")
        vista.tabla_viajes.bind("<<TreeviewSelect>>", vista.acciones.mostrar_seleccion)
        vista.label_sin_viajes = self.moldes.crear_label(panel, "", tema.FUENTE_TEXTO, tema.TEXTO_SUAVE, tema.PANEL, metodo="grid", fila=2, columna=0, sticky="w", margen_y=(5, 8))

        self.moldes.crear_label(panel, "Transacciones de billetera", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL, metodo="grid", fila=3, columna=0, sticky="w", margen_y=(4, 8))
        vista.tabla_transacciones = self.moldes.crear_tabla(panel, (("fecha", "Fecha", 120), ("tipo", "Tipo", 210), ("monto", "Monto", 90)), alto=5, metodo="grid", fila=4, columna=0, sticky="nsew")
        vista.tabla_transacciones.bind("<<TreeviewSelect>>", vista.acciones.mostrar_transaccion)
        vista.label_sin_transacciones = self.moldes.crear_label(panel, "", tema.FUENTE_TEXTO, tema.TEXTO_SUAVE, tema.PANEL, metodo="grid", fila=5, columna=0, sticky="w", margen_y=(5, 8))

        cabecera = self.moldes.crear_frame(panel, tema.PANEL, fila=6, columna=0, sticky="ew", margen_y=(6, 8), columnas_peso=((0, 1),))
        self.moldes.crear_label(cabecera, "Actividad de los ultimos 7 dias", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")
        vista.label_tendencia = self.moldes.crear_label(cabecera, "", tema.FUENTE_BOTON, tema.PRIMARIO, tema.PANEL, metodo="grid", fila=0, columna=1, sticky="e")
        vista.grafico_actividad = tk.Canvas(panel, bg=tema.SECUNDARIO, highlightbackground=tema.BORDE, highlightthickness=1, height=150)
        vista.grafico_actividad.grid(row=7, column=0, sticky="nsew")
        vista.grafico_actividad.bind("<Configure>", vista.renderizador.dibujar_actividad)


class AccionesHistorial:
    """Coordina consultas, filtros y seleccion de filas."""

    def __init__(self, vista):
        self.vista = vista

    def cargar(self):
        resumen = self.vista.controlador.consultar(self.vista.usuario_actual)
        self.vista.viajes = resumen["viajes"]
        self.vista.transacciones = resumen["transacciones"]
        self.vista.renderizador.renderizar_actividad(resumen)
        self.vista.renderizador.renderizar_transacciones(self.vista.transacciones)
        self.aplicar_filtros()

    def aplicar_filtros(self, _evento=None):
        vista = self.vista
        modalidad, tipo = vista.selector_modalidad.get().upper(), vista.selector_tipo.get().upper()
        viajes = [viaje for viaje in vista.viajes if (modalidad == "TODOS" or viaje.modalidad == modalidad) and (tipo == "TODOS" or viaje.tipo_viaje == tipo)]
        vista.renderizador.renderizar_viajes(viajes)

    def mostrar_seleccion(self, _evento=None):
        vista = self.vista
        seleccion = vista.tabla_viajes.selection()
        viaje = vista.viajes_por_item.get(seleccion[0]) if seleccion else None
        if viaje is not None:
            vista.renderizador.mostrar_detalle(viaje)

    def mostrar_transaccion(self, _evento=None):
        vista = self.vista
        seleccion = vista.tabla_transacciones.selection()
        transaccion = vista.transacciones_por_item.get(seleccion[0]) if seleccion else None
        if transaccion is not None:
            vista.renderizador.mostrar_detalle_transaccion(transaccion)


class RenderizadorHistorial:
    """Transforma resultados del historial en contenido visual."""

    def __init__(self, vista):
        self.vista = vista

    def renderizar_viajes(self, viajes):
        vista = self.vista
        for item in vista.tabla_viajes.get_children():
            vista.tabla_viajes.delete(item)
        vista.viajes_por_item = {}
        es_conductor = getattr(vista.usuario_actual, "tipo_usuario", "") == "conductor"
        for viaje in viajes:
            monto = viaje.pago_conductor if es_conductor else viaje.precio
            item = vista.tabla_viajes.insert("", "end", values=(self.formatear_fecha(viaje.fecha_finalizacion), f"{viaje.origen} -> {viaje.destino}", viaje.modalidad.title(), viaje.tipo_viaje.title(), f"${monto:,.0f}"))
            vista.viajes_por_item[item] = viaje
        monto_total = sum((v.pago_conductor if es_conductor else v.precio) for v in viajes)
        vista.label_total.config(text=f"Viajes: {len(viajes)}")
        vista.label_distancia.config(text=f"Distancia: {sum(v.distancia for v in viajes):.1f} km")
        vista.label_monto.config(text=f"{'Ganado' if es_conductor else 'Gastado'}: ${monto_total:,.0f}")
        vista.label_sin_viajes.config(text="No hay viajes para estos filtros." if not viajes else "")
        vista.label_detalle.config(text="Selecciona un viaje o una transaccion.")

    def renderizar_transacciones(self, transacciones):
        vista = self.vista
        for item in vista.tabla_transacciones.get_children():
            vista.tabla_transacciones.delete(item)
        vista.transacciones_por_item = {}
        for transaccion in transacciones:
            item = vista.tabla_transacciones.insert(
                "",
                "end",
                values=(
                    transaccion.fecha,
                    transaccion.tipo,
                    f"${transaccion.monto:,.0f}",
                ),
            )
            vista.transacciones_por_item[item] = transaccion
        vista.label_transacciones.config(text=f"Transacciones: {len(transacciones)}")
        vista.label_sin_transacciones.config(
            text="No hay transacciones registradas." if not transacciones else ""
        )

    def renderizar_actividad(self, resumen):
        vista = self.vista
        vista.actividad = resumen["actividad"]
        tendencia = resumen["tendencia_porcentual"]
        signo = "+" if tendencia > 0 else "-" if tendencia < 0 else "="
        vista.label_tendencia.config(text=f"{resumen['total_ultimos_7_dias']} viajes - {signo} {abs(tendencia):.1f}%")
        vista.after_idle(self.dibujar_actividad)

    def dibujar_actividad(self, _evento=None):
        vista = self.vista
        if not hasattr(vista, "actividad"):
            return
        canvas = vista.grafico_actividad
        canvas.delete("all")
        ancho, alto = max(canvas.winfo_width(), 500), max(canvas.winfo_height(), 190)
        margen_x, margen_superior, margen_inferior = 34, 20, 34
        base, disponible = alto - margen_inferior, max(1, alto - margen_superior - margen_inferior)
        maximo = max((dia["cantidad"] for dia in vista.actividad), default=0) or 1
        separacion = (ancho - 2 * margen_x) / max(1, len(vista.actividad))
        ancho_barra = min(44, separacion * 0.58)
        canvas.create_line(margen_x, base, ancho - margen_x, base, fill=tema.BORDE, width=2)
        for indice, dia in enumerate(vista.actividad):
            centro = margen_x + separacion * (indice + 0.5)
            superior = base - (dia["cantidad"] / maximo) * disponible
            color = tema.PRIMARIO if dia["variacion"] >= 0 else tema.ERROR
            canvas.create_rectangle(centro - ancho_barra / 2, superior, centro + ancho_barra / 2, base, fill=color, outline="")
            canvas.create_text(centro, max(10, superior - 9), text=str(dia["cantidad"]), fill=tema.TEXTO, font=("Arial", 9, "bold"))
            canvas.create_text(centro, base + 15, text=self.formatear_dia(dia["fecha"]), fill=tema.TEXTO_SUAVE, font=("Arial", 8))

    def mostrar_detalle(self, viaje):
        material = ""
        if viaje.tipo_viaje == "MATERIAL":
            material = f"\nMaterial: {viaje.tipo_material}\nPeso: {viaje.peso} kg - Volumen: {viaje.volumen} m3"
        self.vista.label_detalle.config(text=f"{viaje.origen} -> {viaje.destino}\n{viaje.modalidad.title()} - {viaje.tipo_viaje.title()}\nVehiculo: {viaje.vehiculo}\nDistancia: {viaje.distancia:.1f} km\nDuracion: {viaje.duracion:.0f} s{material}")

    def mostrar_detalle_transaccion(self, transaccion):
        self.vista.label_detalle.config(
            text=(
                f"{transaccion.id_transaccion}\n"
                f"{transaccion.tipo}\n"
                f"Monto: ${transaccion.monto:,.0f}\n"
                f"Fecha: {transaccion.fecha}"
            )
        )

    def formatear_fecha(self, valor):
        return datetime.fromisoformat(valor).strftime("%d-%m-%Y %H:%M")

    def formatear_dia(self, valor):
        nombres = ("Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom")
        return nombres[datetime.fromisoformat(valor).date().weekday()]
