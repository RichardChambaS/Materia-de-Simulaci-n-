package vista;

import modelo.Simulacion;
import java.util.Scanner;
import java.util.Locale;
import java.nio.file.Path;
import java.io.IOException;
import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;

/** Consola y gráficas PNG con la biblioteca estándar de Java. */
public class Vista {
    private final Scanner entrada = new Scanner(System.in);
    private static final Color AZUL = new Color(38, 119, 184);
    private static final Color NARANJA = new Color(230, 129, 39);

    private long entero(String nombre, long defecto, long minimo, long maximo) {
        while (true) {
            System.out.print(nombre + " [" + defecto + "]: ");
            String texto = entrada.nextLine().trim();
            try {
                long valor = texto.isEmpty() ? defecto : Long.parseLong(texto);
                if (valor >= minimo && valor <= maximo) return valor;
            } catch (NumberFormatException e) { /* Volver a pedir. */ }
            System.out.println("Ingresa un entero entre " + minimo + " y " + maximo + ".");
        }
    }

    public Simulacion parametros() {
        Simulacion s = new Simulacion();
        System.out.println("\nLCG y pruebas de uniformidad. Enter utiliza el valor entre corchetes.");
        System.out.println("1. Caso base de la práctica");
        System.out.println("2. Ingresar mis propios datos");
        int opcion = (int) entero("Selecciona una opción", 1, 1, 2);
        if (opcion == 1) {
            s.n = 10000;
            s.m = 4294967296L;
            s.a = 1664525;
            s.c = 1013904223;
            s.semilla = 12345;
            s.k = 10;
            s.alfa = 0.05;
            System.out.println("Caso base: N=10000, m=4294967296, a=1664525, c=1013904223,");
            System.out.println("semilla=12345, k=10, alfa=0.05.");
            return s;
        }
        s.n = (int) entero("Cantidad N", 10000, 50, 1000000);
        s.m = entero("Módulo m", 4294967296L, 2, 4503599627370496L);
        s.a = entero("Multiplicador a", Math.min(1664525, s.m - 1), 0, s.m - 1);
        s.c = entero("Incremento c", Math.min(1013904223, s.m - 1), 0, s.m - 1);
        s.semilla = entero("Semilla", Math.min(12345, s.m - 1), 0, s.m - 1);
        s.k = (int) entero("Número de intervalos k", 10, 2, Math.min(100, s.n / 5));
        while (true) {
            System.out.print("Significancia alfa [0.05]: ");
            String texto = entrada.nextLine().trim().replace(',', '.');
            try {
                s.alfa = texto.isEmpty() ? 0.05 : Double.parseDouble(texto);
                if (Double.isFinite(s.alfa) && s.alfa > 0 && s.alfa < 1) break;
            } catch (NumberFormatException e) { /* Volver a pedir. */ }
            System.out.println("Ingresa un número mayor que 0 y menor que 1.");
        }
        return s;
    }

    public static String decision(double p, double alfa) {
        return p < alfa ? "Se rechaza H0" : "No se rechaza H0";
    }

    public void mostrar(Simulacion s) {
        System.out.println("\nPrimeros 20 valores (la secuencia completa se guarda en CSV):");
        for (int i = 0; i < Math.min(20, s.n); i++) {
            System.out.printf(Locale.ROOT, "%4d  X=%16d  U=%.10f%n", i+1, s.valores[i], s.u[i]);
        }
        System.out.println("\nIntervalo             Observada   Esperada");
        for (int i = 0; i < s.k; i++) {
            System.out.printf(Locale.ROOT, "[%.3f, %.3f)  %10d  %9.2f%n",
                    i/(double)s.k, (i+1.0)/s.k, s.frecuencias[i], s.n/(double)s.k);
        }
        System.out.printf(Locale.ROOT, "%nChi-cuadrado = %.8g, gl = %d, p = %.8g%n", s.chi2, s.k-1, s.pChi2);
        System.out.println(decision(s.pChi2, s.alfa));
        System.out.printf(Locale.ROOT, "D+ = %.8g, D- = %.8g%nKS = %.8g, p asintótico = %.8g%n", s.dMas, s.dMenos, s.ks, s.pKs);
        System.out.println(decision(s.pKs, s.alfa));
        System.out.println("No rechazar H0 no demuestra aleatoriedad ni independencia.");
    }

