"""Estimacion de parametros a partir de los datos observados.

Todo se calcula desde ``config.DATOS``. Aqui NO hay aleatoriedad
ni valores quemados.
"""

import numpy as np

from config import DATOS, DDOF


def estimar_parametros(datos=None):
    """Estima r_d, r_c, los residuos epsilon y sigma a partir de los datos.

    Retorna un diccionario con todos los parametros y la tabla de residuos.
    """
    if datos is None:
        datos = DATOS

    datos = np.asarray(datos, dtype=float)
    n = len(datos) - 1  # numero de intervalos

    # --- tasas -------------------------------------------------------
    # r discreto: crecimiento geometrico por periodo (modelos discreto y estocastico)
    r_d = (datos[-1] / datos[0]) ** (1 / n) - 1

    # r continuo: tasa exponencial continua (deterministico y Euler)
    r_c = np.log(datos[-1] / datos[0]) / n

    # --- residuos observados (ruido medido, NO sorteado) -------------
    # epsilon_t = datos[t+1] - (datos[t] + r_d * datos[t])
    epsilon = datos[1:] - (datos[:-1] + r_d * datos[:-1])

    # desviacion estandar de los residuos (ddof=1 -> estimador de muestra)
    sigma = float(np.std(epsilon, ddof=DDOF))

    return {
        "r_d": float(r_d),
        "r_c": float(r_c),
        "epsilon": epsilon,
        "sigma": sigma,
        "n": n,
        "P0": float(datos[0]),
    }


def tabla_epsilon(epsilon):
    """Retorna la tabla de residuos como texto formateado."""
    lineas = [" t   epsilon_t"]
    lineas.append("---  ---------")
    for t, e in enumerate(epsilon, start=1):
        lineas.append(f" {t - 1}->{t}  {e:9.4f}")
    return "\n".join(lineas)


if __name__ == "__main__":
    from config import DT

    p = estimar_parametros()
    print("=== Parametros estimados desde los datos ===")
    print(f"r_d (discreto)      = {p['r_d']:.6f}")
    print(f"r_c (continuo)      = {p['r_c']:.6f}")
    print(f"sigma (ddof={DDOF})        = {p['sigma']:.4f}")
    print(f"dt                  = {DT}")
    print(f"verificacion 1+r_d = e^r_c : {1 + p['r_d']:.6f} vs {np.exp(p['r_c']):.6f}")
    print("\nResiduos observados epsilon_t:")
    print(tabla_epsilon(p["epsilon"]))
