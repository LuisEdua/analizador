def asignacion_multiple(cadena, variables):
    # Separar la cadena por el signo '=' y eliminar espacios en blanco
    partes = cadena.split('=')
    variables_asignadas = partes[0].strip().split(',')
    valores = partes[1].strip().split(',')

    # Convertir valores a los tipos adecuados
    for i in range(len(valores)):
        valor = valores[i].strip()
        if valor == 'false':
            valores[i] = False
        elif valor == 'true':
            valores[i] = True
        elif '.' in valor:
            valores[i] = float(valor)
        else:
            valores[i] = int(valor)

    # Verificar y asignar valores a las variables
    for i in range(len(variables_asignadas)):
        if variables_asignadas[i].strip() not in variables:
            return f"Error semántico: La variable '{variables_asignadas[i]}' no ha sido declarada antes de su asignación."

        tipo_valor = 'BOOLEAN' if str(valores[i]).lower() in ['true', 'false'] else 'NUMBER'
        error = verificar_tipos(variables[variables_asignadas[i].strip()][0], tipo_valor, '=',
                                f"Línea asignación múltiple", variables)
        if error:
            return error

        variables[variables_asignadas[i].strip()] = (tipo_valor, valores[i], "Línea asignación múltiple")

    # Imprimir las asignaciones
    for i in range(len(variables_asignadas)):
        print(f"{variables_asignadas[i].strip()} = {valores[i]}")

    return None


def verificar_tipos(op1, op2, operador, linea, variables):
    if op1 == 'ID':
        op1 = variables.get(op1, (None, None, None))[0]
    if op2 == 'ID':
        op2 = variables.get(op2, (None, None, None))[0]

    if op1 != op2:
        return f"Error semántico: Tipos incompatibles en la operación '{operador}' en la línea {linea}"
    return None


def tokenizar_codigo(codigo):
    # Suponiendo que el código se proporciona como una cadena
    tokens = []
    lineas = codigo.split('\n')
    for linea_numero, linea in enumerate(lineas, 1):
        partes = linea.split()
        for parte in partes:
            if '=' in parte and ',' in parte:
                # Es una asignación múltiple
                tokens.append(('MULTIPLE_ASSIGN', parte, linea_numero))
            elif parte in ['func', 'main', 'print', 'println', 'if', 'else', 'while', 'true', 'false']:
                tokens.append((parte.upper(), parte, linea_numero))
            elif parte.isdigit():
                tokens.append(('NUMBER', parte, linea_numero))
            elif parte in ['true', 'false']:
                tokens.append(('BOOLEAN', parte, linea_numero))
            elif parte.startswith('"') and parte.endswith('"'):
                tokens.append(('STRING', parte, linea_numero))
            elif parte in ['+', '-', '*', '/', '=', '==', '<', '>', '<=', '>=', '!=']:
                tokens.append(('OPERATOR', parte, linea_numero))
            elif parte in ['print(', 'println(', 'if(', 'else(', 'while(']:
                tokens.append(('FUNC', parte[:-1], linea_numero))
            elif parte.isalpha():
                tokens.append(('ID', parte, linea_numero))
            elif parte == '=':
                tokens.append(('ASSIGN', parte, linea_numero))
            elif parte == '(':
                tokens.append(('PARENTESIS_A', parte, linea_numero))
            elif parte == ')':
                tokens.append(('PARENTESIS_C', parte, linea_numero))
    return tokens


def analizador_semantico(tokens):
    variables = {}
    funciones = set()
    salida = []

    def asignar_variable(nombre, tipo, valor, linea):
        if nombre in variables:
            return f"Error semántico: La variable '{nombre}' ya ha sido declarada en la línea {variables[nombre][2]}"
        variables[nombre] = (tipo, valor, linea)
        return None

    def verificar_variable(nombre, linea):
        if nombre not in variables:
            return f"Error semántico: La variable '{nombre}' no ha sido declarada antes de su uso en la línea {linea}"
        return None

    for token in tokens:
        tipo, lexema, linea = token

        if tipo == 'FUNC':
            if lexema in funciones:
                return f"Error semántico: La función '{lexema}' ya ha sido declarada en la línea {linea}"
            funciones.add(lexema)

        elif tipo == 'ID':
            asignar_error = asignar_variable(lexema, 'ID', None, linea)
            if asignar_error:
                return asignar_error

        elif tipo == 'NUMBER':
            asignar_error = asignar_variable(f'temp{linea}', 'NUMBER', lexema, linea)
            if asignar_error:
                return asignar_error

        elif tipo == 'BOOLEAN':
            asignar_error = asignar_variable(f'temp{linea}', 'BOOLEAN', lexema, linea)
            if asignar_error:
                return asignar_error

        elif tipo == 'STRING':
            asignar_error = asignar_variable(f'temp{linea}', 'STRING', lexema, linea)
            if asignar_error:
                return asignar_error

        elif tipo == 'ASSIGN':
            nombre = tokens[tokens.index(token) - 1][1]
            valor = tokens[tokens.index(token) + 1][1]
            error = verificar_variable(nombre, linea)
            if error:
                return error
            tipo_valor = 'BOOLEAN' if valor.lower() in ['true', 'false'] else 'NUMBER'
            error = verificar_tipos(variables[nombre][0], tipo_valor, '=', linea, variables)
            if error:
                return error
            variables[nombre] = (tipo_valor, valor, linea)

        elif tipo == 'OPERATOR':
            op1 = tokens[tokens.index(token) - 1][1]
            op2 = tokens[tokens.index(token) + 1][1]
            error = verificar_tipos(op1, op2, lexema, linea, variables)
            if error:
                return error

        elif tipo == 'MULTIPLE_ASSIGN':
            asignacion_error = asignacion_multiple(lexema, variables)
            if asignacion_error:
                return asignacion_error

        elif tipo == 'PRINT':
            valor = tokens[tokens.index(token) + 2][1][1:-1]  # Obtener el valor del string entre comillas
            salida.append(valor)

        elif tipo == 'PRINTVAR':
            nombre = tokens[tokens.index(token) + 1][1]
            valor = variables[nombre][1]
            salida.append(str(valor).lower())  # Convertir el valor booleano a minúsculas

    if salida:
        return " ".join(salida)  # Cambiado para unir con un espacio en lugar de un salto de línea
    else:
        return "Análisis semántico completado sin errores."


#