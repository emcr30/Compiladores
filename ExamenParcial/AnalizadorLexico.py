import ply.lex as lex

# MEOW
tokens = (
    'Identificador', 'Numeral', 'Oper_plu', 'Oper_min', 'Oper_mul', 'Oper_div',
    'Double_equal', 'Oper_equal', 'Oper_unequal', 'Paren_l', 'Paren_r', 'Key_l', 'Key_r',
    'Formeow', 'Ifmeow', 'Elsemeow', 'Printmeow', 'Comilla_sim', 'Comilla_dob', 'Point',
    'Menor', 'Mayor', 'Menor_equal', 'Mayor_equal', 'Menor_mayor', 'Returnmeow',
    'Defmeow', 'Comma', 'Decim', 'True', 'False', 'Literal', 'Comentario', 'Rangemeow', 'And', 'Or' ,'In', 'Asignameow', 'DotComma', 'comma'
)

t_Oper_plu = r'\+'
t_Oper_min = r'-'
t_Oper_mul = r'\*'
t_Oper_div = r'/'
t_Double_equal = r'=='
t_Oper_equal = r'='
t_Oper_unequal = r'!='
t_Paren_l = r'\('
t_Paren_r = r'\)'
t_Key_l = r'\{'
t_Key_r = r'\}'
t_Point = r'\.'
t_Menor = r'<'
t_Mayor = r'>'
t_Menor_equal = r'<='
t_Mayor_equal = r'>='
t_Menor_mayor = r'<>'
t_Comma = r','
t_Decim = r'[0-9]*\.[0-9]+'
t_DotComma = r';'

def t_Defmeow(t):
    r'Defmeow'
    return t

def t_Returnmeow(t):
    r'Returnmeow'
    return t

def t_Formeow(t):
    r'Formeow'
    return t

def t_Ifmeow(t):
    r'Ifmeow'
    return t

def t_Elsemeow(t):
    r'Elsemeow'
    return t

def t_Printmeow(t):
    r'Printmeow'
    return t

def t_Rangemeow(t):
    r'Rangemeow'
    return t

def t_Asignameow(t):
    r'Asignameow'
    return t

def t_True(t):
    r'True'
    return t

def t_False(t):
    r'False'
    return t

def t_And(t):
    r'And'
    return t

def t_Or(t):
    r'Or'
    return t

def t_In(t):
    r'In'
    return t

def t_Identificador(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_Numeral(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_Literal(t):
    r'\".*?\"'
    return t

def t_Comentario(t):
    r'\#[^\n]*'  
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

#Tokenizar
def tokenize_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
        lexer.input(data)

        with open("diccionariotokens.txt", "w") as f:
            while True:
                tok = lexer.token()
                if not tok:
                    break  
                print(tok)
                
                print(tok.type, end=' ', file=f)

    except FileNotFoundError:
        print(f"El archivo {file_path} no se encontró.")

file_path = 'Ejemplo.txt'
tokenize_from_file(file_path)
