import datetime
import os

def generar_log(tipo_analisis, nombre, tokens_encontrados, errores):
    ahora = datetime.datetime.now()
    fecha = ahora.strftime("%d-%m-%Y")
    hora  = ahora.strftime("%Hh%M")
    nombre_archivo = f"{tipo_analisis}-{nombre}-{fecha}-{hora}.txt"

    os.makedirs("logs", exist_ok=True)
    ruta = os.path.join("logs", nombre_archivo)

    with open(ruta, "w", encoding="utf-8") as f:
        f.write(f"Análisis {tipo_analisis.capitalize()} — {nombre} ===\n")
        f.write(f"Fecha: {fecha}  Hora: {hora}\n")
        f.write("=" * 40 + "\n\n")

        f.write("TOKENS RECONOCIDOS:\n")
        for tok in tokens_encontrados:
            f.write(f"  [{tok.type}]  {repr(tok.value)}  —  línea {tok.lineno}\n")

        f.write(f"\nTotal tokens: {len(tokens_encontrados)}\n")

        if errores:
            f.write("\nErrores:\n")
            for e in errores:
                f.write(f"  {e}\n")
        else:
            f.write("\nSin errores léxicos.\n")

    print(f"Log generado: {ruta}")
    return ruta