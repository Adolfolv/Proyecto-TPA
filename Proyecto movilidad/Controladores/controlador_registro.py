import tkinter as tk
from tkinter import messagebox, ttk

from Modelos.modelo_Usuario.usuario_datos import Pasajero, Conductor, Auto


class ControladorRegistro:

    def __init__(self, servicio_registro):
        self.servicio_registro = servicio_registro

    def conectar_vista(self, vista, al_registrar=None):
        self.vista = vista
        self.al_registrar = al_registrar

        boton_registro = self._buscar_boton(vista, "Registrarse")

        if boton_registro is not None:
            boton_registro.configure(command=self.registrar_desde_vista)

    def registrar_desde_vista(self):
        try:
            usuario = self._registrar_formulario_actual()

        except ValueError as error:
            messagebox.showerror("Registro", str(error))
            return None

        messagebox.showinfo("Registro", "Usuario registrado correctamente.")

        if self.al_registrar is not None:
            self.al_registrar(usuario)

        return usuario

    def _registrar_formulario_actual(self):
        if not hasattr(self, "vista"):
            raise ValueError("La vista de registro no esta conectada.")

        entradas = self._obtener_entradas(self.vista.area_formulario)
        selectores = self._obtener_selectores(self.vista.area_formulario)

        if selectores:
            return self._registrar_conductor_desde_widgets(
                entradas,
                selectores,
            )

        return self._registrar_pasajero_desde_widgets(entradas)

    def _registrar_pasajero_desde_widgets(self, entradas):
        if len(entradas) < 6:
            raise ValueError("Faltan datos para registrar al pasajero.")

        return self.registrar_pasajero(
            entradas[0].get(),
            entradas[1].get(),
            entradas[2].get(),
            "18",
            self._normalizar_telefono(entradas[3].get()),
            entradas[4].get(),
            entradas[5].get(),
        )

    def _registrar_conductor_desde_widgets(self, entradas, selectores):
        if len(entradas) < 11 or len(selectores) < 3:
            raise ValueError("Faltan datos para registrar al conductor.")

        return self.registrar_conductor(
            entradas[0].get(),
            entradas[1].get(),
            entradas[2].get(),
            "18",
            self._normalizar_telefono(entradas[3].get()),
            entradas[4].get(),
            entradas[5].get(),
            selectores[2].get(),
            entradas[10].get(),
            selectores[0].get(),
            selectores[1].get(),
            entradas[7].get(),
            entradas[6].get(),
            entradas[8].get(),
            entradas[9].get(),
        )

    def _obtener_entradas(self, widget):
        entradas = []

        for hijo in widget.winfo_children():
            if isinstance(hijo, tk.Entry):
                entradas.append(hijo)

            entradas.extend(self._obtener_entradas(hijo))

        return entradas

    def _obtener_selectores(self, widget):
        selectores = []

        for hijo in widget.winfo_children():
            if isinstance(hijo, ttk.Combobox):
                selectores.append(hijo)

            selectores.extend(self._obtener_selectores(hijo))

        return selectores

    def _buscar_boton(self, widget, texto):
        for hijo in widget.winfo_children():
            if isinstance(hijo, tk.Button) and hijo.cget("text") == texto:
                return hijo

            boton = self._buscar_boton(hijo, texto)

            if boton is not None:
                return boton

        return None

    def _normalizar_telefono(self, telefono):
        digitos = "".join(
            caracter
            for caracter in str(telefono)
            if caracter.isdigit()
        )

        return digitos[-8:]

    def _validar_contrasenas(self, contrasena, confirmar):
        if not contrasena:
            raise ValueError("Debe ingresar una contraseña.")

        if contrasena != confirmar:
            raise ValueError("Las contraseñas no coinciden.")

    def registrar_pasajero(
        self,
        nombre,
        apellido,
        correo,
        edad,
        telefono,
        contrasena,
        confirmar_contrasena,
    ):
        self._validar_contrasenas(contrasena, confirmar_contrasena)

        usuario = Pasajero(
            id_usuario=None,
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            edad=edad,
            telefono=telefono,
            contrasena=contrasena,
            direccion=""
        )

        return self.servicio_registro.registrar_usuario(usuario)

    def registrar_conductor(
        self,
        nombre,
        apellido,
        correo,
        edad,
        telefono,
        contrasena,
        confirmar_contrasena,
        tipo_licencia,
        licencia_conducir,
        marca,
        modelo,
        ano,
        patente,
        cantidad_asientos,
        peso_equipaje,
    ):
        self._validar_contrasenas(contrasena, confirmar_contrasena)

        auto = Auto(
            marca=marca,
            modelo=modelo,
            año=ano,
            patente=patente,
            cantidad_asientos=cantidad_asientos,
            peso_equipaje=peso_equipaje,
        )

        usuario = Conductor(
            id_usuario=None,
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            edad=edad,
            telefono=telefono,
            contrasena=contrasena,
            tipo_licencia=tipo_licencia,
            licencia_conducir=licencia_conducir,
            auto=auto,
        )

        return self.servicio_registro.registrar_usuario(usuario)
