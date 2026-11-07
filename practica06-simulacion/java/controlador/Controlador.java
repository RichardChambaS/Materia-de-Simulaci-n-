package controlador;

import modelo.Simulacion;
import vista.Vista;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.charset.StandardCharsets;
import java.io.BufferedWriter;
import java.io.IOException;

public class Controlador {
    public void ejecutar() throws IOException {
        Vista vista = new Vista();
        Path carpeta = Path.of("resultados").toAbsolutePath();
        Files.createDirectories(carpeta);
        do {
            Simulacion s = vista.parametros();
            s.calcular();
            vista.mostrar(s);
            guardar(carpeta, s);
            vista.graficas(carpeta, s);
            System.out.println("\nResultados guardados en: " + carpeta);
            System.out.println("Se reemplazan los resultados anteriores de Java.");
        } while (vista.repetir());
    }

    private void guardar(Path carpeta, Simulacion s) throws IOException {
        try (BufferedWriter w = Files.newBufferedWriter(carpeta.resolve("java_secuencia.csv"), StandardCharsets.UTF_8)) {
            w.write("i,x,u\n");
            for (int i = 0; i < s.n; i++) w.write((i+1) + "," + s.valores[i] + "," + s.u[i] + "\n");
        }
        try (BufferedWriter w = Files.newBufferedWriter(carpeta.resolve("java_frecuencias.csv"), StandardCharsets.UTF_8)) {
            w.write("inferior,superior,observada,esperada\n");
            for (int i = 0; i < s.k; i++) {
                w.write(i/(double)s.k + "," + (i+1.0)/s.k + "," + s.frecuencias[i] + "," + s.n/(double)s.k + "\n");
            }
        }
        try (BufferedWriter w = Files.newBufferedWriter(carpeta.resolve("java_resumen.csv"), StandardCharsets.UTF_8)) {
            w.write("n,m,a,c,semilla,k,alfa,chi2,gl,p_chi2,d_mas,d_menos,ks,p_ks,tiempo_segundos,decision_chi2,decision_ks\n");
            w.write(s.n + "," + s.m + "," + s.a + "," + s.c + "," + s.semilla + "," + s.k + "," + s.alfa + ","
                    + s.chi2 + "," + (s.k-1) + "," + s.pChi2 + "," + s.dMas + "," + s.dMenos + "," + s.ks + ","
                    + s.pKs + "," + s.segundos + "," + Vista.decision(s.pChi2, s.alfa) + "," + Vista.decision(s.pKs, s.alfa) + "\n");
        }
    }
}
