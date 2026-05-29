import json
from dataclasses import asdict


def guardar_json(nombre_archivo, lista_objetos):
    datos = [
        asdict(objeto)
        for objeto in lista_objetos
    ]

    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


def cargar_json(nombre_archivo):
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            return json.load(archivo)


def buscar_usuario(lista_usuarios, id_usuario):
    for usuario in lista_usuarios:
        if usuario.id_usuario == id_usuario:
            return usuario
    return None


def agregar_objeto(lista_objetos, objeto):
    lista_objetos.append(objeto)

def eliminar_objeto(lista_objetos, id_objeto):
    objeto = buscar_usuario(lista_objetos, id_objeto)
    if objeto:
        lista_objetos.remove(objeto)