package vista;

import java.util.Locale;
import java.util.Scanner;
import modelo.GeneradorLCG;

public class VistaConsola {
    public long pedirSemilla() {
        Scanner entrada = new Scanner(System.in);
        mostrarSeccion("ENTRADA DE DATOS");
        while (true) {
            System.out.print("Semilla [12345]: ");
            String texto = entrada.nextLine().trim();
            try {
                long semilla = texto.isEmpty() ? 12345L : Long.parseLong(texto);
                if (semilla >= 0 && semilla < GeneradorLCG.M) {
                    return semilla;
                }
            } catch (NumberFormatException e) {
                // Se vuelve a pedir el dato cuando no es un entero válido.
            }
            System.out.println("Ingrese un entero entre 0 y 4294967295.");
        }
    }

    public void mostrarResultados(long semilla, long[] valores) {
        System.out.println("\n================================================================");
        System.out.println("          GENERADOR CONGRUENCIAL LINEAL - JAVA");
        System.out.println("================================================================");
        mostrarSeccion("PARÁMETROS");
        System.out.printf("Multiplicador (a) : %d%n", GeneradorLCG.A);
        System.out.printf("Incremento (c)   : %d%n", GeneradorLCG.C);
        System.out.printf("Módulo (m)       : %d%n", GeneradorLCG.M);
        System.out.printf("Semilla          : %d%n", semilla);
        System.out.printf("Cantidad         : %d%n", valores.length);
        mostrarSeccion("PRIMERAS 20 OBSERVACIONES");
        System.out.printf("%10s | %12s | %15s%n", "Iteración", "X", "U");
        System.out.println("-----------+--------------+----------------");
        for (int i = 0; i < Math.min(20, valores.length); i++) {
            System.out.printf(Locale.ROOT, "%10d | %12d | %15.10f%n",
                    i + 1, valores[i], GeneradorLCG.normalizar(valores[i]));
        }
        System.out.println("-------------------------------------------");
    }

    public void mostrarSeccion(String titulo) {
        System.out.println("\n----------------------------------------------------------------");
        System.out.println(titulo);
        System.out.println("----------------------------------------------------------------");
    }

    public void mostrarMensaje(String mensaje) {
        System.out.println(mensaje);
    }
}
