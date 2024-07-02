from AnalizadorSintactico import Nodo

class SymbolTable:
    def __init__(self):
        self.symbols = []

    def add_symbol(self, name, symbol_type, value=None, scope='local', func_belong=None):
        self.symbols.append({
            'name': name,
            'type': symbol_type,
            'value': value,
            'scope': scope,
            'function_belonging': func_belong
        })

    def __str__(self):
        header = f"{'Nombre':<15} {'Tipo':<10} {'Valor':<20} {'Scope':<10} {'Funcion':<15}"
        rows = [header]
        for symbol in self.symbols:
            row = f"{symbol['name']:<15} {symbol['type']:<10} {str(symbol['value']):<20} {symbol['scope']:<10} {symbol['function_belonging']}"
            rows.append(row)
        return '\n'.join(rows)

def build_symbol_table(node, symbol_table, current_function=None):
    print(f"Procesando nodo: {node.valor}")
    if node.valor == 'FUNCION':
        function_name = node.hijos[1].lexema 
        symbol_table.add_symbol(function_name, 'Función', None, 'global', None)
        print("Añadiendo función:", function_name)
        current_function = function_name

        if len(node.hijos) > 3 and node.hijos[3].valor == 'TERM':
            term_node = node.hijos[3]
            if term_node.hijos[0].valor == 'Identificador':
                identificador = term_node.hijos[0].lexema 
                symbol_table.add_symbol(identificador, 'Parámetro', None, 'local', current_function)
                print("Añadiendo parámetro desde TERM:", identificador)

            for child in term_node.hijos[1:]:
                if child.valor == 'TERM_FUNC':
                    if len(child.hijos) > 1 and child.hijos[1].valor == 'TERM':
                        term_child = child.hijos[1]
                        if term_child.hijos[0].valor == 'Identificador':
                            identificador = term_child.hijos[0].lexema 
                            symbol_table.add_symbol(identificador, 'Parámetro', None, 'local', current_function)
                            print("Añadiendo parámetro desde TERM_FUNC:", identificador)

        if len(node.hijos) > 6 and node.hijos[6].valor == 'TS':
            ts_node = node.hijos[6]
            if ts_node.hijos[0].valor == 'ASIGNA':
                asigna_node = ts_node.hijos[0]
                if len(asigna_node.hijos) > 1 and asigna_node.hijos[1].valor == 'Identificador':
                    identificador = asigna_node.hijos[1].lexema
                    symbol_table.add_symbol(identificador, 'Variable', None, 'local', current_function)
                    print("Añadiendo variable desde ASIGNA:", identificador)

        if len(node.hijos) > 9 and node.hijos[9].valor == 'TS':
            ts_node = node.hijos[9]
            if len(ts_node.hijos) > 0 and ts_node.hijos[0].valor == 'ASIGNA':
                asigna_node = ts_node.hijos[0]
                if len(asigna_node.hijos) > 1 and asigna_node.hijos[1].valor == 'Identificador':
                    identificador = asigna_node.hijos[1].lexema 
                    symbol_table.add_symbol(identificador, 'Variable', None, 'local', current_function)
                    print("Añadiendo variable desde el décimo hijo TS con ASIGNA:", identificador)

    else:
        for child in node.hijos:
            build_symbol_table(child, symbol_table, current_function)
