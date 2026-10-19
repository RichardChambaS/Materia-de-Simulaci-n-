# Gráficas de la práctica. Se guardan en la carpeta graficas/.
import os
import warnings

import matplotlib.pyplot as plt
import numpy as np

CARPETA = "graficas"


def mostrar():
    # Cuando no hay ventana disponible (por SSH, en un servidor o con
    # MPLBACKEND=Agg), plt.show() avisa que el backend no puede mostrar la figura.
    # La imagen ya quedó guardada, así que ese aviso es ruido y se silencia; si hay
    # ventana disponible se muestra igual que siempre.
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message=".*is non-interactive.*")
        plt.show()


def guardar(nombre_archivo):
    try:
        os.makedirs(CARPETA, exist_ok=True)
    except OSError as error:
        # Sin permisos, o con una ruta inválida, no hay dónde dejar la imagen.
        raise SystemExit(f"No se pudo crear la carpeta {CARPETA}/: {error}") from error
    plt.savefig(os.path.join(CARPETA, nombre_archivo), dpi=120)
    mostrar()
    plt.close()     # se cierra para que la próxima gráfica no la vuelva a mostrar


def titulo_escenario(r):
    e = r["escenario"]
    return f"{e.nombre}: λ = {e.llegada}, μ = {e.servicio}, ρ = {r['teoria'].rho:.2f}"


def grafica_cola(resultados):
    # Primera repetición completa (semilla base), un panel por escenario
    plt.figure(figsize=(10, 3 * len(resultados)))
    for i, r in enumerate(resultados):
        historial = r["ejemplo"].historial_cola
        tiempos = [t for t, tamano in historial]
        tamanos = [tamano for t, tamano in historial]

        plt.subplot(len(resultados), 1, i + 1)
        plt.step(tiempos, tamanos, where="post", label="Clientes en la cola")
        plt.axhline(y=r["teoria"].Lq, linestyle="--", color="red", label="Lq teórico")
        plt.axhline(y=r["ejemplo"].cola_promedio(), linestyle=":", color="orange",
                    label=f"Lq primera repetición = {r['ejemplo'].cola_promedio():.4f}")
        plt.ylabel("Clientes")
        plt.title(titulo_escenario(r))
        plt.grid(True)
        plt.legend()
    plt.xlabel("Tiempo")
    plt.tight_layout()
    guardar("cola_en_el_tiempo.png")


def grafica_esperas(resultados):
    # Todos los clientes que iniciaron atención en la primera repetición
    plt.figure(figsize=(10, 3 * len(resultados)))
    for i, r in enumerate(resultados):
        esperas = r["ejemplo"].esperas
        numeros = range(1, len(esperas) + 1)

        plt.subplot(len(resultados), 1, i + 1)
        plt.plot(numeros, esperas, label="Espera de cada cliente")
        plt.axhline(y=r["teoria"].Wq, linestyle="--", color="red", label="Wq teórico")
        plt.axhline(y=r["ejemplo"].espera_promedio(), linestyle=":", color="orange",
                    label=f"Wq primera repetición = {r['ejemplo'].espera_promedio():.4f}")
        plt.ylabel("Tiempo de espera")
        plt.title(titulo_escenario(r))
        plt.grid(True)
        plt.legend()
    plt.xlabel("Número de cliente")
    plt.tight_layout()
    guardar("tiempos_de_espera.png")


def grafica_comparacion(resultados):
    # Barras: teoría frente al promedio de todas las repeticiones de cada escenario
    nombres = [r["escenario"].nombre for r in resultados]
    posiciones = np.arange(len(resultados))
    ancho = 0.35

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.bar(posiciones - ancho / 2, [r["teoria"].Wq for r in resultados], ancho, label="Teórico")
    plt.bar(posiciones + ancho / 2, [r["espera_simulada"] for r in resultados], ancho, label="Simulado")
    plt.xticks(posiciones, nombres)
    plt.ylabel("Tiempo")
    plt.title("Tiempo promedio de espera en la cola (Wq)")
    plt.grid(True, axis="y")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.bar(posiciones - ancho / 2, [r["teoria"].Lq for r in resultados], ancho, label="Teórico")
    plt.bar(posiciones + ancho / 2, [r["cola_simulada"] for r in resultados], ancho, label="Simulado")
    plt.xticks(posiciones, nombres)
    plt.ylabel("Clientes")
    plt.title("Tamaño promedio de la cola (Lq)")
    plt.grid(True, axis="y")
    plt.legend()

    plt.tight_layout()
    guardar("teoria_vs_simulacion.png")
