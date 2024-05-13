import pandas as pd

class Nodo:
    def __init__(self, valor, id):
        self.valor = valor
        self.hijos = []
        self.id = id  # Identificador único para cada nodo

next_id = 0  # Variable global para asegurar que cada nodo tenga un ID único

def cargar_tabla_ll1(ruta_csv):
    return pd.read_csv(ruta_csv, index_col='Nonterminal')

def leer_tokens(ruta_txt):
    with open(ruta_txt, 'r') as file:
        tokens = file.read().split()
    tokens.append('$')  # Añadir el símbolo de fin de entrada
    return tokens

def analizar(tokens, tabla_ll1, simbolo_inicial):
    global next_id
    nodo_final = Nodo('$', next_id)
    next_id += 1
    pila = [nodo_final]
    pila.append(Nodo(simbolo_inicial, next_id))  # Usar Nodo para mantener el árbol sintáctico
    next_id += 1
    nodos = [pila[-1]]  # Para almacenar todos los nodos y luego generar el .dot

    posicion_token = 0
    while pila:
        nodo_actual = pila.pop()
        token_actual = tokens[posicion_token]
        print(f'Pila: {[n.valor for n in pila]}, Token Actual: {token_actual}, Tope de Pila: {nodo_actual.valor}')

        if nodo_actual.valor == '$' and token_actual == '$':
            return True, 'Entrada aceptada', nodos
        elif nodo_actual.valor == token_actual:
            posicion_token += 1  # Consumir token
        elif nodo_actual.valor in tabla_ll1.index:
            regla = tabla_ll1.loc[nodo_actual.valor, token_actual]
            if pd.notna(regla):
                elementos_produccion = regla.split('->')[1].strip().split()[::-1]
                for elemento in elementos_produccion:
                    if elemento != "''" and not elemento.startswith('->'):
                        nuevo_nodo = Nodo(elemento, next_id)
                        next_id += 1
                        nodo_actual.hijos.append(nuevo_nodo)
                        pila.append(nuevo_nodo)
                        nodos.append(nuevo_nodo)  # Agregar el nodo para su uso en .dot
            else:
                return False, f'Error de sintaxis: no hay regla para {nodo_actual.valor} con {token_actual}', None
        else:
            return False, f'Error de coincidencia de token: esperado {nodo_actual.valor}, encontrado {token_actual}', None

    return False, 'La entrada no fue completamente procesada', nodos

def imprimir_dot(nodos, filename="arbol.dot"):
    with open(filename, "w") as f:
        f.write("digraph Arbol {\n")
        for nodo in nodos:
            f.write(f'n{nodo.id} [label="{nodo.valor}"];\n')  # Define nodos
            for hijo in nodo.hijos:
                f.write(f'n{nodo.id} -> n{hijo.id};\n')  # Define conexiones
        f.write("}\n")

# Uso del código
tabla_ll1 = cargar_tabla_ll1('meow.csv')
tokens = leer_tokens('tokens.txt')
resultado, mensaje, nodos = analizar(tokens, tabla_ll1, 'TS')
print(resultado, mensaje)
if nodos:
    imprimir_dot(nodos)
    print("Archivo DOT generado correctamente.")
