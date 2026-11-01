class GeneradorLCG:
    A = 1664525
    C = 1013904223
    M = 2 ** 32

    def __init__(self, semilla):
        if not 0 <= semilla < self.M:
            raise ValueError("La semilla debe estar entre 0 y 4294967295.")
        self.semilla = semilla

    def generar(self, cantidad):
        valores = []
        actual = self.semilla
        for _ in range(cantidad):
            # Cada resultado se utiliza para calcular el siguiente.
            actual = (self.A * actual + self.C) % self.M
            valores.append(actual)
        return valores

    @staticmethod
    def normalizar(valor):
        return valor / GeneradorLCG.M
