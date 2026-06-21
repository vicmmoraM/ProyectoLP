public class Demo {
    Dictionary<string, decimal> clientes = new Dictionary<string, decimal>();

    public void Procesar(int x) {
        if (x > 0) {
            clientes = clientes;
        } else {
            x = x;
        }
    }

    decimal CalcularInteres(decimal capital, decimal tasa) {
        return capital * tasa;
    }
}
