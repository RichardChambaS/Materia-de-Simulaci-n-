"""Ejecuta los cuatro modelos y guarda sus gráficas: python main.py."""

import numpy as np
import pandas as pd

from config import DATOS, DT
from parametros import estimar_parametros, tabla_epsilon
from modelos.deterministico import deterministico
from modelos.discreto import discreto
from modelos.estocastico import estocastico
from modelos.continuo import continuo_euler
from graficas.grafica_deterministico import graficar_deterministico
from graficas.grafica_discreto import graficar_discreto
from graficas.grafica_estocastico import graficar_estocastico
from graficas.grafica_continuo import graficar_continuo
from graficas.grafica_comparativa import graficar_comparativa
from graficas.grafica_influencia_r import graficar_influencia_r


def main():
    p = estimar_parametros()
    t = np.arange(len(DATOS))
    print(f"r discreto = {p['r_d']:.6f}")
    print(f"r continuo = {p['r_c']:.6f}")
    print(f"sigma = {p['sigma']:.4f}")
    print(f"dt = {DT}")
    print("Residuos medidos:")
    print(tabla_epsilon(p["epsilon"]))

    det = deterministico(p["P0"], p["r_c"], p["n"])
    dis = discreto(p["P0"], p["r_d"], p["n"])
    est = estocastico(p["P0"], p["r_d"], p["epsilon"], p["sigma"])
    con = continuo_euler(p["P0"], p["r_c"], p["n"], DT)

    graficar_deterministico(det[0], det[1], t, DATOS)
    graficar_discreto(dis[0], dis[1], t, DATOS)
    graficar_estocastico(est, t, DATOS)
    graficar_continuo(con[0], con[1], t, DATOS)
    graficar_comparativa(det, dis, est, con, t, DATOS)
    graficar_influencia_r(p["r_c"], p["P0"], p["n"], t, DATOS)

    tabla = pd.DataFrame({
        "Tiempo": t,
        "Datos": DATOS,
        "Determinístico": det[1],
        "Discreto": dis[1],
        "Estocástico": est["poblacion"],
        "Euler": np.interp(t, con[0], con[1]),
    })
    print("\nComparación por período:")
    print(tabla.round(2).to_string(index=False))
    print("\nSe guardaron seis gráficas en resultados/.")


if __name__ == "__main__":
    main()