    public boolean repetir() {
        System.out.print("¿Realizar otro análisis? [s/N]: ");
        return entrada.hasNextLine() && entrada.nextLine().trim().equalsIgnoreCase("s");
    }

    // Cada panel usa coordenadas normalizadas entre 0 y 1.
    private static int px(int origen, double x) { return origen + (int)Math.round(x * 360); }
    private static int py(double y) { return 360 - (int)Math.round(y * 260); }

    private static void ejes(Graphics2D g, int origen, String titulo, String horizontal, String vertical, double maximo, double minX, double maxX) {
        ejesRango(g, origen, titulo, horizontal, vertical, 0, maximo, minX, maxX);
    }

    private static void ejesRango(Graphics2D g, int origen, String titulo, String horizontal, String vertical,
                                  double minimo, double maximo, double minX, double maxX) {
        g.setFont(new Font("SansSerif", Font.BOLD, 17));
        g.setColor(Color.DARK_GRAY);
        g.drawString(titulo, origen, 75);
        g.setFont(new Font("SansSerif", Font.PLAIN, 12));
        for (int i = 0; i <= 5; i++) {
            double fraccion = i / 5.0;
            int y = py(fraccion);
            g.setColor(new Color(225, 230, 235));
            g.drawLine(origen, y, origen+360, y);
            g.setColor(Color.DARK_GRAY);
            String etiquetaY = String.format(Locale.ROOT, "%.4g", minimo + fraccion * (maximo-minimo));
            g.drawString(etiquetaY, origen - 7 - g.getFontMetrics().stringWidth(etiquetaY), y+4);
            String etiquetaX = String.format(Locale.ROOT, "%.1f", minX + fraccion * (maxX-minX));
            g.drawString(etiquetaX, px(origen, fraccion)-9, 380);
        }
        g.drawRect(origen, 100, 360, 260);
        g.drawString(horizontal, origen+140, 405);
        g.drawString(vertical, origen, 94);
    }

    public void graficas(Path carpeta, Simulacion s) throws IOException {
        BufferedImage imagen = new BufferedImage(1400, 480, BufferedImage.TYPE_INT_RGB);
        Graphics2D g = imagen.createGraphics();
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g.setColor(Color.WHITE);
        g.fillRect(0, 0, 1400, 480);
        g.setFont(new Font("SansSerif", Font.BOLD, 20));
        g.setColor(Color.DARK_GRAY);
        g.drawString("Java | N=" + s.n + " | semilla=" + s.semilla + " | k=" + s.k, 65, 32);
        double maximo = s.n/(double)s.k;
        for (int f : s.frecuencias) maximo = Math.max(maximo, f);
        maximo *= 1.15;
        ejes(g, 65, "Frecuencias", "U", "Cantidad", maximo, 0, 1);
        g.setColor(AZUL);
        for (int i = 0; i < s.k; i++) {
            int x1 = px(65, (i+.05)/s.k);
            int x2 = px(65, (i+.95)/s.k);
            int y = py(s.frecuencias[i]/maximo);
            g.fillRect(x1, y, Math.max(1, x2-x1), 360-y);
        }
        g.setColor(NARANJA);
        int esperado = py(s.n/(double)s.k/maximo);
        g.drawLine(65, esperado, 425, esperado);
        ejes(g, 535, "Distribución acumulada (KS)", "U", "F(U)", 1, 0, 1);
        g.setColor(AZUL);
        double previoX = 0, previoY = 0;
        for (int i = 0; i < s.n; i++) {
            double x = s.ordenados[i], y = (i+1.0)/s.n;
            g.drawLine(px(535, previoX), py(previoY), px(535, x), py(previoY));
            g.drawLine(px(535, x), py(previoY), px(535, x), py(y));
            previoX = x;
            previoY = y;
        }
        g.drawLine(px(535, previoX), py(1), px(535, 1), py(1));
        g.setColor(NARANJA);
        g.drawLine(535, 360, 895, 100);
        int limite = Math.min(200, s.n);
        ejes(g, 1005, "Primeros " + limite + " valores", "Índice i", "U", 1, 1, limite);
        g.setColor(AZUL);
        for (int i = 0; i < limite; i++) {
            int x = px(1005, i/(double)(limite-1)), y = py(s.u[i]);
            g.fillOval(x-2, y-2, 4, 4);
            if (i > 0) g.drawLine(px(1005, (i-1.0)/(limite-1)), py(s.u[i-1]), x, y);
        }
        g.setColor(AZUL);
        g.drawString("Azul: observada / empírica / secuencia", 65, 445);
        g.setColor(NARANJA);
        g.drawString("Naranja: esperada N/k / teórica F(x)=x", 535, 445);
        g.dispose();
        ImageIO.write(imagen, "png", carpeta.resolve("java_graficas.png").toFile());
        calculos(carpeta, s);
        hipotesis(carpeta, s);
    }

