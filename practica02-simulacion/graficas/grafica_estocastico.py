"""Grafica del modelo estocastico (banda +/- sigma y residuos)."""

import matplotlib.pyplot as plt

from graficas._base import guardar, preparar_ejes


def graficar_estocastico(res, datos_t, datos_p, nombre="estocastico.png"):
    """Curva reconstruida con banda ±σ sombreada, datos reales y barras de residuos."""
    t = res["t"]
    P = res["poblacion"]

    fig, (ax, ax_res) = plt.subplots(
        2, 1, figsize=(8, 8), sharex=True,
        gridspec_kw={"height_ratios": [3, 1]},
    )

    # curva con banda de variabilidad
    ax.fill_between(t, res["banda_inf"], res["banda_sup"],
                    color="tab:orange", alpha=0.3, label="Banda ±σ (variabilidad)")
    ax.plot(t, P, "s-", color="tab:orange", label="Estocástico (reconstrucción)")
    preparar_ejes(ax, "Modelo estocástico (ruido medido de los datos)", datos_t, datos_p)
    ax.legend(loc="upper left")

    # residuos observados
    ax_res.bar(range(len(res["epsilon"])), res["epsilon"],
               color="tab:red", alpha=0.7, label="ε_t observado")
    ax_res.axhline(0, color="black", linewidth=0.8)
    ax_res.set_title(f"Residuos ε_t (σ = {res['sigma']:.2f})")
    ax_res.set_xlabel("Intervalo t → t+1")
    ax_res.set_ylabel("ε")
    ax_res.grid(True, linestyle="--", alpha=0.6)
    ax_res.legend()

    fig.tight_layout()
    return guardar(fig, nombre)

