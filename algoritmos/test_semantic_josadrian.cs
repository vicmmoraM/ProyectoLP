public class TestJoseAdrian {
    public bool EsPositivo(int numero) {
        return 5;           // ERROR: función bool retorna int
    }

    public bool EsNegativo(int numero) {
        return numero < 0;  // OK: retorna bool
    }

    public void Calcular() {
        string nombre = "Juan";
        int resultado = nombre * 2;   // ERROR: string * int
        int otro = nombre / 3;        // ERROR: string / int
        string saludo = nombre + " Perez";  // OK: PLUS sobre string es válido
    }
}
