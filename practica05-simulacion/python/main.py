import argparse

from controlador.controlador_lcg import ControladorLCG
from vista import vista_consola as vista


def main():
    argumentos = argparse.ArgumentParser(description="Generador Congruencial Lineal")
    argumentos.add_argument("semilla", nargs="?", type=int, help="Entero entre 0 y 4294967295")
    argumentos.add_argument("--comparar-semilla", type=int,
                            help="Otra semilla para comparar gráficamente las secuencias en Python")
    opciones = argumentos.parse_args()
    semilla = opciones.semilla if opciones.semilla is not None else vista.pedir_semilla()
    try:
        ControladorLCG().ejecutar(semilla, opciones.comparar_semilla)
    except (ValueError, OSError, KeyError) as error:
        argumentos.exit(1, f"Error: {error}\n")
    except ImportError:
        argumentos.exit(1, "Para generar la gráfica instale Matplotlib: python3 -m pip install matplotlib\n")


if __name__ == "__main__":
    main()
