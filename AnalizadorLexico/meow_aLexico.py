import ply.lex as lex

# Lista de nombres de tokens. Siempre se requiere esto.
tokens = (
    'Identificador',
    'Numeral', 
    'Comments_lar',
    'Oper_plu',
    'Oper_min',
    'Oper_mul',
    'Oper_div',
    'Doble_equal',
    'Oper_equal',
    'Oper_unequal',
    'Paren_l',
    'Paren_r',
    'Key_l',
    'Key_r',
    'For', 
    'If',
    'Else',
    'Print',
    'Comilla_sim',
    'Comilla_dob',
    'Michi',
    'Point', 
    'Menor',
    'Mayor',
    'Menor_equal',
    'Mayor_equal',
    'Menor_mayor',
    'Return',
    'Funcion',
    'Type_string',
    'Type_boolean',
    'Type_int',
    'Type_float',
    'Comma',
    'Decim',
    'Boolean',
    'Literal',
)

reserved = {
    'defmeow': 'Funcion',
    'formeow': 'For',
    'ifmeow': 'If',
    'elsmeow': 'Else',
    '"""': 'Comments_lar',
    'returnmeow': 'Return',
    'printmeoow': 'Print',
    'int': 'Type_int',
    'float': 'Type_float',
    'bool': 'Type_boolean',
    'str': 'Type_string',
}

# Reglas de expresiones regulares para tokens simples
t_Oper_plu = r'\+'
t_Oper_min = r'-'
t_Oper_mul = r'\*'
t_Oper_div = r'/'
t_Oper_equal = r'='
t_Doble_equal = r'=='
t_Oper_unequal = r'!='
t_Paren_l = r'\('
t_Paren_r = r'\)'
t_Key_l = r'{'
t_Key_r = r'}'
t_Comments_lar = r'"""[\s\S]*?"""'
t_Comilla_sim = r'\''
t_Comilla_dob = r'\"'
t_Michi = r'\#'
t_Point = r'\.'
t_Menor = r'<'
t_Mayor = r'>'
t_Menor_equal = r'<='
t_Mayor_equal = r'>='
t_Menor_mayor = r'<>'
t_Comma = r','
t_Decim = r'[0-9]+\.[0-9]+'

# números
def t_Numeral(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

#  identificadores
def t_Identificador(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'Identificador')  
    return t


# Una cadena que contiene caracteres ignorados (espacios y tabulaciones)
t_ignore = ' \t'

# Regla para manejar errores léxicos
def t_error(t):
    print("Caracter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

# Construir el analizador léxico
lexer = lex.lex()

with open('HolaMundo.txt', 'r') as file:
    data = file.read()

# Darle al lexer la entrada desde el archivo
lexer.input(data)

# Tokenizar
while True:
    tok = lexer.token()
    if not tok: 
        break     
    print(f'Token: {tok.type}, Valor: {tok.value}, Fila: {tok.lineno}, Columna: {tok.lexpos}')






