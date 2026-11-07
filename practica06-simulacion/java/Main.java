import controlador.Controlador;
import java.io.IOException;
import java.util.NoSuchElementException;

public class Main {
    public static void main(String[] args) {
        try {
            new Controlador().ejecutar();
        } catch (NoSuchElementException e) {
            System.out.println("\nPrograma finalizado.");
        } catch (IOException e) {
            System.err.println("No se pudieron guardar los resultados: " + e.getMessage());
            System.exit(1);
        }
    }
}
