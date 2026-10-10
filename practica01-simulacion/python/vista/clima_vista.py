"""Capa VISTA de la Práctica 01 de Simulación.

Responsabilidad única: presentar los resultados ya calculados.

  * Tabla por consola con las columnas pedidas.
  * Gráfica 1: índice vs hora, con líneas horizontales en 0.40, 0.60 y 0.75.
  * Gráfica 2: H, N y Tf vs hora en un mismo gráfico.

Esta capa NO hace ningún cálculo del modelo: solo recibe datos y los muestra.
"""

import os

# No se fija el backend con matplotlib.use(): así matplotlib elige uno con
# ventana (QtAgg, TkAgg) y plt.show() abre las gráficas. Si el equipo no tiene
# ningún backend gráfico instalado, matplotlib cae solo en Agg: los PNG se
# siguen guardando igual, únicamente no se abre ninguna ventana.
import matplotlib.pyplot as plt

# Carpeta python/resultados, deducida de la ubicación de este archivo.
CARPETA_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA_RESULTADOS = os.path.join(CARPETA_BASE, "resultados")

# Anchos de columna de la tabla de consola.
# Estos valores deben coincidir con los del formato usado en mostrar_tabla()
# para que la cabecera y las filas queden alineadas.
#                Hora  Hum  Nube  Temp  H    N    Tf   Índice  Estado
ANCHO_HORA = 6
ANCHO_HUMEDAD = 9
ANCHO_NUBOSIDAD = 11
ANCHO_TEMP = 9
ANCHO_DECIMAL = 8
ANCHO_ESTADO = 17

# Ancho de las líneas de separación (=, -).
ANCHO_TABLA = 80


def _encabezado():
    """Construye la fila de encabezados usando los anchos definidos arriba."""
    return (f"{'Hora':<{ANCHO_HORA}}{'Humedad':<{ANCHO_HUMEDAD}}"
            f"{'Nubosidad':<{ANCHO_NUBOSIDAD}}{'Temp':<{ANCHO_TEMP}}"
            f"{'H':<{ANCHO_DECIMAL}}{'N':<{ANCHO_DECIMAL}}{'Tf':<{ANCHO_DECIMAL}}"
            f"{'Índice':<{ANCHO_DECIMAL}}{'Estado':<{ANCHO_ESTADO}}")


