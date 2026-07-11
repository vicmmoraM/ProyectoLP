import sys
import ply.yacc as yacc
import ply.lex as lex

sys.path.insert(0, '.')
import lexer as lexer_module
from lexer import tokens  
from logger import generar_log

sys.stdout.reconfigure(encoding='utf-8')
errores_sintacticos = []
errores_semanticos = []
loop_depth = 0
symbol_table = {}   
current_return_type = None   

def sem_error(msg, lineno=None):
    if lineno:
        msg = f"{msg} (línea {lineno})"
    errores_semanticos.append(msg)
    print(msg)

def declarar(nombre, tipo, lineno=None):
    if nombre in symbol_table:
        sem_error(f"Error Semántico: El tipo ya contiene una definición para '{nombre}'.", lineno)
    symbol_table[nombre] = tipo

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

def p_method_header(p):
    '''method_header : PUBLIC return_type ID LPAREN param_list RPAREN'''
    global current_return_type
    current_return_type = p[2]

def p_method_decl(p):
    '''method_decl : method_header LBRACE stmt_list RBRACE'''
    global current_return_type
    current_return_type = None

def p_return_type(p):
    '''return_type : VOID
                   | INT
                   | BOOL
                   | DECIMAL
                   | STRING'''
    p[0] = p[1].lower()

def p_param_list(p):
    '''param_list : param_list COMMA param
                  | param
                  | empty'''

def p_param(p):
    '''param : type ID'''
    symbol_table[p[2]] = p[1]

def p_type(p):
    '''type : INT
            | DECIMAL
            | STRING
            | BOOL'''
    p[0] = p[1].lower()  

# ── Estructura de datos: List ─────────────────────────────────

def p_list_decl(p):
    '''list_decl : LIST LT type GT ID ASSIGN NEW LIST LT type GT LPAREN RPAREN SEMICOLON
                 | LIST LT type GT ID SEMICOLON
                 | LIST ID SEMICOLON'''
    if len(p) == 15 or len(p) == 7:
        declarar(p[5], f'List<{p[3]}>', p.lineno(5))
    else:
        declarar(p[2], 'List', p.lineno(2))

# ── Estructura de control: Switch ─────────────────────────────

def p_switch_header(p):
    '''switch_header : SWITCH LPAREN ID RPAREN'''
    global loop_depth
    loop_depth += 1

def p_switch_stmt(p):
    '''switch_stmt : switch_header LBRACE case_list RBRACE'''
    global loop_depth
    loop_depth -= 1

def p_case_list(p):
    '''case_list : case_list case_item
                 | case_item'''

