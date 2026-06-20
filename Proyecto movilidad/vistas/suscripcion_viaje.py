"""Pantalla para crear y administrar viajes recurrentes."""

import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox

from Modelos.Suscripcion.modelos_suscripcion import ESTADO_ACTIVA, ESTADO_PAUSADA
from .estilizacion import tema
from .estilizacion.widgets import Moldes


NOMBRES_DIAS = ("Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom")


class FormularioSuscripcion:
    def __init__(self, vista, padre, lugares):
        self.vista = vista
        self.moldes = vista.moldes
        self.variables_dias = []
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
            margen_x=(0, 8),
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
        self.fecha_inicio = self._crear_entrada("Fecha inicial (AAAA-MM-DD)", 3, 0, ahora.date().isoformat())
        self.fecha_fin = self._crear_entrada("Fecha final (AAAA-MM-DD)", 3, 1, (ahora.date() + timedelta(days=30)).isoformat())
        self.hora = self._crear_entrada("Hora (HH:MM)", 5, 0, hora_inicial.strftime("%H:%M"))
        self.pasajeros = self._crear_selector("Pasajeros", ("1", "2", "3", "4"), 5, 1)
        self._crear_dias(7)

        self.boton_crear = self.moldes.crear_boton(
            self.panel,
            "Crear suscripcion",
            True,
            None,
            self.vista.crear_suscripcion,
            metodo="grid",
            fila=9,
            columna=0,
            columnas=2,
            sticky="ew",
            margen_y=(14, 0),
        )

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
            self.variables_dias.append(variable)
            tk.Checkbutton(
                contenedor,
                text=nombre,
                variable=variable,
                bg=tema.PANEL_SUAVE,
                fg=tema.TEXTO,
                selectcolor=tema.SECUNDARIO,
                activebackground=tema.PANEL_SUAVE,
                activeforeground=tema.TEXTO,
                font=("Arial", 9),
            ).pack(side="left", expand=True)

    def datos(self):
        return {
            "origen": self.origen.get(),
            "destino": self.destino.get(),
            "fecha_inicio": self.fecha_inicio.get(),
            "fecha_fin": self.fecha_fin.get(),
            "dias_semana": tuple(
                indice for indice, variable in enumerate(self.variables_dias)
                if variable.get()
            ),
            "hora": self.hora.get(),
            "cantidad_pasajeros": self.pasajeros.get(),
        }


class PanelGestionSuscripciones:
    def __init__(self, vista, padre):
        self.vista = vista
        self.moldes = vista.moldes
        self.suscripciones = {}
        self.viajes = {}
        self.panel = self.moldes.crear_frame(
            padre,
            tema.PANEL_SUAVE,
            tema.BORDE,
            1,
            16,
            16,
            fila=0,
            columna=1,
            sticky="nsew",
            margen_x=(8, 0),
            columnas_peso=((0, 1),),
            filas_peso=((1, 1), (4, 1)),
        )
        self.moldes.crear_label(self.panel, "Mis suscripciones", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=0, sticky="w")
        self.tabla_suscripciones = self.moldes.crear_tabla(
            self.panel,
            (("ruta", "Ruta", 210), ("horario", "Horario", 120), ("estado", "Estado", 100)),
            alto=5,
            metodo="grid",
            fila=1,
            columna=0,
            sticky="nsew",
            margen_y=(8, 5),
        )
        acciones = self.moldes.crear_frame(self.panel, tema.PANEL_SUAVE, fila=2, columna=0, sticky="ew", margen_y=(3, 12))
        self.moldes.crear_boton(acciones, "Pausar / reanudar", False, None, self.vista.alternar_suscripcion, lado="left", margen_x=(0, 5))
        self.moldes.crear_boton(acciones, "Cancelar", False, None, self.vista.cancelar_suscripcion, lado="left", margen_x=5)

        self.moldes.crear_label(self.panel, "Viajes programados", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=3, columna=0, sticky="w")
        self.tabla_viajes = self.moldes.crear_tabla(
            self.panel,
            (("fecha", "Fecha y hora", 125), ("ruta", "Ruta", 180), ("estado", "Estado", 125), ("detalle", "Conductor / detalle", 170)),
            alto=6,
            metodo="grid",
            fila=4,
            columna=0,
            sticky="nsew",
            margen_y=(8, 5),
        )
        self.moldes.crear_boton(self.panel, "Cancelar viaje seleccionado", False, None, self.vista.cancelar_viaje, metodo="grid", fila=5, columna=0, sticky="e", margen_y=(5, 0))

    def actualizar(self, suscripciones, viajes):
        self.suscripciones = {item.id_suscripcion: item for item in suscripciones}
        self.viajes = {item.id_viaje_programado: item for item in viajes}
        self._limpiar(self.tabla_suscripciones)
        self._limpiar(self.tabla_viajes)
        for item in suscripciones:
            dias = ",".join(NOMBRES_DIAS[dia] for dia in item.dias_semana)
            self.tabla_suscripciones.insert(
                "",
                "end",
                iid=item.id_suscripcion,
                values=(f"{item.origen} -> {item.destino}", f"{dias} {item.hora}", item.estado),
            )
        for item in viajes:
            detalle = item.conductor or item.error or "Pendiente"
            if item.precio:
                detalle = f"{detalle} - ${item.precio:,.0f}"
            self.tabla_viajes.insert(
                "",
                "end",
                iid=item.id_viaje_programado,
                values=(item.fecha_hora.replace("T", " "), f"{item.origen} -> {item.destino}", item.estado, detalle),
            )

    def suscripcion_seleccionada(self):
        seleccion = self.tabla_suscripciones.selection()
        return self.suscripciones.get(seleccion[0]) if seleccion else None

    def viaje_seleccionado(self):
        seleccion = self.tabla_viajes.selection()
        return self.viajes.get(seleccion[0]) if seleccion else None

    def _limpiar(self, tabla):
        for item in tabla.get_children():
            tabla.delete(item)


