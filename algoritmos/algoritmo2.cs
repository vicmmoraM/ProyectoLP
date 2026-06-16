public class Inventario
{
    List<string> productos = new List<string>();
    List<int> cantidades = new List<int>();
    int totalProductos = 0;
    string estado = "activo";

    public void Registrar(string nombre, int cantidad, int tipo)
    {
        productos[totalProductos] = nombre;
        cantidades[totalProductos] = cantidad;
        totalProductos += 1;

        switch (tipo)
        {
            case 1:
                estado = "electronico";
                break;
            case 2:
                estado = "ropa";
                break;
            case 3:
                estado = "alimento";
                break;
        }
    }

    public bool Buscar(string nombre)
    {
        int i = 0;
        while (i < totalProductos)
        {
            if (productos[i] == nombre)
            {
                return true;
            }
            i += 1;
        }
        return false;
    }

    public string ObtenerEstado()
    {
        return estado;
    }

    public int ContarDisponibles(int limite)
    {
        int disponibles = 0;
        for (int j = 0; j < totalProductos; j += 1)
        {
            if (cantidades[j] > limite)
            {
                disponibles += 1;
            }
        }
        return disponibles;
    }
}
