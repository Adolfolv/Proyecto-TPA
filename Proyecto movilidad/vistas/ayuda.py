import threading
import tkinter as tk

from .estilizacion import tema
from .estilizacion.widgets import Moldes


def crear_scroll_tematico(padre, contenido):
    scroll = tk.Scrollbar(padre, orient="vertical", command=contenido.yview, bg=tema.SECUNDARIO, activebackground=tema.PRIMARIO, troughcolor=tema.PANEL, highlightbackground=tema.BORDE, highlightcolor=tema.BORDE, relief="flat", bd=0, width=12, elementborderwidth=0, cursor="hand2")
    contenido.configure(yscrollcommand=scroll.set)
    return scroll


def habilitar_rueda(contenido, *componentes):
    def desplazar(evento):
        if getattr(evento, "num", None) in (4, 5):
            unidades = -1 if evento.num == 4 else 1
        else:
            delta = getattr(evento, "delta", 0)
            unidades = -int(delta / 120) if abs(delta) >= 120 else (-1 if delta > 0 else 1)
        contenido.yview_scroll(unidades, "units")
        return "break"

    for componente in (contenido,) + componentes:
        componente.bind("<MouseWheel>", desplazar)
        componente.bind("<Button-4>", desplazar)
        componente.bind("<Button-5>", desplazar)


def nombre_rol(usuario):
    tipo = getattr(usuario, "tipo_usuario", "visitante") if usuario else "visitante"
    return {"pasajero": "Pasajero", "conductor": "Conductor", "administrador": "Administrador"}.get(str(tipo).lower(), "Visitante")


class PanelInformacionAyuda:
    def __init__(self, padre, moldes, secciones, usuario=None):
        self.padre, self.moldes, self.secciones = padre, moldes, secciones
        self.rol = nombre_rol(usuario)

    def crear(self):
        panel = self.moldes.crear_frame(self.padre, tema.PANEL_SUAVE, tema.BORDE, 1, 18, 18, fila=0, columna=0, sticky="nsew", margen_x=(0, 8), columnas_peso=((0, 1),), filas_peso=((1, 1),))
        cabecera = self.moldes.crear_frame(panel, tema.PANEL_SUAVE, fila=0, columna=0, sticky="ew", margen_y=(0, 12), columnas_peso=((0, 1),))
        textos = self.moldes.crear_frame(cabecera, tema.PANEL_SUAVE, fila=0, columna=0, sticky="w")
        self.moldes.crear_label(textos, f"Guia para {self.rol.lower()}", tema.FUENTE_SUBTITULO, tema.TEXTO, tema.PANEL_SUAVE).pack(anchor="w")
        self.moldes.crear_label(textos, "Informacion relevante para tu cuenta", ("Arial", 9), tema.TEXTO_SUAVE, tema.PANEL_SUAVE).pack(anchor="w", pady=(3, 0))
        tk.Label(cabecera, text=self.rol, font=("Arial", 9, "bold"), bg=tema.SECUNDARIO, fg=tema.TEXTO, padx=10, pady=5).grid(row=0, column=1, sticky="e")

        contenido = tk.Frame(panel, bg=tema.PANEL, padx=14, pady=8)
        contenido.grid(row=1, column=0, sticky="nsew")
        for titulo, descripcion in self.secciones:
            bloque = tk.Frame(contenido, bg=tema.PANEL)
            bloque.pack(fill="both", expand=True, pady=2)
            tk.Label(bloque, text=titulo, font=("Arial", 11, "bold"), bg=tema.PANEL, fg=tema.PRIMARIO, anchor="w").pack(fill="x")
            detalle = tk.Label(bloque, text=descripcion, font=("Arial", 12), bg=tema.PANEL, fg=tema.TEXTO_SUAVE, anchor="w", justify="left")
            detalle.pack(fill="x", pady=(2, 0))
            bloque.bind("<Configure>", lambda evento, etiqueta=detalle: etiqueta.configure(wraplength=max(evento.width - 2, 100)))


