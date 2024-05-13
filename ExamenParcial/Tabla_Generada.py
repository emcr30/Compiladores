import csv

def parse_grammar(file_path):
    with open(file_path, 'r') as file:
        rules = file.read().strip().split('\n')
    productions = {}
    nonterminals = set()
    terminals = set()
    for rule in rules:
        left, right = rule.split('->')
        left, right = left.strip(), right.strip().split(' ')
        nonterminals.add(left)
        if left not in productions:
            productions[left] = []
        productions[left].append(right)
        for symbol in right:
            if symbol not in nonterminals and symbol != "''":
                terminals.add(symbol)
    return productions, nonterminals, terminals

def compute_first(productions, nonterminals):
    first = {nonterminal: set() for nonterminal in nonterminals}
    changed = True
    while changed:
        changed = False
        for nonterminal in nonterminals:
            for production in productions[nonterminal]:
                for symbol in production:
                    if symbol == "''":
                        if "''" not in first[nonterminal]:
                            first[nonterminal].add("''")
                            changed = True
                        break
                    elif symbol in nonterminals:
                        before_add = len(first[nonterminal])
                        first[nonterminal].update(first[symbol] - {"''"})
                        if len(first[nonterminal]) > before_add:
                            changed = True
                        if "''" not in first[symbol]:
                            break
                    else:
                        if symbol not in first[nonterminal]:
                            first[nonterminal].add(symbol)
                            changed = True
                        break
    return first

def compute_follow(productions, nonterminals, first, start_symbol):
    follow = {nonterminal: set() for nonterminal in nonterminals}
    follow[start_symbol].add('$')  # Add end-of-input marker to start symbol
    changed = True
    while changed:
        changed = False
        for lhs, rules in productions.items():
            for prod in rules:
                trailer = follow[lhs]
                for i in range(len(prod) - 1, -1, -1):
                    sym = prod[i]
                    if sym in nonterminals:
                        if trailer - follow[sym]:
                            follow[sym].update(trailer)
                            changed = True
                        if "''" in first[sym]:
                            trailer = trailer.union(first[sym] - {"''"})
                        else:
                            trailer = first[sym]
                    else:
                        trailer = {sym}
    return follow

def save_to_csv(nonterminals, rule_table, terminals, first_sets, follow_sets, filename="tablitaMEOW.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        headers = ["Nonterminal", "First", "Follow"] + sorted([t for t in terminals.union({'$'}) if t not in nonterminals])
        writer.writerow(headers)

        for nonterminal in sorted(nonterminals):
            row = [
                nonterminal,
                ', '.join(sorted(first_sets[nonterminal])),
                ', '.join(sorted(follow_sets[nonterminal]))
            ]
            for terminal in sorted([t for t in terminals.union({'$'}) if t not in nonterminals]):
                rule = rule_table[nonterminal].get(terminal, "")
                row.append(rule)
            writer.writerow(row)
def make_rule_table(productions, first, follow, terminals):
    rule_table = {nonterminal: {terminal: "" for terminal in terminals.union({'$'})} for nonterminal in nonterminals}
    for nonterminal, rules in productions.items():
        for rule in rules:
            firsts = collect_firsts(rule, first)
            for symbol in firsts:
                if symbol == "''":  # epsilon production
                    for follow_symbol in follow[nonterminal]:
                        if follow_symbol in terminals or follow_symbol == '$':
                            rule_table[nonterminal][follow_symbol] = ' -> '.join([nonterminal, ' '.join(rule)])
                elif symbol in terminals or symbol == '$':
                    rule_table[nonterminal][symbol] = ' -> '.join([nonterminal, ' '.join(rule)])
    return rule_table

def collect_firsts(production, first):
    firsts = set()
    for symbol in production:
        if symbol in first:
            firsts.update(first[symbol])
            if "''" not in first[symbol]:
                break
        else:
            firsts.add(symbol)
            break
    return firsts


# Main script
file_path = 'MEOW.txt'
productions, nonterminals, terminals = parse_grammar(file_path)
first_sets = compute_first(productions, nonterminals)
start_symbol = list(nonterminals)[0]
follow_sets = compute_follow(productions, nonterminals, first_sets, start_symbol)
ll1_table = make_rule_table(productions, first_sets, follow_sets, terminals)

save_to_csv(nonterminals, ll1_table, terminals, first_sets, follow_sets)
