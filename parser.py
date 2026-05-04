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
            fila       = self._ultima_fila + 1
            col        = 1
            encontrado = '"final de archivo"'
        esperados_visibles = sorted({self._lexema_visible(t) for t in tipos_esperados})
        esperados_str = ', '.join(f'"{e}"' for e in esperados_visibles)
        raise SyntaxError(
            f'<{fila}:{col}> Error sintactico: se encontro: {encontrado}; se esperaba: {esperados_str}.'
        )

    def _parse_ActPara(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_E()
            self._parse_ActSuf()
        elif self._token_tipo() == 'closing_par':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'closing_par', 'consola', 'crear', 'falso', 'id', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_ActSuf(self):
        if self._token_tipo() == 'assign':
            self._emparejar('assign')
            self._parse_E()
        elif self._token_tipo() == 'plus_assign':
            self._emparejar('plus_assign')
            self._parse_E()
        elif self._token_tipo() == 'minus_assign':
            self._emparejar('minus_assign')
            self._parse_E()
        elif self._token_tipo() == 'times_assign':
            self._emparejar('times_assign')
            self._parse_E()
        elif self._token_tipo() == 'div_assign':
            self._emparejar('div_assign')
            self._parse_E()
        elif self._token_tipo() == 'mod_assign':
            self._emparejar('mod_assign')
            self._parse_E()
        elif self._token_tipo() == 'power_assign':
            self._emparejar('power_assign')
            self._parse_E()
        elif self._token_tipo() == 'increment':
            self._emparejar('increment')
        elif self._token_tipo() == 'decrement':
            self._emparejar('decrement')
        elif self._token_tipo() == 'closing_par':
            pass
        else:
            self._error_sintaxis(['assign', 'closing_par', 'decrement', 'div_assign', 'increment', 'minus_assign', 'mod_assign', 'plus_assign', 'power_assign', 'times_assign'])

    def _parse_ArgsFuncion(self):
        if self._token_tipo() == 'opening_par':
            self._emparejar('opening_par')
            self._parse_ListaExpr()
            self._emparejar('closing_par')
        else:
            self._error_sintaxis(['opening_par'])

    def _parse_AsignOpt(self):
        if self._token_tipo() == 'assign':
            self._emparejar('assign')
            self._parse_E()
        elif self._token_tipo() == 'semicolon':
            pass
        else:
            self._error_sintaxis(['assign', 'semicolon'])

    def _parse_CasoList(self):
        if self._token_tipo() == 'caso':
            self._emparejar('caso')
            self._parse_E()
            self._emparejar('colon')
            self._parse_P()
            self._parse_CasoList()
        elif self._token_tipo() == 'porDefecto':
            self._emparejar('porDefecto')
            self._emparejar('colon')
            self._parse_P()
        elif self._token_tipo() == 'closing_key':
            pass
        else:
            self._error_sintaxis(['caso', 'closing_key', 'porDefecto'])

    def _parse_CondPara(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_E()
        elif self._token_tipo() == 'semicolon':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'consola', 'crear', 'falso', 'id', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'semicolon', 'str', 'verdadero'])

    def _parse_DeclConst(self):
        if self._token_tipo() == 'id':
            self._emparejar('id')
            self._parse_InicVar()
            self._parse_MasConst()
        else:
            self._error_sintaxis(['id'])

    def _parse_DeclFuncion(self):
        if self._token_tipo() == 'id':
            self._emparejar('id')
            self._emparejar('opening_par')
            self._parse_Params()
            self._emparejar('closing_par')
            self._emparejar('opening_key')
            self._parse_P()
            self._emparejar('closing_key')
        else:
            self._error_sintaxis(['id'])

    def _parse_DeclVar(self):
        if self._token_tipo() == 'id':
            self._emparejar('id')
            self._parse_InicVar()
            self._parse_MasVars()
        else:
            self._error_sintaxis(['id'])

    def _parse_E(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_E1()
            self._parse_Ternario()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'consola', 'crear', 'falso', 'id', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_E1(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_E2()
            self._parse_E1_prima()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'consola', 'crear', 'falso', 'id', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_E1_prima(self):
        if self._token_tipo() == 'or':
            self._emparejar('or')
            self._parse_E2()
            self._parse_E1_prima()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'and' or self._token_tipo() == 'assign' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_bra' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'closing_par' or self._token_tipo() == 'colon' or self._token_tipo() == 'comma' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'decrement' or self._token_tipo() == 'div' or self._token_tipo() == 'div_assign' or self._token_tipo() == 'elegir' or self._token_tipo() == 'equal' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'geq' or self._token_tipo() == 'greater' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'increment' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'leq' or self._token_tipo() == 'less' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'minus_assign' or self._token_tipo() == 'mod' or self._token_tipo() == 'mod_assign' or self._token_tipo() == 'mut' or self._token_tipo() == 'neq' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'or' or self._token_tipo() == 'para' or self._token_tipo() == 'plus' or self._token_tipo() == 'plus_assign' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'power' or self._token_tipo() == 'power_assign' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'strict_equal' or self._token_tipo() == 'strict_neq' or self._token_tipo() == 'ternary' or self._token_tipo() == 'times' or self._token_tipo() == 'times_assign' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'and', 'assign', 'caso', 'closing_bra', 'closing_key', 'closing_par', 'colon', 'comma', 'consola', 'const', 'continuar', 'crear', 'decrement', 'div', 'div_assign', 'elegir', 'equal', 'falso', 'funcion', 'geq', 'greater', 'hacer', 'id', 'increment', 'indefinido', 'intentar', 'leq', 'less', 'mientras', 'minus', 'minus_assign', 'mod', 'mod_assign', 'mut', 'neq', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'or', 'para', 'plus', 'plus_assign', 'porDefecto', 'power', 'power_assign', 'retornar', 'romper', 'semicolon', 'si', 'str', 'strict_equal', 'strict_neq', 'ternary', 'times', 'times_assign', 'var', 'verdadero'])

    def _parse_E2(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_E3()
            self._parse_E2_prima()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'consola', 'crear', 'falso', 'id', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_E2_prima(self):
        if self._token_tipo() == 'and':
            self._emparejar('and')
            self._parse_E3()
            self._parse_E2_prima()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'and' or self._token_tipo() == 'assign' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_bra' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'closing_par' or self._token_tipo() == 'colon' or self._token_tipo() == 'comma' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'decrement' or self._token_tipo() == 'div' or self._token_tipo() == 'div_assign' or self._token_tipo() == 'elegir' or self._token_tipo() == 'equal' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'geq' or self._token_tipo() == 'greater' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'increment' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'leq' or self._token_tipo() == 'less' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'minus_assign' or self._token_tipo() == 'mod' or self._token_tipo() == 'mod_assign' or self._token_tipo() == 'mut' or self._token_tipo() == 'neq' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'or' or self._token_tipo() == 'para' or self._token_tipo() == 'plus' or self._token_tipo() == 'plus_assign' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'power' or self._token_tipo() == 'power_assign' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'strict_equal' or self._token_tipo() == 'strict_neq' or self._token_tipo() == 'ternary' or self._token_tipo() == 'times' or self._token_tipo() == 'times_assign' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'and', 'assign', 'caso', 'closing_bra', 'closing_key', 'closing_par', 'colon', 'comma', 'consola', 'const', 'continuar', 'crear', 'decrement', 'div', 'div_assign', 'elegir', 'equal', 'falso', 'funcion', 'geq', 'greater', 'hacer', 'id', 'increment', 'indefinido', 'intentar', 'leq', 'less', 'mientras', 'minus', 'minus_assign', 'mod', 'mod_assign', 'mut', 'neq', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'or', 'para', 'plus', 'plus_assign', 'porDefecto', 'power', 'power_assign', 'retornar', 'romper', 'semicolon', 'si', 'str', 'strict_equal', 'strict_neq', 'ternary', 'times', 'times_assign', 'var', 'verdadero'])

    def _parse_E3(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_E4()
            self._parse_E3_prima()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'consola', 'crear', 'falso', 'id', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_E3_prima(self):
        if self._token_tipo() == 'equal':
            self._emparejar('equal')
            self._parse_E4()
        elif self._token_tipo() == 'strict_equal':
            self._emparejar('strict_equal')
            self._parse_E4()
        elif self._token_tipo() == 'neq':
            self._emparejar('neq')
            self._parse_E4()
        elif self._token_tipo() == 'strict_neq':
            self._emparejar('strict_neq')
            self._parse_E4()
        elif self._token_tipo() == 'less':
            self._emparejar('less')
            self._parse_E4()
        elif self._token_tipo() == 'leq':
            self._emparejar('leq')
            self._parse_E4()
        elif self._token_tipo() == 'greater':
            self._emparejar('greater')
            self._parse_E4()
        elif self._token_tipo() == 'geq':
            self._emparejar('geq')
            self._parse_E4()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'and' or self._token_tipo() == 'assign' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_bra' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'closing_par' or self._token_tipo() == 'colon' or self._token_tipo() == 'comma' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'decrement' or self._token_tipo() == 'div' or self._token_tipo() == 'div_assign' or self._token_tipo() == 'elegir' or self._token_tipo() == 'equal' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'geq' or self._token_tipo() == 'greater' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'increment' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'leq' or self._token_tipo() == 'less' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'minus_assign' or self._token_tipo() == 'mod' or self._token_tipo() == 'mod_assign' or self._token_tipo() == 'mut' or self._token_tipo() == 'neq' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'or' or self._token_tipo() == 'para' or self._token_tipo() == 'plus' or self._token_tipo() == 'plus_assign' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'power' or self._token_tipo() == 'power_assign' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'strict_equal' or self._token_tipo() == 'strict_neq' or self._token_tipo() == 'ternary' or self._token_tipo() == 'times' or self._token_tipo() == 'times_assign' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'and', 'assign', 'caso', 'closing_bra', 'closing_key', 'closing_par', 'colon', 'comma', 'consola', 'const', 'continuar', 'crear', 'decrement', 'div', 'div_assign', 'elegir', 'equal', 'falso', 'funcion', 'geq', 'greater', 'hacer', 'id', 'increment', 'indefinido', 'intentar', 'leq', 'less', 'mientras', 'minus', 'minus_assign', 'mod', 'mod_assign', 'mut', 'neq', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'or', 'para', 'plus', 'plus_assign', 'porDefecto', 'power', 'power_assign', 'retornar', 'romper', 'semicolon', 'si', 'str', 'strict_equal', 'strict_neq', 'ternary', 'times', 'times_assign', 'var', 'verdadero'])

    def _parse_E4(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_E5()
            self._parse_E4_prima()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'consola', 'crear', 'falso', 'id', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_E4_prima(self):
        if self._token_tipo() == 'plus':
            self._emparejar('plus')
            self._parse_E5()
            self._parse_E4_prima()
        elif self._token_tipo() == 'minus':
            self._emparejar('minus')
            self._parse_E5()
            self._parse_E4_prima()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'and' or self._token_tipo() == 'assign' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_bra' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'closing_par' or self._token_tipo() == 'colon' or self._token_tipo() == 'comma' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'decrement' or self._token_tipo() == 'div' or self._token_tipo() == 'div_assign' or self._token_tipo() == 'elegir' or self._token_tipo() == 'equal' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'geq' or self._token_tipo() == 'greater' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'increment' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'leq' or self._token_tipo() == 'less' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'minus_assign' or self._token_tipo() == 'mod' or self._token_tipo() == 'mod_assign' or self._token_tipo() == 'mut' or self._token_tipo() == 'neq' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'or' or self._token_tipo() == 'para' or self._token_tipo() == 'plus' or self._token_tipo() == 'plus_assign' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'power' or self._token_tipo() == 'power_assign' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'strict_equal' or self._token_tipo() == 'strict_neq' or self._token_tipo() == 'ternary' or self._token_tipo() == 'times' or self._token_tipo() == 'times_assign' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'and', 'assign', 'caso', 'closing_bra', 'closing_key', 'closing_par', 'colon', 'comma', 'consola', 'const', 'continuar', 'crear', 'decrement', 'div', 'div_assign', 'elegir', 'equal', 'falso', 'funcion', 'geq', 'greater', 'hacer', 'id', 'increment', 'indefinido', 'intentar', 'leq', 'less', 'mientras', 'minus', 'minus_assign', 'mod', 'mod_assign', 'mut', 'neq', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'or', 'para', 'plus', 'plus_assign', 'porDefecto', 'power', 'power_assign', 'retornar', 'romper', 'semicolon', 'si', 'str', 'strict_equal', 'strict_neq', 'ternary', 'times', 'times_assign', 'var', 'verdadero'])

    def _parse_E5(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_E6()
            self._parse_E5_prima()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'consola', 'crear', 'falso', 'id', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_E5_prima(self):
        if self._token_tipo() == 'times':
            self._emparejar('times')
            self._parse_E6()
            self._parse_E5_prima()
        elif self._token_tipo() == 'div':
            self._emparejar('div')
            self._parse_E6()
            self._parse_E5_prima()
        elif self._token_tipo() == 'mod':
            self._emparejar('mod')
            self._parse_E6()
            self._parse_E5_prima()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'and' or self._token_tipo() == 'assign' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_bra' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'closing_par' or self._token_tipo() == 'colon' or self._token_tipo() == 'comma' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'decrement' or self._token_tipo() == 'div' or self._token_tipo() == 'div_assign' or self._token_tipo() == 'elegir' or self._token_tipo() == 'equal' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'geq' or self._token_tipo() == 'greater' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'increment' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'leq' or self._token_tipo() == 'less' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'minus_assign' or self._token_tipo() == 'mod' or self._token_tipo() == 'mod_assign' or self._token_tipo() == 'mut' or self._token_tipo() == 'neq' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'or' or self._token_tipo() == 'para' or self._token_tipo() == 'plus' or self._token_tipo() == 'plus_assign' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'power' or self._token_tipo() == 'power_assign' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'strict_equal' or self._token_tipo() == 'strict_neq' or self._token_tipo() == 'ternary' or self._token_tipo() == 'times' or self._token_tipo() == 'times_assign' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'and', 'assign', 'caso', 'closing_bra', 'closing_key', 'closing_par', 'colon', 'comma', 'consola', 'const', 'continuar', 'crear', 'decrement', 'div', 'div_assign', 'elegir', 'equal', 'falso', 'funcion', 'geq', 'greater', 'hacer', 'id', 'increment', 'indefinido', 'intentar', 'leq', 'less', 'mientras', 'minus', 'minus_assign', 'mod', 'mod_assign', 'mut', 'neq', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'or', 'para', 'plus', 'plus_assign', 'porDefecto', 'power', 'power_assign', 'retornar', 'romper', 'semicolon', 'si', 'str', 'strict_equal', 'strict_neq', 'ternary', 'times', 'times_assign', 'var', 'verdadero'])

    def _parse_E6(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_E7()
            self._parse_E6_prima()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'consola', 'crear', 'falso', 'id', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_E6_prima(self):
        if self._token_tipo() == 'power':
            self._emparejar('power')
            self._parse_E6()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'and' or self._token_tipo() == 'assign' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_bra' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'closing_par' or self._token_tipo() == 'colon' or self._token_tipo() == 'comma' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'decrement' or self._token_tipo() == 'div' or self._token_tipo() == 'div_assign' or self._token_tipo() == 'elegir' or self._token_tipo() == 'equal' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'geq' or self._token_tipo() == 'greater' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'increment' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'leq' or self._token_tipo() == 'less' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'minus_assign' or self._token_tipo() == 'mod' or self._token_tipo() == 'mod_assign' or self._token_tipo() == 'mut' or self._token_tipo() == 'neq' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'or' or self._token_tipo() == 'para' or self._token_tipo() == 'plus' or self._token_tipo() == 'plus_assign' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'power' or self._token_tipo() == 'power_assign' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'strict_equal' or self._token_tipo() == 'strict_neq' or self._token_tipo() == 'ternary' or self._token_tipo() == 'times' or self._token_tipo() == 'times_assign' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'and', 'assign', 'caso', 'closing_bra', 'closing_key', 'closing_par', 'colon', 'comma', 'consola', 'const', 'continuar', 'crear', 'decrement', 'div', 'div_assign', 'elegir', 'equal', 'falso', 'funcion', 'geq', 'greater', 'hacer', 'id', 'increment', 'indefinido', 'intentar', 'leq', 'less', 'mientras', 'minus', 'minus_assign', 'mod', 'mod_assign', 'mut', 'neq', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'or', 'para', 'plus', 'plus_assign', 'porDefecto', 'power', 'power_assign', 'retornar', 'romper', 'semicolon', 'si', 'str', 'strict_equal', 'strict_neq', 'ternary', 'times', 'times_assign', 'var', 'verdadero'])

    def _parse_E7(self):
        if self._token_tipo() == 'minus':
            self._emparejar('minus')
            self._parse_E7()
        elif self._token_tipo() == 'not':
            self._emparejar('not')
            self._parse_E7()
        elif self._token_tipo() == 'plus':
            self._emparejar('plus')
            self._parse_E7()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_E8()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'consola', 'crear', 'falso', 'id', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_E8(self):
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
        elif self._token_tipo() == 'Infinito':
            self._emparejar('Infinito')
        elif self._token_tipo() == 'NuN':
            self._emparejar('NuN')
        elif self._token_tipo() == 'opening_par':
            self._emparejar('opening_par')
            self._parse_ListaExpr()
            self._emparejar('closing_par')
            self._parse_SufijoOArrow()
        elif self._token_tipo() == 'opening_bra':
            self._emparejar('opening_bra')
            self._parse_ListaExpr()
            self._emparejar('closing_bra')
        elif self._token_tipo() == 'opening_key':
            self._emparejar('opening_key')
            self._parse_PropiedadesObj()
            self._emparejar('closing_key')
        elif self._token_tipo() == 'crear':
            self._emparejar('crear')
            self._parse_TipoCrear()
            self._parse_ArgsFuncion()
        elif self._token_tipo() == 'id':
            self._emparejar('id')
            self._parse_Sufijo()
        elif self._token_tipo() == 'consola':
            self._emparejar('consola')
            self._emparejar('period')
            self._parse_MetodoConsola()
            self._parse_ArgsFuncion()
            self._parse_Sufijo()
        elif self._token_tipo() == 'Numero':
            self._emparejar('Numero')
            self._parse_Sufijo()
        elif self._token_tipo() == 'Mate':
            self._emparejar('Mate')
            self._parse_Sufijo()
        elif self._token_tipo() == 'Matriz':
            self._emparejar('Matriz')
            self._parse_Sufijo()
        elif self._token_tipo() == 'Arreglo':
            self._emparejar('Arreglo')
            self._parse_Sufijo()
        elif self._token_tipo() == 'Booleano':
            self._emparejar('Booleano')
            self._parse_Sufijo()
        elif self._token_tipo() == 'Cadena':
            self._emparejar('Cadena')
            self._parse_Sufijo()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'consola', 'crear', 'falso', 'id', 'indefinido', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'str', 'verdadero'])

    def _parse_InicPara(self):
        if self._token_tipo() == 'var':
            self._emparejar('var')
            self._parse_DeclVar()
        elif self._token_tipo() == 'mut':
            self._emparejar('mut')
            self._parse_DeclVar()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_E()
            self._parse_AsignOpt()
        elif self._token_tipo() == 'semicolon':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'consola', 'crear', 'falso', 'id', 'indefinido', 'minus', 'mut', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'semicolon', 'str', 'var', 'verdadero'])

    def _parse_InicVar(self):
        if self._token_tipo() == 'assign':
            self._emparejar('assign')
            self._parse_E()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'comma' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mut' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'para' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'assign', 'caso', 'closing_key', 'comma', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'minus', 'mut', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'para', 'plus', 'porDefecto', 'retornar', 'romper', 'semicolon', 'si', 'str', 'var', 'verdadero'])

    def _parse_ListaExpr(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_E()
            self._parse_MasExpr()
        elif self._token_tipo() == 'closing_bra' or self._token_tipo() == 'closing_par':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'closing_bra', 'closing_par', 'consola', 'crear', 'falso', 'id', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_MasConst(self):
        if self._token_tipo() == 'comma':
            self._emparejar('comma')
            self._emparejar('id')
            self._parse_InicVar()
            self._parse_MasConst()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mut' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'para' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'caso', 'closing_key', 'comma', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'minus', 'mut', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'para', 'plus', 'porDefecto', 'retornar', 'romper', 'semicolon', 'si', 'str', 'var', 'verdadero'])

    def _parse_MasExpr(self):
        if self._token_tipo() == 'comma':
            self._emparejar('comma')
            self._parse_E()
            self._parse_MasExpr()
        elif self._token_tipo() == 'closing_bra' or self._token_tipo() == 'closing_par':
            pass
        else:
            self._error_sintaxis(['closing_bra', 'closing_par', 'comma'])

    def _parse_MasParams(self):
        if self._token_tipo() == 'comma':
            self._emparejar('comma')
            self._emparejar('id')
            self._parse_MasParams()
        elif self._token_tipo() == 'closing_par':
            pass
        else:
            self._error_sintaxis(['closing_par', 'comma'])

    def _parse_MasProps(self):
        if self._token_tipo() == 'comma':
            self._emparejar('comma')
            self._parse_PropObj()
            self._parse_MasProps()
        elif self._token_tipo() == 'closing_key':
            pass
        else:
            self._error_sintaxis(['closing_key', 'comma'])

    def _parse_MasVars(self):
        if self._token_tipo() == 'comma':
            self._emparejar('comma')
            self._emparejar('id')
            self._parse_InicVar()
            self._parse_MasVars()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mut' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'para' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'caso', 'closing_key', 'comma', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'minus', 'mut', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'para', 'plus', 'porDefecto', 'retornar', 'romper', 'semicolon', 'si', 'str', 'var', 'verdadero'])

    def _parse_MetodoConsola(self):
        if self._token_tipo() == 'afirmar':
            self._emparejar('afirmar')
        elif self._token_tipo() == 'agrupar':
            self._emparejar('agrupar')
        elif self._token_tipo() == 'error':
            self._emparejar('error')
        elif self._token_tipo() == 'escribir':
            self._emparejar('escribir')
        elif self._token_tipo() == 'info':
            self._emparejar('info')
        elif self._token_tipo() == 'limpiar':
            self._emparejar('limpiar')
        elif self._token_tipo() == 'tabla':
            self._emparejar('tabla')
        else:
            self._error_sintaxis(['afirmar', 'agrupar', 'error', 'escribir', 'info', 'limpiar', 'tabla'])

    def _parse_P(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mut' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'para' or self._token_tipo() == 'plus' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            self._parse_S()
            self._parse_P()
        elif self._token_tipo() == 'EOF' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'porDefecto':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'caso', 'closing_key', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'minus', 'mut', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'para', 'plus', 'porDefecto', 'retornar', 'romper', 'semicolon', 'si', 'str', 'var', 'verdadero'])

    def _parse_Params(self):
        if self._token_tipo() == 'id':
            self._emparejar('id')
            self._parse_MasParams()
        elif self._token_tipo() == 'closing_par':
            pass
        else:
            self._error_sintaxis(['closing_par', 'id'])

    def _parse_PostExpr(self):
        if self._token_tipo() == 'assign':
            self._emparejar('assign')
            self._parse_E()
            self._parse_SemiOpt()
        elif self._token_tipo() == 'plus_assign':
            self._emparejar('plus_assign')
            self._parse_E()
            self._parse_SemiOpt()
        elif self._token_tipo() == 'minus_assign':
            self._emparejar('minus_assign')
            self._parse_E()
            self._parse_SemiOpt()
        elif self._token_tipo() == 'times_assign':
            self._emparejar('times_assign')
            self._parse_E()
            self._parse_SemiOpt()
        elif self._token_tipo() == 'div_assign':
            self._emparejar('div_assign')
            self._parse_E()
            self._parse_SemiOpt()
        elif self._token_tipo() == 'mod_assign':
            self._emparejar('mod_assign')
            self._parse_E()
            self._parse_SemiOpt()
        elif self._token_tipo() == 'power_assign':
            self._emparejar('power_assign')
            self._parse_E()
            self._parse_SemiOpt()
        elif self._token_tipo() == 'increment':
            self._emparejar('increment')
            self._parse_SemiOpt()
        elif self._token_tipo() == 'decrement':
            self._emparejar('decrement')
            self._parse_SemiOpt()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mut' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'para' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            self._parse_SemiOpt()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'assign', 'caso', 'closing_key', 'consola', 'const', 'continuar', 'crear', 'decrement', 'div_assign', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'increment', 'indefinido', 'intentar', 'mientras', 'minus', 'minus_assign', 'mod_assign', 'mut', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'para', 'plus', 'plus_assign', 'porDefecto', 'power_assign', 'retornar', 'romper', 'semicolon', 'si', 'str', 'times_assign', 'var', 'verdadero'])

    def _parse_PropObj(self):
        if self._token_tipo() == 'id':
            self._emparejar('id')
            self._parse_ValorProp()
        elif self._token_tipo() == 'str':
            self._emparejar('str')
            self._emparejar('colon')
            self._parse_E()
        elif self._token_tipo() == 'num':
            self._emparejar('num')
            self._emparejar('colon')
            self._parse_E()
        else:
            self._error_sintaxis(['id', 'num', 'str'])

    def _parse_PropiedadesObj(self):
        if self._token_tipo() == 'id' or self._token_tipo() == 'num' or self._token_tipo() == 'str':
            self._parse_PropObj()
            self._parse_MasProps()
        elif self._token_tipo() == 'closing_key':
            pass
        else:
            self._error_sintaxis(['closing_key', 'id', 'num', 'str'])

    def _parse_RetExpr(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_E()
            self._parse_SemiOpt()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'consola', 'crear', 'falso', 'id', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_S(self):
        if self._token_tipo() == 'var':
            self._emparejar('var')
            self._parse_DeclVar()
        elif self._token_tipo() == 'mut':
            self._emparejar('mut')
            self._parse_DeclVar()
        elif self._token_tipo() == 'const':
            self._emparejar('const')
            self._parse_DeclConst()
        elif self._token_tipo() == 'funcion':
            self._emparejar('funcion')
            self._parse_DeclFuncion()
        elif self._token_tipo() == 'retornar':
            self._emparejar('retornar')
            self._parse_RetExpr()
        elif self._token_tipo() == 'si':
            self._emparejar('si')
            self._parse_SentSi()
        elif self._token_tipo() == 'elegir':
            self._emparejar('elegir')
            self._parse_SentElegir()
        elif self._token_tipo() == 'mientras':
            self._emparejar('mientras')
            self._parse_SentMientras()
        elif self._token_tipo() == 'hacer':
            self._emparejar('hacer')
            self._parse_SentHacer()
        elif self._token_tipo() == 'para':
            self._emparejar('para')
            self._parse_SentPara()
        elif self._token_tipo() == 'intentar':
            self._emparejar('intentar')
            self._parse_SentIntentar()
        elif self._token_tipo() == 'continuar':
            self._emparejar('continuar')
            self._parse_SemiOpt()
        elif self._token_tipo() == 'romper':
            self._emparejar('romper')
            self._parse_SemiOpt()
        elif self._token_tipo() == 'opening_key':
            self._emparejar('opening_key')
            self._parse_P()
            self._emparejar('closing_key')
        elif self._token_tipo() == 'semicolon':
            self._emparejar('semicolon')
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'consola' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_E()
            self._parse_PostExpr()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'minus', 'mut', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'para', 'plus', 'retornar', 'romper', 'semicolon', 'si', 'str', 'var', 'verdadero'])

    def _parse_SemiOpt(self):
        if self._token_tipo() == 'semicolon':
            self._emparejar('semicolon')
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mut' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'para' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'caso', 'closing_key', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'minus', 'mut', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'para', 'plus', 'porDefecto', 'retornar', 'romper', 'semicolon', 'si', 'str', 'var', 'verdadero'])

    def _parse_SentElegir(self):
        if self._token_tipo() == 'opening_par':
            self._emparejar('opening_par')
            self._parse_E()
            self._emparejar('closing_par')
            self._emparejar('opening_key')
            self._parse_CasoList()
            self._emparejar('closing_key')
        else:
            self._error_sintaxis(['opening_par'])

    def _parse_SentHacer(self):
        if self._token_tipo() == 'opening_key':
            self._emparejar('opening_key')
            self._parse_P()
            self._emparejar('closing_key')
            self._emparejar('mientras')
            self._emparejar('opening_par')
            self._parse_E()
            self._emparejar('closing_par')
            self._emparejar('semicolon')
        else:
            self._error_sintaxis(['opening_key'])

    def _parse_SentIntentar(self):
        if self._token_tipo() == 'opening_key':
            self._emparejar('opening_key')
            self._parse_P()
            self._emparejar('closing_key')
            self._emparejar('capturar')
            self._emparejar('opening_par')
            self._emparejar('id')
            self._emparejar('closing_par')
            self._emparejar('opening_key')
            self._parse_P()
            self._emparejar('closing_key')
        else:
            self._error_sintaxis(['opening_key'])

    def _parse_SentMientras(self):
        if self._token_tipo() == 'opening_par':
            self._emparejar('opening_par')
            self._parse_E()
            self._emparejar('closing_par')
            self._emparejar('opening_key')
            self._parse_P()
            self._emparejar('closing_key')
        else:
            self._error_sintaxis(['opening_par'])

    def _parse_SentPara(self):
        if self._token_tipo() == 'opening_par':
            self._emparejar('opening_par')
            self._parse_InicPara()
            self._emparejar('semicolon')
            self._parse_CondPara()
            self._emparejar('semicolon')
            self._parse_ActPara()
            self._emparejar('closing_par')
            self._emparejar('opening_key')
            self._parse_P()
            self._emparejar('closing_key')
        else:
            self._error_sintaxis(['opening_par'])

    def _parse_SentSi(self):
        if self._token_tipo() == 'opening_par':
            self._emparejar('opening_par')
            self._parse_E()
            self._emparejar('closing_par')
            self._emparejar('opening_key')
            self._parse_P()
            self._emparejar('closing_key')
            self._parse_SentSino()
        else:
            self._error_sintaxis(['opening_par'])

    def _parse_SentSino(self):
        if self._token_tipo() == 'sino':
            self._emparejar('sino')
            self._parse_SinoResto()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mut' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'para' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'caso', 'closing_key', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'minus', 'mut', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'para', 'plus', 'porDefecto', 'retornar', 'romper', 'semicolon', 'si', 'sino', 'str', 'var', 'verdadero'])

    def _parse_SinoResto(self):
        if self._token_tipo() == 'si':
            self._emparejar('si')
            self._emparejar('opening_par')
            self._parse_E()
            self._emparejar('closing_par')
            self._emparejar('opening_key')
            self._parse_P()
            self._emparejar('closing_key')
            self._parse_SentSino()
        elif self._token_tipo() == 'opening_key':
            self._emparejar('opening_key')
            self._parse_P()
            self._emparejar('closing_key')
        else:
            self._error_sintaxis(['opening_key', 'si'])

    def _parse_Sufijo(self):
        if self._token_tipo() == 'period':
            self._emparejar('period')
            self._emparejar('id')
            self._parse_Sufijo()
        elif self._token_tipo() == 'opening_bra':
            self._emparejar('opening_bra')
            self._parse_E()
            self._emparejar('closing_bra')
            self._parse_Sufijo()
        elif self._token_tipo() == 'opening_par':
            self._emparejar('opening_par')
            self._parse_ListaExpr()
            self._emparejar('closing_par')
            self._parse_Sufijo()
        elif self._token_tipo() == 'increment':
            self._emparejar('increment')
        elif self._token_tipo() == 'decrement':
            self._emparejar('decrement')
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'and' or self._token_tipo() == 'assign' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_bra' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'closing_par' or self._token_tipo() == 'colon' or self._token_tipo() == 'comma' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'decrement' or self._token_tipo() == 'div' or self._token_tipo() == 'div_assign' or self._token_tipo() == 'elegir' or self._token_tipo() == 'equal' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'geq' or self._token_tipo() == 'greater' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'increment' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'leq' or self._token_tipo() == 'less' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'minus_assign' or self._token_tipo() == 'mod' or self._token_tipo() == 'mod_assign' or self._token_tipo() == 'mut' or self._token_tipo() == 'neq' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'or' or self._token_tipo() == 'para' or self._token_tipo() == 'plus' or self._token_tipo() == 'plus_assign' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'power' or self._token_tipo() == 'power_assign' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'strict_equal' or self._token_tipo() == 'strict_neq' or self._token_tipo() == 'ternary' or self._token_tipo() == 'times' or self._token_tipo() == 'times_assign' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'and', 'assign', 'caso', 'closing_bra', 'closing_key', 'closing_par', 'colon', 'comma', 'consola', 'const', 'continuar', 'crear', 'decrement', 'div', 'div_assign', 'elegir', 'equal', 'falso', 'funcion', 'geq', 'greater', 'hacer', 'id', 'increment', 'indefinido', 'intentar', 'leq', 'less', 'mientras', 'minus', 'minus_assign', 'mod', 'mod_assign', 'mut', 'neq', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'or', 'para', 'period', 'plus', 'plus_assign', 'porDefecto', 'power', 'power_assign', 'retornar', 'romper', 'semicolon', 'si', 'str', 'strict_equal', 'strict_neq', 'ternary', 'times', 'times_assign', 'var', 'verdadero'])

    def _parse_SufijoOArrow(self):
        if self._token_tipo() == 'arrow':
            self._emparejar('arrow')
            self._parse_E()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'and' or self._token_tipo() == 'assign' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_bra' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'closing_par' or self._token_tipo() == 'colon' or self._token_tipo() == 'comma' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'decrement' or self._token_tipo() == 'div' or self._token_tipo() == 'div_assign' or self._token_tipo() == 'elegir' or self._token_tipo() == 'equal' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'geq' or self._token_tipo() == 'greater' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'increment' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'leq' or self._token_tipo() == 'less' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'minus_assign' or self._token_tipo() == 'mod' or self._token_tipo() == 'mod_assign' or self._token_tipo() == 'mut' or self._token_tipo() == 'neq' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'or' or self._token_tipo() == 'para' or self._token_tipo() == 'period' or self._token_tipo() == 'plus' or self._token_tipo() == 'plus_assign' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'power' or self._token_tipo() == 'power_assign' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'strict_equal' or self._token_tipo() == 'strict_neq' or self._token_tipo() == 'ternary' or self._token_tipo() == 'times' or self._token_tipo() == 'times_assign' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            self._parse_Sufijo()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'and', 'arrow', 'assign', 'caso', 'closing_bra', 'closing_key', 'closing_par', 'colon', 'comma', 'consola', 'const', 'continuar', 'crear', 'decrement', 'div', 'div_assign', 'elegir', 'equal', 'falso', 'funcion', 'geq', 'greater', 'hacer', 'id', 'increment', 'indefinido', 'intentar', 'leq', 'less', 'mientras', 'minus', 'minus_assign', 'mod', 'mod_assign', 'mut', 'neq', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'or', 'para', 'period', 'plus', 'plus_assign', 'porDefecto', 'power', 'power_assign', 'retornar', 'romper', 'semicolon', 'si', 'str', 'strict_equal', 'strict_neq', 'ternary', 'times', 'times_assign', 'var', 'verdadero'])

    def _parse_Ternario(self):
        if self._token_tipo() == 'ternary':
            self._emparejar('ternary')
            self._parse_E()
            self._emparejar('colon')
            self._parse_E()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'and' or self._token_tipo() == 'assign' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_bra' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'closing_par' or self._token_tipo() == 'colon' or self._token_tipo() == 'comma' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'decrement' or self._token_tipo() == 'div' or self._token_tipo() == 'div_assign' or self._token_tipo() == 'elegir' or self._token_tipo() == 'equal' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'geq' or self._token_tipo() == 'greater' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'increment' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'leq' or self._token_tipo() == 'less' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'minus_assign' or self._token_tipo() == 'mod' or self._token_tipo() == 'mod_assign' or self._token_tipo() == 'mut' or self._token_tipo() == 'neq' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'or' or self._token_tipo() == 'para' or self._token_tipo() == 'plus' or self._token_tipo() == 'plus_assign' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'power' or self._token_tipo() == 'power_assign' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'strict_equal' or self._token_tipo() == 'strict_neq' or self._token_tipo() == 'ternary' or self._token_tipo() == 'times' or self._token_tipo() == 'times_assign' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'and', 'assign', 'caso', 'closing_bra', 'closing_key', 'closing_par', 'colon', 'comma', 'consola', 'const', 'continuar', 'crear', 'decrement', 'div', 'div_assign', 'elegir', 'equal', 'falso', 'funcion', 'geq', 'greater', 'hacer', 'id', 'increment', 'indefinido', 'intentar', 'leq', 'less', 'mientras', 'minus', 'minus_assign', 'mod', 'mod_assign', 'mut', 'neq', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'or', 'para', 'plus', 'plus_assign', 'porDefecto', 'power', 'power_assign', 'retornar', 'romper', 'semicolon', 'si', 'str', 'strict_equal', 'strict_neq', 'ternary', 'times', 'times_assign', 'var', 'verdadero'])

    def _parse_TipoCrear(self):
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

    def _parse_ValorProp(self):
        if self._token_tipo() == 'colon':
            self._emparejar('colon')
            self._parse_E()
        elif self._token_tipo() == 'opening_par':
            self._emparejar('opening_par')
            self._parse_Params()
            self._emparejar('closing_par')
            self._emparejar('opening_key')
            self._parse_P()
            self._emparejar('closing_key')
        else:
            self._error_sintaxis(['colon', 'opening_par'])

    def parsear(self):
        self._parse_P()
        if not self._es_eof():
            self._error_sintaxis(['EOF'])
        print('El analisis sintactico ha finalizado exitosamente.')
