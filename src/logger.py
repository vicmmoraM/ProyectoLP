import datetime
import os

def _find_column(source, token):
    line_start = source.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

def generar_log(tipo_analisis, nombre, tokens_encontrados, errores, source=""):
    ahora = datetime.datetime.now()
    fecha = ahora.strftime("%d-%m-%Y")
    hora  = ahora.strftime("%Hh%M")
    nombre_archivo = f"{tipo_analisis}-{nombre}-{fecha}-{hora}.txt"

    base_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.normpath(os.path.join(base_dir, "..", "logs"))
    os.makedirs(logs_dir, exist_ok=True)
    ruta = os.path.join(logs_dir, nombre_archivo)

    with open(ruta, "w", encoding="utf-8") as f:
        f.write(f"Análisis {tipo_analisis.capitalize()} - {nombre} ===\n")
        f.write(f"Fecha: {fecha}  Hora: {hora}\n")
        f.write("=" * 40 + "\n\n")

        f.write("TOKENS RECONOCIDOS:\n")
        for tok in tokens_encontrados:
            col = _find_column(source, tok) if source else "?"
            f.write(f"  [{tok.type}]  {repr(tok.value)}  -  línea {tok.lineno}, columna {col}\n")

        f.write(f"\nTotal tokens: {len(tokens_encontrados)}\n")

        if errores:
            f.write("\nErrores:\n")
            for e in errores:
                f.write(f"  {e}\n")
        else:
            f.write("\nSin errores léxicos.\n")

    print(f"Log generado: {ruta}")
    return ruta