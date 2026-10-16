"""Grafica comparativa de los cuatro modelos."""

import matplotlib.pyplot as plt

from graficas._base import guardar, preparar_ejes


def graficar_comparativa(det, dis, est, con, datos_t, datos_p,
                         nombre="comparativa.png"):
    """Una sola figura con los cuatro modelos + datos reales."""
    fig, ax = plt.subplots(figsize=(9, 6))

    ax.plot(det[0], det[1], "b-", linewidth=2, label="Determinístico")
    ax.step(dis[0], dis[1], where="mid", color="tab:green", linewidth=1.5, label="Discreto")
    ax.fill_between(est["t"], est["banda_inf"], est["banda_sup"],
                    color="tab:orange", alpha=0.25, label="Estocástico ±σ")
    ax.plot(est["t"], est["poblacion"], "s-", color="tab:orange",
            linewidth=1.5, markersize=4, label="Estocástico")
    ax.plot(con[0], con[1], "m--", linewidth=2, label="Continuo (Euler)")

    preparar_ejes(ax, "Comparación de los cuatro modelos", datos_t, datos_p)
    ax.legend(loc="upper left")
    return guardar(fig, nombre)

