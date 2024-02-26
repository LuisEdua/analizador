gramatica = {
    ("S", "FUNC"): ["SF"],
    ("SF", "FUNC"): ["FUNC", "NF", "C", "SF"],
    ("SF", "$"): ["EPSILON"],
    ("NF", "ID"): ["ID"],
    ("NF", "MAIN"): ["MAIN"],
    ("C", "PARENTESISA"): ["PARENTESISA", "P", "PARENTESISC", "LLAVEA", "CO", "LLAVEC"],
    ("P", "ID"): ["ID", "RP"],
    ("P", "PARENTESISC"): ["EPSILON"],
    ("RP", "COMMA"): ["COMMA", "ID", "RP"],
    ("RP", "PARENTESISC"): ["EPSILON"],
    ("CO", "IN"): ["IN", "INASSIGN", "ID", "CO"],
    ("CO", "PRINT"): ["PRINT", "PARENTESISA", "D", "PARENTESISC", "CO"],
    ("D", "STRING"): ["STRING", "RD"],
    ("D", "ID"): ["ID", "RD"],
    ("RD", "COMMA"): ["COMMA", "D"],
    ("RD", "PARENTESISC"): ["EPSILON"],
    ("CO", "WHILE"): ["WHILE", "CONDITION", "LLAVEA", "CO", "LLAVEC", "CO"],
    ("CONDITION", "PARENTESISA"): ["PARENTESISA", "EV", "COMPARE", "EV", "CONTINUE", "PARENTESISC"],
    ("CONTINUE", "AGGREGATECONDITION"): ["AGGREGATECONDITION", "EV", "COMPARE", "EV", "CONTINUE"],
    ("CONTINUE", "PARENTESISC"): ["EPSILON"],
    ("EV", "ID"): ["ID"],
    ("EV", "NUMBER"): ["NUMBER"],
    ("EV", "BOL"): ["BOL"],
    ("EV", "STRING"): ["STRING"],
    ("CO", "IF"): ["IF", "CONDITION", "LLAVEA", "CO", "LLAVEC", "ES", "CO"],
    ("ES", "ELSE"): ["ELSE", "LLAVEA", "CO", "LLAVEC"],
    ("ES", "IN"): ["EPSILON"],
    ("ES", "PRINT"): ["EPSILON"],
    ("ES", "WHILE"): ["EPSILON"],
    ("ES", "IF"): ["EPSILON"],
    ("ES", "ID"): ["EPSILON"],
    ("ES", "LLAVEC"): ["EPSILON"],
    ("CO", "ID"): ["ID", "AID", "CO"],
    ("AID", "COMMA"): ["MID"],
    ("AID", "ASSIGN"): ["ASSIGN", "VALUE", "RVALUE"],
    ("MID", "COMMA"): ["COMMA", "ID", "MID"],
    ("MID", "ASSIGN"): ["ASSIGN", "VALUE", "RVALUE"],
    ("VALUE", "ID"): ["ID"],
    ("VALUE", "NUMBER"): ["NUMBER"],
    ("VALUE", "BOL"): ["BOL"],
    ("VALUE", "STRING"): ["STRING"],
    ("RVALUE", "COMMA"): ["COMMA", "VALUE", "RVALUE"],
    ("RVALUE", "OPERATOR"): ["OPERATOR", "VALUE", "RVALUE"],
    ("RVALUE", "IN"): ["EPSILON"],
    ("RVALUE", "PRINT"): ["EPSILON"],
    ("RVALUE", "WHILE"): ["EPSILON"],
    ("RVALUE", "IF"): ["EPSILON"],
    ("RVALUE", "ID"): ["EPSILON"],
    ("RVALUE", "LLAVEC"): ["EPSILON"],
    ("AID", "PARENTESISA"): ["PARENTESISA", "P", "PARENTESISC"],
    ("CO", "LLAVEC"): ["EPSILON"],
}

terminales = [
    'FUNC', 'MAIN', 'IF', 'ELSE', 'IN', 'INASSIGN', 'PRINT', 'WHILE', 'BOL', 'AGGREGATECONDITION', 'ID', 'NUMBER',
    'STRING', 'OPERATOR', 'COMPARE', 'COMMA', 'SEMICOLON', 'LLAVEA', 'LLAVEC', 'PARENTESISA', 'PARENTESISC', 'CORCHETEA',
    'CORCHETEC', 'ASSIGN', '$'
]



def analizador_sintactico(simbolos):
    stack = ['$', 'S']
    text = str(stack) + '\n'
    index = 0
    simbolos.append(('$', '$', simbolos[-1][2]))
    while True:
        X = stack.pop()
        a = simbolos[index][0]
        if X in terminales:
            if X == a:
                index += 1    
                text += str(stack) + '\n'
                if X == '$':
                    return text
            else:
                return (text + f'\nError de sintaxis en la linea {simbolos[index][2]}' + 
                f'\n Entrada en conflicto: {simbolos[index][0]} con el valor {simbolos[index][1]}')
        else:
            if (X, a) in gramatica:
                producciones = gramatica[(X, a)]
                if producciones != ['EPSILON']:
                    for produccion in reversed(producciones):
                        stack.append(produccion)
                text += str(stack) + '\n'
            else:
                return (text + f'\nError de sintaxis en la linea {simbolos[index][2]}' +
                f'\n Entrada en conflicto: {simbolos[index][0]} con el valor {simbolos[index][1]}')