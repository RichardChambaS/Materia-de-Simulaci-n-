"""Configuración central del proyecto.

Único lugar donde se definen los datos de entrada y los parámetros
ajustables. Todo el resto del código importa desde aquí, de modo que
cambiar el arreglo de datos o dt no requiere tocar los modelos.
"""

import numpy as np

# ----------------------------------------------------------------------
# Datos de entrada: población observada en t = 0, 1, ..., 6
# ----------------------------------------------------------------------
DATOS = np.array([1000, 1100, 1250, 1400, 1600, 1850, 2100], dtype=float)

# ----------------------------------------------------------------------
# Parámetros configurables
# ----------------------------------------------------------------------
# Tamaño de paso para el modelo continuo (Euler).
DT = 0.1

# Desviación estándar muestral de los residuos (ddof=1).
# Si se quiere la poblacional, cambiar a 0.
DDOF = 1

# Escenarios de r utilizados en la gráfica de influencia (sensibilidad).
# Se construyen a partir de r_c estimado de los datos.
def escenarios_r(r_c: float) -> dict:
    """Retorna los valores de r para estudiar su influencia."""
    return {
        f"r_c = {r_c:.4f} (estimado)": r_c,
        "r_c / 2 (crecimiento lento)": r_c / 2,
        "2 · r_c (crecimiento rápido)": 2 * r_c,
        "r = 0 (sin crecimiento)": 0.0,
        f"-r_c = {-r_c:.4f} (decrecimiento)": -r_c,
    }
