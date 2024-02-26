import re

def analizador_lexico(input_string):
    tokens = {
        'FUNC': r'func',
        'MAIN': r'main',
        'IF': r'if',
        'ELSE': r'else',
        'IN': r'in',
        "INASSIGN": r'>>',
        'PRINT': r'println|print',
        'WHILE': r'while',
        'BOL': r'true|false',
        'AGGREGATECONDITION': r'or|and',
        'ID': r'[a-zA-Z]([a-zA-Z0-9_])*',
        'NUMBER': r'\d+(\.\d+)?',
        'STRING': r'\".*?\"',
        'OPERATOR': r'\+|\-|\/|\*',
        'COMPARE': r'==|<=|>=|!=|>|<',
        'COMMA': r',',
        "LLAVEA": r'\{',
        "LLAVEC": r'\}',
        "PARENTESISA": r'\(',
        "PARENTESISC": r'\)',
        "CORCHETEA": r'\[',
        "CORCHETEC": r'\]',
        'ASSIGN': r'=',
        'UNKNOWN': r'\S+'
    }

    token_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in tokens.items())

    line_number = 1
    tokens_with_lines = []
    lines = input_string.split('\n')
    
    for line in lines:
        for match in re.finditer(token_regex, line):
            token_type = match.lastgroup
            lexeme = match.group()
            tokens_with_lines.append([token_type, lexeme, line_number])
        line_number += 1
    
    return tokens_with_lines
