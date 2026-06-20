from ..estilizacion import tema
from .constantes import NOMBRES_DIAS


class PanelGestionSuscripciones:
    """Muestra suscripciones persistidas y expone solamente su seleccion."""

    def __init__(self, padre, moldes, acciones):
        self.moldes = moldes
        self.suscripciones = {}
        self.viajes = {}
        self.panel = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, tema.BORDE, 1, 16, 16, fila=0, columna=1, sticky="nsew", margen_x=(8, 0), columnas_peso=((0, 1),), filas_peso=((1, 1), (4, 1)))
        self.moldes.crear_label(self.panel, "Mis suscripciones", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, sticky="w")
        self.tabla_suscripciones = self.moldes.crear_tabla(self.panel, (("ruta", "Ruta", 190), ("horario", "Horario", 115), ("total", "Total", 80), ("estado", "Estado", 95)), alto=5, metodo="grid", fila=1, columna=0, sticky="nsew", margen_y=(8, 5))
        botones = self.moldes.crear_frame(self.panel, tema.PANEL_SUAVE, fila=2, columna=0, sticky="ew", margen_y=(3, 12))
        self.moldes.crear_boton(botones, "Pausar / reanudar", False, None, acciones["alternar"], lado="left", margen_x=(0, 5))
        self.moldes.crear_boton(botones, "Cancelar suscripcion", False, None, acciones["cancelar_suscripcion"], lado="left", margen_x=5)

        self.moldes.crear_label(self.panel, "Viajes programados", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=3, columna=0, sticky="w")
        self.tabla_viajes = self.moldes.crear_tabla(self.panel, (("fecha", "Fecha y hora", 120), ("ruta", "Ruta", 165), ("estado", "Estado", 120), ("detalle", "Conductor / detalle", 155)), alto=6, metodo="grid", fila=4, columna=0, sticky="nsew", margen_y=(8, 5))
        self.moldes.crear_boton(self.panel, "Cancelar viaje seleccionado", False, None, acciones["cancelar_viaje"], metodo="grid", fila=5, columna=0, sticky="e", margen_y=(5, 0))

    def actualizar(self, suscripciones, viajes):
        self.suscripciones = {item.id_suscripcion: item for item in suscripciones}
        self.viajes = {item.id_viaje_programado: item for item in viajes}
        self._limpiar(self.tabla_suscripciones)
        self._limpiar(self.tabla_viajes)
        for item in suscripciones:
            dias = ",".join(NOMBRES_DIAS[dia] for dia in item.dias_semana)
            self.tabla_suscripciones.insert("", "end", iid=item.id_suscripcion, values=(f"{item.origen} -> {item.destino}", f"{dias} {item.hora}", f"${item.precio_total:,.0f}", item.estado))
        for item in viajes:
            detalle = item.conductor or item.error or "Pendiente"
            if item.precio:
                detalle = f"{detalle} - ${item.precio:,.0f}"
            self.tabla_viajes.insert("", "end", iid=item.id_viaje_programado, values=(item.fecha_hora.replace("T", " "), f"{item.origen} -> {item.destino}", item.estado, detalle))

    def suscripcion_seleccionada(self):
        seleccion = self.tabla_suscripciones.selection()
        return self.suscripciones.get(seleccion[0]) if seleccion else None

    def viaje_seleccionado(self):
        seleccion = self.tabla_viajes.selection()
        return self.viajes.get(seleccion[0]) if seleccion else None

    def _limpiar(self, tabla):
        for item in tabla.get_children():
            tabla.delete(item)
