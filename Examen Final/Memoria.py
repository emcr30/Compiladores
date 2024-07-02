class Nodo:
    def __init__(self, valor, lexema, linea, id):
        self.valor = valor
        self.lexema = lexema
        self.linea = linea
        self.hijos = []
        self.id = id  

def recorrer_arbol(nodo):
    global code_section, label_count
    if nodo.valor == 'FUNCION':
        function_name = nodo.hijos[1].lexema
        code_section += f"\n{function_name}:\n"  #
    elif nodo.valor == 'TS':
        function_name = nodo.hijos[0].lexema
        code_section += f"    jal {function_name}\n"#llamada a la funcion
        
    elif nodo.valor == 'IF':
        condicion = nodo.hijos[1]  
        procesar_condicion(condicion)
    elif nodo.valor == 'ASIGNA':
        identificador = nodo.hijos[0].lexema
        valor_inicial = nodo.hijos[2].hijos[0].lexema
        generar_codigo_assembler(identificador, valor_inicial)
    elif nodo.valor == 'FOR':
        condicion = nodo.hijos[5]  
        procesar_for(nodo)
    for hijo in nodo.hijos:
        recorrer_arbol(hijo)

def procesar_condicion(nodo_cond):
    global code_section, label_count
    comparando = nodo_cond.hijos[0].lexema ==  'CONDICION'
    operador = nodo_cond.hijos[1].lexema    
    comparado = nodo_cond.hijos[2].lexema   
    code_section += f"    lw $a0, {comparando}\n"  
    if comparado.isdigit(): 
        code_section += f"    li $t1, {comparado}\n"
        comparado_reg = "$t1"
    else:  
        code_section += f"    lw $t1, {comparado}\n"
        comparado_reg = "$t1"

    label_true = f"label{label_count}"
    label_false = f"label{label_count+1}"
    label_count += 2

    if operador == '>':
        code_section += f"    bgt $a0, {comparado_reg}, {label_true}\n"
    elif operador == '<':
        code_section += f"    blt $a0, {comparado_reg}, {label_true}\n"
    elif operador == '>=':
        code_section += f"    bge $a0, {comparado_reg}, {label_true}\n"
    elif operador == '<=':
        code_section += f"    ble $a0, {comparado_reg}, {label_true}\n"
    elif operador == '==':
        code_section += f"    beq $a0, {comparado_reg}, {label_true}\n"
    elif operador == '!=':
        code_section += f"    bne $a0, {comparado_reg}, {label_true}\n"#comparar
    elif operador == 'POS':
        code_section += f"    bgtz $a0, {label_true}\n" #<0
    elif operador == 'NEG':
        code_section += f"    bltz $a0, {label_true}\n" #>
        

    code_section += f"    j {label_false}\n"
    code_section += f"{label_true}:\n"

    #verdadero
    code_section += "    li $v0, 4\n"
    code_section += "    la $a0, msg_true\n"
    code_section += "    syscall\n"
    code_section += f"    j end_if\n"

    code_section += f"{label_false}:\n"
    #falso
    code_section += "    li $v0, 4\n"
    code_section += "    la $a0, msg_false\n"
    code_section += "    syscall\n"

    code_section += "end_if:\n"

def procesar_for(nodo_for):
    global code_section, label_count
    if len(nodo_for.hijos) > 5 and nodo_for.hijos[5].valor == 'RANGE':
        start_value = int(nodo_for.hijos[5].hijos[0].lexema)  
        end_value = int(nodo_for.hijos[5].hijos[1].hijos[0].hijos[0].lexema) 

        loop_start = f"loop{label_count}"
        loop_end = f"end_loop{label_count}"
        label_count += 1

        code_section += f"{loop_start}:\n"
        code_section += f"    li $t2, {start_value}\n" 
        
        code_section += "    li $v0, 1\n"
        code_section += "    move $a0, $t2\n"
        code_section += "    syscall\n"  

        code_section += "    li $v0, 4\n"
        code_section += "    la $a0, newLine\n"
        code_section += "    syscall\n"  

        code_section += "    addi $t2, $t2, 1\n"  
        code_section += f"    bne $t2, {end_value + 1}, {loop_start}\n"  
        code_section += f"{loop_end}:\n"


def generar_codigo_assembler(identificador, valor_inicial=None):
    global data_section
    if '"' in valor_inicial:
        data_section += f'{identificador}: .asciiz {valor_inicial}\n'
    else:
        data_section += f'{identificador}: .word {valor_inicial}\n'


data_section = ""
code_section = ""
label_count = 0
