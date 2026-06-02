from PIL import Image, ImageTk

from Servicios.Viajes.datos_viaje import LUGARES_OSORNO
from Servicios.Viajes.trayectoria import Trayectoria


class AnimacionViaje:
    def __init__(self):
        self.trayectoria = Trayectoria()

    def animacion_viaje_conductor(
        self,
        mapa,
        marcadores_lugares,
        ruta_imagenes_usuarios,
        datos_pasajero,
        barra_progreso,
        label_estado,
        label_porcentaje,
        al_terminar_viaje,
    ):
        self._limpiar_marcadores_lugares(marcadores_lugares)

        ruta_llegada = self._ruta_real(
            datos_pasajero["ubicacion_conductor"],
            datos_pasajero["ubicacion_inicial"],
        )
        ruta_viaje = self._ruta_real(
            datos_pasajero["ubicacion_inicial"],
            datos_pasajero["ubicacion_final"],
        )

        imagen = Image.open(ruta_imagenes_usuarios / datos_pasajero["imagen"])
        imagen.thumbnail((46, 46))
        foto_pasajero = ImageTk.PhotoImage(imagen)
        mapa.imagen_pasajero_viaje = foto_pasajero

        marcador_inicio = mapa.set_marker(
            *ruta_llegada[-1],
            text="Ubicacion inicial",
        )
        self._ocultar_simbolo_marcador(mapa, marcador_inicio)
        marcador_destino = mapa.set_marker(*ruta_viaje[-1], text="Ubicacion deseada")
        self._ocultar_simbolo_marcador(mapa, marcador_destino)

        marcador_pasajero = mapa.set_marker(
            *ruta_llegada[-1],
            text=datos_pasajero["nombre_completo"],
            icon=foto_pasajero,
            image_zoom_visibility=(0, float("inf")),
        )

        self._animar_ruta(
            mapa,
            None,
            ruta_llegada,
            max(1, datos_pasajero["tiempo_para_llegar"]),
            barra_progreso,
            label_estado,
            label_porcentaje,
            "Llegando al punto de partida",
            lambda: self._animar_ruta(
                mapa,
                marcador_pasajero,
                ruta_viaje,
                max(1, datos_pasajero["tiempo_transportando"]),
                barra_progreso,
                label_estado,
                label_porcentaje,
                "Transportando pasajero",
                al_terminar_viaje,
            ),
        )
        mapa.marcador_inicio_viaje = marcador_inicio
        mapa.marcador_destino_viaje = marcador_destino

    def animacion_viaje_pasajero(
        self,
        mapa,
        marcadores_conductores,
        ruta_imagenes_conductores,
        datos_vehiculo,
        ubicacion_inicial,
        ubicacion_final,
        barra_progreso,
        label_estado,
        label_porcentaje,
        al_terminar_viaje,
        ruta_llegada=None,
        ruta_viaje=None,
    ):
        self._limpiar_marcadores_lugares(marcadores_conductores)

        if ruta_llegada is None:
            ruta_llegada = self._ruta_relativa_real(
                datos_vehiculo["ubicacion_relativa"],
                LUGARES_OSORNO[ubicacion_inicial],
            )
        if ruta_viaje is None:
            ruta_viaje = self._ruta_real(ubicacion_inicial, ubicacion_final)

        imagen = Image.open(ruta_imagenes_conductores / datos_vehiculo["imagen"])
        imagen.thumbnail((46, 46))
        foto_conductor = ImageTk.PhotoImage(imagen)
        mapa.imagen_conductor_viaje = foto_conductor

        mapa.set_path(ruta_llegada, color="#f59e0b", width=5)
        mapa.set_path(ruta_viaje, color="#1a73e8", width=5)

        marcador_inicio = mapa.set_marker(*ruta_llegada[-1], text="Ubicacion inicial")
        self._ocultar_simbolo_marcador(mapa, marcador_inicio)
        marcador_destino = mapa.set_marker(*ruta_viaje[-1], text="Ubicacion final")
        self._ocultar_simbolo_marcador(mapa, marcador_destino)
        marcador_conductor = mapa.set_marker(
            *ruta_llegada[0],
            text=datos_vehiculo["nombre_completo"],
            icon=foto_conductor,
            image_zoom_visibility=(0, float("inf")),
        )

        self._animar_ruta(
            mapa,
            marcador_conductor,
            ruta_llegada,
            max(1, datos_vehiculo["tiempo"]),
            barra_progreso,
            label_estado,
            label_porcentaje,
            "Conductor en camino",
            lambda: self._animar_ruta(
                mapa,
                marcador_conductor,
                ruta_viaje,
                max(1, datos_vehiculo["tiempo"]),
                barra_progreso,
                label_estado,
                label_porcentaje,
                "Viajando al destino",
                al_terminar_viaje,
            ),
        )
        mapa.marcador_inicio_viaje = marcador_inicio
        mapa.marcador_destino_viaje = marcador_destino

    def _limpiar_marcadores_lugares(self, marcadores_lugares):
        for marcador in marcadores_lugares:
            try:
                marcador.delete()
            except AttributeError:
                pass
        marcadores_lugares.clear()

    def _ruta_real(self, ubicacion_inicial, ubicacion_final):
        ruta_relativa = self.trayectoria.calcular_trayectoria(
            LUGARES_OSORNO[ubicacion_inicial],
            LUGARES_OSORNO[ubicacion_final],
        )
        return [self.trayectoria.coordenada_real(punto) for punto in ruta_relativa]

    def _ruta_relativa_real(self, inicio, destino):
        ruta_relativa = self.trayectoria.calcular_trayectoria(inicio, destino)
        return [self.trayectoria.coordenada_real(punto) for punto in ruta_relativa]

    def _ocultar_simbolo_marcador(self, mapa, marcador):
        def ocultar():
            for atributo in ("polygon", "big_circle", "canvas_icon", "canvas_image", "canvas_marker", "canvas_circle"):
                item = getattr(marcador, atributo, None)
                if item is not None:
                    mapa.canvas.itemconfigure(item, state="hidden")

        ocultar()
        mapa.after(100, ocultar)

    def _animar_ruta(
        self,
        mapa,
        marcador,
        ruta,
        duracion,
        barra_progreso,
        label_estado,
        label_porcentaje,
        estado,
        al_finalizar,
        indice=0,
    ):
        try:
            self._animar_ruta_segura(
                mapa,
                marcador,
                ruta,
                duracion,
                barra_progreso,
                label_estado,
                label_porcentaje,
                estado,
                al_finalizar,
                indice,
            )
        except Exception:
            label_estado.config(text="No se pudo continuar la animacion")
            if al_finalizar:
                barra_progreso.after(600, al_finalizar)

    def _animar_ruta_segura(
        self,
        mapa,
        marcador,
        ruta,
        duracion,
        barra_progreso,
        label_estado,
        label_porcentaje,
        estado,
        al_finalizar,
        indice=0,
    ):
        if not ruta:
            return

        progreso = int((indice / max(1, len(ruta) - 1)) * 100)
        barra_progreso["value"] = progreso
        label_estado.config(text=estado)
        label_porcentaje.config(text=f"{progreso}%")

        if marcador is not None:
            latitud, longitud = ruta[indice]
            try:
                marcador.set_position(latitud, longitud)
            except AttributeError:
                marcador.delete()
                marcador = mapa.set_marker(latitud, longitud)

        if indice >= len(ruta) - 1:
            barra_progreso["value"] = 100
            label_porcentaje.config(text="100%")
            if al_finalizar:
                barra_progreso.after(600, al_finalizar)
            return

        intervalo = max(120, int((duracion * 1000) / max(1, len(ruta) - 1)))
        barra_progreso.after(
            intervalo,
            lambda: self._animar_ruta(
                mapa,
                marcador,
                ruta,
                duracion,
                barra_progreso,
                label_estado,
                label_porcentaje,
                estado,
                al_finalizar,
                indice + 1,
            ),
        )
        #.
