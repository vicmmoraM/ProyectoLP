import sys
import ply.lex as lex
from logger import generar_log
#no se olviden de instalar ply -> comando par instalar: pip install ply

sys.stdout.reconfigure(encoding='utf-8')

errores_lexicos = []
#Listado con tokens

tokens = [
    # Victor Morales - Inicio
    'ID','LBRACKET', 'RBRACKET', 'WHILE', 'RETURN', 'VOID', 'BOOL', 'TRUE', 'FALSE', 'GT', 'LT', 'EQ', 'NEQ', 'AND', 'OR', 'DOT',
    # Victor Morales - Fin
    # Jose Adrian - Inicio
    'LIST', 'PUBLIC', 'CLASS', 'SWITCH', 'CASE', 'STRING_LITERAL', 'COLON',
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

def t_DOT(t):
    r'\.'
    return t

# Victor Morales - Fin del Aporte

# José Adrián - Inicio de Aporte

reserved_adrian = {
    'List'   : 'LIST',
    'public' : 'PUBLIC',
    'class'  : 'CLASS',
    'switch' : 'SWITCH',
    'case'   : 'CASE',
}

# Andres Saltos - palabras reservadas
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

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    reservadas = {**reserved_victor, **reserved_andres, **reserved_adrian}
    t.type = reservadas.get(t.value, 'ID')
    return t

def t_COMMENT_MULTI(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

def t_COMMENT_SINGLE(t):
    r'//.*'
    pass

def t_STRING_LITERAL(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

def find_column(input_data, token):
    line_start = input_data.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

def t_error(t):
    msg = f"Error Léxico: Carácter no reconocido '{t.value[0]}' en la línea {t.lexer.lineno}"
    print(msg)
    errores_lexicos.append(msg)
    t.lexer.skip(1)

def t_COLON(t):
    r':'
    return t

# Jose Adrian - Fin del Aporte

# Andres Saltos - Inicio de Aporte

def t_DECIMAL_LITERAL(t):
    r'\d+\.\d+'
    return t

def t_INT_LITERAL(t):
    r'\d+'
    return t

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

def t_ASSIGN(t):
    r'='
    return t

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

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

# Andres Saltos - Fin del Aporte

if __name__ == "__main__":
    import sys
 
    if len(sys.argv) < 2:
        print("Uso: python lexer.py <archivo.cs>")
        sys.exit(1)
 
    archivo = sys.argv[1]
 
    with open(archivo, "r", encoding="utf-8") as f:
        codigo = f.read()
 
    errores_lexicos.clear()
    lexer = lex.lex()
    lexer.input(codigo)
 
    tokens_encontrados = []
 
    for tok in lexer:
        tokens_encontrados.append(tok)
        print(f"[{tok.type}]  {repr(tok.value)}  -  línea {tok.lineno}")
 
    generar_log(
        tipo_analisis="lexico",
        nombre="JoseAdrian",
        tokens_encontrados=tokens_encontrados,
        errores=errores_lexicos,
        source=codigo,
    )

