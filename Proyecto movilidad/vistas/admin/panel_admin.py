import tkinter as tk
from tkinter import messagebox
from pathlib import Path

from PIL import Image, ImageTk

from vistas.estilizacion import tema
from vistas.estilizacion.decoraciones import crear_logo_admin
from vistas.estilizacion.widgets import Moldes


class VistaPanelAdmin(tk.Frame):
    """Pantalla principal para usuarios con tipo_usuario administrador."""

    COLOR_PANEL = "#16202f"
    COLOR_TARJETA = "#223044"
    COLOR_BORDE = "#5b6b80"
    COLOR_TEXTO = "#f8fafc"
    COLOR_TEXTO_SUAVE = "#d5dde8"
    COLOR_ACCION = "#0f766e"
    COLOR_BORRAR = "#be123c"
    TAMANO_CUADRADO = 142
    SECCIONES = (
        ("pasajero", "Pasajeros", "#2dd4bf", "Revisa cuentas de usuarios que solicitan viajes."),
        ("conductor", "Conductores", "#f59e0b", "Consulta conductores, licencias y datos del vehiculo."),
    )

    def __init__(self, padre, navegar, controlador_admin, usuario_actual):
        self.navegar = navegar
        self.controlador_admin = controlador_admin
        self.usuario_actual = usuario_actual
        self.moldes = Moldes()
        self.imagenes_usuario = []
        self.ancho_tarjeta = 700
        self.tipo_actual = None
        self.titulo_actual = None

        super().__init__(padre, bg=tema.FONDO)
        self.pack(fill="both", expand=True)
        self.crear_widgets()

    def crear_widgets(self):
        self.configure(bg=self.COLOR_PANEL)
        self.panel = self.moldes.crear_frame(self, self.COLOR_PANEL, self.COLOR_BORDE, 1, 16, 16, llenar="both", expandir=True, margen_x=18, margen_y=18, columnas_peso=((0, 1),), filas_peso=((1, 1),))
        self.cabecera = self.moldes.crear_frame(self.panel, self.COLOR_PANEL, fila=0, columna=0, sticky="ew", columnas_peso=((0, 1), (1, 1)))
        self.titulo_cabecera = self.moldes.crear_label(self.cabecera, "Panel administrador", tema.FUENTE_TITULO, self.COLOR_TEXTO, self.COLOR_PANEL, metodo="grid", row=0, column=0, sticky="w")
        self.boton_cabecera = None
        self.contenido = self.moldes.crear_frame(self.panel, self.COLOR_PANEL, fila=1, columna=0, sticky="nsew", columnas_peso=((0, 1),), filas_peso=((0, 1),))
        self.mostrar_inicio()

    def configurar_cabecera(self, titulo, texto_boton, comando_boton):
        self.titulo_cabecera.config(text=titulo)
        if self.boton_cabecera is not None:
            self.boton_cabecera.destroy()
        self.boton_cabecera = self.moldes.crear_boton(self.cabecera, texto_boton, False, None, comando_boton, metodo="grid", row=0, column=1, sticky="e")

    def limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()
        self.contenido.grid_rowconfigure(0, weight=0)
        self.contenido.grid_rowconfigure(1, weight=0)
        self.imagenes_usuario = []

    def mostrar_inicio(self):
        self.limpiar_contenido()
        self.configurar_cabecera("Panel administrador", "Cerrar sesion", lambda: self.navegar("pantalla_inicial"))
        self.contenido.grid_rowconfigure(0, weight=1)
        conteo = self.controlador_admin.contar_por_tipo()
        centro = self.moldes.crear_frame(self.contenido, self.COLOR_PANEL, fila=0, columna=0, sticky="nsew", columnas_peso=((0, 1), (1, 1)), filas_peso=((0, 1),))

        # La pantalla inicial separa las secciones administrativas sin tocar
        # el menu normal de pasajeros/conductores.
        for columna, (tipo, titulo, color, descripcion) in enumerate(self.SECCIONES):
            tarjeta = self.moldes.crear_frame(centro, self.COLOR_TARJETA, self.COLOR_BORDE, 1, 24, 24, fila=0, columna=columna, sticky="nsew", margen_x=10, margen_y=28, columnas_peso=((0, 1),), filas_peso=((0, 1), (1, 0), (2, 1)))
            contenido = self.moldes.crear_frame(tarjeta, self.COLOR_TARJETA, fila=1, columna=0, sticky="ew", columnas_peso=((0, 1),))
            crear_logo_admin(contenido, tipo, color, self.COLOR_TARJETA).grid(row=0, column=0, pady=(0, 18))
            self.moldes.crear_label(contenido, titulo, ("Arial", 26, "bold"), self.COLOR_TEXTO, self.COLOR_TARJETA, metodo="grid", row=1, column=0, sticky="")
            self.moldes.crear_label(contenido, "registrados", ("Arial", 16, "bold"), self.COLOR_TEXTO_SUAVE, self.COLOR_TARJETA, metodo="grid", row=2, column=0, sticky="", pady=(22, 0))
            self.moldes.crear_label(contenido, str(conteo.get(tipo, 0)), ("Arial", 58, "bold"), color, self.COLOR_TARJETA, metodo="grid", row=3, column=0, sticky="")
            self.moldes.crear_label(contenido, descripcion, ("Arial", 13), self.COLOR_TEXTO_SUAVE, self.COLOR_TARJETA, 260, "center", metodo="grid", row=4, column=0, sticky="ew", pady=(22, 28))
            boton = self.moldes.crear_boton(contenido, "Abrir", True, 18, lambda tipo=tipo, titulo=titulo: self.mostrar_listado(tipo, titulo))
            boton.configure(font=("Arial", 15, "bold"), bg=color, activebackground=color, padx=28, pady=16)
            boton.grid(row=5, column=0, ipadx=28, ipady=6)

    def mostrar_listado(self, tipo_usuario, titulo):
        self.limpiar_contenido()
        self.tipo_actual = tipo_usuario
        self.titulo_actual = titulo
        self.configurar_cabecera(titulo, "Volver", self.mostrar_inicio)
        self.contenido.grid_rowconfigure(0, weight=0)
        self.contenido.grid_rowconfigure(1, weight=1)
        usuarios = self.controlador_admin.listar_por_tipo(tipo_usuario)

        zona = self.moldes.crear_frame(self.contenido, self.COLOR_PANEL, fila=1, columna=0, sticky="nsew", margen_y=(8, 0), columnas_peso=((0, 1),), filas_peso=((0, 1),))
        canvas = tk.Canvas(zona, bg=self.COLOR_PANEL, highlightthickness=0)
        scroll = tk.Scrollbar(zona, orient="vertical", command=canvas.yview)
        listado = self.moldes.crear_frame(canvas, self.COLOR_PANEL, columnas_peso=((0, 1),))
        ventana_listado = canvas.create_window((0, 0), window=listado, anchor="nw")
        listado.bind("<Configure>", lambda evento: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda evento: self.ajustar_ancho_listado(canvas, ventana_listado, evento.width))
        canvas.configure(yscrollcommand=scroll.set)
        canvas.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")

        if not usuarios:
            self.moldes.crear_label(listado, "No hay usuarios registrados en esta seccion.", tema.FUENTE_TEXTO, self.COLOR_TEXTO_SUAVE, self.COLOR_PANEL, metodo="grid", row=0, column=0, sticky="w")
            return

        # Cada usuario se muestra como tarjeta para dejar espacio a imagen y
        # datos, parecido a las tarjetas visuales usadas en el flujo de viaje.
        for fila, usuario in enumerate(usuarios):
            self.crear_tarjeta_usuario(listado, usuario, fila)

    def crear_tarjeta_usuario(self, padre, usuario, fila):
        tarjeta = self.moldes.crear_frame(padre, self.COLOR_TARJETA, self.COLOR_BORDE, 1, 14, 14, fila=fila, columna=0, sticky="ew", margen_y=(0, 12), columnas_peso=((1, 1),), filas_peso=((0, 1),))
        self.crear_imagen_usuario(tarjeta, usuario).grid(row=0, column=0, sticky="n", padx=(0, 16))
        cuerpo = self.moldes.crear_frame(tarjeta, self.COLOR_TARJETA, fila=0, columna=1, sticky="nsew", columnas_peso=((0, 1),), filas_peso=((1, 1),))
        nombre = f"{usuario.nombre} {usuario.apellido}"
        self.moldes.crear_label(cuerpo, nombre, ("Arial", 24, "bold"), self.COLOR_TEXTO, self.COLOR_TARJETA, max(400, self.ancho_tarjeta - 610), "center", metodo="grid", row=0, column=0, sticky="ew", pady=(0, 10))
        self.crear_grilla_datos(cuerpo, usuario).grid(row=1, column=0, sticky="nsew")
        acciones = self.moldes.crear_frame(tarjeta, self.COLOR_TARJETA, fila=0, columna=2, sticky="n", margen_x=(16, 0))
        # Estos botones ya llaman al controlador; el servicio valida y persiste.
        cuenta_congelada = getattr(usuario, "cuenta_congelada", False)
        texto_estado = "Descongelar\ncuenta" if cuenta_congelada else "Congelar\ncuenta"
        accion_estado = self.descongelar_cuenta if cuenta_congelada else self.congelar_cuenta
        self.crear_boton_cuadrado(acciones, texto_estado, self.COLOR_ACCION, lambda usuario=usuario: accion_estado(usuario), 0, (0, 8))
        self.crear_boton_cuadrado(acciones, "Borrar\ncuenta", self.COLOR_BORRAR, lambda usuario=usuario: self.eliminar_cuenta(usuario), 1, (8, 0))

    def crear_grilla_datos(self, padre, usuario):
        grilla = self.moldes.crear_frame(padre, self.COLOR_TARJETA, columnas_peso=((0, 1), (1, 1)))
        for indice, (etiqueta, valor) in enumerate(self.datos_usuario(usuario)):
            fila = indice // 2
            columna = indice % 2
            celda = self.moldes.crear_frame(grilla, self.COLOR_TARJETA, fila=fila, columna=columna, sticky="ew", margen_x=(0, 14) if columna == 0 else (14, 0), margen_y=(0, 10), columnas_peso=((0, 1),))
            tk.Label(celda, text=f"{etiqueta}:", font=("Arial", 17, "bold"), fg=self.COLOR_TEXTO_SUAVE, bg=self.COLOR_TARJETA).pack(side="left", anchor="w")
            tk.Label(celda, text=str(valor), font=("Arial", 17), fg=self.COLOR_TEXTO, bg=self.COLOR_TARJETA, wraplength=max(240, (self.ancho_tarjeta - 560) // 2), justify="left").pack(side="left", anchor="w", padx=(6, 0))
        return grilla

    def crear_boton_cuadrado(self, padre, texto, color, comando, columna, margen_x):
        contenedor = self.crear_cuadrado_fijo(padre, self.COLOR_BORDE)
        contenedor.grid(row=0, column=columna, sticky="n", padx=margen_x)
        boton = tk.Button(contenedor, text=texto, command=comando, font=("Arial", 14, "bold"), bg=color, fg="#ffffff", activebackground=color, activeforeground="#ffffff", relief="flat", bd=0, cursor="hand2")
        boton.pack(fill="both", expand=True, padx=2, pady=2)
        return boton

    def crear_cuadrado_fijo(self, padre, color):
        # Frame cuadrado real: grid no debe modificar su ancho ni alto.
        cuadrado = tk.Frame(padre, bg=color, width=self.TAMANO_CUADRADO, height=self.TAMANO_CUADRADO)
        cuadrado.grid_propagate(False)
        cuadrado.pack_propagate(False)
        return cuadrado

    def congelar_cuenta(self, usuario):
        # La vista solo dispara la accion y refresca la seccion actual.
        self.controlador_admin.congelar_cuenta(usuario.id_usuario)
        self.mostrar_listado(self.tipo_actual, self.titulo_actual)

    def descongelar_cuenta(self, usuario):
        # La vista solo dispara la accion y refresca la seccion actual.
        self.controlador_admin.descongelar_cuenta(usuario.id_usuario)
        self.mostrar_listado(self.tipo_actual, self.titulo_actual)

    def eliminar_cuenta(self, usuario):
        # Confirmacion visual antes de borrar; el borrado real sigue en servicio.
        nombre = f"{usuario.nombre} {usuario.apellido}"
        if not messagebox.askyesno("Borrar cuenta", f"¿Borrar la cuenta de {nombre}?"):
            return

        self.controlador_admin.eliminar_cuenta(usuario.id_usuario)
        self.mostrar_listado(self.tipo_actual, self.titulo_actual)

    def ajustar_ancho_listado(self, canvas, ventana_listado, ancho):
        self.ancho_tarjeta = max(360, ancho - 18)
        canvas.itemconfigure(ventana_listado, width=self.ancho_tarjeta)

    def crear_imagen_usuario(self, padre, usuario):
        contenedor = self.crear_cuadrado_fijo(padre, self.COLOR_PANEL)
        ruta = self.ruta_imagen_usuario(usuario)
        if ruta is not None:
            try:
                imagen = Image.open(ruta)
                imagen.thumbnail((self.TAMANO_CUADRADO - 10, self.TAMANO_CUADRADO - 10))
                foto = ImageTk.PhotoImage(imagen)
                self.imagenes_usuario.append(foto)
                tk.Label(contenedor, image=foto, bg=self.COLOR_PANEL).place(relx=0.5, rely=0.5, anchor="center")
                return contenedor
            except (OSError, ValueError):
                pass

        tk.Label(contenedor, text="X", font=("Arial", 42, "bold"), fg=self.COLOR_TEXTO_SUAVE, bg=self.COLOR_PANEL).place(relx=0.5, rely=0.5, anchor="center")
        return contenedor

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

    def datos_usuario(self, usuario):
        tipo = getattr(usuario, "tipo_usuario", "usuario")
        datos = [
            ("ID", usuario.id_usuario),
            ("Tipo", tipo),
            ("Correo", usuario.correo),
            ("Telefono", usuario.telefono),
            ("Edad", usuario.edad),
            ("Estado", "Congelada" if getattr(usuario, "cuenta_congelada", False) else "Activa"),
        ]

        if tipo == "pasajero":
            datos.append(("Direccion", getattr(usuario, "direccion", "")))

        if tipo == "conductor":
            auto = getattr(usuario, "auto", None)
            datos.append(("Licencia", f"{getattr(usuario, 'tipo_licencia', '')} | {getattr(usuario, 'licencia_conducir', '')}"))
            if auto is not None:
                datos.append(("Auto", f"{auto.marca} {auto.modelo} | {auto.ano} | Patente: {auto.patente}"))

        return datos
