"""Modelo continuo mediante aproximacion de Euler.

    P(t + dt) = P(t) + dt * (r_c * P(t))
"""

import numpy as np


def continuo_euler(P0, r_c, tiempo, dt):
    """Retorna (t, P) integrando dP/dt = r_c * P con paso dt."""
    t = np.arange(0, tiempo + dt / 2, dt)  # /2 para evitar errores de redondeo
    poblacion = [float(P0)]

    for _ in range(1, len(t)):
        actual = poblacion[-1]
        cambio = r_c * actual
        nueva = actual + dt * cambio
        poblacion.append(nueva)

    return t, np.array(poblacion)


if __name__ == "__main__":
    from config import DT
    from parametros import estimar_parametros

    p = estimar_parametros()
    t, P = continuo_euler(p["P0"], p["r_c"], p["n"], DT)
    print(f"dt = {DT}  (len t = {len(t)})")
    print("t[0:10] =", t[:10])
    print("P[0:10] =", P[:10])
