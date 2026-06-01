from math import asin, cos, radians, sin, sqrt
from random import choice, randint

import tkinter as tk
from PIL import Image, ImageTk

from Servicios.Viajes.datos_viaje import LUGARES_OSORNO, PASAJEROS_SIMULADOS
from Servicios.Viajes.trayectoria import calcular_trayectoria, coordenada_real


class ServicioViaje:

    def buscar_pasajeros(
        self,
        ubicacion_inicial,
        boton_buscar_pasajeros,
        selector_ubicacion,
        label_cronometro,
        frame_pasajero,
        ruta_imagenes_usuarios,
        moldes,
        tema,
        al_finalizar,
    ):
        pasajero = choice(PASAJEROS_SIMULADOS)
        datos_pasajero = self.obtener_datos_pasajero(pasajero, ubicacion_inicial)
        duracion_busqueda = randint(5, 10)
        boton_buscar_pasajeros.config(state="disabled", cursor="arrow")
        selector_ubicacion.config(state="disabled")
        self.actualizar_cronometro(
            label_cronometro,
            duracion_busqueda,
            frame_pasajero,
            pasajero,
            datos_pasajero,
            ruta_imagenes_usuarios,
            moldes,
            tema,
            al_finalizar,
        )
        return datos_pasajero

    def obtener_datos_pasajero(self, pasajero, ubicacion_conductor):
        distancias = self.calcular_km_viaje(ubicacion_conductor, pasajero)
        tiempos = self.calcular_tiempos_viaje(
            distancias["km_para_llegar"],
            distancias["km_transportando"],
        )
        return {
            "nombre_completo": f"{pasajero['nombre']} {pasajero['apellido']}",
            "vehiculo": f"{pasajero['marca_vehiculo']} {pasajero['modelo_vehiculo']}",
            "trayecto": f"{pasajero['ubicacion_inicial']} -> {pasajero['ubicacion_final']}",
            "ubicacion_inicial": pasajero["ubicacion_inicial"],
            "ubicacion_final": pasajero["ubicacion_final"],
            **distancias,
            **tiempos,
        }

    def calcular_km_viaje(self, ubicacion_conductor, pasajero):
        ruta_llegada = calcular_trayectoria(
            LUGARES_OSORNO[ubicacion_conductor],
            LUGARES_OSORNO[pasajero["ubicacion_inicial"]],
        )
        ruta_transporte = calcular_trayectoria(
            LUGARES_OSORNO[pasajero["ubicacion_inicial"]],
            LUGARES_OSORNO[pasajero["ubicacion_final"]],
        )
        return {
            "km_para_llegar": round(self.calcular_km_trayectoria(ruta_llegada), 2),
            "km_transportando": round(self.calcular_km_trayectoria(ruta_transporte), 2),
        }

    def calcular_tiempos_viaje(self, km_para_llegar, km_transportando):
        distancia_total = km_para_llegar + km_transportando
        if distancia_total <= 0:
            return {
                "tiempo_para_llegar": 0,
                "tiempo_transportando": 0,
            }
        if km_para_llegar <= 0:
            return {
                "tiempo_para_llegar": 0,
                "tiempo_transportando": 20,
            }
        if km_transportando <= 0:
            return {
                "tiempo_para_llegar": 20,
                "tiempo_transportando": 0,
            }

        tiempo_para_llegar = round(20 * (km_para_llegar / distancia_total))
        tiempo_para_llegar = min(19, max(1, tiempo_para_llegar))
        tiempo_transportando = 20 - tiempo_para_llegar
        return {
            "tiempo_para_llegar": tiempo_para_llegar,
            "tiempo_transportando": tiempo_transportando,
        }

    def calcular_km_trayectoria(self, ruta_relativa):
        if len(ruta_relativa) < 2:
            return 0

        distancia = 0
        for inicio, destino in zip(ruta_relativa, ruta_relativa[1:]):
            distancia += self.calcular_km_entre_coordenadas(
                coordenada_real(inicio),
                coordenada_real(destino),
            )
        return distancia

    def calcular_km_entre_coordenadas(self, inicio, destino):
        latitud_inicio, longitud_inicio = inicio
        latitud_destino, longitud_destino = destino
        radio_tierra = 6371
        diferencia_latitud = radians(latitud_destino - latitud_inicio)
        diferencia_longitud = radians(longitud_destino - longitud_inicio)
        a = (
            sin(diferencia_latitud / 2) ** 2
            + cos(radians(latitud_inicio))
            * cos(radians(latitud_destino))
            * sin(diferencia_longitud / 2) ** 2
        )
        return 2 * radio_tierra * asin(sqrt(a))

    def formar_trayectoria(self, mapa, ubicacion_inicial, ubicacion_final):
        inicio = LUGARES_OSORNO[ubicacion_inicial]
        destino = LUGARES_OSORNO[ubicacion_final]
        ruta_relativa = calcular_trayectoria(inicio, destino)
        ruta_real = [coordenada_real(punto) for punto in ruta_relativa]
        return mapa.set_path(ruta_real, color="#1a73e8", width=5)

    def actualizar_cronometro(
        self,
        label_cronometro,
        duracion_busqueda,
        frame_pasajero,
        pasajero,
        datos_pasajero,
        ruta_imagenes_usuarios,
        moldes,
        tema,
        al_finalizar,
        segundos_transcurridos=0,
    ):
        label_cronometro.config(text=f"00:{segundos_transcurridos:02d}")

        if segundos_transcurridos < duracion_busqueda:
            label_cronometro.after(
                1000,
                lambda: self.actualizar_cronometro(
                    label_cronometro,
                    duracion_busqueda,
                    frame_pasajero,
                    pasajero,
                    datos_pasajero,
                    ruta_imagenes_usuarios,
                    moldes,
                    tema,
                    al_finalizar,
                    segundos_transcurridos + 1,
                ),
            )
            return

        self.mostrar_pasajeros(
            frame_pasajero,
            pasajero,
            datos_pasajero,
            ruta_imagenes_usuarios,
            moldes,
            tema,
            al_finalizar,
        )

    def mostrar_pasajeros(self, frame_pasajero, pasajero, datos_pasajero, ruta_imagenes_usuarios, moldes, tema, al_finalizar):
        for widget in frame_pasajero.winfo_children():
            widget.destroy()

        imagen = Image.open(ruta_imagenes_usuarios / pasajero["imagen"])
        imagen.thumbnail((64, 64))
        imagen_pasajero = ImageTk.PhotoImage(imagen)
        frame_pasajero.imagen_pasajero = imagen_pasajero

        foto = tk.Label(frame_pasajero, image=imagen_pasajero, bg=tema.PANEL_SUAVE)
        foto.grid(row=0, column=0, rowspan=4, sticky="nw", padx=10, pady=10)

        nombre_completo = f"{pasajero['nombre']} {pasajero['apellido']}"
        vehiculo = f"{pasajero['marca_vehiculo']} {pasajero['modelo_vehiculo']}"
        trayecto = f"{pasajero['ubicacion_inicial']} -> {pasajero['ubicacion_final']}"
        pago = f"${pasajero['pago']}"
        llegada = f"Llegar: {datos_pasajero['km_para_llegar']} km | {datos_pasajero['tiempo_para_llegar']} s"
        traslado = f"Traslado: {datos_pasajero['km_transportando']} km | {datos_pasajero['tiempo_transportando']} s"

        moldes.crear_label(frame_pasajero, nombre_completo, ("Arial", 12, "bold"), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=0, columna=1, sticky="w", margen_x=8, margen_y=(10, 2))
        moldes.crear_label(frame_pasajero, trayecto, ("Arial", 9), tema.TEXTO, tema.PANEL_SUAVE, 300, "left", metodo="grid", fila=1, columna=1, sticky="w", margen_x=8)
        moldes.crear_label(frame_pasajero, f"Vehiculo: {vehiculo}", ("Arial", 9), tema.TEXTO_SUAVE, tema.PANEL_SUAVE, metodo="grid", fila=2, columna=1, sticky="w", margen_x=8)
        moldes.crear_label(frame_pasajero, f"Pago: {pago}", ("Arial", 9, "bold"), tema.PRIMARIO, tema.PANEL_SUAVE, metodo="grid", fila=3, columna=1, sticky="w", margen_x=8, margen_y=(0, 10))
        moldes.crear_label(frame_pasajero, llegada, ("Arial", 9), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=4, columna=0, columnas=2, sticky="w", margen_x=10, margen_y=(0, 2))
        moldes.crear_label(frame_pasajero, traslado, ("Arial", 9), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", fila=5, columna=0, columnas=2, sticky="w", margen_x=10, margen_y=(0, 10))
        al_finalizar()
        return imagen_pasajero
