package controlador;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.List;
import modelo.SimulacionSIR;
import vista.VistaConsola;

public class SimulacionControlador {
    // Coordina la simulación, la exportación y la salida en consola.
    public void ejecutar() throws IOException {
        // Mide solo el cálculo, antes de escribir archivos y mostrar resultados.
        long inicio = System.nanoTime();
        List<int[]> resultados = new SimulacionSIR().ejecutar();
        double segundos = (System.nanoTime() - inicio) / 1_000_000_000.0;

        Path archivo = Paths.get("resultados", "resultados_java.csv");
        guardarCsv(resultados, archivo);
        Files.createDirectories(Paths.get("netlogo"));
        // Deja una copia del mismo CSV junto al modelo de NetLogo.
        Files.copy(archivo, Paths.get("netlogo", "resultados_java.csv"),
                StandardCopyOption.REPLACE_EXISTING);
        new VistaConsola().mostrar(resultados, segundos);
    }

    // Escribe el encabezado y una fila de tiempo, S, I y R por cada registro.
    private void guardarCsv(List<int[]> resultados, Path archivo) throws IOException {
        Files.createDirectories(archivo.getParent());
        try (BufferedWriter escritor = Files.newBufferedWriter(archivo, StandardCharsets.UTF_8)) {
            escritor.write("tiempo,susceptibles,infectados,recuperados");
            escritor.newLine();
            for (int[] fila : resultados) {
                escritor.write(fila[0] + "," + fila[1] + "," + fila[2] + "," + fila[3]);
                escritor.newLine();
            }
        }
    }
}
