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
    'INT', 'DECIMAL', 'STRING', 'VAR',
    'PLUS_ASSIGN', 'MINUS_ASSIGN', 'TIMES_ASSIGN', 'DIV_ASSIGN',
    'SEMICOLON', 'COMMA', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'IF', 'ELSE', 'FOR', 'NEW', 'BREAK', 'ASSIGN',
    'INT_LITERAL', 'DECIMAL_LITERAL',
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
    t.type = reserved_victor.get(t.value) or reserved_andres.get(t.value, 'ID')
    return t

# Victor Morales - Fin del Aporte

# Andres Saltos - Inicio de Aporte

reserved_andres = {
    'int'     : 'INT',
    'decimal' : 'DECIMAL',
    'string'  : 'STRING',
    'var'     : 'VAR',
    'if'      : 'IF',
    'else'    : 'ELSE',
    'for'     : 'FOR',
    'new'     : 'NEW',
    'break'   : 'BREAK',
}

# Literales numéricos: el decimal debe ir antes que el entero para que PLY lo priorice
def t_DECIMAL_LITERAL(t):
    r'\d+\.\d+'
    return t

def t_INT_LITERAL(t):
    r'\d+'
    return t

# Asignación compuesta (multi-carácter) antes que los operadores simples
def t_PLUS_ASSIGN(t):
    r'\+='
    return t

def t_MINUS_ASSIGN(t):
    r'-='
    return t

def t_TIMES_ASSIGN(t):
    r'\*='
    return t

def t_DIV_ASSIGN(t):
    r'/='
    return t

# Operadores aritméticos simples
def t_PLUS(t):
    r'\+'
    return t

def t_MINUS(t):
    r'-'
    return t

def t_TIMES(t):
    r'\*'
    return t

def t_DIVIDE(t):
    r'/'
    return t

# Asignación simple (después de '==' de Victor y de los compuestos)
def t_ASSIGN(t):
    r'='
    return t

# Puntuación
def t_SEMICOLON(t):
    r';'
    return t

def t_COMMA(t):
    r','
    return t

def t_LPAREN(t):
    r'\('
    return t

def t_RPAREN(t):
    r'\)'
    return t

def t_LBRACE(t):
    r'\{'
    return t

def t_RBRACE(t):
    r'\}'
    return t

# Conteo de líneas y caracteres ignorados
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

# Andres Saltos - Fin del Aporte

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
        nombre="AndresSaltos", #Cambiar el nombre
        tokens_encontrados=tokens_encontrados,
        errores=[]
    )

