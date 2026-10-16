"""Modelo discreto: crecimiento por periodos.

    P(t+1) = P(t) + r_d * P(t)
"""

import numpy as np


def discreto(P0, r_d, tiempo):
    """Retorna (t, P) simulando el crecimiento periodo a periodo."""
    poblacion = [float(P0)]
    actual = float(P0)

    for _ in range(int(tiempo)):
        incremento = r_d * actual
        actual = actual + incremento
        poblacion.append(actual)

    t = np.arange(0, int(tiempo) + 1, dtype=float)
    return t, np.array(poblacion)


if __name__ == "__main__":
    from parametros import estimar_parametros

    p = estimar_parametros()
    t, P = discreto(p["P0"], p["r_d"], p["n"])
    print("t =", t)
    print("P =", P)
