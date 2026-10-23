import controlador.SimulacionControlador;
import java.io.IOException;

public class Main {
    // Inicia el programa y avisa si falla la escritura del CSV.
    public static void main(String[] args) {
        try {
            new SimulacionControlador().ejecutar();
        } catch (IOException e) {
            System.err.println("No se pudo guardar el CSV: " + e.getMessage());
            System.exit(1);
        }
    }
}
