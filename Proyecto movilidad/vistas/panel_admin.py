import tkinter as tk
from pathlib import Path

from PIL import Image, ImageOps, ImageTk

from .estilizacion import tema
from .estilizacion.decoraciones import crear_logo_admin, crear_panel_confirmacion_admin
from .estilizacion.widgets import Moldes


class PanelInicioAdmin:
    """Pantalla inicial con accesos a pasajeros y conductores."""

    def __init__(self, vista):
        self.vista = vista
        self.moldes = vista.moldes

    def crear(self):
        vista = self.vista
        vista.limpiar_contenido()
        vista.configurar_cabecera("Panel administrador", "Cerrar sesión", vista.acciones.presionar_boton_cerrar_sesion, tema.texto_boton(), vista.acciones.presionar_boton_cambiar_tema)
        vista.contenido.grid_rowconfigure(0, weight=1)
        conteo = vista.controlador_admin.contar_por_tipo()
        centro = self.moldes.crear_frame(vista.contenido, tema.PANEL, fila=0, columna=0, sticky="nsew", columnas_peso=((0, 1), (1, 1)), filas_peso=((0, 1),))

        # La pantalla inicial separa las secciones administrativas sin tocar
        # el menu normal de pasajeros/conductores.
        secciones = (
            ("pasajero", "Pasajeros", tema.ADMIN_PASAJERO, "Revisa cuentas de usuarios que solicitan viajes."),
            ("conductor", "Conductores", tema.ADMIN_CONDUCTOR, "Consulta conductores, licencias y datos del vehículo."),
        )
        for columna, (tipo, titulo, color, descripcion) in enumerate(secciones):
            self.crear_tarjeta_seccion(centro, columna, tipo, titulo, color, descripcion, conteo)

    def crear_tarjeta_seccion(self, padre, columna, tipo, titulo, color, descripcion, conteo):
        vista = self.vista
        tarjeta = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, tema.BORDE, 1, 24, 24, fila=0, columna=columna, sticky="nsew", margen_x=10, margen_y=28, columnas_peso=((0, 1),), filas_peso=((0, 1), (1, 0), (2, 1)))
        contenido = self.moldes.crear_frame(tarjeta, tema.PANEL_SUAVE, fila=1, columna=0, sticky="ew", columnas_peso=((0, 1),))
        crear_logo_admin(contenido, tipo, color, tema.PANEL_SUAVE).grid(row=0, column=0, pady=(0, 18))
        self.moldes.crear_label(contenido, titulo, ("Arial", 26, "bold"), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", row=1, column=0, sticky="")
        self.moldes.crear_label(contenido, "registrados", ("Arial", 16, "bold"), tema.TEXTO_SUAVE, tema.PANEL_SUAVE, metodo="grid", row=2, column=0, sticky="", pady=(22, 0))
        self.moldes.crear_label(contenido, str(conteo.get(tipo, 0)), ("Arial", 58, "bold"), color, tema.PANEL_SUAVE, metodo="grid", row=3, column=0, sticky="")
        self.moldes.crear_label(contenido, descripcion, ("Arial", 13), tema.TEXTO_SUAVE, tema.PANEL_SUAVE, 260, "center", metodo="grid", row=4, column=0, sticky="ew", pady=(22, 28))
        boton = self.moldes.crear_boton(contenido, "Abrir", True, 18, lambda: vista.acciones.presionar_boton_abrir_seccion(tipo, titulo))
        boton.configure(font=("Arial", 15, "bold"), bg=color, fg=tema.ADMIN_ACENTO_TEXTO, activebackground=color, activeforeground=tema.ADMIN_ACENTO_TEXTO, padx=28, pady=16)
        boton.grid(row=5, column=0, ipadx=28, ipady=6)


class PanelListadoAdmin:
    """Listado scrolleable de usuarios de una seccion."""

    def __init__(self, vista):
        self.vista = vista
        self.moldes = vista.moldes

    def crear(self, tipo_usuario, titulo):
        vista = self.vista
        vista.limpiar_contenido()
        vista.tipo_actual = tipo_usuario
        vista.titulo_actual = titulo
        vista.configurar_cabecera(titulo, "Volver", vista.acciones.presionar_boton_volver)
        vista.contenido.grid_rowconfigure(0, weight=0)
        vista.contenido.grid_rowconfigure(1, weight=1)
        vista.contenido.grid_rowconfigure(2, weight=0)
        vista.mostrar_confirmacion = crear_panel_confirmacion_admin(vista.contenido, fila=2)
        usuarios = vista.controlador_admin.listar_por_tipo(tipo_usuario)

        zona = self.moldes.crear_frame(vista.contenido, tema.PANEL, fila=1, columna=0, sticky="nsew", margen_y=(8, 0), columnas_peso=((0, 1),), filas_peso=((0, 1),))
        canvas = tk.Canvas(zona, bg=tema.PANEL, highlightthickness=0)
        scroll = tk.Scrollbar(zona, orient="vertical", command=canvas.yview)
        listado = self.moldes.crear_frame(canvas, tema.PANEL, columnas_peso=((0, 1),))
        ventana_listado = canvas.create_window((0, 0), window=listado, anchor="nw")
        listado.bind("<Configure>", lambda evento: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda evento: self.ajustar_ancho_listado(canvas, ventana_listado, evento.width))
        canvas.configure(yscrollcommand=scroll.set)
        canvas.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")

        if not usuarios:
            self.moldes.crear_label(listado, "No hay usuarios registrados en esta sección.", tema.FUENTE_TEXTO, tema.TEXTO_SUAVE, tema.PANEL, metodo="grid", row=0, column=0, sticky="w")
            return

        # Cada usuario se muestra como tarjeta para dejar espacio a imagen y
        # datos, parecido a las tarjetas visuales usadas en el flujo de viaje.
        tarjeta_usuario = TarjetaUsuarioAdmin(vista)
        for fila, usuario in enumerate(usuarios):
            tarjeta_usuario.crear(listado, usuario, fila)

    def ajustar_ancho_listado(self, canvas, ventana_listado, ancho):
        self.vista.ancho_tarjeta = max(360, ancho - 18)
        canvas.itemconfigure(ventana_listado, width=self.vista.ancho_tarjeta)


class TarjetaUsuarioAdmin:
    """Tarjeta individual con foto, datos y acciones administrativas."""

    def __init__(self, vista):
        self.vista = vista
        self.moldes = vista.moldes

    def crear(self, padre, usuario, fila):
        tarjeta = self.crear_contenedor(padre, fila)
        self.crear_imagen_usuario(tarjeta, usuario).grid(row=0, column=0, sticky="nsew")
        cuerpo = self.moldes.crear_frame(tarjeta, tema.PANEL_SUAVE, fila=0, columna=1, sticky="nsew", margen_x=12, margen_y=8, columnas_peso=((0, 1),), filas_peso=((1, 1),))
        self.crear_nombre(cuerpo, usuario)
        self.crear_datos(cuerpo, usuario).grid(row=1, column=0, sticky="nsew")
        self.crear_acciones(tarjeta, usuario)

    def crear_contenedor(self, padre, fila):
        tarjeta = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, tema.BORDE, 1, fila=fila, columna=0, sticky="ew", margen_y=(0, 12), alto_fijo=188, columnas_peso=((1, 1),), filas_peso=((0, 1),))
        tarjeta.grid_propagate(False)
        tarjeta.grid_columnconfigure(0, minsize=188)
        tarjeta.grid_columnconfigure(1, weight=1)
        tarjeta.grid_columnconfigure(2, minsize=378)
        return tarjeta

    def crear_nombre(self, padre, usuario):
        nombre_completo = " ".join(parte for parte in (getattr(usuario, "nombre", ""), getattr(usuario, "apellido", "")) if parte)
        self.moldes.crear_label(padre, f"Nombre: {nombre_completo}", ("Arial", 17, "bold"), tema.TEXTO, tema.PANEL_SUAVE, metodo="grid", row=0, column=0, sticky="ew", pady=(0, 4))

    def crear_datos(self, padre, usuario):
        contenedor = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, columnas_peso=((0, 1),))
        grilla = self.moldes.crear_frame(contenedor, tema.PANEL_SUAVE)
        grilla.grid(row=0, column=0, sticky="n", pady=(0, 0))
        ancho_valor = max(190, (self.vista.ancho_tarjeta - 188 - 378 - 88) // 2)
        for indice, (etiqueta, valor) in enumerate(self.vista.controlador_admin.datos_usuario(usuario)):
            self.crear_dato(grilla, indice, etiqueta, valor, ancho_valor)
        return contenedor

    def crear_dato(self, padre, indice, etiqueta, valor, ancho_valor):
        fila = indice // 2
        columna = indice % 2
        margen_x = (0, 38) if columna == 0 else (38, 0)
        celda = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, fila=fila, columna=columna, sticky="ew", margen_x=margen_x, margen_y=(0, 4), columnas_peso=((0, 1),))
        self.moldes.crear_label(celda, f"{etiqueta}:", ("Arial", 12, "bold"), tema.TEXTO_SUAVE, tema.PANEL_SUAVE).pack(side="left", anchor="w")
        self.moldes.crear_label(celda, str(valor), ("Arial", 12), tema.TEXTO, tema.PANEL_SUAVE, ancho_valor, "left").pack(side="left", anchor="w", padx=(4, 0))

    def crear_acciones(self, padre, usuario):
        for widget in padre.grid_slaves(row=0, column=2):
            widget.destroy()

        acciones = self.moldes.crear_frame(padre, tema.PANEL_SUAVE, fila=0, columna=2, sticky="nsew", ancho_fijo=378, alto_fijo=188, columnas_peso=((0, 1), (1, 1)), filas_peso=((0, 1),))
        acciones.grid_propagate(False)
        cuenta_congelada = getattr(usuario, "cuenta_congelada", False)
        texto_estado = "Descongelar\ncuenta" if cuenta_congelada else "Congelar\ncuenta"
        accion_estado = self.vista.acciones.presionar_boton_descongelar_cuenta if cuenta_congelada else self.vista.acciones.presionar_boton_congelar_cuenta
        self.crear_boton_accion(acciones, texto_estado, tema.ADMIN_ACCION, tema.ADMIN_ACCION_ACTIVO, lambda usuario=usuario, tarjeta=padre: accion_estado(usuario, tarjeta), 0, (0, 1))
        self.crear_boton_accion(acciones, "Borrar\ncuenta", tema.ADMIN_PELIGRO, tema.ADMIN_PELIGRO_ACTIVO, lambda usuario=usuario, tarjeta=padre: self.vista.acciones.presionar_boton_eliminar_cuenta(usuario, tarjeta), 1, (1, 0))

    def crear_boton_accion(self, padre, texto, color, color_activo, comando, columna, margen_x):
        contenedor = self.moldes.crear_frame(padre, tema.BORDE, ancho_fijo=188, alto_fijo=188, fila=0, columna=columna, sticky="nsew", margen_x=margen_x)
        contenedor.grid_propagate(False)
        contenedor.pack_propagate(False)
        boton = self.moldes.crear_boton(contenedor, texto, False, None, comando, llenar="both", expandir=True, margen_x=2, margen_y=2)
        boton.configure(font=("Arial", 11, "bold"), bg=color, fg=tema.ADMIN_ACCION_TEXTO, activebackground=color_activo, activeforeground=tema.ADMIN_ACCION_TEXTO, wraplength=176, justify="center")
        return boton

    def crear_imagen_usuario(self, padre, usuario):
        contenedor = self.moldes.crear_frame(padre, tema.FONDO, ancho_fijo=188, alto_fijo=188)
        contenedor.grid_propagate(False)
        contenedor.pack_propagate(False)
        ruta = self.ruta_imagen_usuario(usuario)
        if ruta is not None and self.mostrar_imagen(contenedor, ruta):
            return contenedor

        self.moldes.crear_label(contenedor, "Sin\nfoto", ("Arial", 16, "bold"), tema.TEXTO_SUAVE, tema.FONDO, metodo="place", relx=0.5, rely=0.5, anchor="center")
        return contenedor

    def mostrar_imagen(self, padre, ruta):
        try:
            imagen = Image.open(ruta)
            imagen = ImageOps.fit(imagen, (188, 188), method=Image.LANCZOS)
            foto = ImageTk.PhotoImage(imagen)
            self.vista.imagenes_usuario.append(foto)
            tk.Label(padre, image=foto, bg=tema.FONDO, bd=0).pack(fill="both", expand=True)
            return True
        except (OSError, ValueError):
            return False

    def ruta_imagen_usuario(self, usuario):
        imagen = getattr(usuario, "selfie", "") or getattr(usuario, "imagen", "")
        if not imagen:
            return None

        ruta = Path(imagen)
        if ruta.exists():
            return ruta

        base = Path(__file__).resolve().parents[1] / "estilizacion" / "Imagenes"
        for carpeta in ("imagenes_usuarios", "imagenes_conductores"):
            candidata = base / carpeta / imagen
            if candidata.exists():
                return candidata

        return None

