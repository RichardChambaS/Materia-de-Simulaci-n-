"""Generación LCG y pruebas de uniformidad."""
from scipy.stats import chi2, kstwobign
from math import sqrt


def generar(n, semilla, a, c, m):
    valores = []
    x = semilla
    for _ in range(n):
        x = (a * x + c) % m
        valores.append(x)
    return valores


def analizar(valores, m, k):
    n = len(valores)
    u = [x / m for x in valores]
    frecuencias = [0] * k
    for x in valores:
        # Clasificación con enteros para evitar errores en los límites.
        frecuencias[x * k // m] += 1
    esperado = n / k
    chi = sum((o - esperado) ** 2 / esperado for o in frecuencias)
    ordenados = sorted(u)
    d_mas = max((i + 1) / n - x for i, x in enumerate(ordenados))
    d_menos = max(x - i / n for i, x in enumerate(ordenados))
    d = max(d_mas, d_menos)
    return u, ordenados, frecuencias, {
        'chi2': chi, 'gl': k - 1, 'p_chi2': float(chi2.sf(chi, k - 1)),
        'd_mas': d_mas, 'd_menos': d_menos, 'ks': d,
        'p_ks': float(kstwobign.sf(sqrt(n) * d)),
    }
