int [] cuotas = new int [5];
bool aprobado = false;
bool pagado = true;

void VerificarPrestamo()
{
    int intentos = 0;
    while (intentos < 3)
    {
        intentos +=1;
    }
}

bool AprobarPrestamos(int monto, int plazo)
{
    if (monto > 0 && plazo > 0)
    {
        aprobado = true;
        return true;
    }
    else
    {
        aprobado = false;
        return false;
    }
}

bool ValidarCuotas(int totalCuotas, int cuotasPagadas)
{
    if (cuotasPagadas == totalCuotas)
    {
        pagado = true;
        return true;
    }
 
    if (cuotasPagadas != totalCuotas && cuotasPagadas > 0)
    {
        pagado = false;
        return false;
    }
 
    return false;
}