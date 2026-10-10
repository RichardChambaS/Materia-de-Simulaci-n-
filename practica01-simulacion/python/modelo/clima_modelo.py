"""Capa MODELO de la Práctica 01 de Simulación.

Responsabilidad única: hacer los cálculos del modelo matemático de lluvia.

    I = peso_h * H + peso_n * N + peso_tf * Tf

Donde:
    H  = humedad normalizada      (humedad / 100)
    N  = nubosidad normalizada    (nubosidad / 100)
    Tf = factor de temperatura    (ver tabla de la guía)

Reglas de esta capa:
  * NO imprime nada (no hay print).
  * NO genera gráficas.
  * NO contiene los datos de la tabla de entrada (los aporta el controlador).
  * Los pesos son PARÁMETROS del modelo, nunca constantes dentro de la fórmula.
"""

# Umbrales de la tabla de reglas de la guía (constantes del modelo).
UMBRAL_BAJA = 0.40      # I >= 0.40  -> deja de ser "Sin lluvia"
UMBRAL_PROBABLE = 0.60  # I >= 0.60  -> "Lluvia probable"
UMBRAL_LLUVIA = 0.75    # I >= 0.75  -> "Lluvia"


class ClimaModelo:
    """Modelo matemático de lluvia con pesos configurables.

    Los tres pesos se inyectan al construir el objeto, por lo que la misma
    fórmula sirve para el modelo ORIGINAL y para el modelo AJUSTADO.
    """

    def __init__(self, peso_h=0.5, peso_n=0.3, peso_tf=0.2, nombre="original"):
        # Parámetros del modelo (se pueden cambiar sin tocar la fórmula).
        self.peso_h = peso_h
        self.peso_n = peso_n
        self.peso_tf = peso_tf
        # Nombre usado por la vista para nombrar los archivos PNG.
        self.nombre = nombre

    # ------------------------------------------------------------------
    # Variables del modelo
    # ------------------------------------------------------------------
    @staticmethod
    def normalizar(porcentaje):
        """Convierte un porcentaje (0-100) en el valor normalizado H o N."""
        return porcentaje / 100.0

    @staticmethod
    def factor_temperatura(temperatura):
        """Tf = clamp(1.0 - 0.05 * (T - 10), 0.1, 1.0).

        Esta forma lineal reproduce exactamente la tabla de la guía:
            <=10 -> 1.00 | 12->0.90 | 14->0.80 | 16->0.70 | 18->0.60
            20->0.50 | 22->0.40 | 24->0.30 | 26->0.20 | >=28 -> 0.10
        y además cubre las temperaturas intermedias (15 -> 0.75, 17 -> 0.65).
        """
        valor = 1.0 - 0.05 * (temperatura - 10.0)
        # clamp: limita el resultado al rango [0.1, 1.0]
        return max(0.1, min(1.0, valor))

    # ------------------------------------------------------------------
    # Relaciones matemáticas
    # ------------------------------------------------------------------
    def indice(self, h, n, tf):
        """Índice de lluvia: I = peso_h*H + peso_n*N + peso_tf*Tf.

        Recibe las variables ya normalizadas para dejar el cálculo explícito.
        """
        return self.peso_h * h + self.peso_n * n + self.peso_tf * tf

    @staticmethod
    def estado(indice):
        """Traduce el índice I al estado correspondiente (tabla de reglas)."""
        if indice < UMBRAL_BAJA:
            return "Sin lluvia"
        if indice < UMBRAL_PROBABLE:
            return "Baja posibilidad"
        if indice < UMBRAL_LLUVIA:
            return "Lluvia probable"
        return "Lluvia"

    def calcular(self, humedad, nubosidad, temperatura):
        """Calcula todas las variables del modelo para una fila de entrada.

        Entrada : los valores medidos de una hora -> humedad (%), nubosidad (%)
                  y temperatura (°C). La hora no interviene en el cálculo.
        Salida  : diccionario con h, n, tf, indice y estado.
        """
        h = self.normalizar(humedad)
        n = self.normalizar(nubosidad)
        tf = self.factor_temperatura(temperatura)
        indice = self.indice(h, n, tf)
        return {
            "h": h,
            "n": n,
            "tf": tf,
            "indice": indice,
            "estado": self.estado(indice),
        }
