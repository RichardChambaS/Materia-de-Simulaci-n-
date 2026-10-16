"""Adaptación del algoritmo del APE: usa residuos medidos, sin sortear ruido."""

import numpy as np


def estocastico(P0, r_d, epsilon, sigma):
    """Aplica P(t+1) = P(t) + r_d * P(t) + epsilon[t]."""
    poblacion = [float(P0)]
    for ruido in epsilon:
        actual = poblacion[-1]
        nueva = actual + r_d * actual + ruido
        if nueva < 0:
            nueva = 0.0
        poblacion.append(nueva)

    poblacion = np.array(poblacion)
    return {
        "t": np.arange(len(poblacion)),
        "poblacion": poblacion,
        "epsilon": epsilon,
        "sigma": sigma,
        "banda_inf": poblacion - sigma,
        "banda_sup": poblacion + sigma,
    }


if __name__ == "__main__":
    from parametros import estimar_parametros

    p = estimar_parametros()
    res = estocastico(p["P0"], p["r_d"], p["epsilon"], p["sigma"])
    print("t =", res["t"])
    print("P =", res["poblacion"])
