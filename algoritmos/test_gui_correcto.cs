public class BancoCorrecto
{
    public void Ejecutar()
    {
        decimal saldo = 100.50;
        int intentos = 0;
        string titular = "Juan Perez";
        bool activo = true;

        List<decimal> transacciones = new List<decimal>();
        int[] cuentas = new int[5];
        Dictionary<string, decimal> clientes = new Dictionary<string, decimal>();

        // Condicional
        if (saldo > 0.0 && activo == true)
        {
            saldo -= 25.25;
        }
        else
        {
            Console.WriteLine("Cuenta sin fondos");
        }

        // Bucle while
        while (intentos < 3)
        {
            intentos = intentos + 1;
        }

        for (int j = 0; j < 5; j += 1)
        {
            saldo += 1.10;
        }

        switch (intentos)
        {
            case 1:
                Console.WriteLine("Un intento");
                break;
            case 3:
                Console.WriteLine("Bloqueado");
                break;
        }

        Console.WriteLine(titular);
    }
}
