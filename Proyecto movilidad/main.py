"""Punto de entrada de la aplicacion..."""

import sys

sys.dont_write_bytecode = True

from Controladores.navegacion import Navegacion


def main():
    Navegacion().iniciar()


if __name__ == "__main__":
    main()