class ClimaVista:
    """Muestra la tabla en consola y genera/guarda las gráficas en PNG."""

    def __init__(self):
        # Se crea la carpeta de resultados si no existe.
        os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

    # ------------------------------------------------------------------
    # Tabla en consola
    # ------------------------------------------------------------------
    def mostrar_encabezado(self):
        """Imprime solo la fila de encabezados de la tabla."""
        print(_encabezado())

    def mostrar_tabla(self, titulo, filas):
        """Imprime la tabla pedida: Hora, Humedad, Nubosidad, Temp, H, N, Tf, Índice, Estado."""
        print()
        print("=" * ANCHO_TABLA)
        print(titulo)
        print("=" * ANCHO_TABLA)

        # Encabezados
        self.mostrar_encabezado()
        print("-" * ANCHO_TABLA)

        # Una fila por registro; los valores ya vienen calculados desde el modelo.
        for fila in filas:
            temperatura = f"{fila['temperatura']} °C"
            print(
                f"{fila['hora']:<{ANCHO_HORA}}"
                f"{fila['humedad']:<{ANCHO_HUMEDAD}}"
                f"{fila['nubosidad']:<{ANCHO_NUBOSIDAD}}"
                f"{temperatura:<{ANCHO_TEMP}}"
                f"{fila['h']:<{ANCHO_DECIMAL}.3f}"
                f"{fila['n']:<{ANCHO_DECIMAL}.3f}"
                f"{fila['tf']:<{ANCHO_DECIMAL}.3f}"
                f"{fila['indice']:<{ANCHO_DECIMAL}.3f}"
                f"{fila['estado']:<{ANCHO_ESTADO}}"
            )
        print("=" * ANCHO_TABLA)

    # ------------------------------------------------------------------
    # Gráficas
    # ------------------------------------------------------------------
    def grafica_indice(self, filas, etiqueta):
        """Gráfica del índice vs hora con las líneas de los umbrales."""
        horas = [fila["hora"] for fila in filas]
        indices = [fila["indice"] for fila in filas]

        figura, eje = plt.subplots(figsize=(9, 5))
        eje.plot(horas, indices, marker="o", linewidth=2, color="#1f77b4",
                 label="Índice de lluvia (I)")

        # Líneas horizontales en los tres umbrales de la tabla de reglas.
        for umbral, color in ((0.40, "#2ca02c"), (0.60, "#ff7f0e"), (0.75, "#d62728")):
            eje.axhline(umbral, linestyle="--", linewidth=1, color=color,
                        label=f"Umbral {umbral:.2f}")

        # Relleno suave para visualizar dónde supera cada umbral.
        eje.fill_between(horas, indices, 0.75, where=[i >= 0.75 for i in indices],
                         color="#d62728", alpha=0.10, label="Lluvia (I >= 0.75)")

        eje.set_title(f"Índice de lluvia vs hora - Modelo {etiqueta}")
        eje.set_xlabel("Hora")
        eje.set_ylabel("Índice I")
        eje.set_ylim(0, 1.0)
        eje.grid(True, linestyle=":", alpha=0.6)
        eje.legend(loc="lower right", fontsize=9)

        ruta = os.path.join(CARPETA_RESULTADOS, f"indice_{etiqueta}.png")
        figura.tight_layout()
        figura.savefig(ruta, dpi=120)
        # La figura NO se cierra aquí: queda abierta para que plt.show() la muestre.
        print(f"Gráfica guardada en: {ruta}")

    def grafica_componentes(self, filas, etiqueta):
        """Gráfica con H, N y Tf vs hora en un mismo eje."""
        horas = [fila["hora"] for fila in filas]
        valores_h = [fila["h"] for fila in filas]
        valores_n = [fila["n"] for fila in filas]
        valores_tf = [fila["tf"] for fila in filas]

        figura, eje = plt.subplots(figsize=(9, 5))
        eje.plot(horas, valores_h, marker="s", linewidth=2, label="H (humedad normalizada)")
        eje.plot(horas, valores_n, marker="^", linewidth=2, label="N (nubosidad normalizada)")
        eje.plot(horas, valores_tf, marker="D", linewidth=2, label="Tf (factor de temperatura)")

        eje.set_title(f"Variables del modelo vs hora - Modelo {etiqueta}")
        eje.set_xlabel("Hora")
        eje.set_ylabel("Valor normalizado (0 - 1)")
        eje.set_ylim(0, 1.05)
        eje.grid(True, linestyle=":", alpha=0.6)
        eje.legend(loc="lower right", fontsize=9)

        ruta = os.path.join(CARPETA_RESULTADOS, f"componentes_{etiqueta}.png")
        figura.tight_layout()
        figura.savefig(ruta, dpi=120)
        # La figura NO se cierra aquí: queda abierta para que plt.show() la muestre.
        print(f"Gráfica guardada en: {ruta}")

    def graficar(self, filas, etiqueta):
        """Genera las dos gráficas de una ejecución, las guarda y las muestra en ventana."""
        print(f"\nGenerando gráficas del modelo {etiqueta}...")
        self.grafica_indice(filas, etiqueta)
        self.grafica_componentes(filas, etiqueta)

        # Abre las ventanas con las gráficas ya guardadas. El programa queda
        # esperando aquí hasta que se cierren; luego se liberan los recursos.
        print("Mostrando gráficas en ventana (ciérralas para terminar)...")
        plt.show()
        plt.close("all")
