import re

def analizador_lexico(input_string):
    tokens = {
        'FUNC': r'func',
        'MAIN': r'main',
        'IF': r'if',
        'ELSE': r'else',
        'IN': r'in|>>',
        'PRINT': r'println|print',
        'WHILE': r'while',
        'BOL': r'true|false',
        'OR': r'or',
        'AND': r'and',
        'ID': r'[a-zA-Z]([a-zA-Z0-9_])*', # hola, a, a_2
        'NUMBER': r'\d+(\.\d+)?', #9, 9.7, 55, 10.52
        'STRING': r'\".*?\"', # "", "lkjsdlkjs", "hola mundo", "Jodjsja@madñk"
        'OPERATOR': r'\+|\-|\/|\*',#no poner \
        'COMPARE': r'==|<=|>=|!=|>|<',
        'SYMBOL': r'\,|\;|\{|\}|\(|\)|\[|\]|_', #no poner \
        'ASSIGN': r'=',
        'UNKNOWN': r'\S+'
    }

    token_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in tokens.items())

    output = []
    for match in re.finditer(token_regex, input_string):
        token_type = match.lastgroup
        lexeme = match.group()
        output.append(f'{token_type}: {lexeme}')

    return '\n'.join(output)