    private void calculos(Path carpeta, Simulacion s) throws IOException {
        BufferedImage imagen = new BufferedImage(1000, 550, BufferedImage.TYPE_INT_RGB);
        Graphics2D g = imagen.createGraphics();
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g.setColor(Color.WHITE);
        g.fillRect(0, 0, 1000, 550);
        g.setColor(Color.DARK_GRAY);
        g.setFont(new Font("SansSerif", Font.BOLD, 20));
        g.drawString("Cálculo de las pruebas | Java | N=" + s.n + " | semilla=" + s.semilla, 65, 32);
        double esperado = s.n / (double) s.k;
        double[] aportes = new double[s.k];
        double techo = 0;
        for (int i = 0; i < s.k; i++) {
            aportes[i] = Math.pow(s.frecuencias[i] - esperado, 2) / esperado;
            techo = Math.max(techo, aportes[i]);
        }
        techo = techo == 0 ? 1 : techo * 1.15;
        ejes(g, 65, "Chi²: suma de los aportes", "Intervalo j", "(Oj - Ej)² / Ej", techo, .5, s.k+.5);
        g.setColor(AZUL);
        for (int i = 0; i < s.k; i++) {
            int x1 = px(65, (i+.05)/s.k), x2 = px(65, (i+.95)/s.k);
            int y = py(aportes[i]/techo);
            g.fillRect(x1, y, Math.max(1, x2-x1), 360-y);
        }
        double rango = s.ks * 1.15;
        ejesRango(g, 535, "KS: máximo de D+ y D-", "Posición i ordenada", "Diferencia con la uniforme", -rango, rango, 1, s.n);
        g.setColor(Color.GRAY);
        g.drawLine(535, py(.5), 895, py(.5));
        // Dos curvas de diferencias; se conserva cada observación, sin muestreo.
        for (int curva = 0; curva < 2; curva++) {
            Color color = curva == 0 ? AZUL : NARANJA;
            g.setColor(color);
            double anterior = 0, mayor = -Double.MAX_VALUE;
            int indiceMayor = 0;
            for (int i = 0; i < s.n; i++) {
                double valor = curva == 0 ? (i+1.0)/s.n - s.ordenados[i]
                                         : s.ordenados[i] - i/(double)s.n;
                int x = px(535, i/(double)(s.n-1));
                int y = py((valor+rango)/(2*rango));
                if (i > 0) g.drawLine(px(535, (i-1.0)/(s.n-1)), py((anterior+rango)/(2*rango)), x, y);
                if (valor > mayor) { mayor = valor; indiceMayor = i; }
                anterior = valor;
            }
            int x = px(535, indiceMayor/(double)(s.n-1)), y = py((mayor+rango)/(2*rango));
            g.fillOval(x-5, y-5, 10, 10);
            g.setColor(Color.BLACK);
            g.drawOval(x-5, y-5, 10, 10);
            g.setColor(color);
            String formula = curva == 0 ? "i/N - U(i); D+ = " : "U(i) - (i-1)/N; D- = ";
            g.drawString(formula + String.format(Locale.ROOT, "%.8g", mayor), 535, 430+curva*20);
        }
        g.setColor(Color.DARK_GRAY);
        g.drawString(String.format(Locale.ROOT, "Chi² = %.8g; gl = %d; alfa = %.4g", s.chi2, s.k-1, s.alfa), 65, 430);
        g.drawString("Cada barra aporta a la suma total.", 65, 450);
        g.drawString(String.format(Locale.ROOT, "p = %.8g | %s", s.pChi2, decision(s.pChi2, s.alfa)), 65, 485);
        g.drawString(String.format(Locale.ROOT, "D = %.8g; p asintótico = %.8g", s.ks, s.pKs), 535, 485);
        g.drawString(decision(s.pKs, s.alfa) + "; puntos: máximos de cada curva", 535, 505);
        g.dispose();
        ImageIO.write(imagen, "png", carpeta.resolve("java_calculos.png").toFile());
    }

