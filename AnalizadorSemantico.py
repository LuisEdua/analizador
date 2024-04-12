def formatear_valores(val):
    if val == 'true':
        return True
    if val == 'false':
        return False
    try:
        return int(val)
    except:
        try:
            return float(val)
        except:
            return f'"{val}"'
def analizador_semantico(tokens):
    variables = []
    functions = []
    salida = []
    error = []
    lines = []
    current_line = 1
    current_types = []
    current_values = []
    to_execute = []
    
    for token in tokens:
        tipo, lexema, line = token
        if line != current_line:
            lines.append([current_line, current_types, current_values, to_execute])
            to_execute = []
            current_line = line
            current_types = []
            current_values = []

        to_execute.append([tipo, lexema])
        current_types.append(tipo)
        current_values.append(lexema)
        
    for line, types, values, _ in lines:
        if 'FUNC' == types[0]:
            name_function = values[1]
            parameters = [param for param in values[3:-2] if param != ',']
            num_parameters = len(parameters)
        
            if any(name_function == func['name'] for func in functions):
                line_before = [func['line'] for func in functions if func['name'] == name_function][0]
                return [f"Error semántico: La función '{name_function}' ya ha sido declarada en la línea {line_before}"]
            functions.append({'name': name_function, "part_of": None, "number_parameters": num_parameters, 'line': line, 'operations': [], 'ends': 0})
            variables.append({'name_function': name_function, 'variables': [], "parameters": parameters})
            
        elif 'ID' == types[0]:
            if 'OPERATOR' not in types and 'PARENTESISA' not in types:
                asign_index = types.index('ASSIGN')
                var_list = [v for v in values[:asign_index] if v != ',']
                values_list = [v for v in values[asign_index+1:] if v != ',']
                variables_list = []
                if len(var_list) == len(values_list):
                    variables_function_name = ''
                    for func in reversed(functions):
                        if func['ends'] == 0:
                            variables_function_name = func['name']
                    for i, v in enumerate(var_list):
                        for variable in variables:
                            if variable['name_function'] == variables_function_name:
                                if any(v in varia[0] for varia in variable['variables']) or v in variable['parameters']:
                                    return [f'Error semántico: La variable {v} ya ha sido declarada']
                                else:
                                    variables_list.append([v, values_list[i], line])
                    for variable in variables:
                        if variable['name_function'] == variables_function_name:
                            variable['variables'].extend(variables_list)
                            break
                else:
                    return [f'Error semántico: La cantidad de variables no coincide con la cantidad de valores']
            elif 'PARENTESISA' in types:
                for func in reversed(functions):
                    if func['ends'] == 0:
                        func['operations'].append(['Llamada a la funcion', line])
                        break
            elif 'OPERATOR' in types:
                for func in reversed(functions):
                    if func['ends'] == 0:
                        func['operations'].append(['Operacion matematica', line])
                        break
        elif 'PRINT' in types:
            for func in reversed(functions):
                if func['ends'] == 0:
                    func['operations'].append(['Imprimir', line])
                    break
        elif 'IN' in types:
            for func in reversed(functions):
                if func['ends'] == 0:
                    func['operations'].append(['Ingresar', line])
                    break
        elif 'IF' in types:
            for func in reversed(functions):
                if func['ends'] == 0:
                    name = f'{types[0]} de la linea {line}'
                    part_of = func['name']
                    func['operations'].append(['IF', line])
                    functions.append({'name': name, "part_of": part_of, "number_parameters": 0, 'line': line, 'operations': [], 'ends': 0})
                    break
            var_temp = []
            for var in variables:
                if var['name_function'] == part_of:
                    var_temp = var['variables']
                    break
            variables.append({'name_function': name, 'variables': var_temp, "parameters": 0})
        elif 'ELSE' in types:
            if 'LLAVEC' in types:
                function_name=''
                for func in reversed(functions):
                    if func['ends'] == 0:
                        func['ends'] = line
                        break
                for i in range(len(functions)):
                    if functions[i]['name'] == function_name:
                        functions[i]['ends'] = line
                        break
            for func in reversed(functions):
                if func['ends'] == 0:
                    name = f'{types[1]} de la linea {line}'
                    part_of = func['name']
                    func['operations'].append(['ELSE', line])
                    functions.append({'name': name, "part_of": part_of, "number_parameters": 0, 'line': line, 'operations': [], 'ends': 0})
                    break
            var_temp = []
            for var in variables:
                if var['name_function'] == part_of:
                    var_temp = var['variables']
                    break
            variables.append({'name_function': name, 'variables': var_temp, "parameters": 0})
        elif 'WHILE' in types:
            for func in reversed(functions):
                if func['ends'] == 0:
                    name = f'{types[0]} de la linea {line}'
                    part_of = func['name']
                    func['operations'].append(['WHILE', line])
                    functions.append({'name': name, "part_of": part_of, "number_parameters": 0, 'line': line, 'operations': [], 'ends': 0})
                    break
            var_temp = []
            for var in variables:
                if var['name_function'] == part_of:
                    var_temp = var['variables']
                    break
            variables.append({'name_function': name, 'variables': var_temp, "parameters": 0})
        elif 'LLAVEC' in types:
            function_name=''
            for func in reversed(functions):
                if func['ends'] == 0:
                    func['ends'] = line
                    break
            for i in range(len(functions)):
                if functions[i]['name'] == function_name:
                    functions[i]['ends'] = line
                    break
            
    def get_functions(function_current_name):
        for func in functions:
            if func['name'] == function_current_name:
                for i, operation in enumerate(func['operations']):
                    if operation[0] == 'Imprimir':
                        line = lines[operation[1]-1][3]
                        text = ''
                        for t in line:
                            if t[0] == 'STRING':
                                text += t[1].strip('"')
                            if t[0] == 'ID':
                                exist = False
                                for var in variables:
                                    if var['name_function'] == function_current_name:
                                        for v in var['variables']:
                                            if v[0] == t[1] and v[2] < operation[1]:
                                                text += v[1]
                                                exist = True
                                if not exist:
                                    error.append([f'Error semántico: La variable {t[1]} no ha sido declarada en la linea {operation[1]}'])    
                        salida.append(text)
                    if operation[0] == 'Ingresar':
                        line = lines[operation[1]-1][3]
                        for t in line:
                            if t[0] == 'ID':
                                exist = False
                                for var in variables:
                                    if var['name_function'] == function_current_name:
                                        for v in var['variables']:
                                            if v[0] == t[1] and v[2] < operation[1]:
                                                print(v[0])
                                                v[1] = input(f"Ingresar el valor de la variable ")
                                                exist = True
                                if not exist:
                                    error.append([f'Error semántico: La variable {t[1]} no ha sido declarada en la linea {operation[1]}'])
                    if operation[0] == 'IF':
                        line = lines[operation[1]-1][3]
                        condicion = []
                        for t in line:
                            if t[0] == 'ID':
                                exist = False
                                for var in variables:
                                    if var['name_function'] == function_current_name:
                                        for v in var['variables']:
                                            if v[0] == t[1] and v[2] < operation[1]:
                                                exist = True
                                                condicion.append(str(formatear_valores(v[1])))
                                if not exist:
                                    error.append([f'Error semántico: La variable {t[1]} no ha sido declarada en la linea {operation[1]}'])
                            if t[0] == 'COMPARE':
                                condicion.append(t[1])
                            if t[0] == 'AGGREGATECONDITION':
                                condicion.append(t[1])
                            if t[0] == 'STRING':
                                condicion.append(t[1])
                            if t[0] == 'NUMBER':
                                condicion.append(str(formatear_valores(t[1])))
                            if t[0] == 'BOL':
                                condicion.append(str(formatear_valores(t[1])))
                        text = ' '.join(condicion)
                        if eval(text):
                            get_functions(f'IF de la linea {operation[1]}')
                        else:
                            next_operation = func['operations'][i+1]
                            if next_operation[0] == 'ELSE':
                                get_functions(f'ELSE de la linea {next_operation[1]}')
                    if operation[0] == 'WHILE':
                        line = lines[operation[1]-1][3]
                        condicion = []
                        for t in line:
                            if t[0] == 'ID':
                                exist = False
                                for var in variables:
                                    if var['name_function'] == function_current_name:
                                        for v in var['variables']:
                                            if v[0] == t[1] and v[2] < operation[1]:
                                                exist = True
                                                condicion.append(str(formatear_valores(v[1])))
                                if not exist:
                                    error.append([f'Error semántico: La variable {t[1]} no ha sido declarada en la linea {operation[1]}'])
                            if t[0] == 'COMPARE':
                                condicion.append(t[1])
                            if t[0] == 'AGGREGATECONDITION':
                                condicion.append(t[1])
                            if t[0] == 'STRING':
                                condicion.append(t[1])
                            if t[0] == 'NUMBER':
                                condicion.append(str(formatear_valores(t[1])))
                            if t[0] == 'BOL':
                                condicion.append(str(formatear_valores(t[1])))
                        text = ' '.join(condicion)
                        while eval(text):
                            print("Ciclo")
                            get_functions(f'WHILE de la linea {operation[1]}')                            
                            line = lines[operation[1]-1][3]
                            condicion = []
                            for t in line:
                                if t[0] == 'ID':
                                    exist = False
                                    for var in variables:
                                        if var['name_function'] == function_current_name:
                                            for v in var['variables']:
                                                if v[0] == t[1] and v[2] < operation[1]:
                                                    exist = True
                                                    condicion.append(str(formatear_valores(v[1])))
                                    if not exist:
                                        error.append([f'Error semántico: La variable {t[1]} no ha sido declarada en la linea {operation[1]}'])
                                if t[0] == 'COMPARE':
                                    condicion.append(t[1])
                                if t[0] == 'AGGREGATECONDITION':
                                    condicion.append(t[1])
                                if t[0] == 'STRING':
                                    condicion.append(t[1])
                                if t[0] == 'NUMBER':
                                    condicion.append(str(formatear_valores(t[1])))
                                if t[0] == 'BOL':
                                    condicion.append(str(formatear_valores(t[1])))
                            text = ' '.join(condicion)
                    if operation[0] == 'Llamada a la funcion':
                        line = lines[operation[1]-1][3]
                        function_name = ''
                        num_line = 0
                        parameters = []
                        first = True
                        for t in line:
                            if t[0] == 'ID' and first:
                                exist = False
                                first = False
                                for func in functions:
                                    if func['name'] == t[1]:
                                        num_line = func['line']
                                        function_name = func['name']
                                        exist = True
                                        if func['number_parameters'] == 0:
                                            get_functions(t[1])
                                if not exist:
                                    error.append([f'Error semántico: La variable {t[1]} no ha sido declarada en la linea {operation[1]}'])
                            elif t[0] == 'ID' and not first:
                                exist_variables = False
                                for var in variables:
                                    if var['name_function'] == function_current_name:
                                        for v in var['variables']:
                                            if v[0] == t[1] and v[2] < operation[1]:
                                                exist_variables = True
                                                parameters.append(v[1])
                                if not exist_variables:
                                    error.append([f'Error semántico: La variable {t[1]} no ha sido declarada en la linea {operation[1]}'])
                        for var in variables:
                            if var['name_function'] == function_name:
                                if len(parameters) != len(var['parameters']):
                                    error.append([f'Error semántico: La cantidad de parámetros no coincide con la cantidad de valores'])
                                else:
                                    name_variables = var['parameters']
                                    variables_temp = []
                                    for i, p in enumerate(parameters):
                                        variables_temp.append([name_variables[i], p, line])
                                    var['variables'].extend(variables_temp)
                                    get_functions(function_name)
                    if operation[0] == 'Operacion matematica':
                        line = lines[operation[1]-1][3]
                        operados = []
                        calulate = ''
                        first = True
                        for t in line:
                            if t[0] == 'ID':
                                exist = False
                                for var in variables:
                                    if var['name_function'] == function_current_name:
                                        for v in var['variables']:
                                            if v[0] == t[1] and v[2] < operation[1] and first:
                                                exist = True
                                                first = False
                                                to_calculate = v[0]
                                            elif v[0] == t[1] and v[2] < operation[1] and not first:
                                                exist = True
                                                try:
                                                    operados.append(str(int(v[1])))
                                                except:
                                                    try:
                                                        operados.append(str(float(v[1])))
                                                    except:
                                                        error.append([f'Error semántico: La variable {t[1]} no es numerica'])
                                if not exist:
                                    error.append([f'Error semántico: La variable {t[1]} no ha sido declarada en la linea {operation[1]}'])
                            if t[0] == 'NUMBER':
                                operados.append(str(formatear_valores(t[1])))
                            if t[0] == 'OPERATOR':
                                operados.append(t[1])
                        text = ' '.join(operados)
                        result = eval(text)
                        for var in variables:
                            if var['name_function'] == function_current_name:
                                for v in var['variables']:
                                    if v[0] == to_calculate:
                                        v[1] = str(result)
                                        break
                        
    
    get_functions('main')
    
    if error:
        return error
                        
    return salida
        