"""Verificación numérica independiente y coincidencia entre lenguajes."""
from pathlib import Path
import subprocess
import sys
import tempfile
import math
from scipy.stats import chi2, kstwobign, kstest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'python'))
from modelo.simulacion import generar, analizar


def cerca(actual, esperado):
    assert math.isclose(actual, esperado, rel_tol=1e-10, abs_tol=1e-12), (actual, esperado)


with tempfile.TemporaryDirectory() as carpeta:
    subprocess.run(['javac', '-encoding', 'UTF-8', '--release', '11', '-d', carpeta,
                    str(RAIZ / 'java/modelo/Simulacion.java'),
                    str(RAIZ / 'tests/VerificarModelo.java')], check=True)

    def java(*args):
        return subprocess.check_output(['java', '-cp', carpeta, 'VerificarModelo', *map(str, args)], text=True).splitlines()

    for linea in java():
        tipo, gl, x, actual = linea.split(',')
        esperado = chi2.sf(float(x), int(gl)) if tipo == 'chi' else kstwobign.sf(float(x))
        cerca(float(actual), esperado)
    print('OK: 1001 comprobaciones de valores p de Java contra SciPy.')

    casos = [
        (10000, 12345, 1664525, 1013904223, 4294967296, 10),
        (50, 0, 0, 0, 16, 10),
        (1000, 1, 5, 1, 16, 10),
        (1000, 4503599627370495, 4503599627370495, 4503599627370495, 4503599627370496, 100),
    ]
    assert generar(5, 1, 5, 1, 16) == [6, 15, 12, 13, 2]
    for n, semilla, a, c, m, k in casos:
        valores = generar(n, semilla, a, c, m)
        u, ordenados, frecuencias, r = analizar(valores, m, k)
        lineas = java(n, semilla, a, c, m, k)
        assert list(map(int, lineas[1:])) == valores
        assert sum(frecuencias) == n and all(0 <= x < 1 for x in u)
        for actual, campo in zip(map(float, lineas[0].split(',')), ('chi2', 'p_chi2', 'd_mas', 'd_menos', 'ks', 'p_ks')):
            cerca(actual, r[campo])
        referencia = kstest(u, 'uniform', method='asymp')
        cerca(r['ks'], referencia.statistic)
        cerca(r['p_ks'], referencia.pvalue)
    print('OK: secuencias, límites, generador constante, desbordamiento y pruebas KS en 4 escenarios.')
