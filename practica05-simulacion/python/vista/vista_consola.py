from modelo.generador_lcg import GeneradorLCG


def pedir_semilla():
    mostrar_seccion("ENTRADA DE DATOS")
    while True:
        texto = input("Semilla [12345]: ").strip()
        try:
            semilla = int(texto) if texto else 12345
            if 0 <= semilla < GeneradorLCG.M:
                return semilla
        except ValueError:
            pass
        print("Ingrese un entero entre 0 y 4294967295.")


def mostrar_resultados(semilla, valores):
    print("\n" + "=" * 64)
    print("          GENERADOR CONGRUENCIAL LINEAL - PYTHON")
    print("=" * 64)
    mostrar_seccion("PARÁMETROS")
    print(f"Multiplicador (a) : {GeneradorLCG.A}")
    print(f"Incremento (c)   : {GeneradorLCG.C}")
    print(f"Módulo (m)       : {GeneradorLCG.M}")
    print(f"Semilla          : {semilla}")
    print(f"Cantidad         : {len(valores)}")
    mostrar_seccion("PRIMERAS 20 OBSERVACIONES")
    print(f"{'Iteración':>10} | {'X':>12} | {'U':>15}")
    print("-----------+--------------+----------------")
    for i, valor in enumerate(valores[:20], start=1):
        print(f"{i:10d} | {valor:12d} | {GeneradorLCG.normalizar(valor):15.10f}")
    print("-" * 43)


def mostrar_comparacion(filas):
    print("Primeras 20 observaciones:\n")
    print(f"{'Iteración':>10} | {'X Java':>12} | {'X Python':>12} | {'Coincide':>10}")
    print("-----------+--------------+--------------+-----------")
    for fila in filas[:20]:
        print(f"{fila[0]:10d} | {fila[1]:12d} | {fila[2]:12d} | {fila[5]:>10}")
    print("-" * 52)


def cargar_pyplot():
    import matplotlib
    # Guarda la imagen incluso en equipos sin interfaz gráfica.
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    return plt


def guardar_grafica(valores, semilla, archivo):
    plt = cargar_pyplot()

    normalizados = [GeneradorLCG.normalizar(x) for x in valores]
    figura, eje = plt.subplots(figsize=(10, 4))
    eje.scatter(range(1, len(valores) + 1), normalizados, s=2, alpha=0.5)
    eje.set(title=f"Secuencia LCG - semilla {semilla}",
            xlabel="Iteración", ylabel="U = X / m", ylim=(0, 1))
    eje.grid(alpha=0.2)
    figura.tight_layout()
    figura.savefig(archivo, dpi=150)
    plt.close(figura)


def guardar_comparacion_lenguajes(filas, semilla, archivo):
    plt = cargar_pyplot()
    figura, ejes = plt.subplots(2, 1, figsize=(11, 7), layout="constrained")
    coincidencias = sum(fila[5] == "Sí" for fila in filas)
    figura.suptitle(f"Java vs. Python | LCG | semilla {semilla}\n"
                    f"Coincidencias exactas (X y U): {coincidencias:,} / {len(filas):,}",
                    fontsize=14)

    # Dos estilos permiten ver ambos lenguajes aunque sus valores se superpongan.
    primeras = filas[:20]
    ejes[0].plot([f[0] for f in primeras], [f[3] for f in primeras],
                 color="#2563eb", marker="o", markersize=8, markerfacecolor="none",
                 label="Java (círculos)")
    ejes[0].plot([f[0] for f in primeras], [f[4] for f in primeras],
                 color="#ea580c", linestyle="--", marker="x", label="Python (cruces)")
    ejes[0].set(title="Primeras 20 observaciones: las curvas se superponen si coinciden",
                xlabel="Iteración", ylabel="U = X / m", ylim=(0, 1))
    ejes[0].set_xticks(range(1, len(primeras) + 1))
    ejes[0].legend(loc="upper left", bbox_to_anchor=(1.01, 1))

    diferencias = [abs(f[3] - f[4]) for f in filas]
    ejes[1].plot([f[0] for f in filas], diferencias, color="#15803d")
    ejes[1].set(title=f"Las {len(filas):,} observaciones | Diferencia máxima: {max(diferencias):.6g}",
                xlabel="Iteración", ylabel="|U Java - U Python|")
    if max(diferencias) == 0:
        ejes[1].set_ylim(-0.01, 0.01)
        ejes[1].set_yticks([0])
    for eje in ejes:
        eje.grid(alpha=0.2)
    figura.savefig(archivo, dpi=180)
    plt.close(figura)


def guardar_comparacion_semillas(valores, otros_valores, semilla, otra_semilla, archivo):
    plt = cargar_pyplot()
    figura, ejes = plt.subplots(2, 1, figsize=(11, 7), layout="constrained")
    figura.suptitle(f"Cambio de semilla en Python | LCG | {len(valores):,} valores por secuencia",
                    fontsize=14)
    for datos, inicial, color, estilo in (
            (valores, semilla, "#2563eb", "-"),
            (otros_valores, otra_semilla, "#ea580c", "--")):
        normalizados = [GeneradorLCG.normalizar(x) for x in datos]
        ejes[0].plot(range(1, 21), normalizados[:20], marker="o", markersize=4,
                     linestyle=estilo, color=color, label=f"Semilla {inicial}")
        # Los mismos intervalos hacen comparables las dos distribuciones.
        ejes[1].hist(normalizados, bins=[i / 20 for i in range(21)],
                     histtype="step", linewidth=2, linestyle=estilo,
                     color=color, label=f"Semilla {inicial}")
    ejes[0].set(title="Primeras 20 observaciones: efecto de cambiar el punto de partida",
                xlabel="Iteración", ylabel="U = X / m", ylim=(0, 1))
    ejes[0].set_xticks(range(1, 21))
    ejes[1].set(title="Distribución de los valores (20 intervalos comunes)",
                xlabel="U = X / m", ylabel="Frecuencia", xlim=(0, 1))
    for eje in ejes:
        eje.legend(loc="upper left", bbox_to_anchor=(1.01, 1))
        eje.grid(alpha=0.2)
    figura.savefig(archivo, dpi=180)
    plt.close(figura)


def mostrar_mensaje(mensaje):
    print(mensaje)


def mostrar_seccion(titulo):
    print("\n" + "-" * 64)
    print(titulo)
    print("-" * 64)
