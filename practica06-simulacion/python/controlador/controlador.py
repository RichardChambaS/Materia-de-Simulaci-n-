"""Coordina la consola, el modelo y la exportación."""
import csv
from pathlib import Path
from time import perf_counter
from modelo.simulacion import generar, analizar
from vista.vista import parametros, mostrar, graficas, decision


def ejecutar():
    carpeta = Path(__file__).resolve().parents[2] / 'resultados'
    carpeta.mkdir(exist_ok=True)
    while True:
        p = parametros()
        inicio = perf_counter()
        valores = generar(p['n'], p['semilla'], p['a'], p['c'], p['m'])
        u, ordenados, frecuencias, r = analizar(valores, p['m'], p['k'])
        r['tiempo_segundos'] = perf_counter() - inicio
        mostrar(p, valores, u, frecuencias, r)
        with (carpeta / 'python_secuencia.csv').open('w', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)
            escritor.writerow(['i', 'x', 'u'])
            escritor.writerows((i, x, valor) for i, (x, valor) in enumerate(zip(valores, u), 1))
        with (carpeta / 'python_frecuencias.csv').open('w', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)
            escritor.writerow(['inferior', 'superior', 'observada', 'esperada'])
            escritor.writerows((i/p['k'], (i+1)/p['k'], o, p['n']/p['k']) for i, o in enumerate(frecuencias))
        resumen = dict(p, **r, decision_chi2=decision(r['p_chi2'], p['alfa']), decision_ks=decision(r['p_ks'], p['alfa']))
        with (carpeta / 'python_resumen.csv').open('w', newline='', encoding='utf-8') as f:
            escritor = csv.DictWriter(f, fieldnames=resumen.keys())
            escritor.writeheader()
            escritor.writerow(resumen)
        graficas(carpeta, p, u, ordenados, frecuencias, r)
        print(f'\nResultados guardados en: {carpeta}')
        print('Se reemplazan los resultados anteriores de Python.')
        if input('¿Realizar otro análisis? [s/N]: ').strip().lower() != 's':
            break
