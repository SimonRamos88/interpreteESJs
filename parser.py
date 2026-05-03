class Parser:

    def __init__(self, gen):
        self._gen = gen
        self._token_actual = next(self._gen, None)
        self._ultima_fila = 1
        self._ultima_col  = 1

    def _es_eof(self) -> bool:
        return self._token_actual is None

    def _token_tipo(self) -> str:
        return self._token_actual.tipo if not self._es_eof() else 'EOF'

    def _avanzar(self):
        if self._token_actual is not None:
            self._ultima_fila = self._token_actual.fila
            self._ultima_col  = self._token_actual.columna
        self._token_actual = next(self._gen, None)

    def _emparejar(self, tipo_esperado: str):
        if self._token_tipo() == tipo_esperado:
            self._avanzar()
        else:
            self._error_sintaxis([tipo_esperado])

    def _lexema_visible(self, tipo: str) -> str:
        _MAPA = {
            'and': '&&',
            'or': '||',
            'nulish': '??',
            'spread': '...',
            'arrow': '=>',
            'not': '!',
            'period': '.',
            'comma': ',',
            'semicolon': ';',
            'colon': ':',
            'ternary': '?',
            'opening_key': '{',
            'closing_key': '}',
            'opening_bra': '[',
            'closing_bra': ']',
            'opening_par': '(',
            'closing_par': ')',
            'increment': '++',
            'decrement': '--',
            'plus_assign': '+=',
            'minus_assign': '-=',
            'times_assign': '*=',
            'div_assign': '/=',
            'mod_assign': '%=',
            'power_assign': '**=',
            'plus': '+',
            'minus': '-',
            'times': '*',
            'div': '/',
            'power': '**',
            'mod': '%',
            'strict_equal': '===',
            'equal': '==',
            'strict_neq': '!==',
            'neq': '!=',
            'leq': '<=',
            'geq': '>=',
            'less': '<',
            'greater': '>',
            'assign': '=',
            'num': 'valor_numerico',
            'str': 'cadena_de_caracteres',
            'id':  'id',
            'EOF': 'EOF',
        }
        return _MAPA.get(tipo, tipo)

    def _error_sintaxis(self, tipos_esperados: list):
        if not self._es_eof():
            fila       = self._token_actual.fila
            col        = self._token_actual.columna
            encontrado = f'"{self._token_actual.lexema}"'
        else:
            fila       = self._ultima_fila
            col        = self._ultima_col + 1
            encontrado = '"final de archivo"'
        esperados_visibles = sorted({self._lexema_visible(t) for t in tipos_esperados})
        esperados_str = ', '.join(f'"{e}"' for e in esperados_visibles)
        raise SyntaxError(
            f'<{fila}:{col}> Error sintactico: se encontro: {encontrado}; se esperaba: {esperados_str}.'
        )

    def _parse_Accesos(self):
        if self._token_tipo() == '.':
            self._emparejar('.')
            self._emparejar('id')
            self._parse_Accesos()
        elif self._token_tipo() == '[':
            self._emparejar('[')
            self._parse_Expresion()
            self._emparejar(']')
            self._parse_Accesos()
        elif self._token_tipo() == '(':
            self._emparejar('(')
            self._parse_Args()
            self._emparejar(')')
            self._parse_Accesos()
        elif self._token_tipo() == '!' or self._token_tipo() == '!=' or self._token_tipo() == '!==' or self._token_tipo() == '%' or self._token_tipo() == '&&' or self._token_tipo() == '(' or self._token_tipo() == ')' or self._token_tipo() == '*' or self._token_tipo() == '**' or self._token_tipo() == '*=' or self._token_tipo() == '+' or self._token_tipo() == '+=' or self._token_tipo() == ',' or self._token_tipo() == '-' or self._token_tipo() == '-=' or self._token_tipo() == '/' or self._token_tipo() == '/=' or self._token_tipo() == ':' or self._token_tipo() == ';' or self._token_tipo() == '<' or self._token_tipo() == '<=' or self._token_tipo() == '=' or self._token_tipo() == '==' or self._token_tipo() == '===' or self._token_tipo() == '>' or self._token_tipo() == '>=' or self._token_tipo() == '?' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == ']' or self._token_tipo() == 'caso' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'mut' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'para' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{' or self._token_tipo() == '||' or self._token_tipo() == '}':
            pass
        else:
            self._error_sintaxis(['!', '!=', '!==', '%', '&&', '(', ')', '*', '**', '*=', '+', '+=', ',', '-', '-=', '.', '/', '/=', ':', ';', '<', '<=', '=', '==', '===', '>', '>=', '?', 'Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', ']', 'caso', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'mut', 'nulo', 'num', 'para', 'porDefecto', 'retornar', 'romper', 'si', 'str', 'var', 'verdadero', '{', '||', '}'])

    def _parse_AccesosOFlecha(self):
        if self._token_tipo() == '=>':
            self._emparejar('=>')
            self._parse_Expresion()
        elif self._token_tipo() == '!' or self._token_tipo() == '!=' or self._token_tipo() == '!==' or self._token_tipo() == '%' or self._token_tipo() == '&&' or self._token_tipo() == '(' or self._token_tipo() == ')' or self._token_tipo() == '*' or self._token_tipo() == '**' or self._token_tipo() == '*=' or self._token_tipo() == '+' or self._token_tipo() == '+=' or self._token_tipo() == ',' or self._token_tipo() == '-' or self._token_tipo() == '-=' or self._token_tipo() == '.' or self._token_tipo() == '/' or self._token_tipo() == '/=' or self._token_tipo() == ':' or self._token_tipo() == ';' or self._token_tipo() == '<' or self._token_tipo() == '<=' or self._token_tipo() == '=' or self._token_tipo() == '==' or self._token_tipo() == '===' or self._token_tipo() == '>' or self._token_tipo() == '>=' or self._token_tipo() == '?' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == ']' or self._token_tipo() == 'caso' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'mut' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'para' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{' or self._token_tipo() == '||' or self._token_tipo() == '}':
            self._parse_Accesos()
        else:
            self._error_sintaxis(['!', '!=', '!==', '%', '&&', '(', ')', '*', '**', '*=', '+', '+=', ',', '-', '-=', '.', '/', '/=', ':', ';', '<', '<=', '=', '==', '===', '=>', '>', '>=', '?', 'Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', ']', 'caso', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'mut', 'nulo', 'num', 'para', 'porDefecto', 'retornar', 'romper', 'si', 'str', 'var', 'verdadero', '{', '||', '}'])

    def _parse_Aditiva(self):
        if self._token_tipo() == '!' or self._token_tipo() == '(' or self._token_tipo() == '+' or self._token_tipo() == '-' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{':
            self._parse_Multiplicativa()
            self._parse_Aditiva_prima()
        else:
            self._error_sintaxis(['!', '(', '+', '-', 'Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', 'consola', 'crear', 'falso', 'id', 'indefinido', 'nulo', 'num', 'str', 'verdadero', '{'])

    def _parse_Aditiva_prima(self):
        if self._token_tipo() == '+':
            self._emparejar('+')
            self._parse_Multiplicativa()
            self._parse_Aditiva_prima()
        elif self._token_tipo() == '-':
            self._emparejar('-')
            self._parse_Multiplicativa()
            self._parse_Aditiva_prima()
        elif self._token_tipo() == '!' or self._token_tipo() == '!=' or self._token_tipo() == '!==' or self._token_tipo() == '%' or self._token_tipo() == '&&' or self._token_tipo() == '(' or self._token_tipo() == ')' or self._token_tipo() == '*' or self._token_tipo() == '**' or self._token_tipo() == '*=' or self._token_tipo() == '+' or self._token_tipo() == '+=' or self._token_tipo() == ',' or self._token_tipo() == '-' or self._token_tipo() == '-=' or self._token_tipo() == '/' or self._token_tipo() == '/=' or self._token_tipo() == ':' or self._token_tipo() == ';' or self._token_tipo() == '<' or self._token_tipo() == '<=' or self._token_tipo() == '=' or self._token_tipo() == '==' or self._token_tipo() == '===' or self._token_tipo() == '>' or self._token_tipo() == '>=' or self._token_tipo() == '?' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == ']' or self._token_tipo() == 'caso' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'mut' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'para' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{' or self._token_tipo() == '||' or self._token_tipo() == '}':
            pass
        else:
            self._error_sintaxis(['!', '!=', '!==', '%', '&&', '(', ')', '*', '**', '*=', '+', '+=', ',', '-', '-=', '/', '/=', ':', ';', '<', '<=', '=', '==', '===', '>', '>=', '?', 'Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', ']', 'caso', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'mut', 'nulo', 'num', 'para', 'porDefecto', 'retornar', 'romper', 'si', 'str', 'var', 'verdadero', '{', '||', '}'])

    def _parse_Args(self):
        if self._token_tipo() == '!' or self._token_tipo() == '(' or self._token_tipo() == '+' or self._token_tipo() == '-' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{':
            self._parse_Expresion()
            self._parse_MasArgs()
        elif self._token_tipo() == ')' or self._token_tipo() == ']':
            pass
        else:
            self._error_sintaxis(['!', '(', ')', '+', '-', 'Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', ']', 'consola', 'crear', 'falso', 'id', 'indefinido', 'nulo', 'num', 'str', 'verdadero', '{'])

    def _parse_Asignacion(self):
        if self._token_tipo() == '!' or self._token_tipo() == '(' or self._token_tipo() == '+' or self._token_tipo() == '-' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{':
            self._parse_Ternaria()
            self._parse_OpcAsig()
        else:
            self._error_sintaxis(['!', '(', '+', '-', 'Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', 'consola', 'crear', 'falso', 'id', 'indefinido', 'nulo', 'num', 'str', 'verdadero', '{'])

    def _parse_Bloque(self):
        if self._token_tipo() == '{':
            self._emparejar('{')
            self._parse_ListaSentencias()
            self._emparejar('}')
        else:
            self._error_sintaxis(['{'])

    def _parse_Declaracion(self):
        if self._token_tipo() == 'var':
            self._emparejar('var')
            self._emparejar('id')
            self._parse_OpcAsignacion()
            self._parse_MasVariables()
            self._parse_OpcPuntoComa()
        elif self._token_tipo() == 'mut':
            self._emparejar('mut')
            self._emparejar('id')
            self._parse_OpcAsignacion()
            self._parse_MasVariables()
            self._parse_OpcPuntoComa()
        elif self._token_tipo() == 'const':
            self._emparejar('const')
            self._emparejar('id')
            self._emparejar('=')
            self._parse_Expresion()
            self._parse_MasConstantes()
            self._parse_OpcPuntoComa()
        else:
            self._error_sintaxis(['const', 'mut', 'var'])

    def _parse_DefinicionFuncion(self):
        if self._token_tipo() == 'funcion':
            self._emparejar('funcion')
            self._emparejar('id')
            self._emparejar('(')
            self._parse_Params()
            self._emparejar(')')
            self._parse_Bloque()
        else:
            self._error_sintaxis(['funcion'])

    def _parse_EstructuraControl(self):
        if self._token_tipo() == 'si':
            self._emparejar('si')
            self._emparejar('(')
            self._parse_Expresion()
            self._emparejar(')')
            self._parse_Bloque()
            self._parse_OpcSino()
        elif self._token_tipo() == 'mientras':
            self._emparejar('mientras')
            self._emparejar('(')
            self._parse_Expresion()
            self._emparejar(')')
            self._parse_Bloque()
        elif self._token_tipo() == 'hacer':
            self._emparejar('hacer')
            self._parse_Bloque()
            self._emparejar('mientras')
            self._emparejar('(')
            self._parse_Expresion()
            self._emparejar(')')
            self._parse_OpcPuntoComa()
        elif self._token_tipo() == 'para':
            self._emparejar('para')
            self._emparejar('(')
            self._parse_OpcParaInit()
            self._emparejar(';')
            self._parse_OpcExp()
            self._emparejar(';')
            self._parse_OpcExp()
            self._emparejar(')')
            self._parse_Bloque()
        elif self._token_tipo() == 'elegir':
            self._emparejar('elegir')
            self._emparejar('(')
            self._parse_Expresion()
            self._emparejar(')')
            self._emparejar('{')
            self._parse_ListaCasos()
            self._emparejar('}')
        else:
            self._error_sintaxis(['elegir', 'hacer', 'mientras', 'para', 'si'])

    def _parse_Expresion(self):
        if self._token_tipo() == '!' or self._token_tipo() == '(' or self._token_tipo() == '+' or self._token_tipo() == '-' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{':
            self._parse_Asignacion()
        else:
            self._error_sintaxis(['!', '(', '+', '-', 'Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', 'consola', 'crear', 'falso', 'id', 'indefinido', 'nulo', 'num', 'str', 'verdadero', '{'])

    def _parse_Igualdad(self):
        if self._token_tipo() == '!' or self._token_tipo() == '(' or self._token_tipo() == '+' or self._token_tipo() == '-' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{':
            self._parse_Relacional()
            self._parse_Igualdad_prima()
        else:
            self._error_sintaxis(['!', '(', '+', '-', 'Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', 'consola', 'crear', 'falso', 'id', 'indefinido', 'nulo', 'num', 'str', 'verdadero', '{'])

    def _parse_Igualdad_prima(self):
        if self._token_tipo() == '!=' or self._token_tipo() == '!==' or self._token_tipo() == '==' or self._token_tipo() == '===':
            self._parse_OpIgual()
            self._parse_Relacional()
            self._parse_Igualdad_prima()
        elif self._token_tipo() == '!' or self._token_tipo() == '!=' or self._token_tipo() == '!==' or self._token_tipo() == '%' or self._token_tipo() == '&&' or self._token_tipo() == '(' or self._token_tipo() == ')' or self._token_tipo() == '*' or self._token_tipo() == '**' or self._token_tipo() == '*=' or self._token_tipo() == '+' or self._token_tipo() == '+=' or self._token_tipo() == ',' or self._token_tipo() == '-' or self._token_tipo() == '-=' or self._token_tipo() == '/' or self._token_tipo() == '/=' or self._token_tipo() == ':' or self._token_tipo() == ';' or self._token_tipo() == '<' or self._token_tipo() == '<=' or self._token_tipo() == '=' or self._token_tipo() == '==' or self._token_tipo() == '===' or self._token_tipo() == '>' or self._token_tipo() == '>=' or self._token_tipo() == '?' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == ']' or self._token_tipo() == 'caso' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'mut' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'para' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{' or self._token_tipo() == '||' or self._token_tipo() == '}':
            pass
        else:
            self._error_sintaxis(['!', '!=', '!==', '%', '&&', '(', ')', '*', '**', '*=', '+', '+=', ',', '-', '-=', '/', '/=', ':', ';', '<', '<=', '=', '==', '===', '>', '>=', '?', 'Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', ']', 'caso', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'mut', 'nulo', 'num', 'para', 'porDefecto', 'retornar', 'romper', 'si', 'str', 'var', 'verdadero', '{', '||', '}'])

    def _parse_Intentar(self):
        if self._token_tipo() == 'intentar':
            self._emparejar('intentar')
            self._parse_Bloque()
            self._emparejar('capturar')
            self._emparejar('(')
            self._emparejar('id')
            self._emparejar(')')
            self._parse_Bloque()
        else:
            self._error_sintaxis(['intentar'])

    def _parse_ListaCasos(self):
        if self._token_tipo() == 'caso':
            self._emparejar('caso')
            self._parse_Expresion()
            self._emparejar(':')
            self._parse_ListaSentencias()
            self._parse_ListaCasos()
        elif self._token_tipo() == 'porDefecto':
            self._emparejar('porDefecto')
            self._emparejar(':')
            self._parse_ListaSentencias()
        elif self._token_tipo() == '}':
            pass
        else:
            self._error_sintaxis(['caso', 'porDefecto', '}'])

    def _parse_ListaPropiedades(self):
        if self._token_tipo() == 'id':
            self._parse_Propiedad()
            self._parse_MasPropiedades()
        elif self._token_tipo() == '}':
            pass
        else:
            self._error_sintaxis(['id', '}'])

    def _parse_ListaSentencias(self):
        if self._token_tipo() == '!' or self._token_tipo() == '(' or self._token_tipo() == '+' or self._token_tipo() == '-' or self._token_tipo() == ';' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'mut' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'para' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{':
            self._parse_Sentencia()
            self._parse_ListaSentencias()
        elif self._token_tipo() == 'EOF' or self._token_tipo() == 'caso' or self._token_tipo() == 'porDefecto' or self._token_tipo() == '}':
            pass
        else:
            self._error_sintaxis(['!', '(', '+', '-', ';', 'Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', 'caso', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'mut', 'nulo', 'num', 'para', 'porDefecto', 'retornar', 'romper', 'si', 'str', 'var', 'verdadero', '{', '}'])

    def _parse_Literal(self):
        if self._token_tipo() == 'num':
            self._emparejar('num')
        elif self._token_tipo() == 'str':
            self._emparejar('str')
        elif self._token_tipo() == 'verdadero':
            self._emparejar('verdadero')
        elif self._token_tipo() == 'falso':
            self._emparejar('falso')
        elif self._token_tipo() == 'nulo':
            self._emparejar('nulo')
        elif self._token_tipo() == 'indefinido':
            self._emparejar('indefinido')
        elif self._token_tipo() == 'NuN':
            self._emparejar('NuN')
        elif self._token_tipo() == 'Infinito':
            self._emparejar('Infinito')
        elif self._token_tipo() == 'Numero':
            self._emparejar('Numero')
        elif self._token_tipo() == 'Mate':
            self._emparejar('Mate')
        elif self._token_tipo() == 'Matriz':
            self._emparejar('Matriz')
        elif self._token_tipo() == 'Arreglo':
            self._emparejar('Arreglo')
        elif self._token_tipo() == 'Booleano':
            self._emparejar('Booleano')
        elif self._token_tipo() == 'Cadena':
            self._emparejar('Cadena')
        elif self._token_tipo() == '[':
            self._parse_LiteralArr()
        elif self._token_tipo() == '{':
            self._parse_LiteralObj()
        elif self._token_tipo() == 'crear':
            self._parse_LlamadaCrear()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', 'crear', 'falso', 'indefinido', 'nulo', 'num', 'str', 'verdadero', '{'])

    def _parse_LiteralArr(self):
        if self._token_tipo() == '[':
            self._emparejar('[')
            self._parse_Args()
            self._emparejar(']')
        else:
            self._error_sintaxis(['['])

    def _parse_LiteralObj(self):
        if self._token_tipo() == '{':
            self._emparejar('{')
            self._parse_ListaPropiedades()
            self._emparejar('}')
        else:
            self._error_sintaxis(['{'])

    def _parse_LlamadaCrear(self):
        if self._token_tipo() == 'crear':
            self._emparejar('crear')
            self._parse_TipoCreable()
        else:
            self._error_sintaxis(['crear'])

    def _parse_LogicaAnd(self):
        if self._token_tipo() == '!' or self._token_tipo() == '(' or self._token_tipo() == '+' or self._token_tipo() == '-' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{':
            self._parse_Igualdad()
            self._parse_LogicaAnd_prima()
        else:
            self._error_sintaxis(['!', '(', '+', '-', 'Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', 'consola', 'crear', 'falso', 'id', 'indefinido', 'nulo', 'num', 'str', 'verdadero', '{'])

    def _parse_LogicaAnd_prima(self):
        if self._token_tipo() == '&&':
            self._emparejar('&&')
            self._parse_Igualdad()
            self._parse_LogicaAnd_prima()
        elif self._token_tipo() == '!' or self._token_tipo() == '!=' or self._token_tipo() == '!==' or self._token_tipo() == '%' or self._token_tipo() == '&&' or self._token_tipo() == '(' or self._token_tipo() == ')' or self._token_tipo() == '*' or self._token_tipo() == '**' or self._token_tipo() == '*=' or self._token_tipo() == '+' or self._token_tipo() == '+=' or self._token_tipo() == ',' or self._token_tipo() == '-' or self._token_tipo() == '-=' or self._token_tipo() == '/' or self._token_tipo() == '/=' or self._token_tipo() == ':' or self._token_tipo() == ';' or self._token_tipo() == '<' or self._token_tipo() == '<=' or self._token_tipo() == '=' or self._token_tipo() == '==' or self._token_tipo() == '===' or self._token_tipo() == '>' or self._token_tipo() == '>=' or self._token_tipo() == '?' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == ']' or self._token_tipo() == 'caso' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'mut' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'para' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{' or self._token_tipo() == '||' or self._token_tipo() == '}':
            pass
        else:
            self._error_sintaxis(['!', '!=', '!==', '%', '&&', '(', ')', '*', '**', '*=', '+', '+=', ',', '-', '-=', '/', '/=', ':', ';', '<', '<=', '=', '==', '===', '>', '>=', '?', 'Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', ']', 'caso', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'mut', 'nulo', 'num', 'para', 'porDefecto', 'retornar', 'romper', 'si', 'str', 'var', 'verdadero', '{', '||', '}'])

    def _parse_LogicaOr(self):
        if self._token_tipo() == '!' or self._token_tipo() == '(' or self._token_tipo() == '+' or self._token_tipo() == '-' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{':
            self._parse_LogicaAnd()
            self._parse_LogicaOr_prima()
        else:
            self._error_sintaxis(['!', '(', '+', '-', 'Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', 'consola', 'crear', 'falso', 'id', 'indefinido', 'nulo', 'num', 'str', 'verdadero', '{'])

    def _parse_LogicaOr_prima(self):
        if self._token_tipo() == '||':
            self._emparejar('||')
            self._parse_LogicaAnd()
            self._parse_LogicaOr_prima()
        elif self._token_tipo() == '!' or self._token_tipo() == '!=' or self._token_tipo() == '!==' or self._token_tipo() == '%' or self._token_tipo() == '&&' or self._token_tipo() == '(' or self._token_tipo() == ')' or self._token_tipo() == '*' or self._token_tipo() == '**' or self._token_tipo() == '*=' or self._token_tipo() == '+' or self._token_tipo() == '+=' or self._token_tipo() == ',' or self._token_tipo() == '-' or self._token_tipo() == '-=' or self._token_tipo() == '/' or self._token_tipo() == '/=' or self._token_tipo() == ':' or self._token_tipo() == ';' or self._token_tipo() == '<' or self._token_tipo() == '<=' or self._token_tipo() == '=' or self._token_tipo() == '==' or self._token_tipo() == '===' or self._token_tipo() == '>' or self._token_tipo() == '>=' or self._token_tipo() == '?' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == ']' or self._token_tipo() == 'caso' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'mut' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'para' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{' or self._token_tipo() == '||' or self._token_tipo() == '}':
            pass
        else:
            self._error_sintaxis(['!', '!=', '!==', '%', '&&', '(', ')', '*', '**', '*=', '+', '+=', ',', '-', '-=', '/', '/=', ':', ';', '<', '<=', '=', '==', '===', '>', '>=', '?', 'Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', ']', 'caso', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'mut', 'nulo', 'num', 'para', 'porDefecto', 'retornar', 'romper', 'si', 'str', 'var', 'verdadero', '{', '||', '}'])

    def _parse_MasArgs(self):
        if self._token_tipo() == ',':
            self._emparejar(',')
            self._parse_Expresion()
            self._parse_MasArgs()
        elif self._token_tipo() == ')' or self._token_tipo() == ']':
            pass
        else:
            self._error_sintaxis([')', ',', ']'])

    def _parse_MasConstantes(self):
        if self._token_tipo() == ',':
            self._emparejar(',')
            self._emparejar('id')
            self._emparejar('=')
            self._parse_Expresion()
            self._parse_MasConstantes()
        elif self._token_tipo() == '!' or self._token_tipo() == '(' or self._token_tipo() == '+' or self._token_tipo() == '-' or self._token_tipo() == ';' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == 'caso' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'mut' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'para' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{' or self._token_tipo() == '}':
            pass
        else:
            self._error_sintaxis(['!', '(', '+', ',', '-', ';', 'Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', 'caso', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'mut', 'nulo', 'num', 'para', 'porDefecto', 'retornar', 'romper', 'si', 'str', 'var', 'verdadero', '{', '}'])

    def _parse_MasParams(self):
        if self._token_tipo() == ',':
            self._emparejar(',')
            self._emparejar('id')
            self._parse_MasParams()
        elif self._token_tipo() == ')':
            pass
        else:
            self._error_sintaxis([')', ','])

    def _parse_MasPropiedades(self):
        if self._token_tipo() == ',':
            self._emparejar(',')
            self._parse_Propiedad()
            self._parse_MasPropiedades()
        elif self._token_tipo() == '}':
            pass
        else:
            self._error_sintaxis([',', '}'])

    def _parse_MasVariables(self):
        if self._token_tipo() == ',':
            self._emparejar(',')
            self._emparejar('id')
            self._parse_OpcAsignacion()
            self._parse_MasVariables()
        elif self._token_tipo() == '!' or self._token_tipo() == '(' or self._token_tipo() == '+' or self._token_tipo() == '-' or self._token_tipo() == ';' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == 'caso' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'mut' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'para' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{' or self._token_tipo() == '}':
            pass
        else:
            self._error_sintaxis(['!', '(', '+', ',', '-', ';', 'Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', 'caso', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'mut', 'nulo', 'num', 'para', 'porDefecto', 'retornar', 'romper', 'si', 'str', 'var', 'verdadero', '{', '}'])

    def _parse_Multiplicativa(self):
        if self._token_tipo() == '!' or self._token_tipo() == '(' or self._token_tipo() == '+' or self._token_tipo() == '-' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{':
            self._parse_Potencia()
            self._parse_Multiplicativa_prima()
        else:
            self._error_sintaxis(['!', '(', '+', '-', 'Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', 'consola', 'crear', 'falso', 'id', 'indefinido', 'nulo', 'num', 'str', 'verdadero', '{'])

    def _parse_Multiplicativa_prima(self):
        if self._token_tipo() == '*':
            self._emparejar('*')
            self._parse_Potencia()
            self._parse_Multiplicativa_prima()
        elif self._token_tipo() == '/':
            self._emparejar('/')
            self._parse_Potencia()
            self._parse_Multiplicativa_prima()
        elif self._token_tipo() == '%':
            self._emparejar('%')
            self._parse_Potencia()
            self._parse_Multiplicativa_prima()
        elif self._token_tipo() == '!' or self._token_tipo() == '!=' or self._token_tipo() == '!==' or self._token_tipo() == '%' or self._token_tipo() == '&&' or self._token_tipo() == '(' or self._token_tipo() == ')' or self._token_tipo() == '*' or self._token_tipo() == '**' or self._token_tipo() == '*=' or self._token_tipo() == '+' or self._token_tipo() == '+=' or self._token_tipo() == ',' or self._token_tipo() == '-' or self._token_tipo() == '-=' or self._token_tipo() == '/' or self._token_tipo() == '/=' or self._token_tipo() == ':' or self._token_tipo() == ';' or self._token_tipo() == '<' or self._token_tipo() == '<=' or self._token_tipo() == '=' or self._token_tipo() == '==' or self._token_tipo() == '===' or self._token_tipo() == '>' or self._token_tipo() == '>=' or self._token_tipo() == '?' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == ']' or self._token_tipo() == 'caso' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'mut' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'para' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{' or self._token_tipo() == '||' or self._token_tipo() == '}':
            pass
        else:
            self._error_sintaxis(['!', '!=', '!==', '%', '&&', '(', ')', '*', '**', '*=', '+', '+=', ',', '-', '-=', '/', '/=', ':', ';', '<', '<=', '=', '==', '===', '>', '>=', '?', 'Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', ']', 'caso', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'mut', 'nulo', 'num', 'para', 'porDefecto', 'retornar', 'romper', 'si', 'str', 'var', 'verdadero', '{', '||', '}'])

    def _parse_OpIgual(self):
        if self._token_tipo() == '==':
            self._emparejar('==')
        elif self._token_tipo() == '===':
            self._emparejar('===')
        elif self._token_tipo() == '!=':
            self._emparejar('!=')
        elif self._token_tipo() == '!==':
            self._emparejar('!==')
        else:
            self._error_sintaxis(['!=', '!==', '==', '==='])

    def _parse_OpRel(self):
        if self._token_tipo() == '<':
            self._emparejar('<')
        elif self._token_tipo() == '>':
            self._emparejar('>')
        elif self._token_tipo() == '<=':
            self._emparejar('<=')
        elif self._token_tipo() == '>=':
            self._emparejar('>=')
        else:
            self._error_sintaxis(['<', '<=', '>', '>='])

    def _parse_OpcAsig(self):
        if self._token_tipo() == '=':
            self._emparejar('=')
            self._parse_Asignacion()
        elif self._token_tipo() == '+=':
            self._emparejar('+=')
            self._parse_Asignacion()
        elif self._token_tipo() == '-=':
            self._emparejar('-=')
            self._parse_Asignacion()
        elif self._token_tipo() == '*=':
            self._emparejar('*=')
            self._parse_Asignacion()
        elif self._token_tipo() == '/=':
            self._emparejar('/=')
            self._parse_Asignacion()
        elif self._token_tipo() == '!' or self._token_tipo() == '!=' or self._token_tipo() == '!==' or self._token_tipo() == '%' or self._token_tipo() == '&&' or self._token_tipo() == '(' or self._token_tipo() == ')' or self._token_tipo() == '*' or self._token_tipo() == '**' or self._token_tipo() == '*=' or self._token_tipo() == '+' or self._token_tipo() == '+=' or self._token_tipo() == ',' or self._token_tipo() == '-' or self._token_tipo() == '-=' or self._token_tipo() == '/' or self._token_tipo() == '/=' or self._token_tipo() == ':' or self._token_tipo() == ';' or self._token_tipo() == '<' or self._token_tipo() == '<=' or self._token_tipo() == '=' or self._token_tipo() == '==' or self._token_tipo() == '===' or self._token_tipo() == '>' or self._token_tipo() == '>=' or self._token_tipo() == '?' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == ']' or self._token_tipo() == 'caso' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'mut' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'para' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{' or self._token_tipo() == '||' or self._token_tipo() == '}':
            pass
        else:
            self._error_sintaxis(['!', '!=', '!==', '%', '&&', '(', ')', '*', '**', '*=', '+', '+=', ',', '-', '-=', '/', '/=', ':', ';', '<', '<=', '=', '==', '===', '>', '>=', '?', 'Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', ']', 'caso', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'mut', 'nulo', 'num', 'para', 'porDefecto', 'retornar', 'romper', 'si', 'str', 'var', 'verdadero', '{', '||', '}'])

    def _parse_OpcAsignacion(self):
        if self._token_tipo() == '=':
            self._emparejar('=')
            self._parse_Expresion()
        elif self._token_tipo() == '!' or self._token_tipo() == '(' or self._token_tipo() == '+' or self._token_tipo() == ',' or self._token_tipo() == '-' or self._token_tipo() == ';' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == 'caso' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'mut' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'para' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{' or self._token_tipo() == '}':
            pass
        else:
            self._error_sintaxis(['!', '(', '+', ',', '-', ';', '=', 'Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', 'caso', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'mut', 'nulo', 'num', 'para', 'porDefecto', 'retornar', 'romper', 'si', 'str', 'var', 'verdadero', '{', '}'])

    def _parse_OpcExp(self):
        if self._token_tipo() == '!' or self._token_tipo() == '(' or self._token_tipo() == '+' or self._token_tipo() == '-' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{':
            self._parse_Expresion()
        elif self._token_tipo() == '!' or self._token_tipo() == '(' or self._token_tipo() == ')' or self._token_tipo() == '+' or self._token_tipo() == '-' or self._token_tipo() == ';' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == 'caso' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'mut' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'para' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{' or self._token_tipo() == '}':
            pass
        else:
            self._error_sintaxis(['!', '(', ')', '+', '-', ';', 'Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', 'caso', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'mut', 'nulo', 'num', 'para', 'porDefecto', 'retornar', 'romper', 'si', 'str', 'var', 'verdadero', '{', '}'])

    def _parse_OpcParaInit(self):
        if self._token_tipo() == 'const' or self._token_tipo() == 'mut' or self._token_tipo() == 'var':
            self._parse_Declaracion()
        elif self._token_tipo() == '!' or self._token_tipo() == '(' or self._token_tipo() == '+' or self._token_tipo() == '-' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{':
            self._parse_Expresion()
        elif self._token_tipo() == ';':
            pass
        else:
            self._error_sintaxis(['!', '(', '+', '-', ';', 'Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', 'consola', 'const', 'crear', 'falso', 'id', 'indefinido', 'mut', 'nulo', 'num', 'str', 'var', 'verdadero', '{'])

    def _parse_OpcProp(self):
        if self._token_tipo() == ':':
            self._emparejar(':')
            self._parse_Expresion()
        elif self._token_tipo() == '(':
            self._emparejar('(')
            self._parse_Params()
            self._emparejar(')')
            self._parse_Bloque()
        else:
            self._error_sintaxis(['(', ':'])

    def _parse_OpcPuntoComa(self):
        if self._token_tipo() == ';':
            self._emparejar(';')
        elif self._token_tipo() == '!' or self._token_tipo() == '(' or self._token_tipo() == '+' or self._token_tipo() == '-' or self._token_tipo() == ';' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == 'caso' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'mut' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'para' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{' or self._token_tipo() == '}':
            pass
        else:
            self._error_sintaxis(['!', '(', '+', '-', ';', 'Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', 'caso', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'mut', 'nulo', 'num', 'para', 'porDefecto', 'retornar', 'romper', 'si', 'str', 'var', 'verdadero', '{', '}'])

    def _parse_OpcSino(self):
        if self._token_tipo() == 'sino':
            self._emparejar('sino')
            self._parse_Bloque()
        elif self._token_tipo() == 'sino':
            self._emparejar('sino')
            self._emparejar('si')
            self._emparejar('(')
            self._parse_Expresion()
            self._emparejar(')')
            self._parse_Bloque()
            self._parse_OpcSino()
        elif self._token_tipo() == '!' or self._token_tipo() == '(' or self._token_tipo() == '+' or self._token_tipo() == '-' or self._token_tipo() == ';' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == 'caso' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'mut' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'para' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{' or self._token_tipo() == '}':
            pass
        else:
            self._error_sintaxis(['!', '(', '+', '-', ';', 'Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', 'caso', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'mut', 'nulo', 'num', 'para', 'porDefecto', 'retornar', 'romper', 'si', 'sino', 'str', 'var', 'verdadero', '{', '}'])

    def _parse_OpcTern(self):
        if self._token_tipo() == '?':
            self._emparejar('?')
            self._parse_Expresion()
            self._emparejar(':')
            self._parse_Ternaria()
        elif self._token_tipo() == '!' or self._token_tipo() == '!=' or self._token_tipo() == '!==' or self._token_tipo() == '%' or self._token_tipo() == '&&' or self._token_tipo() == '(' or self._token_tipo() == ')' or self._token_tipo() == '*' or self._token_tipo() == '**' or self._token_tipo() == '*=' or self._token_tipo() == '+' or self._token_tipo() == '+=' or self._token_tipo() == ',' or self._token_tipo() == '-' or self._token_tipo() == '-=' or self._token_tipo() == '/' or self._token_tipo() == '/=' or self._token_tipo() == ':' or self._token_tipo() == ';' or self._token_tipo() == '<' or self._token_tipo() == '<=' or self._token_tipo() == '=' or self._token_tipo() == '==' or self._token_tipo() == '===' or self._token_tipo() == '>' or self._token_tipo() == '>=' or self._token_tipo() == '?' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == ']' or self._token_tipo() == 'caso' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'mut' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'para' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{' or self._token_tipo() == '||' or self._token_tipo() == '}':
            pass
        else:
            self._error_sintaxis(['!', '!=', '!==', '%', '&&', '(', ')', '*', '**', '*=', '+', '+=', ',', '-', '-=', '/', '/=', ':', ';', '<', '<=', '=', '==', '===', '>', '>=', '?', 'Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', ']', 'caso', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'mut', 'nulo', 'num', 'para', 'porDefecto', 'retornar', 'romper', 'si', 'str', 'var', 'verdadero', '{', '||', '}'])

    def _parse_Params(self):
        if self._token_tipo() == 'id':
            self._emparejar('id')
            self._parse_MasParams()
        elif self._token_tipo() == ')':
            pass
        else:
            self._error_sintaxis([')', 'id'])

    def _parse_Potencia(self):
        if self._token_tipo() == '!' or self._token_tipo() == '(' or self._token_tipo() == '+' or self._token_tipo() == '-' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{':
            self._parse_Unaria()
            self._parse_Potencia_prima()
        else:
            self._error_sintaxis(['!', '(', '+', '-', 'Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', 'consola', 'crear', 'falso', 'id', 'indefinido', 'nulo', 'num', 'str', 'verdadero', '{'])

    def _parse_Potencia_prima(self):
        if self._token_tipo() == '**':
            self._emparejar('**')
            self._parse_Unaria()
            self._parse_Potencia_prima()
        elif self._token_tipo() == '!' or self._token_tipo() == '!=' or self._token_tipo() == '!==' or self._token_tipo() == '%' or self._token_tipo() == '&&' or self._token_tipo() == '(' or self._token_tipo() == ')' or self._token_tipo() == '*' or self._token_tipo() == '**' or self._token_tipo() == '*=' or self._token_tipo() == '+' or self._token_tipo() == '+=' or self._token_tipo() == ',' or self._token_tipo() == '-' or self._token_tipo() == '-=' or self._token_tipo() == '/' or self._token_tipo() == '/=' or self._token_tipo() == ':' or self._token_tipo() == ';' or self._token_tipo() == '<' or self._token_tipo() == '<=' or self._token_tipo() == '=' or self._token_tipo() == '==' or self._token_tipo() == '===' or self._token_tipo() == '>' or self._token_tipo() == '>=' or self._token_tipo() == '?' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == ']' or self._token_tipo() == 'caso' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'mut' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'para' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{' or self._token_tipo() == '||' or self._token_tipo() == '}':
            pass
        else:
            self._error_sintaxis(['!', '!=', '!==', '%', '&&', '(', ')', '*', '**', '*=', '+', '+=', ',', '-', '-=', '/', '/=', ':', ';', '<', '<=', '=', '==', '===', '>', '>=', '?', 'Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', ']', 'caso', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'mut', 'nulo', 'num', 'para', 'porDefecto', 'retornar', 'romper', 'si', 'str', 'var', 'verdadero', '{', '||', '}'])

    def _parse_Primaria(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{':
            self._parse_Literal()
            self._parse_Accesos()
        elif self._token_tipo() == 'id':
            self._emparejar('id')
            self._parse_Accesos()
        elif self._token_tipo() == 'consola':
            self._emparejar('consola')
            self._parse_Accesos()
        elif self._token_tipo() == '(':
            self._emparejar('(')
            self._parse_Expresion()
            self._emparejar(')')
            self._parse_AccesosOFlecha()
        else:
            self._error_sintaxis(['(', 'Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', 'consola', 'crear', 'falso', 'id', 'indefinido', 'nulo', 'num', 'str', 'verdadero', '{'])

    def _parse_Programa(self):
        if self._token_tipo() == '!' or self._token_tipo() == '(' or self._token_tipo() == '+' or self._token_tipo() == '-' or self._token_tipo() == ';' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'mut' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'para' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{':
            self._parse_ListaSentencias()
        else:
            self._error_sintaxis(['!', '(', '+', '-', ';', 'Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'mut', 'nulo', 'num', 'para', 'retornar', 'romper', 'si', 'str', 'var', 'verdadero', '{'])

    def _parse_Propiedad(self):
        if self._token_tipo() == 'id':
            self._emparejar('id')
            self._parse_OpcProp()
        else:
            self._error_sintaxis(['id'])

    def _parse_Relacional(self):
        if self._token_tipo() == '!' or self._token_tipo() == '(' or self._token_tipo() == '+' or self._token_tipo() == '-' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{':
            self._parse_Aditiva()
            self._parse_Relacional_prima()
        else:
            self._error_sintaxis(['!', '(', '+', '-', 'Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', 'consola', 'crear', 'falso', 'id', 'indefinido', 'nulo', 'num', 'str', 'verdadero', '{'])

    def _parse_Relacional_prima(self):
        if self._token_tipo() == '<' or self._token_tipo() == '<=' or self._token_tipo() == '>' or self._token_tipo() == '>=':
            self._parse_OpRel()
            self._parse_Aditiva()
            self._parse_Relacional_prima()
        elif self._token_tipo() == '!' or self._token_tipo() == '!=' or self._token_tipo() == '!==' or self._token_tipo() == '%' or self._token_tipo() == '&&' or self._token_tipo() == '(' or self._token_tipo() == ')' or self._token_tipo() == '*' or self._token_tipo() == '**' or self._token_tipo() == '*=' or self._token_tipo() == '+' or self._token_tipo() == '+=' or self._token_tipo() == ',' or self._token_tipo() == '-' or self._token_tipo() == '-=' or self._token_tipo() == '/' or self._token_tipo() == '/=' or self._token_tipo() == ':' or self._token_tipo() == ';' or self._token_tipo() == '<' or self._token_tipo() == '<=' or self._token_tipo() == '=' or self._token_tipo() == '==' or self._token_tipo() == '===' or self._token_tipo() == '>' or self._token_tipo() == '>=' or self._token_tipo() == '?' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == ']' or self._token_tipo() == 'caso' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'mut' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'para' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{' or self._token_tipo() == '||' or self._token_tipo() == '}':
            pass
        else:
            self._error_sintaxis(['!', '!=', '!==', '%', '&&', '(', ')', '*', '**', '*=', '+', '+=', ',', '-', '-=', '/', '/=', ':', ';', '<', '<=', '=', '==', '===', '>', '>=', '?', 'Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', ']', 'caso', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'mut', 'nulo', 'num', 'para', 'porDefecto', 'retornar', 'romper', 'si', 'str', 'var', 'verdadero', '{', '||', '}'])

    def _parse_Retorno(self):
        if self._token_tipo() == 'retornar':
            self._emparejar('retornar')
            self._parse_OpcExp()
            self._parse_OpcPuntoComa()
        else:
            self._error_sintaxis(['retornar'])

    def _parse_RomperContinuar(self):
        if self._token_tipo() == 'romper':
            self._emparejar('romper')
            self._parse_OpcPuntoComa()
        elif self._token_tipo() == 'continuar':
            self._emparejar('continuar')
            self._parse_OpcPuntoComa()
        else:
            self._error_sintaxis(['continuar', 'romper'])

    def _parse_Sentencia(self):
        if self._token_tipo() == 'const' or self._token_tipo() == 'mut' or self._token_tipo() == 'var':
            self._parse_Declaracion()
        elif self._token_tipo() == 'elegir' or self._token_tipo() == 'hacer' or self._token_tipo() == 'mientras' or self._token_tipo() == 'para' or self._token_tipo() == 'si':
            self._parse_EstructuraControl()
        elif self._token_tipo() == 'funcion':
            self._parse_DefinicionFuncion()
        elif self._token_tipo() == 'retornar':
            self._parse_Retorno()
        elif self._token_tipo() == 'intentar':
            self._parse_Intentar()
        elif self._token_tipo() == 'continuar' or self._token_tipo() == 'romper':
            self._parse_RomperContinuar()
        elif self._token_tipo() == '!' or self._token_tipo() == '(' or self._token_tipo() == '+' or self._token_tipo() == '-' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{':
            self._parse_Expresion()
            self._parse_OpcPuntoComa()
        elif self._token_tipo() == ';':
            self._emparejar(';')
        else:
            self._error_sintaxis(['!', '(', '+', '-', ';', 'Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'mut', 'nulo', 'num', 'para', 'retornar', 'romper', 'si', 'str', 'var', 'verdadero', '{'])

    def _parse_Ternaria(self):
        if self._token_tipo() == '!' or self._token_tipo() == '(' or self._token_tipo() == '+' or self._token_tipo() == '-' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{':
            self._parse_LogicaOr()
            self._parse_OpcTern()
        else:
            self._error_sintaxis(['!', '(', '+', '-', 'Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', 'consola', 'crear', 'falso', 'id', 'indefinido', 'nulo', 'num', 'str', 'verdadero', '{'])

    def _parse_TipoCreable(self):
        if self._token_tipo() == 'Arreglo':
            self._emparejar('Arreglo')
        elif self._token_tipo() == 'Cadena':
            self._emparejar('Cadena')
        elif self._token_tipo() == 'Matriz':
            self._emparejar('Matriz')
        elif self._token_tipo() == 'id':
            self._emparejar('id')
        else:
            self._error_sintaxis(['Arreglo', 'Cadena', 'Matriz', 'id'])

    def _parse_Unaria(self):
        if self._token_tipo() == '!':
            self._emparejar('!')
            self._parse_Unaria()
        elif self._token_tipo() == '-':
            self._emparejar('-')
            self._parse_Unaria()
        elif self._token_tipo() == '+':
            self._emparejar('+')
            self._parse_Unaria()
        elif self._token_tipo() == '(' or self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == '[' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero' or self._token_tipo() == '{':
            self._parse_Primaria()
        else:
            self._error_sintaxis(['!', '(', '+', '-', 'Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', '[', 'consola', 'crear', 'falso', 'id', 'indefinido', 'nulo', 'num', 'str', 'verdadero', '{'])

    def parsear(self):
        self._parse_Programa()
        if not self._es_eof():
            self._error_sintaxis(['EOF'])
        print('El analisis sintactico ha finalizado exitosamente.')