class AccionesBotonesAdmin:
    """Acciones de botones del panel admin, separadas del armado visual."""

    def __init__(self, vista):
        self.vista = vista

    def presionar_boton_cerrar_sesion(self):
        self.vista.navegar("pantalla_inicial")

    def presionar_boton_cambiar_tema(self):
        # FLUJO TEMA 1: Lo llama el boton de tema en el inicio del panel admin.
        # Siguiente paso: tema.alternar_tema() en vistas/estilizacion/tema.py.
        tema.alternar_tema()

        # FLUJO TEMA 3: Despues del cambio, vuelve a navegacion.py para
        # reconstruir VistaPanelAdmin desde su pantalla inicial.
        self.vista.navegar("panel_admin")

    def presionar_boton_abrir_seccion(self, tipo_usuario, titulo):
        PanelListadoAdmin(self.vista).crear(tipo_usuario, titulo)

    def presionar_boton_volver(self):
        PanelInicioAdmin(self.vista).crear()

    def presionar_boton_congelar_cuenta(self, usuario, tarjeta):
        self.pedir_confirmacion(usuario, "congelar", lambda: self.confirmar_congelar_cuenta(usuario, tarjeta))

    def confirmar_congelar_cuenta(self, usuario, tarjeta):
        self.vista.controlador_admin.congelar_cuenta(usuario.id_usuario)
        usuario.cuenta_congelada = True
        TarjetaUsuarioAdmin(self.vista).crear_acciones(tarjeta, usuario)

    def presionar_boton_descongelar_cuenta(self, usuario, tarjeta):
        self.pedir_confirmacion(usuario, "descongelar", lambda: self.confirmar_descongelar_cuenta(usuario, tarjeta))

    def confirmar_descongelar_cuenta(self, usuario, tarjeta):
        self.vista.controlador_admin.descongelar_cuenta(usuario.id_usuario)
        usuario.cuenta_congelada = False
        TarjetaUsuarioAdmin(self.vista).crear_acciones(tarjeta, usuario)

    def presionar_boton_eliminar_cuenta(self, usuario, tarjeta):
        self.pedir_confirmacion(usuario, "borrar", lambda: self.confirmar_eliminar_cuenta(usuario, tarjeta))

    def confirmar_eliminar_cuenta(self, usuario, tarjeta):
        self.vista.controlador_admin.eliminar_cuenta(usuario.id_usuario)
        tarjeta.destroy()

    def pedir_confirmacion(self, usuario, accion, al_confirmar):
        nombre = f"{usuario.nombre} {usuario.apellido}"
        self.vista.mostrar_confirmacion(
            f"¿Confirmar {accion} la cuenta de {nombre}?",
            al_confirmar,
        )

    def refrescar_listado(self):
        if self.vista.tipo_actual is None or self.vista.titulo_actual is None:
            return
        PanelListadoAdmin(self.vista).crear(self.vista.tipo_actual, self.vista.titulo_actual)


