package modelo;

public class GeneradorLCG {
    public static final long A = 1664525L;
    public static final long C = 1013904223L;
    public static final long M = 4294967296L;
    private final long semilla;

    public GeneradorLCG(long semilla) {
        if (semilla < 0 || semilla >= M) {
            throw new IllegalArgumentException("La semilla debe estar entre 0 y " + (M - 1));
        }
        this.semilla = semilla;
    }

    public long[] generar(int cantidad) {
        long[] valores = new long[cantidad];
        long actual = semilla;
        for (int i = 0; i < cantidad; i++) {
            // long permite calcular el producto sin desbordar int.
            actual = (A * actual + C) % M;
            valores[i] = actual;
        }
        return valores;
    }

    public static double normalizar(long valor) {
        // La conversión evita una división entera.
        return valor / (double) M;
    }
}
