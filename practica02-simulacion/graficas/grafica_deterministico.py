"""Grafica del modelo deterministico."""

import matplotlib.pyplot as plt

from graficas._base import guardar, preparar_ejes


def graficar_deterministico(t, P, datos_t, datos_p, nombre="deterministico.png"):
    """Curva exponencial + datos reales."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(t, P, "b-", linewidth=2, label="Determinístico  P(t)=P0·e^(r·t)")
    preparar_ejes(ax, "Modelo determinístico (crecimiento exponencial)", datos_t, datos_p)
    return guardar(fig, nombre)

