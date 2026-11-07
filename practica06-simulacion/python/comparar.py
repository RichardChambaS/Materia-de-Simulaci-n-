"""Compara las últimas ejecuciones de Java y Python sin modificar sus datos."""
import csv
from itertools import zip_longest
from pathlib import Path

CARPETA = Path(__file__).resolve().parents[1] / 'resultados'


def comparar():
    resumenes = []
    for lenguaje in ('java', 'python'):
        with (CARPETA / f'{lenguaje}_resumen.csv').open(encoding='utf-8') as f:
            resumenes.append(next(csv.DictReader(f)))
    java, python = resumenes
    for campo in ('n', 'm', 'a', 'c', 'semilla', 'k', 'alfa'):
        convertir = float if campo == 'alfa' else int
        if convertir(java[campo]) != convertir(python[campo]):
            print(f'No se puede comparar: el parámetro {campo} es diferente.')
            print('Ejecuta ambos programas con los mismos parámetros.')
            return
    diferencias = 0
    cantidad = 0
    with (CARPETA / 'java_secuencia.csv').open(encoding='utf-8') as fj, \
         (CARPETA / 'python_secuencia.csv').open(encoding='utf-8') as fp, \
         (CARPETA / 'comparacion.csv').open('w', newline='', encoding='utf-8') as salida:
        escritor = csv.writer(salida)
        escritor.writerow(['i', 'x_java', 'x_python', 'u_java', 'u_python', 'coincide'])
        for j, p in zip_longest(csv.DictReader(fj), csv.DictReader(fp)):
            if j is None or p is None:
                raise ValueError('Las secuencias tienen distinta cantidad de filas.')
            cantidad += 1
            igual = (int(j['i']) == int(p['i']) == cantidad and int(j['x']) == int(p['x'])
                     and abs(float(j['u']) - float(p['u'])) <= 1e-15)
            diferencias += not igual
            escritor.writerow([j['i'], j['x'], p['x'], j['u'], p['u'], igual])
    if cantidad != int(java['n']):
        raise ValueError('La cantidad de filas no coincide con N.')
    print(f'Valores comparados: {cantidad}. Diferencias: {diferencias}.')
    print('\nMedida                 Java              Python')
    for campo in ('chi2', 'p_chi2', 'ks', 'p_ks', 'tiempo_segundos'):
        print(f'{campo:18s} {float(java[campo]):17.10g} {float(python[campo]):17.10g}')
    print(f'\nTabla completa: {CARPETA / "comparacion.csv"}')
    print('Los tiempos incluyen generación y pruebas; excluyen consola, CSV y gráficas.')


if __name__ == '__main__':
    try:
        comparar()
    except FileNotFoundError:
        print('Primero ejecuta Java y Python con los mismos parámetros.')
        raise SystemExit(1)
    except (ValueError, KeyError, StopIteration, OSError) as error:
        print(f'No se pudo completar la comparación: {error}')
        raise SystemExit(1)
