"""Capa CONTROLADOR de la Práctica 01 de Simulación.

Responsabilidades:
  1. Definir los datos de entrada (la tabla de la guía).
  2. Llamar al modelo una vez por fila.
  3. Pasar los resultados ya calculados a la vista.
  4. Ejecutar las dos versiones pedidas: ORIGINAL y AJUSTADA.

No hace cálculos matemáticos: eso es trabajo del modelo.
"""

from modelo.clima_modelo import ClimaModelo
from vista.clima_vista import ClimaVista

# ----------------------------------------------------------------------
# Datos de entrada de la guía: (hora, humedad %, nubosidad %, temperatura °C)
# ----------------------------------------------------------------------
DATOS = [
    ("06:00", 65, 40, 14),
    ("08:00", 70, 50, 16),
    ("10:00", 68, 45, 18),
    ("12:00", 60, 30, 22),
    ("14:00", 75, 70, 20),
    ("16:00", 85, 85, 18),
    ("18:00", 92, 95, 16),
    ("20:00", 88, 90, 17),
    ("22:00", 80, 75, 15),
]

# ----------------------------------------------------------------------
# Las dos ejecuciones a comparar (los pesos son el ajuste del modelo)
# ----------------------------------------------------------------------
PESOS_ORIGINAL = (0.5, 0.3, 0.2)
PESOS_AJUSTADO = (0.6, 0.25, 0.15)


class ClimaControlador:
    """Orquesta la simulación completa."""

    def __init__(self):
        # El controlador es quien conoce y crea las capas de modelo y vista.
        self.vista = ClimaVista()

    def ejecutar(self):
        """Punto de entrada de la aplicación: corre las dos simulaciones."""
        print("PRÁCTICA 01 - SIMULACIÓN: modelo matemático de lluvia")
        print("I = peso_h*H + peso_n*N + peso_tf*Tf")

        # Las dos ejecuciones a comparar. El título de cada tabla se arma con
        # f-string a partir de los mismos pesos, así no hay datos duplicados.
        self._simular("original", *PESOS_ORIGINAL)
        self._simular("ajustado", *PESOS_AJUSTADO)

    def _simular(self, nombre, peso_h, peso_n, peso_tf):
        """Crea el modelo con los pesos recibidos, simula y delega la presentación.

        Los pesos son parámetros del modelo; la fórmula no cambia entre
        ejecuciones, solo la calibración.
        """
        modelo = ClimaModelo(peso_h=peso_h, peso_n=peso_n, peso_tf=peso_tf, nombre=nombre)
        titulo = f"MODELO {nombre.upper()} - pesos {peso_h:.2f} / {peso_n:.2f} / {peso_tf:.2f}"

        filas = []
        for hora, humedad, nubosidad, temperatura in DATOS:
            # Una llamada al modelo por fila de la tabla.
            resultado = modelo.calcular(humedad, nubosidad, temperatura)
            # Se juntan los datos de entrada con los resultados calculados.
            filas.append({
                "hora": hora,
                "humedad": humedad,
                "nubosidad": nubosidad,
                "temperatura": temperatura,
                **resultado,
            })

        # La vista solo presenta: tabla en consola y gráficas.
        self.vista.mostrar_tabla(titulo, filas)
        self.vista.graficar(filas, modelo.nombre)