class VistaPanelAdmin(tk.Frame):
    """Pantalla principal para usuarios con tipo_usuario administrador."""

    def __init__(self, padre, navegar, controlador_admin, usuario_actual):
        self.navegar = navegar
        self.controlador_admin = controlador_admin
        self.usuario_actual = usuario_actual
        self.moldes = Moldes()
        self.imagenes_usuario = []
        self.ancho_tarjeta = 700
        self.tipo_actual = None
        self.titulo_actual = None
        self.mostrar_confirmacion = None
        self.acciones = AccionesBotonesAdmin(self)

        super().__init__(padre, bg=tema.FONDO)
        self.pack(fill="both", expand=True)
        self.crear_widgets()

    def crear_widgets(self):
        self.configure(bg=tema.FONDO)
        self.panel = self.moldes.crear_frame(self, tema.PANEL, tema.BORDE, 1, 16, 16, llenar="both", expandir=True, margen_x=18, margen_y=18, columnas_peso=((0, 1),), filas_peso=((1, 1),))
        self.cabecera = self.moldes.crear_frame(self.panel, tema.PANEL, fila=0, columna=0, sticky="ew", columnas_peso=((0, 1), (1, 1)))
        self.titulo_cabecera = self.moldes.crear_label(self.cabecera, "Panel administrador", tema.FUENTE_TITULO, tema.TEXTO, tema.PANEL, metodo="grid", row=0, column=0, sticky="w")
        self.acciones_cabecera = None
        self.contenido = self.moldes.crear_frame(self.panel, tema.PANEL, fila=1, columna=0, sticky="nsew", columnas_peso=((0, 1),), filas_peso=((0, 1),))
        PanelInicioAdmin(self).crear()

    def configurar_cabecera(self, titulo, texto_boton, comando_boton, texto_boton_secundario=None, comando_boton_secundario=None):
        self.titulo_cabecera.config(text=titulo)
        if self.acciones_cabecera is not None:
            self.acciones_cabecera.destroy()

        self.acciones_cabecera = self.moldes.crear_frame(self.cabecera, tema.PANEL, fila=0, columna=1, sticky="e")

        # FLUJO TEMA 0: PanelInicioAdmin.crear() pide este boton secundario.
        # El boton llama AccionesBotonesAdmin.presionar_boton_cambiar_tema().
        if texto_boton_secundario is not None and comando_boton_secundario is not None:
            self.moldes.crear_boton(self.acciones_cabecera, texto_boton_secundario, False, None, comando_boton_secundario, lado="left", margen_x=(0, 8))

        self.moldes.crear_boton(self.acciones_cabecera, texto_boton, False, None, comando_boton, lado="left")

    def limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()
        self.contenido.grid_rowconfigure(0, weight=0)
        self.contenido.grid_rowconfigure(1, weight=0)
        self.imagenes_usuario = []
