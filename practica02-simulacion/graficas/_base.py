"""Utilidades comunes para las graficas."""

import os
import sys

import matplotlib

# Backend sin ventana solo si no hay display y pyplot aun no se cargo.
if (sys.platform.startswith("linux") and not os.environ.get("DISPLAY")
        and "matplotlib.pyplot" not in sys.modules):
    matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402

CARPETA_RESULTADOS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resultados")


def preparar_ejes(ax, titulo, datos_t=None, datos_p=None):
    """Aplica titulo, ejes, leyenda y cuadrícula; agrega los datos reales."""
    ax.set_title(titulo)
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Población")
    ax.grid(True, linestyle="--", alpha=0.6)
    if datos_t is not None:
        ax.plot(datos_t, datos_p, "ko", label="Datos reales", zorder=5)
    ax.legend()


def guardar(fig, nombre):
    """Guarda la figura en resultados/ y la cierra."""
    os.makedirs(CARPETA_RESULTADOS, exist_ok=True)
    ruta = os.path.join(CARPETA_RESULTADOS, nombre)
    fig.savefig(ruta, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return ruta
