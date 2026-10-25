"""Genera las figuras vectoriales del informe a partir de los CSV de las corridas."""
from pathlib import Path
import csv
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / 'figures'
OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10.5,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.labelcolor': '#263442', 'text.color': '#263442',
    'axes.edgecolor': '#8A98A2', 'grid.color': '#DFE6EA',
    'pdf.fonttype': 42, 'savefig.facecolor': 'white'})


def leer(nombre):
    with (BASE / 'data' / nombre).open() as archivo:
        return [{k: int(float(v)) for k, v in row.items()} for row in csv.DictReader(archivo)]


def guardar(fig, nombre):
    fig.savefig(OUT / f'{nombre}.pdf', bbox_inches='tight')
    fig.savefig(OUT / f'{nombre}.png', dpi=240, bbox_inches='tight')
    plt.close(fig)


def preparar(ax, titulo, ymax=100):
    ax.set(title=titulo, xlabel='Tiempo (pasos)', ylabel='Personas', xlim=(0, 100), ylim=(0, ymax))
    ax.set_xticks(range(0, 101, 10))
    ax.grid(alpha=0.8, linewidth=0.65)
    ax.set_axisbelow(True)


def evolucion(datos, nombre, herramienta):
    fig, ax = plt.subplots(figsize=(6.5, 3.05), layout='constrained')
    preparar(ax, f'Evolución SIR en {herramienta}')
    for key, etiqueta, color in [('susceptibles', 'S: susceptibles', '#2068B4'),
            ('infectados', 'I: infectados', '#C63145'), ('recuperados', 'R: recuperados', '#26854B')]:
        ax.plot([r['tiempo'] for r in datos], [r[key] for r in datos], label=etiqueta, color=color, lw=1.9)
    peak = max(datos, key=lambda r: r['infectados'])
    ax.scatter([peak['tiempo']], [peak['infectados']], s=25, color='#C63145', zorder=4)
    ax.annotate(f"Pico: {peak['infectados']} en t = {peak['tiempo']}",
        (peak['tiempo'], peak['infectados']), xytext=(15, 24), textcoords='offset points',
        fontsize=9, arrowprops={'arrowstyle':'-', 'color':'#7D8791'})
    ax.legend(loc='upper right', frameon=True, fontsize=8.6, edgecolor='#DDE3E7')
    guardar(fig, nombre)

java = leer('resultados_java.csv')
netlogo = leer('resultados_netlogo.csv')
evolucion(java, '01_evolucion_java', 'Java')
evolucion(netlogo, '02_evolucion_netlogo', 'NetLogo')
for idx, key, titulo in [(3, 'susceptibles', 'Susceptibles'), (4, 'infectados', 'Infectados'), (5, 'recuperados', 'Recuperados')]:
    fig, ax = plt.subplots(figsize=(6.5, 2.9), layout='constrained')
    preparar(ax, f'Comparación de {titulo.lower()}', 50 if key=='infectados' else 100)
    for datos, etiqueta, color, estilo in [(java, 'Java', '#202A35', '-'), (netlogo, 'NetLogo', '#D27A16', '--')]:
        ax.plot([r['tiempo'] for r in datos], [r[key] for r in datos], label=etiqueta, color=color, ls=estilo, lw=1.9)
    ax.legend(loc='upper right', frameon=True, fontsize=9, edgecolor='#DDE3E7')
    guardar(fig, f'{idx:02d}_comparacion_{key}')

fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.1), sharey=True, layout='constrained')
for ax, herramienta, bajo, alto in [(axes[0], 'Java', java, leer('gamma040_java.csv')),
        (axes[1], 'NetLogo', netlogo, leer('gamma040_netlogo.csv'))]:
    preparar(ax, herramienta, 50)
    ax.set_xticks([0, 25, 50, 75, 100])
    for datos, etiqueta, color, estilo in [(bajo, r'$\gamma = 0.10$', '#2068B4', '-'),
            (alto, r'$\gamma = 0.40$', '#B44B31', '--')]:
        ax.plot([r['tiempo'] for r in datos], [r['infectados'] for r in datos], label=etiqueta, color=color, ls=estilo, lw=1.9)
    ax.legend(loc='upper right', fontsize=8.6, frameon=True)
axes[1].set_ylabel('')
guardar(fig, '06_efecto_gamma')

resumen = {}
for nombre in ['resultados_java.csv', 'resultados_netlogo.csv', 'gamma040_java.csv', 'gamma040_netlogo.csv']:
    rows = leer(nombre)
    assert len(rows)==101 and all(sum(r[k] for k in ['susceptibles','infectados','recuperados'])==100 for r in rows)
    assert all(b['susceptibles']<=a['susceptibles'] and b['recuperados']>=a['recuperados'] for a,b in zip(rows,rows[1:]))
    peak = max(rows, key=lambda r:r['infectados'])
    resumen[nombre] = {'pico_i':peak['infectados'], 'tiempo_pico':peak['tiempo'],
        'primer_tiempo_sin_infectados':next((r['tiempo'] for r in rows if r['infectados']==0), None),
        'estado_final':rows[-1]}
(BASE / 'data' / 'resumen_resultados.json').write_text(json.dumps(resumen, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(resumen, ensure_ascii=False, indent=2))
