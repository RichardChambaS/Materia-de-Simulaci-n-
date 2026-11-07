package modelo;

import java.math.BigInteger;
import java.util.Arrays;

/** LCG y pruebas de uniformidad; no contiene entrada ni salida. */
public class Simulacion {
    public int n, k;
    public long semilla, a, c, m;
    public double alfa, chi2, pChi2, dMas, dMenos, ks, pKs, segundos;
    public long[] valores;
    public double[] u, ordenados;
    public int[] frecuencias;

    public void calcular() {
        long inicio = System.nanoTime();
        valores = new long[n];
        u = new double[n];
        frecuencias = new int[k];
        BigInteger modulo = BigInteger.valueOf(m);
        BigInteger multiplicador = BigInteger.valueOf(a);
        BigInteger incremento = BigInteger.valueOf(c);
        BigInteger x = BigInteger.valueOf(semilla);
        // BigInteger evita desbordamientos en a*x+c con parámetros grandes.
        for (int i = 0; i < n; i++) {
            x = multiplicador.multiply(x).add(incremento).mod(modulo);
            valores[i] = x.longValue();
            u[i] = valores[i] / (double) m;
            frecuencias[(int) (valores[i] * k / m)]++;
        }
        double esperado = n / (double) k;
        chi2 = 0;
        for (int observada : frecuencias) {
            chi2 += (observada - esperado) * (observada - esperado) / esperado;
        }
        pChi2 = gammaQ((k - 1) / 2.0, chi2 / 2.0);
        ordenados = u.clone();
        Arrays.sort(ordenados);
        dMas = 0;
        dMenos = 0;
        for (int i = 0; i < n; i++) {
            dMas = Math.max(dMas, (i + 1.0) / n - ordenados[i]);
            dMenos = Math.max(dMenos, ordenados[i] - i / (double) n);
        }
        ks = Math.max(dMas, dMenos);
        pKs = probabilidadKS(Math.sqrt(n) * ks);
        segundos = (System.nanoTime() - inicio) / 1e9;
    }

    /** Cola de Kolmogorov: aproximación asintótica bilateral, igual que Python. */
    public static double probabilidadKS(double z) {
        if (z <= 0) return 1;
        double suma = 0;
        if (z < 1.18) {
            // Serie para la CDF: evita cancelación cuando p está cerca de 1.
            for (int j = 1; j < 10000; j++) {
                double termino = Math.exp(-Math.pow(2.0 * j - 1, 2) * Math.PI * Math.PI / (8 * z * z));
                suma += termino;
                if (termino < 1e-16) break;
            }
            return limitar(1 - Math.sqrt(2 * Math.PI) * suma / z);
        }
        for (int j = 1; j < 10000; j++) {
            double termino = 2 * Math.exp(-2.0 * j * j * z * z);
            suma += (j % 2 == 1) ? termino : -termino;
            if (termino < 1e-16) break;
        }
        return limitar(suma);
    }

    /** Q(s,x), cola gamma regularizada para s=(k-1)/2. */
    public static double gammaQ(double s, double x) {
        if (x <= 0) return 1;
        // s es entero o semientero: Gamma(1)=1 y Gamma(1/2)=sqrt(pi).
        double base = (s == Math.floor(s)) ? 1 : 0.5;
        double logGamma = (base == 1) ? 0 : Math.log(Math.PI) / 2;
        for (double t = base; t < s; t++) logGamma += Math.log(t);
        double factor = Math.exp(s * Math.log(x) - x - logGamma);
        if (x < s + 1) {
            double termino = 1 / s;
            double suma = termino;
            for (int i = 1; i < 10000; i++) {
                termino *= x / (s + i);
                suma += termino;
                if (Math.abs(termino) < Math.abs(suma) * 1e-14) break;
            }
            return limitar(1 - factor * suma);
        }
        // Fracción continua para calcular directamente la cola pequeña.
        double b = x + 1 - s;
        double c = 1e300;
        double d = 1 / b;
        double h = d;
        for (int i = 1; i < 10000; i++) {
            double an = -i * (i - s);
            b += 2;
            d = an * d + b;
            if (Math.abs(d) < 1e-300) d = 1e-300;
            c = b + an / c;
            if (Math.abs(c) < 1e-300) c = 1e-300;
            d = 1 / d;
            double cambio = d * c;
            h *= cambio;
            if (Math.abs(cambio - 1) < 1e-14) break;
        }
        return limitar(factor * h);
    }

    /** Valor crítico cuya probabilidad de cola es alfa. */
    public static double criticoChi2(int gl, double alfa) {
        double inferior = 0, superior = Math.max(1, gl);
        while (gammaQ(gl / 2.0, superior / 2) > alfa) superior *= 2;
        for (int i = 0; i < 1100; i++) {
            double medio = (inferior + superior) / 2;
            if (medio == inferior || medio == superior) break;
            if (gammaQ(gl / 2.0, medio / 2) > alfa) inferior = medio;
            else superior = medio;
        }
        return (inferior + superior) / 2;
    }

    public static double densidadChi2(int gl, double x) {
        double s = gl / 2.0;
        double base = (s == Math.floor(s)) ? 1 : .5;
        double logGamma = base == 1 ? 0 : Math.log(Math.PI) / 2;
        for (double t = base; t < s; t++) logGamma += Math.log(t);
        return Math.exp((s-1)*Math.log(x) - x/2 - s*Math.log(2) - logGamma);
    }

    private static double limitar(double p) {
        return Math.max(0, Math.min(1, p));
    }
}
