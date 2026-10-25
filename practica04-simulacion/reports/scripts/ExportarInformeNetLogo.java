import java.nio.file.Path;
import org.nlogo.headless.HeadlessWorkspace;

/** Exporta la corrida del modelo real de NetLogo para las figuras del informe. */
public class ExportarInformeNetLogo {
    public static void main(String[] args) throws Exception {
        if (args.length != 2) {
            throw new IllegalArgumentException("Uso: ExportarInformeNetLogo modelo.nlogox salida.csv");
        }
        HeadlessWorkspace workspace = HeadlessWorkspace.newInstance();
        try {
            workspace.open(Path.of(args[0]).toAbsolutePath().toString(), false);
            workspace.command("setup set PAUSA 0 repeat tiempo-maximo [go]");
            String salida = Path.of(args[1]).toAbsolutePath().toString()
                    .replace("\\", "/").replace("\"", "\\\"");
            workspace.command("csv:to-file \"" + salida + "\" "
                    + "fput [\"tiempo\" \"susceptibles\" \"infectados\" \"recuperados\"] datos-netlogo");
            System.out.println("Parámetros: " + workspace.report(
                    "(list poblacion infectados-iniciales beta gamma tiempo-maximo semilla)"));
            System.out.println("Final: " + workspace.report("last datos-netlogo"));
            System.out.println("Filas: " + workspace.report("length datos-netlogo"));
        } finally {
            workspace.dispose();
        }
    }
}
