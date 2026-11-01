package controlador;

import java.io.IOException;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import modelo.GeneradorLCG;
import vista.VistaConsola;

public class ControladorLCG {
    private final VistaConsola vista;

    public ControladorLCG(VistaConsola vista) {
        this.vista = vista;
    }

    public void ejecutar(long semilla) throws IOException {
        GeneradorLCG modelo = new GeneradorLCG(semilla);
        long[] valores = modelo.generar(10000);
        vista.mostrarResultados(semilla, valores);

        Path carpeta = Path.of("resultados");
        Files.createDirectories(carpeta);
        Path archivo = carpeta.resolve("java_" + semilla + ".csv");
        try (PrintWriter salida = new PrintWriter(
                Files.newBufferedWriter(archivo, StandardCharsets.UTF_8))) {
            salida.println("iteracion,X,U");
            for (int i = 0; i < valores.length; i++) {
                salida.println((i + 1) + "," + valores[i] + ","
                        + GeneradorLCG.normalizar(valores[i]));
            }
            if (salida.checkError()) {
                throw new IOException("No se pudo completar el archivo CSV.");
            }
        }
        vista.mostrarSeccion("ARCHIVO GENERADO");
        vista.mostrarMensaje("Datos CSV: " + archivo);
        vista.mostrarMensaje("\n====================== PROCESO FINALIZADO ======================\n");
    }
}
