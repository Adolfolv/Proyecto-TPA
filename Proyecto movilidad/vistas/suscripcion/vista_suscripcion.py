import tkinter as tk
from tkinter import messagebox

from Modelos.Suscripcion.modelos_suscripcion import ESTADO_ACTIVA, ESTADO_PAUSADA
from ..estilizacion import tema
from ..estilizacion.decoraciones import crear_panel_mensaje_registro
from ..estilizacion.widgets import Moldes
from .estado_visual_suscripcion import (
    EstadoConfirmacionPago,
    EstadoCotizacion,
    EstadoFormulario,
    EstadoProcesandoPago,
    FlujoVisualSuscripcion,
)
from .formulario_suscripcion import FormularioSuscripcion
from .panel_gestion import PanelGestionSuscripciones
from .tarjeta_resumen import TarjetaResumenSuscripcion


class VistaSuscripcionViaje(tk.Frame):
    """Orquesta componentes visuales y traduce acciones hacia el controlador."""

    def __init__(self, padre, navegar, controlador, usuario_actual, controlador_viaje):
        self.navegar = navegar
        self.controlador = controlador
        self.usuario_actual = usuario_actual
        self.moldes = Moldes()
        self.datos_pendientes = None
        self.resumen_pendiente = None
        super().__init__(padre, bg=tema.FONDO)
        self.pack(fill="both", expand=True)
        self._crear_widgets(tuple(controlador_viaje.obtener_lugares_disponibles()))
        self.flujo = FlujoVisualSuscripcion(self)
        self.flujo.cambiar(EstadoFormulario)
        self.actualizar_listados()
        if getattr(self.usuario_actual, "tipo_usuario", "") != "pasajero":
            self.formulario.habilitar(False)
            self.mostrar_mensaje(
                "Solo las cuentas de pasajero pueden crear suscripciones."
            )
        self.after(30_000, self._refrescar_si_visible)

    def _crear_widgets(self, lugares):
        principal = self.moldes.crear_frame(
            self,
            tema.PANEL,
            tema.BORDE,
            1,
            22,
            22,
            llenar="both",
            expandir=True,
            margen_x=24,
            margen_y=24,
            columnas_peso=((0, 1),),
            filas_peso=((1, 1),),
        )
        cabecera = self.moldes.crear_frame(
            principal,
            tema.PANEL,
            fila=0,
            columna=0,
            sticky="ew",
            columnas_peso=((0, 1),),
        )
        self.moldes.crear_label(
            cabecera,
            "Suscripcion de viaje",
            tema.FUENTE_TITULO,
            tema.TEXTO,
            tema.PANEL,
            metodo="grid",
            fila=0,
            columna=0,
            sticky="w",
        )
        self.moldes.crear_boton(
            cabecera,
            "Volver",
            False,
            None,
            lambda: self.navegar("menu"),
            metodo="grid",
            fila=0,
            columna=1,
            sticky="e",
        )
        cuerpo = self.moldes.crear_frame(
            principal,
            tema.PANEL,
            fila=1,
            columna=0,
            sticky="nsew",
            margen_y=(16, 8),
            columnas_peso=((0, 2), (1, 3)),
            filas_peso=((0, 1),),
        )
        creacion = self.moldes.crear_frame(
            cuerpo,
            tema.PANEL,
            fila=0,
            columna=0,
            sticky="nsew",
            margen_x=(0, 8),
            columnas_peso=((0, 1),),
            filas_peso=((0, 1),),
        )
        self.formulario = FormularioSuscripcion(
            creacion, self.moldes, lugares, self.previsualizar_suscripcion
        )
        self.tarjeta = TarjetaResumenSuscripcion(
            creacion,
            self.moldes,
            {
                "editar": self.editar_datos,
                "pagar": self.solicitar_confirmacion_pago,
                "confirmar": self.confirmar_pago,
                "cancelar": self.cancelar_alta,
            },
        )
        self.gestion = PanelGestionSuscripciones(
            cuerpo,
            self.moldes,
            {
                "alternar": self.alternar_suscripcion,
                "cancelar_suscripcion": self.cancelar_suscripcion,
                "cancelar_viaje": self.cancelar_viaje,
            },
        )
        area_mensaje = self.moldes.crear_frame(
            principal,
            tema.PANEL,
            fila=2,
            columna=0,
            sticky="ew",
        )
        self.mostrar_mensaje = crear_panel_mensaje_registro(
            area_mensaje, compacto=True
        )

    def previsualizar_suscripcion(self):
        datos = self.formulario.datos()
        resultado = self.controlador.previsualizar(self.usuario_actual, datos)
        if not resultado.exitoso:
            self.mostrar_mensaje(f"Revisa este dato: {resultado.error}")
            return
        self.datos_pendientes = datos
        self.resumen_pendiente = resultado.datos
        self.tarjeta.actualizar(resultado.datos)
        self.flujo.cambiar(EstadoCotizacion)
        self.mostrar_mensaje(
            "Cotizacion generada. Revisa los datos antes de pagar.", True
        )

    def editar_datos(self):
        self.flujo.cambiar(EstadoFormulario)

    def solicitar_confirmacion_pago(self):
        self.flujo.cambiar(EstadoConfirmacionPago)
        self.mostrar_mensaje(
            "Confirma el pago para activar y guardar la suscripcion.", True
        )

    def confirmar_pago(self):
        if self.datos_pendientes is None:
            self.flujo.cambiar(EstadoFormulario)
            return
        self.flujo.cambiar(EstadoProcesandoPago)
        resultado = self.controlador.confirmar(
            self.usuario_actual, self.datos_pendientes
        )
        if not resultado.exitoso:
            self.flujo.cambiar(EstadoConfirmacionPago)
            self.mostrar_mensaje(f"No se pudo pagar: {resultado.error}")
            return
        self.datos_pendientes = None
        self.resumen_pendiente = None
        self.flujo.cambiar(EstadoFormulario)
        self.actualizar_listados()
        self.mostrar_mensaje(
            "Pago realizado. La suscripcion ya aparece en tus listados.", True
        )

    def cancelar_alta(self):
        self.datos_pendientes = None
        self.resumen_pendiente = None
        self.flujo.cambiar(EstadoFormulario)
        self.mostrar_mensaje(
            "Suscripcion cancelada antes del pago. No se realizo ningun cobro.", True
        )

    def alternar_suscripcion(self):
        suscripcion = self.gestion.suscripcion_seleccionada()
        if suscripcion is None:
            self.mostrar_mensaje("Revisa este dato: selecciona una suscripcion.")
            return
        nuevo_estado = (
            ESTADO_PAUSADA
            if suscripcion.estado == ESTADO_ACTIVA
            else ESTADO_ACTIVA
        )
        resultado = self.controlador.cambiar_estado(
            self.usuario_actual, suscripcion.id_suscripcion, nuevo_estado
        )
        self._finalizar_accion(
            resultado, f"Suscripcion en estado {nuevo_estado}."
        )

    def cancelar_suscripcion(self):
        suscripcion = self.gestion.suscripcion_seleccionada()
        if suscripcion is None:
            self.mostrar_mensaje("Revisa este dato: selecciona una suscripcion.")
            return
        if not messagebox.askyesno(
            "Cancelar suscripcion",
            "Se cancelaran y reembolsaran sus viajes pendientes. Continuar?",
        ):
            return
        resultado = self.controlador.cambiar_estado(
            self.usuario_actual, suscripcion.id_suscripcion, "CANCELADA"
        )
        self._finalizar_accion(
            resultado, "Suscripcion cancelada y viajes pendientes reembolsados."
        )

    def cancelar_viaje(self):
        viaje = self.gestion.viaje_seleccionado()
        if viaje is None:
            self.mostrar_mensaje("Revisa este dato: selecciona un viaje programado.")
            return
        resultado = self.controlador.cancelar_viaje(
            self.usuario_actual, viaje.id_viaje_programado
        )
        self._finalizar_accion(
            resultado, "Viaje cancelado y monto reembolsado."
        )

    def _finalizar_accion(self, resultado, mensaje):
        if not resultado.exitoso:
            self.mostrar_mensaje(f"Revisa este dato: {resultado.error}")
            return
        self.actualizar_listados()
        self.mostrar_mensaje(mensaje, True)

    def actualizar_listados(self):
        resultado_suscripciones = self.controlador.listar(self.usuario_actual)
        resultado_viajes = self.controlador.listar_viajes(self.usuario_actual)
        if not resultado_suscripciones.exitoso or not resultado_viajes.exitoso:
            self.mostrar_mensaje(
                resultado_suscripciones.error or resultado_viajes.error
            )
            return
        self.gestion.actualizar(
            resultado_suscripciones.datos, resultado_viajes.datos
        )

    def _refrescar_si_visible(self):
        if not self.winfo_exists():
            return
        self.actualizar_listados()
        self.after(30_000, self._refrescar_si_visible)
