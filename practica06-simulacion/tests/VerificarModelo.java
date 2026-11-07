import modelo.Simulacion;

/** Puente pequeño para comprobar Java contra SciPy desde verificar.py. */
public class VerificarModelo {
    public static void main(String[] args) {
        if (args.length == 0) {
            for (int gl = 1; gl <= 99; gl++) {
                for (double x : new double[]{0, 0.01, 0.5, 1, 5, 10, 50, 100, 500, 1000}) {
                    System.out.println("chi," + gl + "," + x + "," + Simulacion.gammaQ(gl/2.0, x/2));
                }
            }
            for (double z : new double[]{0, 0.01, 0.2, 0.5, 1, 1.179, 1.18, 1.5, 2, 5, 20}) {
                System.out.println("ks,0," + z + "," + Simulacion.probabilidadKS(z));
            }
            return;
        }
        Simulacion s = new Simulacion();
        s.n = Integer.parseInt(args[0]);
        s.semilla = Long.parseLong(args[1]);
        s.a = Long.parseLong(args[2]);
        s.c = Long.parseLong(args[3]);
        s.m = Long.parseLong(args[4]);
        s.k = Integer.parseInt(args[5]);
        s.calcular();
        System.out.println(s.chi2 + "," + s.pChi2 + "," + s.dMas + "," + s.dMenos + "," + s.ks + "," + s.pKs);
        for (long x : s.valores) System.out.println(x);
    }
}
