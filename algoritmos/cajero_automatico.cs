// Cajero Automatico - Safe C# Linter
// Prueba #2 - José Adrián (@arzel01)

/*
   Simulacion de un cajero automatico financiero.
   Incluye retiro, deposito, consulta de saldo y validacion de montos.
   Usa: decimal, List, if/else, operadores aritmeticos y logicos.
*/

public class CajeroAutomatico
{
    decimal saldo;
    decimal limiteDiario;
    decimal totalRetirado;
    bool activo;
    List historial;

    public void Inicializar(decimal saldoInicial, decimal limite)
    {
        saldo = saldoInicial;
        limiteDiario = limite;
        totalRetirado = 0;
        activo = true;
    }

    public bool ValidarMonto(decimal monto)
    {
        if (monto > 0 && monto < limiteDiario)
        {
            return true;
        }
        else
        {
            return false;
        }
    }

    public bool Retirar(decimal monto)
    {
        if (activo && ValidarMonto(monto))
        {
            if (saldo > monto)
            {
                saldo -= monto;
                totalRetirado += monto;
                return true;
            }
            else
            {
                return false;
            }
        }
        else
        {
            return false;
        }
    }

    public bool Depositar(decimal monto)
    {
        if (activo && monto > 0)
        {
            saldo += monto;
            return true;
        }
        else
        {
            return false;
        }
    }

    public decimal ConsultarSaldo()
    {
        return saldo;
    }

    public void BloquearCuenta()
    {
        activo = false;
        totalRetirado = 0;
    }

    public bool VerificarLimite(decimal monto)
    {
        if (totalRetirado + monto > limiteDiario)
        {
            return false;
        }
        else
        {
            return true;
        }
    }

    public bool CuentaActiva()
    {
        if (activo)
        {
            return true;
        }
        else
        {
            return false;
        }
    }
}
