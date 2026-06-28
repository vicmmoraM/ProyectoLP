public class TestAndres {
    public void Ejemplo() {
        int cantidad = 10;
        decimal monto = "texto";    // ERROR: string -> decimal
        string nombre = cantidad;   // ERROR: int -> string
        int total = cantidad;       // OK: int = int

        int resultado = inexistente + 1;  // ERROR: 'inexistente' no declarada
    }
}
