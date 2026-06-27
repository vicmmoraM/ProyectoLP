import sys
import ply.yacc as yacc
import ply.lex as lex

sys.path.insert(0, '.')
import lexer as lexer_module
from lexer import tokens  # noqa: F401 — PLY requiere 'tokens' en este namespace
from logger import generar_log

sys.stdout.reconfigure(encoding='utf-8')
errores_sintacticos = []

# ── José Adrián – Precedencia de operadores ──────────────────
precedence = (
    ('left',     'OR'),
    ('left',     'AND'),
    ('nonassoc', 'EQ', 'NEQ'),
    ('nonassoc', 'LT', 'GT'),
    ('left',     'PLUS', 'MINUS'),
    ('left',     'TIMES', 'DIVIDE'),
)

# ── Definición de función: clase pública con métodos ─────────

def p_program(p):
    '''program : PUBLIC CLASS ID LBRACE class_body RBRACE'''

def p_class_body(p):
    '''class_body : class_body method_decl
                  | class_body list_decl
                  | class_body dict_decl
                  | class_body func_decl
                  | class_body void_func_decl
                  | class_body array_decl
                  | class_body var_decl
                  | empty'''  # Andrés Saltos: dict_decl y func_decl; Victor Morales: void_func_decl, array_decl, var_decl

def p_method_decl(p):
    '''method_decl : PUBLIC return_type ID LPAREN param_list RPAREN LBRACE stmt_list RBRACE'''

def p_return_type(p):
    '''return_type : VOID
                   | INT
                   | BOOL
                   | DECIMAL
                   | STRING'''

def p_param_list(p):
    '''param_list : param_list COMMA param
                  | param
                  | empty'''

def p_param(p):
    '''param : type ID'''

def p_type(p):
    '''type : INT
            | DECIMAL
            | STRING
            | BOOL'''

# ── Estructura de datos: List ─────────────────────────────────

def p_list_decl(p):
    '''list_decl : LIST LT type GT ID ASSIGN NEW LIST LT type GT LPAREN RPAREN SEMICOLON
                 | LIST LT type GT ID SEMICOLON
                 | LIST ID SEMICOLON'''

# ── Estructura de control: Switch ─────────────────────────────

def p_switch_stmt(p):
    '''switch_stmt : SWITCH LPAREN ID RPAREN LBRACE case_list RBRACE'''

def p_case_list(p):
    '''case_list : case_list case_item
                 | case_item'''

def p_case_item(p):
    '''case_item : CASE case_value COLON stmt_list BREAK SEMICOLON'''

def p_case_value(p):
    '''case_value : INT_LITERAL
                  | STRING_LITERAL
                  | ID'''

# ── Sentencias ────────────────────────────────────────────────

def p_stmt_list(p):
    '''stmt_list : stmt_list stmt
                 | empty'''

def p_stmt(p):
    '''stmt : ID ASSIGN expr SEMICOLON
            | expr SEMICOLON
            | switch_stmt
            | list_decl
            | dict_decl
            | if_stmt
            | while_stmt
            | void_func_decl
            | array_decl
            | var_decl
            | RETURN expr SEMICOLON'''  # fix issue #4: list_decl; Andrés Saltos: dict_decl, if_stmt, return; Victor Morales: void_func_decl, while_stmt, array_decl, var_decl

# ── Expresiones aritméticas y condicionales ───────────────────

def p_expr_binop(p):
    '''expr : expr PLUS   expr
            | expr MINUS  expr
            | expr TIMES  expr
            | expr DIVIDE expr
            | expr AND    expr
            | expr OR     expr
            | expr EQ     expr
            | expr NEQ    expr
            | expr LT     expr
            | expr GT     expr'''

def p_expr_group(p):
    '''expr : LPAREN expr RPAREN'''

def p_expr_call(p):
    '''expr : ID LPAREN arg_list RPAREN'''

def p_arg_list(p):
    '''arg_list : arg_list COMMA expr
                | expr
                | empty'''

def p_expr_atom(p):
    '''expr : ID
            | INT_LITERAL
            | DECIMAL_LITERAL
            | STRING_LITERAL
            | TRUE
            | FALSE'''

# ── Andrés Saltos: Estructura de datos Diccionario ────────────
# Reconoce 'Dictionary<K,V> nombre = new Dictionary<K,V>();' y la declaración simple.
# 'Dictionary' llega como ID (no es reservada); reutiliza el no-terminal 'type' para K y V.
def p_dict_decl(p):
    '''dict_decl : ID LT type COMMA type GT ID ASSIGN NEW ID LT type COMMA type GT LPAREN RPAREN SEMICOLON
                 | ID LT type COMMA type GT ID SEMICOLON'''

# ── Andrés Saltos: Estructura de control if / else ────────────
# Reconoce 'if (expr) { stmt_list } else { stmt_list }' y la variante sin else.
def p_if_stmt(p):
    '''if_stmt : IF LPAREN expr RPAREN LBRACE stmt_list RBRACE ELSE LBRACE stmt_list RBRACE
               | IF LPAREN expr RPAREN LBRACE stmt_list RBRACE'''

# ── Andrés Saltos: Función con retorno (sin 'public') ─────────
# Reconoce 'tipo Nombre(params) { ... }', distinta de method_decl (que lleva 'public').
# Reutiliza 'type' (retorno) y 'param_list'. El cuerpo usa la sentencia 'return expr;'.
def p_func_decl(p):
    '''func_decl : type ID LPAREN param_list RPAREN LBRACE stmt_list RBRACE'''

# ── Victor Morales – Inicio ───────────────────────────────────

def p_void_func_decl(p):
    '''void_func_decl : VOID ID LPAREN param_list RPAREN LBRACE stmt_list RBRACE'''

def p_while_stmt(p):
    '''while_stmt : WHILE LPAREN expr RPAREN LBRACE stmt_list RBRACE'''

def p_array_decl(p):
    '''array_decl : type LBRACKET RBRACKET ID ASSIGN NEW type LBRACKET expr RBRACKET SEMICOLON
                  | type LBRACKET RBRACKET ID SEMICOLON'''

def p_var_decl(p):
    '''var_decl : type ID ASSIGN expr SEMICOLON
                | type ID SEMICOLON'''

def p_expr_index(p):
    '''expr : ID LBRACKET expr RBRACKET'''

def p_expr_method_call(p):
    '''expr : ID DOT ID LPAREN arg_list RPAREN'''

# ── Victor Morales – Fin ──────────────────────────────────────

# ── Producción vacía y manejo de errores ──────────────────────

def p_empty(p):
    '''empty :'''

def p_error(p):
    msg = f"Error Sintáctico: '{p.value}' en línea {p.lineno}" if p else "Error Sintáctico: EOF inesperado"
    print(msg)
    errores_sintacticos.append(msg)

# debug=False suprime la generación del archivo parser.out
parser = yacc.yacc(debug=False)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python parser.py <archivo.cs>")
        sys.exit(1)
    archivo = sys.argv[1]
    with open(archivo, "r", encoding="utf-8") as f:
        codigo = f.read()
    errores_sintacticos.clear()
    lexer_instance = lex.lex(module=lexer_module)
    parser.parse(codigo, lexer=lexer_instance)
    estado = "exitoso" if not errores_sintacticos else f"con {len(errores_sintacticos)} error(es)"
    print(f"Parsing {estado}: {archivo}")
    generar_log(tipo_analisis="sintactico", nombre="vicmmoraM",
                tokens_encontrados=[], errores=errores_sintacticos, source=codigo)
