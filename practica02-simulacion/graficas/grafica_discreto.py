"""Grafica del modelo discreto."""

import matplotlib.pyplot as plt

from graficas._base import guardar, preparar_ejes


def graficar_discreto(t, P, datos_t, datos_p, nombre="discreto.png"):
    """Puntos y escalones por periodo + datos reales."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.step(t, P, where="mid", color="tab:green", linewidth=1.5,
            label="Discreto  P(t+1)=P(t)+r·P(t)")
    ax.plot(t, P, "o", color="tab:green", label="Valores por período")
    preparar_ejes(ax, "Modelo discreto (cambios por período)", datos_t, datos_p)
    return guardar(fig, nombre)