    private void hipotesis(Path carpeta, Simulacion s) throws IOException {
        int gl = s.k - 1;
        double critico = Simulacion.criticoChi2(gl, s.alfa);
        double limite = Math.max(Simulacion.criticoChi2(gl, .001), critico * 1.2);
        double[] densidad = new double[2000];
        double altura = 0;
        for (int i = 0; i < densidad.length; i++) {
            densidad[i] = Simulacion.densidadChi2(gl, (i+1)*limite/2000);
            altura = Math.max(altura, densidad[i]);
        }
        altura *= 1.1;
        BufferedImage imagen = new BufferedImage(1100, 650, BufferedImage.TYPE_INT_RGB);
        Graphics2D g = imagen.createGraphics();
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g.setColor(Color.WHITE);
        g.fillRect(0, 0, 1100, 650);
        g.setColor(Color.DARK_GRAY);
        g.setFont(new Font("SansSerif", Font.BOLD, 21));
        g.drawString("Decisión de la hipótesis | Java | N=" + s.n + " | gl=" + gl, 80, 35);
        for (int i = 0; i < densidad.length; i++) {
            double x = (i+1)*limite/2000;
            int px = 80 + (int)Math.round(x/limite*920);
            int y = 410 - (int)Math.round(densidad[i]/altura*320);
            g.setColor(x <= critico ? new Color(184,219,206) : new Color(234,166,166));
            g.drawLine(px, 410, px, y);
        }
        g.setColor(Color.DARK_GRAY);
        for (int i = 1; i < densidad.length; i++) {
            g.drawLine(80+(int)Math.round(i/2000.0*920), 410-(int)Math.round(densidad[i-1]/altura*320),
                       80+(int)Math.round((i+1)/2000.0*920), 410-(int)Math.round(densidad[i]/altura*320));
        }
        g.setFont(new Font("SansSerif", Font.PLAIN, 13));
        g.drawRect(80, 90, 920, 320);
        for (int i = 0; i <= 5; i++) {
            g.drawString(String.format(Locale.ROOT, "%.4g", limite*i/5), 70+i*184, 432);
            g.drawString(String.format(Locale.ROOT, "%.3g", altura*i/5), 15, 415-i*64);
        }
        g.drawString("Densidad", 80, 77);
        g.drawString("Valor del estadístico Chi²", 420, 455);
        int xc = 80+(int)Math.round(critico/limite*920);
        g.setColor(new Color(184,58,58));
        for (int y = 90; y < 410; y += 12) g.drawLine(xc, y, xc, Math.min(y+6, 410));
        g.drawString(String.format(Locale.ROOT, "Rojo: valor crítico = %.7g; rechazo a su derecha (área total alfa = %.4g)", critico, s.alfa), 80, 495);
        g.setColor(AZUL);
        if (s.chi2 <= limite) {
            int xo = 80+(int)Math.round(s.chi2/limite*920);
            g.drawLine(xo, 90, xo, 410);
        } else {
            g.drawString("Observado fuera del eje →", 820, 65);
        }
        g.drawString(String.format(Locale.ROOT, "Azul: Chi² observado = %.8g", s.chi2), 80, 518);
        g.setColor(Color.DARK_GRAY);
        g.drawString("Verde: región de no rechazo de H0. Rosa: región de rechazo de H0.", 80, 475);
        g.setFont(new Font("SansSerif", Font.BOLD, 17));
        g.drawString(String.format(Locale.ROOT, "p = %.8g | alfa = %.4g | %s", s.pChi2, s.alfa, decision(s.pChi2, s.alfa)), 80, 560);
        g.setFont(new Font("SansSerif", Font.PLAIN, 13));
        g.drawString("Se rechaza si p < alfa. No rechazar no demuestra H0. La cola continúa más allá del eje.", 80, 592);
        g.dispose();
        ImageIO.write(imagen, "png", carpeta.resolve("java_hipotesis.png").toFile());
    }
}
