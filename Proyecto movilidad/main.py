import tkinter as tk

from modelo_Usuario.usuario_datos import Usuario
from Billetera.datos_billetera import Billetera
from Billetera.servicio_billetera import ServicioBilletera
from Controladores.controlador_billetera import ControladorBilletera
from vista_billetera import VistaBilletera


def main():

    usuario = Usuario(
    id_usuario="1",
    nombre="Juan",
    correo="juan@mail.com",
    edad=20,
    telefono="123",
    contraseña="123"
)

    servicio = ServicioBilletera()
    controlador = ControladorBilletera(servicio)

    root = tk.Tk()
    app = VistaBilletera(root, controlador, usuario)

    root.mainloop()


main()
'''''''''
pruebas:
servicio = ServicioUsuario("usuarios.json")

    print(" USUARIOS EN SISTEMA:")
    for u in servicio.listar_usuarios():
        print(u)

    # -------------------------
    # 2. Crear perfil (usuario logueado)
    # -------------------------
    perfil = Perfil(servicio)

    usuario = perfil.cargar_perfil(1)  # 👈 ID usuario

    if not usuario:
        print("\nUsuario no encontrado")
        return

    print("\n PERFIL CARGADO:")
    print(perfil.ver_perfil())

    # -------------------------
    # 3. Actualizar perfil
    # -------------------------
    print("\n ACTUALIZANDO PERFIL...")

    perfil.actualizar_perfil({
        "nombre": "Adolfo Modificado",
        "telefono": "999999999",
        "edad": 25
    })

    # -------------------------
    # 4. Ver resultado en memoria
    # -------------------------
    print("\nPERFIL DESPUÉS DE ACTUALIZAR:")
    print(perfil.ver_perfil())

    # -------------------------
    # 5. Verificar persistencia (recargar desde JSON)
    # -------------------------
    print("\nRECARGANDO DESDE JSON...")

    servicio2 = ServicioUsuario("usuarios.json")

    for u in servicio2.listar_usuarios():
        print(u)
    servicio = ServicioUsuario("usuarios.json")
    
    # 🔵 AGREGAR USUARIO NORMAL
    servicio.agregar_usuario(Usuario(
        id_usuario=1,
        nombre="Juan",
        correo="juan@mail.com",
        edad=20,
        telefono="111",
        contraseña="1234"
    ))

    # 🟢 PASAJERO
    servicio.agregar_usuario(Pasajero(
        id_usuario=2,
        nombre="Ana",
        correo="ana@mail.com",
        edad=22,
        telefono="222",
        contraseña="abcd",
        direccion="Centro"
    ))

    # 🔴 CONDUCTOR
    servicio.agregar_usuario(Conductor(
        id_usuario=3,
        nombre="Pedro",
        correo="pedro@mail.com",
        edad=30,
        telefono="333",
        contraseña="pass",
        licencia_conducir="ABC123",
        auto=Auto("Toyota", "Yaris", 2020, "AA11BB")
    ))

    # 📋 LISTAR
    print("\n--- USUARIOS ---")
    for u in servicio.listar_usuarios():
        print(u)

    # 🔍 BUSCAR
    print("\n--- BUSCAR ID 2 ---")
    print(servicio.buscar_usuario(2))
    '''''''''