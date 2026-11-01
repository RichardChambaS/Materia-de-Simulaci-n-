import java.io.IOException;
import controlador.ControladorLCG;
import vista.VistaConsola;

public class Main {
    public static void main(String[] args) {
        VistaConsola vista = new VistaConsola();
        try {
            if (args.length > 1) {
                throw new IllegalArgumentException("Uso: java -cp java/bin Main [semilla]");
            }
            long semilla = args.length == 1 ? Long.parseLong(args[0]) : vista.pedirSemilla();
            new ControladorLCG(vista).ejecutar(semilla);
        } catch (IllegalArgumentException | IOException e) {
            vista.mostrarMensaje("Error: " + e.getMessage());
            System.exit(1);
        }
    }
}