class VistaSuscripcionViaje(tk.Frame):
    def __init__(self, padre, navegar, controlador, usuario_actual, controlador_viaje):
        self.navegar = navegar
        self.controlador = controlador
        self.usuario_actual = usuario_actual
        self.moldes = Moldes()
        super().__init__(padre, bg=tema.FONDO)
        self.pack(fill="both", expand=True)
        self._crear_widgets(controlador_viaje.obtener_lugares_disponibles())
        self.actualizar_listados()
        self.after(30_000, self._refrescar_si_visible)

    def _crear_widgets(self, lugares):
        principal = self.moldes.crear_frame(self, tema.PANEL, tema.BORDE, 1, 22, 22, llenar="both", expandir=True, margen_x=24, margen_y=24, columnas_peso=((0, 1),), filas_peso=((1, 1),))
        cabecera = self.moldes.crear_frame(principal, tema.PANEL, fila=0, columna=0, sticky="ew", columnas_peso=((0, 1),))
        self.moldes.crear_label(cabecera, "Suscripcion de viaje", tema.FUENTE_TITULO, tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")
        self.moldes.crear_boton(cabecera, "Volver", False, None, lambda: self.navegar("menu"), metodo="grid", fila=0, columna=1, sticky="e")
        cuerpo = self.moldes.crear_frame(principal, tema.PANEL, fila=1, columna=0, sticky="nsew", margen_y=(16, 8), columnas_peso=((0, 2), (1, 3)), filas_peso=((0, 1),))
        self.formulario = FormularioSuscripcion(self, cuerpo, tuple(lugares))
        self.gestion = PanelGestionSuscripciones(self, cuerpo)
        self.mensaje = self.moldes.crear_label(principal, "El sistema revisa los horarios cada 30 segundos mientras la aplicacion esta abierta.", tema.FUENTE_TEXTO, tema.TEXTO_SUAVE, tema.PANEL, 900, "center", metodo="grid", fila=2, columna=0, sticky="ew")
        if getattr(self.usuario_actual, "tipo_usuario", "") != "pasajero":
            self.formulario.boton_crear.configure(state="disabled")
            self.mostrar_mensaje("Solo las cuentas de pasajero pueden crear suscripciones.", error=True)

    def crear_suscripcion(self):
        resultado = self.controlador.crear(self.usuario_actual, self.formulario.datos())
        if not resultado.exitoso:
            self.mostrar_mensaje(resultado.error, error=True)
            return
        self.mostrar_mensaje("Suscripcion creada y viajes programados correctamente.")
        self.actualizar_listados()

    def alternar_suscripcion(self):
        suscripcion = self.gestion.suscripcion_seleccionada()
        if suscripcion is None:
            self.mostrar_mensaje("Selecciona una suscripcion.", error=True)
            return
        nuevo_estado = ESTADO_PAUSADA if suscripcion.estado == ESTADO_ACTIVA else ESTADO_ACTIVA
        resultado = self.controlador.cambiar_estado(self.usuario_actual, suscripcion.id_suscripcion, nuevo_estado)
        self._finalizar_accion(resultado, f"Suscripcion en estado {nuevo_estado}.")

    def cancelar_suscripcion(self):
        suscripcion = self.gestion.suscripcion_seleccionada()
        if suscripcion is None:
            self.mostrar_mensaje("Selecciona una suscripcion.", error=True)
            return
        if not messagebox.askyesno("Cancelar suscripcion", "Se cancelaran todos sus viajes pendientes. Continuar?"):
            return
        resultado = self.controlador.cambiar_estado(self.usuario_actual, suscripcion.id_suscripcion, "CANCELADA")
        self._finalizar_accion(resultado, "Suscripcion cancelada.")

    def cancelar_viaje(self):
        viaje = self.gestion.viaje_seleccionado()
        if viaje is None:
            self.mostrar_mensaje("Selecciona un viaje programado.", error=True)
            return
        resultado = self.controlador.cancelar_viaje(self.usuario_actual, viaje.id_viaje_programado)
        self._finalizar_accion(resultado, "Viaje programado cancelado.")

    def _finalizar_accion(self, resultado, mensaje):
        if not resultado.exitoso:
            self.mostrar_mensaje(resultado.error, error=True)
            return
        self.mostrar_mensaje(mensaje)
        self.actualizar_listados()

    def actualizar_listados(self):
        resultado_suscripciones = self.controlador.listar(self.usuario_actual)
        resultado_viajes = self.controlador.listar_viajes(self.usuario_actual)
        if not resultado_suscripciones.exitoso or not resultado_viajes.exitoso:
            self.mostrar_mensaje(resultado_suscripciones.error or resultado_viajes.error, error=True)
            return
        self.gestion.actualizar(resultado_suscripciones.datos, resultado_viajes.datos)

    def mostrar_mensaje(self, texto, error=False):
        self.mensaje.configure(text=texto, fg=tema.ERROR if error else tema.EXITO)

    def _refrescar_si_visible(self):
        if not self.winfo_exists():
            return
        self.actualizar_listados()
        self.after(30_000, self._refrescar_si_visible)
