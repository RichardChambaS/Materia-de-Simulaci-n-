"""Grafica de sensibilidad: influencia de la tasa r sobre el crecimiento."""

import numpy as np
import matplotlib.pyplot as plt

from config import escenarios_r
from graficas._base import guardar, preparar_ejes


def graficar_influencia_r(r_c, P0, tiempo, datos_t, datos_p,
                          nombre="influencia_r.png"):
    """Curvas del modelo deterministico con distintos r (crecimiento y decrecimiento)."""
    fig, ax = plt.subplots(figsize=(9, 6))
    t = np.arange(0, tiempo + 1, dtype=float)

    for etiqueta, r in escenarios_r(r_c).items():
        ax.plot(t, P0 * np.exp(r * t), linewidth=2, label=etiqueta)

    preparar_ejes(ax, "Influencia de la tasa r en el modelo determinístico",
                  datos_t, datos_p)
    ax.legend(loc="upper left")
    return guardar(fig, nombre)

