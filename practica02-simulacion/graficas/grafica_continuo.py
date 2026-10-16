"""Gráfica del modelo continuo mediante Euler."""

import matplotlib.pyplot as plt
from graficas._base import guardar, preparar_ejes


def graficar_continuo(t, P, datos_t, datos_p, nombre="continuo.png"):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(t, P, "m-", label="Continuo (Euler)")
    preparar_ejes(ax, "Modelo continuo (aproximación de Euler)", datos_t, datos_p)
    return guardar(fig, nombre)