class PanelAsistenteAyuda:
    def __init__(self, vista, padre, sugerencias):
        self.vista, self.padre, self.sugerencias = vista, padre, sugerencias
        self.moldes = vista.moldes
        self.chat_iniciado = False
        self.canvas = self.mensajes = self.ventana_mensajes = self.scroll = self.bienvenida = self.entrada = self.boton_enviar = self.estado = None

    def crear(self):
        panel = self.moldes.crear_frame(self.padre, tema.PANEL_SUAVE, tema.BORDE, 1, fila=0, columna=1, sticky="nsew", margen_x=(8, 0), columnas_peso=((0, 1),), filas_peso=((1, 1),))
        self.crear_cabecera(panel)
        self.crear_chat(panel)
        self.crear_bienvenida(panel)
        self.crear_entrada(panel)

    def crear_cabecera(self, panel):
        cabecera = tk.Frame(panel, bg=tema.PRIMARIO, padx=14, pady=9)
        cabecera.grid(row=0, column=0, columnspan=2, sticky="ew")
        cabecera.grid_columnconfigure(1, weight=1)
        tk.Label(cabecera, text="IA", font=("Arial", 11, "bold"), bg=tema.PRIMARIO_TEXTO, fg=tema.PRIMARIO, width=3, height=2).grid(row=0, column=0, padx=(0, 10))
        textos = tk.Frame(cabecera, bg=tema.PRIMARIO)
        textos.grid(row=0, column=1, sticky="w")
        tk.Label(textos, text="ASISTENTE DE MOVILIDAD", font=("Arial", 11, "bold"), bg=tema.PRIMARIO, fg=tema.PRIMARIO_TEXTO).pack(anchor="w")
        self.estado = tk.Label(textos, text="Disponible", font=("Arial", 9), bg=tema.PRIMARIO, fg=tema.PRIMARIO_TEXTO)
        self.estado.pack(anchor="w", pady=(2, 0))

    def crear_chat(self, panel):
        self.canvas = tk.Canvas(panel, bg=tema.PANEL, relief="flat", bd=0, highlightthickness=0)
        self.mensajes = tk.Frame(self.canvas, bg=tema.PANEL)
        self.ventana_mensajes = self.canvas.create_window(0, 0, window=self.mensajes, anchor="nw")
        self.scroll = crear_scroll_tematico(panel, self.canvas)
        self.canvas.grid(row=1, column=0, sticky="nsew", padx=(12, 0), pady=12)
        self.scroll.grid(row=1, column=1, sticky="ns", padx=(8, 12), pady=12)
        self.canvas.bind("<Configure>", self.ajustar_chat)
        self.mensajes.bind("<Configure>", self.ajustar_chat)
        habilitar_rueda(self.canvas, self.mensajes, self.scroll)
        self.canvas.grid_remove()
        self.scroll.grid_remove()

    def ajustar_chat(self, _evento=None):
        ancho = max(self.canvas.winfo_width(), 1)
        alto = max(self.canvas.winfo_height(), 1)
        self.canvas.itemconfigure(self.ventana_mensajes, width=ancho)
        alto_mensajes = self.mensajes.winfo_reqheight()
        self.canvas.coords(self.ventana_mensajes, 0, 0)
        self.canvas.configure(scrollregion=(0, 0, ancho, max(alto, alto_mensajes)))

    def crear_bienvenida(self, panel):
        self.bienvenida = tk.Frame(panel, bg=tema.PANEL, padx=14, pady=12)
        self.bienvenida.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=12, pady=12)
        tk.Label(self.bienvenida, text="IA", font=("Arial", 20, "bold"), bg=tema.SECUNDARIO, fg=tema.PRIMARIO, width=3, height=1).pack(pady=(4, 7))
        tk.Label(self.bienvenida, text="En que puedo ayudarte?", font=tema.FUENTE_SUBTITULO, bg=tema.PANEL, fg=tema.TEXTO).pack()
        tk.Label(self.bienvenida, text="Elige una consulta rapida o escribe abajo.", font=("Arial", 9), bg=tema.PANEL, fg=tema.TEXTO_SUAVE).pack(pady=(4, 10))
        opciones = tk.Frame(self.bienvenida, bg=tema.PANEL)
        opciones.pack(fill="both", expand=True)
        opciones.grid_columnconfigure(0, weight=1, uniform="sugerencias")
        opciones.grid_columnconfigure(1, weight=1, uniform="sugerencias")
        opciones.grid_rowconfigure(0, weight=1)
        opciones.grid_rowconfigure(1, weight=1)
        for indice, sugerencia in enumerate(self.sugerencias):
            boton = tk.Button(opciones, text=sugerencia, command=lambda texto=sugerencia: self.usar_sugerencia(texto), font=("Arial", 9, "bold"), bg=tema.SECUNDARIO, fg=tema.TEXTO, activebackground=tema.PRIMARIO, activeforeground=tema.PRIMARIO_TEXTO, relief="flat", bd=0, highlightbackground=tema.BORDE, highlightthickness=1, cursor="hand2", wraplength=125, padx=5, pady=5)
            boton.grid(row=indice // 2, column=indice % 2, sticky="nsew", padx=4, pady=4)

    def crear_entrada(self, panel):
        contenedor = tk.Frame(panel, bg=tema.PANEL_SUAVE)
        contenedor.grid(row=2, column=0, columnspan=2, sticky="ew")
        tk.Frame(contenedor, bg=tema.PRIMARIO, height=2).pack(fill="x")
        controles = tk.Frame(contenedor, bg=tema.PANEL_SUAVE, padx=12, pady=10)
        controles.pack(fill="x")
        self.entrada = tk.Entry(controles, font=tema.FUENTE_TEXTO, bg=tema.SECUNDARIO, fg=tema.TEXTO, insertbackground=tema.TEXTO, selectbackground=tema.PRIMARIO, selectforeground=tema.PRIMARIO_TEXTO, relief="flat", bd=0, highlightbackground=tema.BORDE, highlightcolor=tema.PRIMARIO, highlightthickness=1)
        self.entrada.pack(side="left", fill="x", expand=True, padx=(0, 8), ipady=9)
        self.entrada.bind("<Return>", self.enviar_con_teclado)
        self.boton_enviar = tk.Button(controles, text="Preguntar", command=self.enviar, font=tema.FUENTE_BOTON, bg=tema.PRIMARIO, fg=tema.PRIMARIO_TEXTO, activebackground=tema.PRIMARIO, activeforeground=tema.PRIMARIO_TEXTO, relief="flat", bd=0, padx=12, pady=9, cursor="hand2")
        self.boton_enviar.pack(side="right")

    def usar_sugerencia(self, texto):
        self.entrada.delete(0, "end")
        self.entrada.insert(0, texto)
        self.enviar()

    def enviar_con_teclado(self, _evento):
        self.enviar()
        return "break"

    def enviar(self):
        pregunta = self.entrada.get().strip()
        if not pregunta:
            self.estado.configure(text="Escribe una consulta")
            return
        self.iniciar_chat()
        self.agregar_mensaje("Tu", pregunta)
        self.entrada.delete(0, "end")
        self.cambiar_estado_envio(False)
        threading.Thread(target=self.consultar, args=(pregunta,), daemon=True).start()

    def iniciar_chat(self):
        if self.chat_iniciado:
            return
        self.bienvenida.grid_remove()
        self.canvas.grid()
        self.scroll.grid()
        self.chat_iniciado = True

    def consultar(self, pregunta):
        resultado = self.vista.controlador.consultar_asistente(pregunta, self.vista.usuario_actual)
        self.vista.after(0, lambda: self.mostrar_resultado(resultado))

    def mostrar_resultado(self, resultado):
        self.agregar_mensaje("Asistente" if resultado.exitoso else "Sistema", resultado.texto if resultado.exitoso else resultado.error)
        self.cambiar_estado_envio(True)

    def cambiar_estado_envio(self, habilitado):
        estado = "normal" if habilitado else "disabled"
        self.entrada.configure(state=estado)
        self.boton_enviar.configure(state=estado, text="Preguntar" if habilitado else "...", cursor="hand2" if habilitado else "arrow")
        self.estado.configure(text="Disponible" if habilitado else "Generando respuesta...")
        if habilitado:
            self.entrada.focus_set()

    def agregar_mensaje(self, autor, texto):
        tipo = {"Asistente": "ia", "Tu": "usuario"}.get(autor, "sistema")
        fondo = {"ia": tema.PANEL_SUAVE, "usuario": tema.SECUNDARIO, "sistema": tema.ERROR_FONDO}[tipo]
        color_autor = tema.ERROR if tipo == "sistema" else tema.PRIMARIO
        margen = (8, 45) if tipo == "ia" else ((45, 8) if tipo == "usuario" else (8, 8))
        fila = tk.Frame(self.mensajes, bg=tema.PANEL)
        fila.pack(fill="x", pady=6)
        burbuja = tk.Frame(fila, bg=fondo, highlightbackground=tema.BORDE, highlightthickness=1, padx=12, pady=9)
        burbuja.pack(fill="x", padx=margen)
        etiqueta_autor = tk.Label(burbuja, text=autor, font=tema.FUENTE_BOTON, bg=fondo, fg=color_autor, anchor="center", justify="center")
        etiqueta_autor.pack(fill="x", pady=(0, 4))
        etiqueta_texto = tk.Label(burbuja, text=str(texto).strip(), font=tema.FUENTE_TEXTO, bg=fondo, fg=tema.TEXTO, anchor="center", justify="center")
        etiqueta_texto.pack(fill="x")
        burbuja.bind("<Configure>", lambda evento: etiqueta_texto.configure(wraplength=max(evento.width - 28, 100)))
        habilitar_rueda(self.canvas, fila, burbuja, etiqueta_autor, etiqueta_texto)
        self.mensajes.update_idletasks()
        self.ajustar_chat()
        self.canvas.after_idle(lambda: self.canvas.yview_moveto(1.0))


class VistaAyuda(tk.Frame):
    def __init__(self, padre, navegar, controlador, usuario_actual=None, destino_volver="menu"):
        self.navegar, self.controlador, self.usuario_actual, self.destino_volver = navegar, controlador, usuario_actual, destino_volver
        self.moldes = Moldes()
        super().__init__(padre, bg=tema.FONDO)
        self.pack(fill="both", expand=True)
        self.crear_widgets()

    def crear_widgets(self):
        panel = self.moldes.crear_frame(self, tema.PANEL, tema.BORDE, 1, 22, 22, llenar="both", expandir=True, margen_x=24, margen_y=24, columnas_peso=((0, 1),), filas_peso=((1, 1),))
        cabecera = self.moldes.crear_frame(panel, tema.PANEL, fila=0, columna=0, sticky="ew", margen_y=(0, 16), columnas_peso=((0, 1), (1, 0)))
        self.moldes.crear_label(cabecera, "Ayuda", tema.FUENTE_TITULO, tema.TEXTO, tema.PANEL, metodo="grid", fila=0, columna=0, sticky="w")
        self.moldes.crear_boton(cabecera, "Volver", False, None, lambda: self.navegar(self.destino_volver), metodo="grid", fila=0, columna=1, sticky="e")
        contenido = self.moldes.crear_frame(panel, tema.PANEL, fila=1, columna=0, sticky="nsew", columnas_peso=((0, 1), (1, 1)), filas_peso=((0, 1),))
        contenido.grid_columnconfigure(0, uniform="ayuda")
        contenido.grid_columnconfigure(1, uniform="ayuda")
        PanelInformacionAyuda(contenido, self.moldes, self.controlador.listar_secciones(self.usuario_actual), self.usuario_actual).crear()
        PanelAsistenteAyuda(self, contenido, self.controlador.listar_sugerencias(self.usuario_actual)).crear()
