"""Tema visual comun para las vistas."""

from abc import ABC, abstractmethod

from .constantes_vistas import (FUENTE_BOTON,FUENTE_LOGIN_BOTON,FUENTE_LOGIN_CAMPO,FUENTE_LOGIN_ENTRADA,FUENTE_LOGIN_TEXTO,FUENTE_LOGIN_TITULO,FUENTE_SUBTITULO,FUENTE_TEXTO,FUENTE_TITULO,)


class Tema(ABC):
    """Base para agregar nuevos temas sin cambiar las vistas."""

    nombre = ""

    @abstractmethod
    def colores(self):
        pass


class TemaOscuro(Tema):
    nombre = "oscuro"

    def colores(self):
        return {
            "FONDO": "#111827",
            "PANEL": "#1f2937",
            "PANEL_SUAVE": "#273449",
            "TEXTO": "#f9fafb",
            "TEXTO_SUAVE": "#cbd5e1",
            "PRIMARIO": "#3b82f6",
            "PRIMARIO_TEXTO": "#ffffff",
            "SECUNDARIO": "#374151",
            "BORDE": "#4b5563",
            "ERROR": "#ef4444",
            "ERROR_FONDO": "#3b1f2a",
            "EXITO": "#22c55e",
            "EXITO_FONDO": "#1d3a2a",
        }


class TemaClaro(Tema):
    nombre = "claro"

    def colores(self):
        return {
            "FONDO": "#f4f7fb",
            "PANEL": "#ffffff",
            "PANEL_SUAVE": "#eef3f8",
            "TEXTO": "#1f2937",
            "TEXTO_SUAVE": "#475569",
            "PRIMARIO": "#2563eb",
            "PRIMARIO_TEXTO": "#ffffff",
            "SECUNDARIO": "#dfe7f1",
            "BORDE": "#cbd5e1",
            "ERROR": "#dc2626",
            "ERROR_FONDO": "#fee2e2",
            "EXITO": "#15803d",
            "EXITO_FONDO": "#dcfce7",
        }


class TemaAzul(Tema):
    nombre = "azul"

    def colores(self):
        return {
            "FONDO": "#0f172a",
            "PANEL": "#172554",
            "PANEL_SUAVE": "#1e3a8a",
            "TEXTO": "#eff6ff",
            "TEXTO_SUAVE": "#bfdbfe",
            "PRIMARIO": "#38bdf8",
            "PRIMARIO_TEXTO": "#082f49",
            "SECUNDARIO": "#1d4ed8",
            "BORDE": "#60a5fa",
            "ERROR": "#f87171",
            "ERROR_FONDO": "#450a0a",
            "EXITO": "#4ade80",
            "EXITO_FONDO": "#052e16",
        }


_temas = [TemaOscuro(), TemaClaro(), TemaAzul()]
_indice_tema = 0
_tema_actual = _temas[_indice_tema]


# FLUJO TEMA 2: Llega desde los botones de pantalla_inicial.py, menu.py o
# admin/panel_admin.py. Actualiza estas constantes; el siguiente paso vuelve
# a navegacion para reconstruir la pantalla que llamo al cambio.
def _actualizar_constantes():
    globals().update(_tema_actual.colores())


def alternar_tema():
    global _indice_tema, _tema_actual

    _indice_tema += 1

    if _indice_tema >= len(_temas):
        _indice_tema = 0

    _tema_actual = _temas[_indice_tema]

    _actualizar_constantes()
    return _tema_actual.nombre


def nombre_actual():
    return _tema_actual.nombre


def texto_boton():
    indice_siguiente = _indice_tema + 1

    if indice_siguiente >= len(_temas):
        indice_siguiente = 0

    return f"Tema {_temas[indice_siguiente].nombre}"


_actualizar_constantes()
