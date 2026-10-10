"""Punto de entrada de la Práctica 01 de Simulación.

Este archivo no tiene lógica propia: solo crea el controlador y lo ejecuta.
Se ejecuta desde la carpeta python/ con:  python main.py
"""

from controlador.clima_controlador import ClimaControlador


def main():
    """Crea el controlador y lanza la simulación."""
    controlador = ClimaControlador()
    controlador.ejecutar()


if __name__ == "__main__":
    main()
