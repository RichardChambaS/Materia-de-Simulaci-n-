"""Modelo deterministico: crecimiento exponencial continuo.

    P(t) = P0 * e^(r_c * t)
"""

import numpy as np


def deterministico(P0, r_c, tiempo):
    """Retorna (t, P) con la curva exponencial evaluada en t = 0..tiempo."""
    t = np.arange(0, tiempo + 1, dtype=float)
    P = P0 * np.exp(r_c * t)
    return t, P


if __name__ == "__main__":
    from parametros import estimar_parametros

    p = estimar_parametros()
    t, P = deterministico(p["P0"], p["r_c"], p["n"])
    print("t =", t)
    print("P =", P)