def p_case_item(p):
    '''case_item : CASE case_value COLON stmt_list'''

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
            | RETURN expr SEMICOLON
            | for_stmt
            | compound_assign
            | BREAK SEMICOLON'''  # fix issue #4: list_decl; Andrés Saltos: dict_decl, if_stmt, return; Victor Morales: void_func_decl, while_stmt, array_decl, var_decl, for_stmt, compound_assign, break
    if p.slice[1].type == 'RETURN':
        tipo_retorno = p[2] if isinstance(p[2], str) else None
        if current_return_type == 'bool' and tipo_retorno != 'bool':
            sem_error("Error Semántico: El tipo de valor devuelto por la función no coincide con el tipo 'bool'.")
    if p.slice[1].type == 'BREAK':
        if loop_depth == 0:
            sem_error("Error Semántico: Ningún bucle o instrucción switch envolvente para abandonar o continuar.", p.lineno(1))
    # Bloque de Andrés: reasignación ID = expr
    if p.slice[1].type == 'ID' and len(p) == 5:
        tipo_var = symbol_table.get(p[1], None)
        tipo_expr = p[3] if isinstance(p[3], str) else None
        if tipo_var and tipo_expr and tipo_expr not in (tipo_var, 'unknown'):
            if not (tipo_var == 'int' and tipo_expr == 'decimal'):
                sem_error(f"Error Semántico: No se puede convertir implícitamente el tipo '{tipo_expr}' en '{tipo_var}'.", p.lineno(1))

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
    op = p.slice[2].type
    tipo_izq = p[1] if isinstance(p[1], str) else 'unknown'
    tipo_der = p[3] if isinstance(p[3], str) else 'unknown'
    if op in ('TIMES', 'DIVIDE'):
        if tipo_izq == 'string' or tipo_der == 'string':
            op_sym = '*' if op == 'TIMES' else '/'
            sem_error(f"Error Semántico: El operador '{op_sym}' no se puede aplicar a operandos del tipo 'string'.")
    if op in ('AND', 'OR', 'EQ', 'NEQ', 'LT', 'GT'):
        p[0] = 'bool'
    else:
        p[0] = tipo_izq

def p_expr_group(p):
    '''expr : LPAREN expr RPAREN'''
    p[0] = p[2]

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
    tok = p.slice[1].type
    if tok == 'ID':
        if p[1] not in symbol_table:
            sem_error(f"Error Semántico: La variable '{p[1]}' no existe en el contexto actual.", p.lineno(1))
        p[0] = symbol_table.get(p[1], 'unknown')
    elif tok == 'INT_LITERAL':
        p[0] = 'int'
    elif tok == 'DECIMAL_LITERAL':
        p[0] = 'decimal'
    elif tok == 'STRING_LITERAL':
        p[0] = 'string'
    elif tok in ('TRUE', 'FALSE'):
        p[0] = 'bool'

# ── Andrés Saltos: Estructura de datos Diccionario ────────────
# Reconoce 'Dictionary<K,V> nombre = new Dictionary<K,V>();' y la declaración simple.
# 'Dictionary' llega como ID (no es reservada); reutiliza el no-terminal 'type' para K y V.
def p_dict_decl(p):
    '''dict_decl : ID LT type COMMA type GT ID ASSIGN NEW ID LT type COMMA type GT LPAREN RPAREN SEMICOLON
                 | ID LT type COMMA type GT ID SEMICOLON'''
    declarar(p[7], f'Dictionary<{p[3]},{p[5]}>', p.lineno(7))

# ── Andrés Saltos: Estructura de control if / else ────────────
# Reconoce 'if (expr) { stmt_list } else { stmt_list }' y la variante sin else.
def p_if_stmt(p):
    '''if_stmt : IF LPAREN expr RPAREN LBRACE stmt_list RBRACE ELSE LBRACE stmt_list RBRACE
               | IF LPAREN expr RPAREN LBRACE stmt_list RBRACE'''

# ── Andrés Saltos: Función con retorno (sin 'public') ─────────
# Reconoce 'tipo Nombre(params) { ... }', distinta de method_decl (que lleva 'public').
# Reutiliza 'type' (retorno) y 'param_list'. El cuerpo usa la sentencia 'return expr;'.
def p_func_header(p):
    '''func_header : type ID LPAREN param_list RPAREN'''
    global current_return_type
    current_return_type = p[1]

def p_func_decl(p):
    '''func_decl : func_header LBRACE stmt_list RBRACE'''
    global current_return_type
    current_return_type = None

# ── Victor Morales – Inicio ───────────────────────────────────

def p_void_func_header(p):
    '''void_func_header : VOID ID LPAREN param_list RPAREN'''
    global current_return_type
    current_return_type = 'void'

def p_void_func_decl(p):
    '''void_func_decl : void_func_header LBRACE stmt_list RBRACE'''
    global current_return_type
    current_return_type = None

def p_while_header(p):
    '''while_header : WHILE LPAREN expr RPAREN'''
    global loop_depth
    loop_depth += 1

def p_while_stmt(p):
    '''while_stmt : while_header LBRACE stmt_list RBRACE'''
    global loop_depth
    loop_depth -= 1

def p_array_decl(p):
    '''array_decl : type LBRACKET RBRACKET ID ASSIGN NEW type LBRACKET expr RBRACKET SEMICOLON
                  | type LBRACKET RBRACKET ID SEMICOLON'''
    declarar(p[4], p[1] + '[]', p.lineno(4))

def p_var_decl(p):
    '''var_decl : type ID ASSIGN expr SEMICOLON
                | type ID SEMICOLON'''
    tipo_declarado = p[1]
    nombre_var = p[2]
    declarar(nombre_var, tipo_declarado, p.lineno(2))
    if len(p) == 6:  # tiene asignación
        tipo_expr = p[4] if isinstance(p[4], str) else None
        if tipo_declarado == 'int' and tipo_expr == 'decimal':       # Victor (NO eliminar)
            sem_error("Error Semántico: Posible pérdida de precisión. Falta una conversión explícita.", p.lineno(2))
        elif tipo_expr and tipo_expr not in (tipo_declarado, 'unknown'):   # Andrés
            # 'unknown' = el tipo no se pudo determinar (p.ej. var no declarada que ya dio error). Se ignora para no encadenar un 2º error.
            sem_error(f"Error Semántico: No se puede convertir implícitamente el tipo '{tipo_expr}' en '{tipo_declarado}'.", p.lineno(2))

def p_for_header(p):
    '''for_header : FOR LPAREN for_init SEMICOLON expr SEMICOLON for_update RPAREN'''
    global loop_depth
    loop_depth += 1

def p_for_stmt(p):
    '''for_stmt : for_header LBRACE stmt_list RBRACE'''
    global loop_depth
    loop_depth -= 1

def p_for_init(p):
    '''for_init : type ID ASSIGN expr
                | ID ASSIGN expr
                | empty'''
    if len(p) == 5: 
        symbol_table[p[2]] = p[1]

def p_for_update(p):
    '''for_update : ID ASSIGN expr
                  | compound_assign_expr
                  | empty'''

def p_compound_assign_expr(p):
    '''compound_assign_expr : ID PLUS_ASSIGN expr
                            | ID MINUS_ASSIGN expr
                            | ID TIMES_ASSIGN expr
                            | ID DIV_ASSIGN expr'''

def p_compound_assign(p):
    '''compound_assign : ID PLUS_ASSIGN expr SEMICOLON
                       | ID MINUS_ASSIGN expr SEMICOLON
                       | ID TIMES_ASSIGN expr SEMICOLON
                       | ID DIV_ASSIGN expr SEMICOLON'''
    tipo_var = globals().get('symbol_table', {}).get(p[1], 'unknown')
    tipo_expr = p[3] if isinstance(p[3], str) else None
    if tipo_var == 'int' and tipo_expr == 'decimal':
        sem_error("Error Semántico: Posible pérdida de precisión. Falta una conversión explícita.", p.lineno(1))

def p_expr_index(p):
    '''expr : ID LBRACKET expr RBRACKET'''

def p_expr_method_call(p):
    '''expr : ID DOT ID LPAREN arg_list RPAREN'''

# ── Victor Morales – Fin ──────────────────────────────────────

# ── Producción vacía y manejo de errores ──────────────────────

def p_empty(p):
    '''empty :'''

def p_error(p):
    if p is None:
        msg = ("Error Sintáctico: el código terminó antes de lo esperado. "
               "Probablemente falta una llave de cierre '}' o un ';' al final.")
    else:
        msg = f"Error Sintáctico: token inesperado '{p.value}' en línea {p.lineno}"
        if p.lexpos == 0:
            msg += (". Todo programa debe comenzar con 'public class Nombre { ... }'; "
                    "no se permiten declaraciones sueltas a nivel superior.")
        elif p.type == 'RBRACE':
            msg += ". Llave de cierre inesperada: revise que las llaves estén balanceadas o que la sentencia anterior esté completa."
        elif p.type == 'SEMICOLON':
            msg += ". Hay un ';' donde no corresponde o la expresión anterior está incompleta."
        elif p.type in ('FOR', 'WHILE', 'IF', 'SWITCH'):
            msg += f". La estructura '{p.value}' no es válida en esta posición; solo puede aparecer dentro del cuerpo de una función."
        else:
            msg += ". El token no encaja en la gramática en esta posición; revise la sentencia anterior (¿falta ';', '{' o un operador?)."
    print(msg)
    errores_sintacticos.append(msg)

parser = yacc.yacc(debug=False)

def analizar(codigo):
    """Ejecuta el análisis completo (léxico + sintáctico + semántico) sobre un
    string de código y retorna los resultados como estructuras de datos.
    Resetea el estado global entre llamadas para que la GUI pueda reanalizarse
    sin reiniciar el proceso. No escribe logs (eso queda a cargo del llamador)."""
    global loop_depth
    errores_sintacticos.clear()
    errores_semanticos.clear()
    symbol_table.clear()
    loop_depth = 0
    lexer_module.errores_lexicos.clear()

    # Pasada léxica: recolecta tokens y errores léxicos (con línea/columna)
    lx = lex.lex(module=lexer_module)
    lx.input(codigo)
    tokens_encontrados = list(lx)
    errores_lexicos = list(lexer_module.errores_lexicos)

    # Pasada sintáctica + semántica (lexer fresco para reiniciar lineno)
    lexer_module.errores_lexicos.clear()
    parser.parse(codigo, lexer=lex.lex(module=lexer_module))

    return {
        "tokens": tokens_encontrados,
        "errores_lexicos": errores_lexicos,
        "errores_sintacticos": list(errores_sintacticos),
        "errores_semanticos": list(errores_semanticos),
    }

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
    generar_log(tipo_analisis="semantico", nombre="arzel01",
                tokens_encontrados=[], errores=errores_semanticos, source=codigo)
