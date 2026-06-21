public class TestVictor {

    int[] cuotas = new int[5];
    bool aprobado;

    public void VerificarPrestamo(int intentos) {
        while (intentos < 3) {
            intentos = intentos + 1;
        }
    }

    public bool AprobarPrestamos(int monto, int plazo) {
        if (monto > 0 && plazo > 0) {
            aprobado = true;
            return true;
        } else {
            aprobado = false;
            return false;
        }
    }

    public bool ValidarCuotas(int totalCuotas, int cuotasPagadas) {
        if (cuotasPagadas == totalCuotas) {
            Console.WriteLine(totalCuotas);
            return true;
        }
        if (cuotasPagadas != totalCuotas && cuotasPagadas > 0) {
            Console.WriteLine(cuotasPagadas);
            return false;
        }
        return false;
    }
}
