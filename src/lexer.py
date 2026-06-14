import ply.lex as lex
from logger import generar_log
#no se olviden de instalar ply -> comando par instalar: pip install ply
#Listado con tokens

tokens = [
    # Victor Morales - Inicio
    'ID','LBRACKET', 'RBRACKET', 'WHILE', 'RETURN', 'VOID', 'BOOL', 'TRUE', 'FALSE', 'GT', 'LT', 'EQ', 'NEQ', 'AND', 'OR',
    # Victor Morales - Fin
    # Jose Adrian - Inicio

    # Jose Adrian - Fin
    # Andres Saltos - Inicio

    # Andres Saltos - Fin
]

# Victor Morales - Inicio de Aporte

reserved_victor = {
    'while' : 'WHILE',
    'return' : 'RETURN',
    'void' : 'VOID',
    'bool' : 'BOOL',
    'true' : 'TRUE',
    'false' : 'FALSE',
}

def t_LBRACKET(t):
    r'\['
    return t

def t_RBRACKET(t):
    r'\]'
    return t

def t_EQ(t):
    r'=='
    return t

def t_NEQ(t):
    r'!='
    return t

def t_GT(t):
    r'>'
    return t

def t_LT(t):
    r'<'
    return t

def t_AND(t):
    r'&&'
    return t
 
def t_OR(t):
    r'\|\|'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved_victor.get(t.value, 'ID')
    return t

# Victor Morales - Fin del Aporte

# Manejos de errores
def t_error(t):
    col = find_column(t.lexer.lexdata, t)
    print(f"Error léxico: carácter no reconocido '{t.value[0]}' en línea {t.lexer.lineno}, columna {col}")
    t.lexer.skip(1)
 
def find_column(input_text, token):
    line_start = input_text.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

if __name__ == "__main__":
    import sys
 
    if len(sys.argv) < 2:
        print("Uso: python lexer.py <archivo.cs>")
        sys.exit(1)
 
    archivo = sys.argv[1]
 
    with open(archivo, "r", encoding="utf-8") as f:
        codigo = f.read()
 
    lexer = lex.lex()
    lexer.input(codigo)
 
    tokens_encontrados = []
 
    for tok in lexer:
        tokens_encontrados.append(tok)
        print(f"[{tok.type}]  {repr(tok.value)}  —  línea {tok.lineno}")
 
    generar_log(
        tipo_analisis="lexico",
        nombre="VictorMorales", #Cambiar el nombre 
        tokens_encontrados=tokens_encontrados,
        errores=[]
    )

