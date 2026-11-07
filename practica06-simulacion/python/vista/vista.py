"""Entrada por consola, presentación y gráficas."""
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def entero(nombre, defecto, minimo, maximo):
    while True:
        try:
            texto = input(f'{nombre} [{defecto}]: ').strip()
            valor = int(texto) if texto else defecto
            if minimo <= valor <= maximo:
                return valor
        except ValueError:
            pass
        print(f'Ingresa un entero entre {minimo} y {maximo}.')


def parametros():
    print('\nLCG y pruebas de uniformidad. Enter utiliza el valor entre corchetes.')
    print('1. Caso base de la práctica')
    print('2. Ingresar mis propios datos')
    opcion = entero('Selecciona una opción', 1, 1, 2)
    if opcion == 1:
        print('Caso base: N=10000, m=4294967296, a=1664525, c=1013904223,')
        print('semilla=12345, k=10, alfa=0.05.')
        return dict(n=10000, m=4294967296, a=1664525, c=1013904223,
                    semilla=12345, k=10, alfa=0.05)
    n = entero('Cantidad N', 10000, 50, 1000000)
    m = entero('Módulo m', 4294967296, 2, 4503599627370496)
    a = entero('Multiplicador a', min(1664525, m - 1), 0, m - 1)
    c = entero('Incremento c', min(1013904223, m - 1), 0, m - 1)
    semilla = entero('Semilla', min(12345, m - 1), 0, m - 1)
    k = entero('Número de intervalos k', 10, 2, min(100, n // 5))
    while True:
        try:
            texto = input('Significancia alfa [0.05]: ').strip()
            alfa = float(texto.replace(',', '.')) if texto else 0.05
            if math.isfinite(alfa) and 0 < alfa < 1:
                break
        except ValueError:
            pass
        print('Ingresa un número mayor que 0 y menor que 1.')
    return dict(n=n, m=m, a=a, c=c, semilla=semilla, k=k, alfa=alfa)


def decision(p, alfa):
    return 'Se rechaza H0' if p < alfa else 'No se rechaza H0'


def mostrar(p, valores, u, frecuencias, r):
    print('\nPrimeros 20 valores (la secuencia completa se guarda en CSV):')
    for i, (x, valor) in enumerate(zip(valores[:20], u[:20]), 1):
        print(f'{i:4d}  X={x:16d}  U={valor:.10f}')
    print('\nIntervalo             Observada   Esperada')
    for i, f in enumerate(frecuencias):
        print(f'[{i/p["k"]:.3f}, {(i+1)/p["k"]:.3f})  {f:10d}  {p["n"]/p["k"]:9.2f}')
    print(f'\nChi-cuadrado = {r["chi2"]:.8g}, gl = {r["gl"]}, p = {r["p_chi2"]:.8g}')
    print(decision(r['p_chi2'], p['alfa']))
    print(f'D+ = {r["d_mas"]:.8g}, D- = {r["d_menos"]:.8g}')
    print(f'KS = {r["ks"]:.8g}, p asintótico = {r["p_ks"]:.8g}')
    print(decision(r['p_ks'], p['alfa']))
    print('No rechazar H0 no demuestra aleatoriedad ni independencia.')


def graficas(carpeta, p, u, ordenados, frecuencias, r):
    fig, ejes = plt.subplots(1, 3, figsize=(16, 4.8))
    fig.suptitle(f'Python | N={p["n"]} | semilla={p["semilla"]} | k={p["k"]}')
    k = p['k']
    ejes[0].bar([(i + .5) / k for i in range(k)], frecuencias,
                width=.9 / k, color='#2677b8', label='Observada')
    ejes[0].axhline(p['n'] / k, color='#e68127', label='Esperada N/k')
    ejes[0].set(title='Frecuencias', xlabel='U', ylabel='Cantidad', xlim=(0, 1))
    ejes[0].legend()
    # Escalones completos, incluidos extremos y valores repetidos.
    ejes[1].step([0] + ordenados + [1], [0] + [(i+1)/len(u) for i in range(len(u))] + [1],
                 where='post', color='#2677b8', label='Empírica')
    ejes[1].plot([0, 1], [0, 1], '--', color='#e68127', label='Teórica F(x)=x')
    ejes[1].set(title='Distribución acumulada (KS)', xlabel='U', ylabel='F(U)', xlim=(0, 1), ylim=(0, 1))
    ejes[1].legend()
    limite = min(200, len(u))
    ejes[2].plot(range(1, limite+1), u[:limite], '.-', linewidth=.6, color='#2677b8')
    ejes[2].set(title=f'Primeros {limite} valores', xlabel='Índice i', ylabel='Uᵢ', ylim=(0, 1))
    for eje in ejes:
        eje.grid(alpha=.2)
    fig.tight_layout()
    fig.savefig(carpeta / 'python_graficas.png', dpi=150)
    plt.close(fig)

    # Desglose de los estadísticos: suma de aportes y máximo de diferencias.
    esperado = p['n'] / k
    aportes = [(o - esperado) ** 2 / esperado for o in frecuencias]
    posiciones = range(1, p['n'] + 1)
    mas = [i / p['n'] - x for i, x in zip(posiciones, ordenados)]
    menos = [x - (i - 1) / p['n'] for i, x in zip(posiciones, ordenados)]
    fig, ejes = plt.subplots(1, 2, figsize=(12, 5.5))
    fig.suptitle(f'Cálculo de las pruebas | Python | N={p["n"]} | semilla={p["semilla"]}')
    ejes[0].bar(range(1, k + 1), aportes, color='#2677b8')
    ejes[0].set(title=f'Chi² = suma de aportes = {r["chi2"]:.8g}',
                xlabel='Intervalo j', ylabel='Aporte (Oj - Ej)² / Ej')
    if k <= 20:
        ejes[0].set_xticks(range(1, k + 1))
    ejes[1].plot(posiciones, mas, color='#2677b8', label='i/N - U(i)')
    ejes[1].plot(posiciones, menos, color='#e68127', label='U(i) - (i-1)/N')
    for datos, color, nombre in [(mas, '#2677b8', 'D+'), (menos, '#e68127', 'D-')]:
        indice = max(range(len(datos)), key=datos.__getitem__)
        ejes[1].scatter(indice + 1, datos[indice], s=60, color=color, edgecolor='black', zorder=4,
                        label=f'{nombre} = {datos[indice]:.8g}')
    ejes[1].axhline(0, color='gray', linewidth=.7)
    ejes[1].set(title=f'KS = máximo de D+ y D- = {r["ks"]:.8g}',
                xlabel='Posición i en la secuencia ordenada', ylabel='Diferencia con la uniforme')
    ejes[1].legend(fontsize=8)
    for eje in ejes:
        eje.grid(axis='y', alpha=.2)
    fig.text(.08, .04, f'p Chi² = {r["p_chi2"]:.8g} | alfa = {p["alfa"]:g} | {decision(r["p_chi2"], p["alfa"])}')
    fig.text(.54, .04, f'p KS asintótico = {r["p_ks"]:.8g} | {decision(r["p_ks"], p["alfa"])}')
    fig.tight_layout(rect=(0, .08, 1, .95))
    fig.savefig(carpeta / 'python_calculos.png', dpi=150)
    plt.close(fig)

    grafica_hipotesis(carpeta, p, r)


def grafica_hipotesis(carpeta, p, r):
    from scipy.stats import chi2
    import numpy as np

    gl = p['k'] - 1
    critico = chi2.isf(p['alfa'], gl)
    limite = max(chi2.isf(.001, gl), critico * 1.2)
    # Incluir exactamente el punto crítico para delimitar el sombreado.
    x = np.unique(np.append(np.linspace(limite / 2000, limite, 2000), critico))
    y = chi2.pdf(x, gl)
    fig, eje = plt.subplots(figsize=(11, 6))
    eje.plot(x, y, color='#333333', label=f'Distribución Chi², gl={gl}')
    eje.fill_between(x, y, where=x <= critico, color='#b8dbce', label='Región de no rechazo de H₀')
    eje.fill_between(x, y, where=x >= critico, color='#eaa6a6', label=f'Región de rechazo (área total α={p["alfa"]:g})')
    eje.axvline(critico, color='#b83a3a', linestyle='--', label=f'Valor crítico = {critico:.6g}')
    if r['chi2'] <= limite:
        eje.axvline(r['chi2'], color='#2677b8', linewidth=2, label=f'Chi² observado = {r["chi2"]:.6g}')
    else:
        eje.plot([], [], color='#2677b8', label=f'Chi² observado = {r["chi2"]:.6g} (fuera del eje, a la derecha)')
        eje.annotate('Observado →', xy=(.98, .45), xycoords='axes fraction', ha='right', color='#2677b8')
    eje.set(xlim=(0, limite), ylim=(0, max(y)*1.1), xlabel='Valor del estadístico Chi²', ylabel='Densidad',
            title=f'Decisión de la hipótesis | Python | N={p["n"]} | gl={gl}')
    eje.legend(fontsize=9)
    eje.grid(alpha=.15)
    fig.text(.10, .065, f'p = {r["p_chi2"]:.8g} | α = {p["alfa"]:g} | {decision(r["p_chi2"], p["alfa"])}', fontsize=12)
    fig.text(.10, .025, 'Se rechaza si p < α. No rechazar no demuestra H₀. La cola continúa más allá del eje.', fontsize=10)
    fig.tight_layout(rect=(0, .11, 1, 1))
    fig.savefig(carpeta / 'python_hipotesis.png', dpi=150)
    plt.close(fig)
