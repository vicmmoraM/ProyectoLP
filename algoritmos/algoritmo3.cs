int totalUsuarios = 3;
decimal comision = 0.50;
var saldoGlobal = 0.0;

Dictionary<string, decimal> billeteras = new Dictionary<string, decimal>();

decimal Depositar(string cuenta, decimal monto, int veces)
{
    decimal acumulado = 0.0;
    int i = 0;
    while (i < veces)
    {
        acumulado += monto;
        i += 1;
    }
    billeteras[cuenta] = acumulado;
    return acumulado;
}

bool Retirar(string cuenta, decimal monto)
{
    decimal saldo = billeteras[cuenta];
    if (saldo < monto)
    {
        return false;
    }
    else
    {
        saldo -= monto;
        billeteras[cuenta] = saldo;
        return true;
    }
}

decimal CobrarComisiones(int cantidad)
{
    decimal total = 0.0;
    for (int j = 0; j < cantidad; j += 1)
    {
        if (j == 5)
        {
            break;
        }
        total += comision;
    }
    return total;
}

void Procesar()
{
    decimal nuevo = Depositar(cuentaA, 100.25, 4);
    decimal escala = nuevo;
    escala *= 2;
    escala /= 3;
    bool ok = Retirar(cuentaA, 50.75);
    decimal cargos = CobrarComisiones(10);
    saldoGlobal += cargos;
}
