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

    def _parse_ARGS(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR()
            self._parse_ARGS_RESTO()
        elif self._token_tipo() == 'closing_par':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'closing_par', 'crear', 'falso', 'id', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_ARGS_RESTO(self):
        if self._token_tipo() == 'comma':
            self._emparejar('comma')
            self._parse_EXPR()
            self._parse_ARGS_RESTO()
        elif self._token_tipo() == 'closing_par':
            pass
        else:
            self._error_sintaxis(['closing_par', 'comma'])

    def _parse_ARROW_BODY(self):
        if self._token_tipo() == 'opening_key':
            self._emparejar('opening_key')
            self._parse_SL()
            self._emparejar('closing_key')
        elif self._token_tipo() == 'Infinito' or self._token_tipo() == 'NuN' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR_NO_KEY()
        else:
            self._error_sintaxis(['Infinito', 'NuN', 'crear', 'falso', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_ARROW_OPT(self):
        if self._token_tipo() == 'arrow':
            self._emparejar('arrow')
            self._parse_ARROW_BODY()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'and' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_bra' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'closing_par' or self._token_tipo() == 'colon' or self._token_tipo() == 'comma' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'decrement' or self._token_tipo() == 'div' or self._token_tipo() == 'elegir' or self._token_tipo() == 'equal' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'geq' or self._token_tipo() == 'greater' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'increment' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'leq' or self._token_tipo() == 'less' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mod' or self._token_tipo() == 'mut' or self._token_tipo() == 'neq' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'or' or self._token_tipo() == 'para' or self._token_tipo() == 'period' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'power' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'strict_equal' or self._token_tipo() == 'strict_neq' or self._token_tipo() == 'ternary' or self._token_tipo() == 'times' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'and', 'arrow', 'caso', 'closing_bra', 'closing_key', 'closing_par', 'colon', 'comma', 'consola', 'const', 'continuar', 'crear', 'decrement', 'div', 'elegir', 'equal', 'falso', 'funcion', 'geq', 'greater', 'hacer', 'id', 'increment', 'indefinido', 'intentar', 'leq', 'less', 'mientras', 'minus', 'mod', 'mut', 'neq', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'or', 'para', 'period', 'plus', 'porDefecto', 'power', 'retornar', 'romper', 'semicolon', 'si', 'str', 'strict_equal', 'strict_neq', 'ternary', 'times', 'var', 'verdadero'])

    def _parse_ASIGN_O_LLAMADA(self):
        if self._token_tipo() == 'id':
            self._emparejar('id')
            self._parse_ASIGN_O_LLAMADA_SUF()
            self._parse_SEMI_OPT()
        else:
            self._error_sintaxis(['id'])

    def _parse_ASIGN_O_LLAMADA_SUF(self):
        if self._token_tipo() == 'assign':
            self._emparejar('assign')
            self._parse_EXPR()
        elif self._token_tipo() == 'plus_assign':
            self._emparejar('plus_assign')
            self._parse_EXPR()
        elif self._token_tipo() == 'minus_assign':
            self._emparejar('minus_assign')
            self._parse_EXPR()
        elif self._token_tipo() == 'times_assign':
            self._emparejar('times_assign')
            self._parse_EXPR()
        elif self._token_tipo() == 'div_assign':
            self._emparejar('div_assign')
            self._parse_EXPR()
        elif self._token_tipo() == 'mod_assign':
            self._emparejar('mod_assign')
            self._parse_EXPR()
        elif self._token_tipo() == 'power_assign':
            self._emparejar('power_assign')
            self._parse_EXPR()
        elif self._token_tipo() == 'increment':
            self._emparejar('increment')
        elif self._token_tipo() == 'decrement':
            self._emparejar('decrement')
        elif self._token_tipo() == 'opening_bra':
            self._emparejar('opening_bra')
            self._parse_EXPR()
            self._emparejar('closing_bra')
            self._parse_SUBSCRIPT_SUF()
        elif self._token_tipo() == 'opening_par':
            self._emparejar('opening_par')
            self._parse_ARGS()
            self._emparejar('closing_par')
            self._parse_ENCADENADO()
        elif self._token_tipo() == 'period':
            self._emparejar('period')
            self._emparejar('id')
            self._parse_POSTFIX_LLAMADA()
        else:
            self._error_sintaxis(['assign', 'decrement', 'div_assign', 'increment', 'minus_assign', 'mod_assign', 'opening_bra', 'opening_par', 'period', 'plus_assign', 'power_assign', 'times_assign'])

    def _parse_BLOQUE(self):
        if self._token_tipo() == 'opening_key':
            self._emparejar('opening_key')
            self._parse_SL()
            self._emparejar('closing_key')
        else:
            self._error_sintaxis(['opening_key'])

    def _parse_CASO(self):
        if self._token_tipo() == 'caso':
            self._emparejar('caso')
            self._parse_EXPR()
            self._emparejar('colon')
            self._parse_SL_CASO()
            self._parse_ROMPER_OPT()
        else:
            self._error_sintaxis(['caso'])

    def _parse_CASOS(self):
        if self._token_tipo() == 'caso':
            self._parse_CASO()
            self._parse_CASOS()
        elif self._token_tipo() == 'closing_key' or self._token_tipo() == 'porDefecto':
            pass
        else:
            self._error_sintaxis(['caso', 'closing_key', 'porDefecto'])

    def _parse_CONSOLA_STMT(self):
        if self._token_tipo() == 'consola':
            self._emparejar('consola')
            self._emparejar('period')
            self._parse_METODO_CONSOLA()
            self._emparejar('opening_par')
            self._parse_ARGS()
            self._emparejar('closing_par')
            self._parse_SEMI_OPT()
        else:
            self._error_sintaxis(['consola'])

    def _parse_CONST_DECL(self):
        if self._token_tipo() == 'const':
            self._emparejar('const')
            self._emparejar('id')
            self._emparejar('assign')
            self._parse_EXPR()
            self._parse_SEMI_OPT()
        else:
            self._error_sintaxis(['const'])

    def _parse_CONTINUAR_STMT(self):
        if self._token_tipo() == 'continuar':
            self._emparejar('continuar')
            self._parse_SEMI_OPT()
        else:
            self._error_sintaxis(['continuar'])

    def _parse_CREAR_TARGET(self):
        if self._token_tipo() == 'id':
            self._emparejar('id')
        elif self._token_tipo() == 'Arreglo':
            self._emparejar('Arreglo')
        elif self._token_tipo() == 'Cadena':
            self._emparejar('Cadena')
        elif self._token_tipo() == 'Matriz':
            self._emparejar('Matriz')
        else:
            self._error_sintaxis(['Arreglo', 'Cadena', 'Matriz', 'id'])

    def _parse_DECL(self):
        if self._token_tipo() == 'var':
            self._emparejar('var')
            self._parse_DECL_LISTA()
            self._parse_SEMI_OPT()
        elif self._token_tipo() == 'mut':
            self._emparejar('mut')
            self._parse_DECL_LISTA()
            self._parse_SEMI_OPT()
        else:
            self._error_sintaxis(['mut', 'var'])

    def _parse_DECL_INIT(self):
        if self._token_tipo() == 'assign':
            self._emparejar('assign')
            self._parse_EXPR()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'comma' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mut' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'para' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'assign', 'caso', 'closing_key', 'comma', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'minus', 'mut', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'para', 'plus', 'porDefecto', 'retornar', 'romper', 'semicolon', 'si', 'str', 'var', 'verdadero'])

    def _parse_DECL_LISTA(self):
        if self._token_tipo() == 'id':
            self._emparejar('id')
            self._parse_DECL_INIT()
            self._parse_DECL_LISTA_RESTO()
        else:
            self._error_sintaxis(['id'])

    def _parse_DECL_LISTA_RESTO(self):
        if self._token_tipo() == 'comma':
            self._emparejar('comma')
            self._emparejar('id')
            self._parse_DECL_INIT()
            self._parse_DECL_LISTA_RESTO()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mut' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'para' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'caso', 'closing_key', 'comma', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'minus', 'mut', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'para', 'plus', 'porDefecto', 'retornar', 'romper', 'semicolon', 'si', 'str', 'var', 'verdadero'])

    def _parse_DEFECTO_OPT(self):
        if self._token_tipo() == 'porDefecto':
            self._emparejar('porDefecto')
            self._emparejar('colon')
            self._parse_SL_CASO()
            self._parse_ROMPER_OPT2()
        elif self._token_tipo() == 'closing_key':
            pass
        else:
            self._error_sintaxis(['closing_key', 'porDefecto'])

    def _parse_ELEGIR_STMT(self):
        if self._token_tipo() == 'elegir':
            self._emparejar('elegir')
            self._emparejar('opening_par')
            self._parse_EXPR()
            self._emparejar('closing_par')
            self._emparejar('opening_key')
            self._parse_CASOS()
            self._parse_DEFECTO_OPT()
            self._emparejar('closing_key')
        else:
            self._error_sintaxis(['elegir'])

    def _parse_ENCADENADO(self):
        if self._token_tipo() == 'opening_par':
            self._emparejar('opening_par')
            self._parse_ARGS()
            self._emparejar('closing_par')
            self._parse_ENCADENADO()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mut' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'para' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'caso', 'closing_key', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'minus', 'mut', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'para', 'plus', 'porDefecto', 'retornar', 'romper', 'semicolon', 'si', 'str', 'var', 'verdadero'])

    def _parse_ENCADENADO_EXPR(self):
        if self._token_tipo() == 'opening_par':
            self._emparejar('opening_par')
            self._parse_ARGS()
            self._emparejar('closing_par')
            self._parse_ENCADENADO_EXPR()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'and' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_bra' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'closing_par' or self._token_tipo() == 'colon' or self._token_tipo() == 'comma' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'decrement' or self._token_tipo() == 'div' or self._token_tipo() == 'elegir' or self._token_tipo() == 'equal' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'geq' or self._token_tipo() == 'greater' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'increment' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'leq' or self._token_tipo() == 'less' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mod' or self._token_tipo() == 'mut' or self._token_tipo() == 'neq' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'or' or self._token_tipo() == 'para' or self._token_tipo() == 'period' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'power' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'strict_equal' or self._token_tipo() == 'strict_neq' or self._token_tipo() == 'ternary' or self._token_tipo() == 'times' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'and', 'caso', 'closing_bra', 'closing_key', 'closing_par', 'colon', 'comma', 'consola', 'const', 'continuar', 'crear', 'decrement', 'div', 'elegir', 'equal', 'falso', 'funcion', 'geq', 'greater', 'hacer', 'id', 'increment', 'indefinido', 'intentar', 'leq', 'less', 'mientras', 'minus', 'mod', 'mut', 'neq', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'or', 'para', 'period', 'plus', 'porDefecto', 'power', 'retornar', 'romper', 'semicolon', 'si', 'str', 'strict_equal', 'strict_neq', 'ternary', 'times', 'var', 'verdadero'])

    def _parse_EXPR(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR_OR()
            self._parse_TERNARIO_OPT()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'crear', 'falso', 'id', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_EXPR_ADD(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR_MUL()
            self._parse_EXPR_ADD_prima()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'crear', 'falso', 'id', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_EXPR_ADD_prima(self):
        if self._token_tipo() == 'plus':
            self._emparejar('plus')
            self._parse_EXPR_MUL()
            self._parse_EXPR_ADD_prima()
        elif self._token_tipo() == 'minus':
            self._emparejar('minus')
            self._parse_EXPR_MUL()
            self._parse_EXPR_ADD_prima()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'and' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_bra' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'closing_par' or self._token_tipo() == 'colon' or self._token_tipo() == 'comma' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'decrement' or self._token_tipo() == 'div' or self._token_tipo() == 'elegir' or self._token_tipo() == 'equal' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'geq' or self._token_tipo() == 'greater' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'increment' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'leq' or self._token_tipo() == 'less' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mod' or self._token_tipo() == 'mut' or self._token_tipo() == 'neq' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'or' or self._token_tipo() == 'para' or self._token_tipo() == 'period' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'power' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'strict_equal' or self._token_tipo() == 'strict_neq' or self._token_tipo() == 'ternary' or self._token_tipo() == 'times' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'and', 'caso', 'closing_bra', 'closing_key', 'closing_par', 'colon', 'comma', 'consola', 'const', 'continuar', 'crear', 'decrement', 'div', 'elegir', 'equal', 'falso', 'funcion', 'geq', 'greater', 'hacer', 'id', 'increment', 'indefinido', 'intentar', 'leq', 'less', 'mientras', 'minus', 'mod', 'mut', 'neq', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'or', 'para', 'period', 'plus', 'porDefecto', 'power', 'retornar', 'romper', 'semicolon', 'si', 'str', 'strict_equal', 'strict_neq', 'ternary', 'times', 'var', 'verdadero'])

    def _parse_EXPR_ADD_NK(self):
        if self._token_tipo() == 'Infinito' or self._token_tipo() == 'NuN' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR_MUL_NK()
            self._parse_EXPR_ADD_prima()
        else:
            self._error_sintaxis(['Infinito', 'NuN', 'crear', 'falso', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_EXPR_AND(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR_EQ()
            self._parse_EXPR_AND_prima()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'crear', 'falso', 'id', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_EXPR_AND_prima(self):
        if self._token_tipo() == 'and':
            self._emparejar('and')
            self._parse_EXPR_EQ()
            self._parse_EXPR_AND_prima()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'and' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_bra' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'closing_par' or self._token_tipo() == 'colon' or self._token_tipo() == 'comma' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'decrement' or self._token_tipo() == 'div' or self._token_tipo() == 'elegir' or self._token_tipo() == 'equal' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'geq' or self._token_tipo() == 'greater' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'increment' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'leq' or self._token_tipo() == 'less' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mod' or self._token_tipo() == 'mut' or self._token_tipo() == 'neq' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'or' or self._token_tipo() == 'para' or self._token_tipo() == 'period' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'power' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'strict_equal' or self._token_tipo() == 'strict_neq' or self._token_tipo() == 'ternary' or self._token_tipo() == 'times' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'and', 'caso', 'closing_bra', 'closing_key', 'closing_par', 'colon', 'comma', 'consola', 'const', 'continuar', 'crear', 'decrement', 'div', 'elegir', 'equal', 'falso', 'funcion', 'geq', 'greater', 'hacer', 'id', 'increment', 'indefinido', 'intentar', 'leq', 'less', 'mientras', 'minus', 'mod', 'mut', 'neq', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'or', 'para', 'period', 'plus', 'porDefecto', 'power', 'retornar', 'romper', 'semicolon', 'si', 'str', 'strict_equal', 'strict_neq', 'ternary', 'times', 'var', 'verdadero'])

    def _parse_EXPR_AND_NK(self):
        if self._token_tipo() == 'Infinito' or self._token_tipo() == 'NuN' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR_EQ_NK()
            self._parse_EXPR_AND_prima()
        else:
            self._error_sintaxis(['Infinito', 'NuN', 'crear', 'falso', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_EXPR_EQ(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR_REL()
            self._parse_EXPR_EQ_prima()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'crear', 'falso', 'id', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_EXPR_EQ_prima(self):
        if self._token_tipo() == 'equal':
            self._emparejar('equal')
            self._parse_EXPR_REL()
            self._parse_EXPR_EQ_prima()
        elif self._token_tipo() == 'neq':
            self._emparejar('neq')
            self._parse_EXPR_REL()
            self._parse_EXPR_EQ_prima()
        elif self._token_tipo() == 'strict_equal':
            self._emparejar('strict_equal')
            self._parse_EXPR_REL()
            self._parse_EXPR_EQ_prima()
        elif self._token_tipo() == 'strict_neq':
            self._emparejar('strict_neq')
            self._parse_EXPR_REL()
            self._parse_EXPR_EQ_prima()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'and' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_bra' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'closing_par' or self._token_tipo() == 'colon' or self._token_tipo() == 'comma' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'decrement' or self._token_tipo() == 'div' or self._token_tipo() == 'elegir' or self._token_tipo() == 'equal' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'geq' or self._token_tipo() == 'greater' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'increment' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'leq' or self._token_tipo() == 'less' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mod' or self._token_tipo() == 'mut' or self._token_tipo() == 'neq' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'or' or self._token_tipo() == 'para' or self._token_tipo() == 'period' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'power' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'strict_equal' or self._token_tipo() == 'strict_neq' or self._token_tipo() == 'ternary' or self._token_tipo() == 'times' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'and', 'caso', 'closing_bra', 'closing_key', 'closing_par', 'colon', 'comma', 'consola', 'const', 'continuar', 'crear', 'decrement', 'div', 'elegir', 'equal', 'falso', 'funcion', 'geq', 'greater', 'hacer', 'id', 'increment', 'indefinido', 'intentar', 'leq', 'less', 'mientras', 'minus', 'mod', 'mut', 'neq', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'or', 'para', 'period', 'plus', 'porDefecto', 'power', 'retornar', 'romper', 'semicolon', 'si', 'str', 'strict_equal', 'strict_neq', 'ternary', 'times', 'var', 'verdadero'])

    def _parse_EXPR_EQ_NK(self):
        if self._token_tipo() == 'Infinito' or self._token_tipo() == 'NuN' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR_REL_NK()
            self._parse_EXPR_EQ_prima()
        else:
            self._error_sintaxis(['Infinito', 'NuN', 'crear', 'falso', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_EXPR_MUL(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR_POW()
            self._parse_EXPR_MUL_prima()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'crear', 'falso', 'id', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_EXPR_MUL_prima(self):
        if self._token_tipo() == 'times':
            self._emparejar('times')
            self._parse_EXPR_POW()
            self._parse_EXPR_MUL_prima()
        elif self._token_tipo() == 'div':
            self._emparejar('div')
            self._parse_EXPR_POW()
            self._parse_EXPR_MUL_prima()
        elif self._token_tipo() == 'mod':
            self._emparejar('mod')
            self._parse_EXPR_POW()
            self._parse_EXPR_MUL_prima()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'and' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_bra' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'closing_par' or self._token_tipo() == 'colon' or self._token_tipo() == 'comma' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'decrement' or self._token_tipo() == 'div' or self._token_tipo() == 'elegir' or self._token_tipo() == 'equal' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'geq' or self._token_tipo() == 'greater' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'increment' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'leq' or self._token_tipo() == 'less' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mod' or self._token_tipo() == 'mut' or self._token_tipo() == 'neq' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'or' or self._token_tipo() == 'para' or self._token_tipo() == 'period' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'power' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'strict_equal' or self._token_tipo() == 'strict_neq' or self._token_tipo() == 'ternary' or self._token_tipo() == 'times' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'and', 'caso', 'closing_bra', 'closing_key', 'closing_par', 'colon', 'comma', 'consola', 'const', 'continuar', 'crear', 'decrement', 'div', 'elegir', 'equal', 'falso', 'funcion', 'geq', 'greater', 'hacer', 'id', 'increment', 'indefinido', 'intentar', 'leq', 'less', 'mientras', 'minus', 'mod', 'mut', 'neq', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'or', 'para', 'period', 'plus', 'porDefecto', 'power', 'retornar', 'romper', 'semicolon', 'si', 'str', 'strict_equal', 'strict_neq', 'ternary', 'times', 'var', 'verdadero'])

    def _parse_EXPR_MUL_NK(self):
        if self._token_tipo() == 'Infinito' or self._token_tipo() == 'NuN' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR_POW_NK()
            self._parse_EXPR_MUL_prima()
        else:
            self._error_sintaxis(['Infinito', 'NuN', 'crear', 'falso', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_EXPR_NO_KEY(self):
        if self._token_tipo() == 'Infinito' or self._token_tipo() == 'NuN' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR_OR_NK()
            self._parse_TERNARIO_OPT()
        else:
            self._error_sintaxis(['Infinito', 'NuN', 'crear', 'falso', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_EXPR_OR(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR_AND()
            self._parse_EXPR_OR_prima()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'crear', 'falso', 'id', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_EXPR_OR_prima(self):
        if self._token_tipo() == 'or':
            self._emparejar('or')
            self._parse_EXPR_AND()
            self._parse_EXPR_OR_prima()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'and' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_bra' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'closing_par' or self._token_tipo() == 'colon' or self._token_tipo() == 'comma' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'decrement' or self._token_tipo() == 'div' or self._token_tipo() == 'elegir' or self._token_tipo() == 'equal' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'geq' or self._token_tipo() == 'greater' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'increment' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'leq' or self._token_tipo() == 'less' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mod' or self._token_tipo() == 'mut' or self._token_tipo() == 'neq' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'or' or self._token_tipo() == 'para' or self._token_tipo() == 'period' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'power' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'strict_equal' or self._token_tipo() == 'strict_neq' or self._token_tipo() == 'ternary' or self._token_tipo() == 'times' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'and', 'caso', 'closing_bra', 'closing_key', 'closing_par', 'colon', 'comma', 'consola', 'const', 'continuar', 'crear', 'decrement', 'div', 'elegir', 'equal', 'falso', 'funcion', 'geq', 'greater', 'hacer', 'id', 'increment', 'indefinido', 'intentar', 'leq', 'less', 'mientras', 'minus', 'mod', 'mut', 'neq', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'or', 'para', 'period', 'plus', 'porDefecto', 'power', 'retornar', 'romper', 'semicolon', 'si', 'str', 'strict_equal', 'strict_neq', 'ternary', 'times', 'var', 'verdadero'])

    def _parse_EXPR_OR_NK(self):
        if self._token_tipo() == 'Infinito' or self._token_tipo() == 'NuN' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR_AND_NK()
            self._parse_EXPR_OR_prima()
        else:
            self._error_sintaxis(['Infinito', 'NuN', 'crear', 'falso', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_EXPR_POSTFIX(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR_PRIMARIO()
            self._parse_EXPR_POSTFIX_prima()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'crear', 'falso', 'id', 'indefinido', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'str', 'verdadero'])

    def _parse_EXPR_POSTFIX_prima(self):
        if self._token_tipo() == 'period':
            self._emparejar('period')
            self._emparejar('id')
            self._parse_EXPR_POSTFIX_CALL_prima()
        elif self._token_tipo() == 'opening_bra':
            self._emparejar('opening_bra')
            self._parse_EXPR()
            self._emparejar('closing_bra')
            self._parse_EXPR_POSTFIX_prima()
        elif self._token_tipo() == 'increment':
            self._emparejar('increment')
            self._parse_EXPR_POSTFIX_prima()
        elif self._token_tipo() == 'decrement':
            self._emparejar('decrement')
            self._parse_EXPR_POSTFIX_prima()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'and' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_bra' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'closing_par' or self._token_tipo() == 'colon' or self._token_tipo() == 'comma' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'decrement' or self._token_tipo() == 'div' or self._token_tipo() == 'elegir' or self._token_tipo() == 'equal' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'geq' or self._token_tipo() == 'greater' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'increment' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'leq' or self._token_tipo() == 'less' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mod' or self._token_tipo() == 'mut' or self._token_tipo() == 'neq' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'or' or self._token_tipo() == 'para' or self._token_tipo() == 'period' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'power' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'strict_equal' or self._token_tipo() == 'strict_neq' or self._token_tipo() == 'ternary' or self._token_tipo() == 'times' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'and', 'caso', 'closing_bra', 'closing_key', 'closing_par', 'colon', 'comma', 'consola', 'const', 'continuar', 'crear', 'decrement', 'div', 'elegir', 'equal', 'falso', 'funcion', 'geq', 'greater', 'hacer', 'id', 'increment', 'indefinido', 'intentar', 'leq', 'less', 'mientras', 'minus', 'mod', 'mut', 'neq', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'or', 'para', 'period', 'plus', 'porDefecto', 'power', 'retornar', 'romper', 'semicolon', 'si', 'str', 'strict_equal', 'strict_neq', 'ternary', 'times', 'var', 'verdadero'])

    def _parse_EXPR_POSTFIX_CALL_prima(self):
        if self._token_tipo() == 'opening_par':
            self._emparejar('opening_par')
            self._parse_ARGS()
            self._emparejar('closing_par')
            self._parse_EXPR_POSTFIX_prima()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'and' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_bra' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'closing_par' or self._token_tipo() == 'colon' or self._token_tipo() == 'comma' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'decrement' or self._token_tipo() == 'div' or self._token_tipo() == 'elegir' or self._token_tipo() == 'equal' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'geq' or self._token_tipo() == 'greater' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'increment' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'leq' or self._token_tipo() == 'less' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mod' or self._token_tipo() == 'mut' or self._token_tipo() == 'neq' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'or' or self._token_tipo() == 'para' or self._token_tipo() == 'period' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'power' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'strict_equal' or self._token_tipo() == 'strict_neq' or self._token_tipo() == 'ternary' or self._token_tipo() == 'times' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            self._parse_EXPR_POSTFIX_prima()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'and', 'caso', 'closing_bra', 'closing_key', 'closing_par', 'colon', 'comma', 'consola', 'const', 'continuar', 'crear', 'decrement', 'div', 'elegir', 'equal', 'falso', 'funcion', 'geq', 'greater', 'hacer', 'id', 'increment', 'indefinido', 'intentar', 'leq', 'less', 'mientras', 'minus', 'mod', 'mut', 'neq', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'or', 'para', 'period', 'plus', 'porDefecto', 'power', 'retornar', 'romper', 'semicolon', 'si', 'str', 'strict_equal', 'strict_neq', 'ternary', 'times', 'var', 'verdadero'])

    def _parse_EXPR_POSTFIX_NK(self):
        if self._token_tipo() == 'Infinito' or self._token_tipo() == 'NuN' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR_PRIMARIO_NK()
            self._parse_EXPR_POSTFIX_prima()
        else:
            self._error_sintaxis(['Infinito', 'NuN', 'crear', 'falso', 'indefinido', 'nulo', 'num', 'opening_bra', 'opening_par', 'str', 'verdadero'])

    def _parse_EXPR_POW(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR_UNARY()
            self._parse_EXPR_POW_prima()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'crear', 'falso', 'id', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_EXPR_POW_prima(self):
        if self._token_tipo() == 'power':
            self._emparejar('power')
            self._parse_EXPR_UNARY()
            self._parse_EXPR_POW_prima()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'and' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_bra' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'closing_par' or self._token_tipo() == 'colon' or self._token_tipo() == 'comma' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'decrement' or self._token_tipo() == 'div' or self._token_tipo() == 'elegir' or self._token_tipo() == 'equal' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'geq' or self._token_tipo() == 'greater' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'increment' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'leq' or self._token_tipo() == 'less' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mod' or self._token_tipo() == 'mut' or self._token_tipo() == 'neq' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'or' or self._token_tipo() == 'para' or self._token_tipo() == 'period' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'power' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'strict_equal' or self._token_tipo() == 'strict_neq' or self._token_tipo() == 'ternary' or self._token_tipo() == 'times' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'and', 'caso', 'closing_bra', 'closing_key', 'closing_par', 'colon', 'comma', 'consola', 'const', 'continuar', 'crear', 'decrement', 'div', 'elegir', 'equal', 'falso', 'funcion', 'geq', 'greater', 'hacer', 'id', 'increment', 'indefinido', 'intentar', 'leq', 'less', 'mientras', 'minus', 'mod', 'mut', 'neq', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'or', 'para', 'period', 'plus', 'porDefecto', 'power', 'retornar', 'romper', 'semicolon', 'si', 'str', 'strict_equal', 'strict_neq', 'ternary', 'times', 'var', 'verdadero'])

    def _parse_EXPR_POW_NK(self):
        if self._token_tipo() == 'Infinito' or self._token_tipo() == 'NuN' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR_UNARY_NK()
            self._parse_EXPR_POW_prima()
        else:
            self._error_sintaxis(['Infinito', 'NuN', 'crear', 'falso', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_EXPR_PRIMARIO(self):
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
        elif self._token_tipo() == 'id':
            self._emparejar('id')
            self._parse_ID_EXPR_SUF()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'Numero':
            self._parse_NOMBRE_OBJETO()
            self._emparejar('period')
            self._emparejar('id')
            self._emparejar('opening_par')
            self._parse_ARGS()
            self._emparejar('closing_par')
        elif self._token_tipo() == 'opening_par':
            self._emparejar('opening_par')
            self._parse_PAR_EXPR_O_ARROW()
        elif self._token_tipo() == 'opening_bra':
            self._emparejar('opening_bra')
            self._parse_LISTA_EXPR()
            self._emparejar('closing_bra')
        elif self._token_tipo() == 'opening_key':
            self._emparejar('opening_key')
            self._parse_OBJ_PROPS()
            self._emparejar('closing_key')
        elif self._token_tipo() == 'crear':
            self._emparejar('crear')
            self._parse_CREAR_TARGET()
            self._emparejar('opening_par')
            self._parse_ARGS()
            self._emparejar('closing_par')
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'crear', 'falso', 'id', 'indefinido', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'str', 'verdadero'])

    def _parse_EXPR_PRIMARIO_NK(self):
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
            self._parse_PAR_EXPR_O_ARROW()
        elif self._token_tipo() == 'opening_bra':
            self._emparejar('opening_bra')
            self._parse_LISTA_EXPR()
            self._emparejar('closing_bra')
        elif self._token_tipo() == 'crear':
            self._emparejar('crear')
            self._parse_CREAR_TARGET()
            self._emparejar('opening_par')
            self._parse_ARGS()
            self._emparejar('closing_par')
        else:
            self._error_sintaxis(['Infinito', 'NuN', 'crear', 'falso', 'indefinido', 'nulo', 'num', 'opening_bra', 'opening_par', 'str', 'verdadero'])

    def _parse_EXPR_REL(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR_ADD()
            self._parse_EXPR_REL_prima()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'crear', 'falso', 'id', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_EXPR_REL_prima(self):
        if self._token_tipo() == 'less':
            self._emparejar('less')
            self._parse_EXPR_ADD()
            self._parse_EXPR_REL_prima()
        elif self._token_tipo() == 'greater':
            self._emparejar('greater')
            self._parse_EXPR_ADD()
            self._parse_EXPR_REL_prima()
        elif self._token_tipo() == 'leq':
            self._emparejar('leq')
            self._parse_EXPR_ADD()
            self._parse_EXPR_REL_prima()
        elif self._token_tipo() == 'geq':
            self._emparejar('geq')
            self._parse_EXPR_ADD()
            self._parse_EXPR_REL_prima()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'and' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_bra' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'closing_par' or self._token_tipo() == 'colon' or self._token_tipo() == 'comma' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'decrement' or self._token_tipo() == 'div' or self._token_tipo() == 'elegir' or self._token_tipo() == 'equal' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'geq' or self._token_tipo() == 'greater' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'increment' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'leq' or self._token_tipo() == 'less' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mod' or self._token_tipo() == 'mut' or self._token_tipo() == 'neq' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'or' or self._token_tipo() == 'para' or self._token_tipo() == 'period' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'power' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'strict_equal' or self._token_tipo() == 'strict_neq' or self._token_tipo() == 'ternary' or self._token_tipo() == 'times' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'and', 'caso', 'closing_bra', 'closing_key', 'closing_par', 'colon', 'comma', 'consola', 'const', 'continuar', 'crear', 'decrement', 'div', 'elegir', 'equal', 'falso', 'funcion', 'geq', 'greater', 'hacer', 'id', 'increment', 'indefinido', 'intentar', 'leq', 'less', 'mientras', 'minus', 'mod', 'mut', 'neq', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'or', 'para', 'period', 'plus', 'porDefecto', 'power', 'retornar', 'romper', 'semicolon', 'si', 'str', 'strict_equal', 'strict_neq', 'ternary', 'times', 'var', 'verdadero'])

    def _parse_EXPR_REL_NK(self):
        if self._token_tipo() == 'Infinito' or self._token_tipo() == 'NuN' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR_ADD_NK()
            self._parse_EXPR_REL_prima()
        else:
            self._error_sintaxis(['Infinito', 'NuN', 'crear', 'falso', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_EXPR_STMT(self):
        if self._token_tipo() == 'Infinito' or self._token_tipo() == 'NuN' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR_NO_KEY()
            self._parse_SEMI_OPT()
        else:
            self._error_sintaxis(['Infinito', 'NuN', 'crear', 'falso', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_EXPR_UNARY(self):
        if self._token_tipo() == 'not':
            self._emparejar('not')
            self._parse_EXPR_UNARY()
        elif self._token_tipo() == 'minus':
            self._emparejar('minus')
            self._parse_EXPR_UNARY()
        elif self._token_tipo() == 'plus':
            self._emparejar('plus')
            self._parse_EXPR_UNARY()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR_POSTFIX()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'crear', 'falso', 'id', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_EXPR_UNARY_NK(self):
        if self._token_tipo() == 'not':
            self._emparejar('not')
            self._parse_EXPR_UNARY()
        elif self._token_tipo() == 'minus':
            self._emparejar('minus')
            self._parse_EXPR_UNARY()
        elif self._token_tipo() == 'plus':
            self._emparejar('plus')
            self._parse_EXPR_UNARY()
        elif self._token_tipo() == 'Infinito' or self._token_tipo() == 'NuN' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR_POSTFIX_NK()
        else:
            self._error_sintaxis(['Infinito', 'NuN', 'crear', 'falso', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_FINALMENTE_OPT(self):
        if self._token_tipo() == 'finalmente':
            self._emparejar('finalmente')
            self._parse_BLOQUE()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mut' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'para' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'caso', 'closing_key', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'finalmente', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'minus', 'mut', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'para', 'plus', 'porDefecto', 'retornar', 'romper', 'semicolon', 'si', 'str', 'var', 'verdadero'])

    def _parse_FUNCION_DECL(self):
        if self._token_tipo() == 'funcion':
            self._emparejar('funcion')
            self._emparejar('id')
            self._emparejar('opening_par')
            self._parse_PARAMS()
            self._emparejar('closing_par')
            self._parse_BLOQUE()
        else:
            self._error_sintaxis(['funcion'])

    def _parse_HACER_STMT(self):
        if self._token_tipo() == 'hacer':
            self._emparejar('hacer')
            self._parse_BLOQUE()
            self._emparejar('mientras')
            self._emparejar('opening_par')
            self._parse_EXPR()
            self._emparejar('closing_par')
            self._parse_SEMI_OPT()
        else:
            self._error_sintaxis(['hacer'])

    def _parse_ID_EXPR_SUF(self):
        if self._token_tipo() == 'opening_par':
            self._emparejar('opening_par')
            self._parse_ARGS()
            self._emparejar('closing_par')
            self._parse_ENCADENADO_EXPR()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'and' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_bra' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'closing_par' or self._token_tipo() == 'colon' or self._token_tipo() == 'comma' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'decrement' or self._token_tipo() == 'div' or self._token_tipo() == 'elegir' or self._token_tipo() == 'equal' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'geq' or self._token_tipo() == 'greater' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'increment' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'leq' or self._token_tipo() == 'less' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mod' or self._token_tipo() == 'mut' or self._token_tipo() == 'neq' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'or' or self._token_tipo() == 'para' or self._token_tipo() == 'period' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'power' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'strict_equal' or self._token_tipo() == 'strict_neq' or self._token_tipo() == 'ternary' or self._token_tipo() == 'times' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'and', 'caso', 'closing_bra', 'closing_key', 'closing_par', 'colon', 'comma', 'consola', 'const', 'continuar', 'crear', 'decrement', 'div', 'elegir', 'equal', 'falso', 'funcion', 'geq', 'greater', 'hacer', 'id', 'increment', 'indefinido', 'intentar', 'leq', 'less', 'mientras', 'minus', 'mod', 'mut', 'neq', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'or', 'para', 'period', 'plus', 'porDefecto', 'power', 'retornar', 'romper', 'semicolon', 'si', 'str', 'strict_equal', 'strict_neq', 'ternary', 'times', 'var', 'verdadero'])

    def _parse_INTENTAR_STMT(self):
        if self._token_tipo() == 'intentar':
            self._emparejar('intentar')
            self._parse_BLOQUE()
            self._emparejar('capturar')
            self._emparejar('opening_par')
            self._emparejar('id')
            self._emparejar('closing_par')
            self._parse_BLOQUE()
            self._parse_FINALMENTE_OPT()
        else:
            self._error_sintaxis(['intentar'])

    def _parse_LISTA_EXPR(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR()
            self._parse_LISTA_EXPR_RESTO()
        elif self._token_tipo() == 'closing_bra':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'closing_bra', 'crear', 'falso', 'id', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_LISTA_EXPR_RESTO(self):
        if self._token_tipo() == 'comma':
            self._emparejar('comma')
            self._parse_EXPR()
            self._parse_LISTA_EXPR_RESTO()
        elif self._token_tipo() == 'closing_bra':
            pass
        else:
            self._error_sintaxis(['closing_bra', 'comma'])

    def _parse_METODO_CONSOLA(self):
        if self._token_tipo() == 'escribir':
            self._emparejar('escribir')
        elif self._token_tipo() == 'error':
            self._emparejar('error')
        elif self._token_tipo() == 'info':
            self._emparejar('info')
        elif self._token_tipo() == 'agrupar':
            self._emparejar('agrupar')
        elif self._token_tipo() == 'limpiar':
            self._emparejar('limpiar')
        elif self._token_tipo() == 'tabla':
            self._emparejar('tabla')
        elif self._token_tipo() == 'afirmar':
            self._emparejar('afirmar')
        else:
            self._error_sintaxis(['afirmar', 'agrupar', 'error', 'escribir', 'info', 'limpiar', 'tabla'])

    def _parse_MIENTRAS_STMT(self):
        if self._token_tipo() == 'mientras':
            self._emparejar('mientras')
            self._emparejar('opening_par')
            self._parse_EXPR()
            self._emparejar('closing_par')
            self._parse_BLOQUE()
        else:
            self._error_sintaxis(['mientras'])

    def _parse_NOMBRE_OBJETO(self):
        if self._token_tipo() == 'Numero':
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
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Mate', 'Matriz', 'Numero'])

    def _parse_OBJETO_STMT(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'Numero':
            self._parse_NOMBRE_OBJETO()
            self._emparejar('period')
            self._emparejar('id')
            self._emparejar('opening_par')
            self._parse_ARGS()
            self._emparejar('closing_par')
            self._parse_SEMI_OPT()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Mate', 'Matriz', 'Numero'])

    def _parse_OBJ_PROP(self):
        if self._token_tipo() == 'id':
            self._emparejar('id')
            self._parse_OBJ_PROP_VAL()
        elif self._token_tipo() == 'str':
            self._emparejar('str')
            self._emparejar('colon')
            self._parse_EXPR()
        elif self._token_tipo() == 'num':
            self._emparejar('num')
            self._emparejar('colon')
            self._parse_EXPR()
        else:
            self._error_sintaxis(['id', 'num', 'str'])

    def _parse_OBJ_PROPS(self):
        if self._token_tipo() == 'id' or self._token_tipo() == 'num' or self._token_tipo() == 'str':
            self._parse_OBJ_PROP()
            self._parse_OBJ_PROPS_RESTO()
        elif self._token_tipo() == 'closing_key':
            pass
        else:
            self._error_sintaxis(['closing_key', 'id', 'num', 'str'])

    def _parse_OBJ_PROPS_CONT(self):
        if self._token_tipo() == 'id' or self._token_tipo() == 'num' or self._token_tipo() == 'str':
            self._parse_OBJ_PROP()
            self._parse_OBJ_PROPS_RESTO()
        elif self._token_tipo() == 'closing_key':
            pass
        else:
            self._error_sintaxis(['closing_key', 'id', 'num', 'str'])

    def _parse_OBJ_PROPS_RESTO(self):
        if self._token_tipo() == 'comma':
            self._emparejar('comma')
            self._parse_OBJ_PROPS_CONT()
        elif self._token_tipo() == 'closing_key':
            pass
        else:
            self._error_sintaxis(['closing_key', 'comma'])

    def _parse_OBJ_PROP_VAL(self):
        if self._token_tipo() == 'colon':
            self._emparejar('colon')
            self._parse_EXPR()
        elif self._token_tipo() == 'opening_par':
            self._emparejar('opening_par')
            self._parse_PARAMS()
            self._emparejar('closing_par')
            self._parse_BLOQUE()
        else:
            self._error_sintaxis(['colon', 'opening_par'])

    def _parse_P(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mut' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'para' or self._token_tipo() == 'plus' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            self._parse_SL()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'minus', 'mut', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'para', 'plus', 'retornar', 'romper', 'semicolon', 'si', 'str', 'var', 'verdadero'])

    def _parse_PARAMS(self):
        if self._token_tipo() == 'id':
            self._emparejar('id')
            self._parse_PARAMS_RESTO()
        elif self._token_tipo() == 'closing_par':
            pass
        else:
            self._error_sintaxis(['closing_par', 'id'])

    def _parse_PARAMS_RESTO(self):
        if self._token_tipo() == 'comma':
            self._emparejar('comma')
            self._emparejar('id')
            self._parse_PARAMS_RESTO()
        elif self._token_tipo() == 'closing_par':
            pass
        else:
            self._error_sintaxis(['closing_par', 'comma'])

    def _parse_PARA_COND(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR()
        elif self._token_tipo() == 'semicolon':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'crear', 'falso', 'id', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'semicolon', 'str', 'verdadero'])

    def _parse_PARA_INIT(self):
        if self._token_tipo() == 'var':
            self._emparejar('var')
            self._emparejar('id')
            self._emparejar('assign')
            self._parse_EXPR()
        elif self._token_tipo() == 'mut':
            self._emparejar('mut')
            self._emparejar('id')
            self._emparejar('assign')
            self._parse_EXPR()
        elif self._token_tipo() == 'id':
            self._emparejar('id')
            self._emparejar('assign')
            self._parse_EXPR()
        elif self._token_tipo() == 'semicolon':
            pass
        else:
            self._error_sintaxis(['id', 'mut', 'semicolon', 'var'])

    def _parse_PARA_PASO(self):
        if self._token_tipo() == 'id':
            self._emparejar('id')
            self._parse_PARA_PASO_SUF()
        elif self._token_tipo() == 'closing_par':
            pass
        else:
            self._error_sintaxis(['closing_par', 'id'])

    def _parse_PARA_PASO_SUF(self):
        if self._token_tipo() == 'assign':
            self._emparejar('assign')
            self._parse_EXPR()
        elif self._token_tipo() == 'plus_assign':
            self._emparejar('plus_assign')
            self._parse_EXPR()
        elif self._token_tipo() == 'minus_assign':
            self._emparejar('minus_assign')
            self._parse_EXPR()
        elif self._token_tipo() == 'times_assign':
            self._emparejar('times_assign')
            self._parse_EXPR()
        elif self._token_tipo() == 'div_assign':
            self._emparejar('div_assign')
            self._parse_EXPR()
        elif self._token_tipo() == 'mod_assign':
            self._emparejar('mod_assign')
            self._parse_EXPR()
        elif self._token_tipo() == 'power_assign':
            self._emparejar('power_assign')
            self._parse_EXPR()
        elif self._token_tipo() == 'increment':
            self._emparejar('increment')
        elif self._token_tipo() == 'decrement':
            self._emparejar('decrement')
        else:
            self._error_sintaxis(['assign', 'decrement', 'div_assign', 'increment', 'minus_assign', 'mod_assign', 'plus_assign', 'power_assign', 'times_assign'])

    def _parse_PARA_STMT(self):
        if self._token_tipo() == 'para':
            self._emparejar('para')
            self._emparejar('opening_par')
            self._parse_PARA_INIT()
            self._emparejar('semicolon')
            self._parse_PARA_COND()
            self._emparejar('semicolon')
            self._parse_PARA_PASO()
            self._emparejar('closing_par')
            self._parse_BLOQUE()
        else:
            self._error_sintaxis(['para'])

    def _parse_PAR_EXPR_O_ARROW(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR()
            self._parse_PAR_RESTO()
            self._emparejar('closing_par')
            self._parse_ARROW_OPT()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'crear', 'falso', 'id', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'str', 'verdadero'])

    def _parse_PAR_RESTO(self):
        if self._token_tipo() == 'comma':
            self._emparejar('comma')
            self._parse_EXPR()
            self._parse_PAR_RESTO()
        elif self._token_tipo() == 'closing_par':
            pass
        else:
            self._error_sintaxis(['closing_par', 'comma'])

    def _parse_POSTFIX_LLAMADA(self):
        if self._token_tipo() == 'opening_par':
            self._emparejar('opening_par')
            self._parse_ARGS()
            self._emparejar('closing_par')
            self._parse_ENCADENADO()
        elif self._token_tipo() == 'period':
            self._emparejar('period')
            self._emparejar('id')
            self._parse_POSTFIX_LLAMADA()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mut' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'para' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'caso', 'closing_key', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'minus', 'mut', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'para', 'period', 'plus', 'porDefecto', 'retornar', 'romper', 'semicolon', 'si', 'str', 'var', 'verdadero'])

    def _parse_RETORNAR_STMT(self):
        if self._token_tipo() == 'retornar':
            self._emparejar('retornar')
            self._parse_RETORNAR_VAL()
        else:
            self._error_sintaxis(['retornar'])

    def _parse_RETORNAR_VAL(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR()
            self._parse_SEMI_OPT()
        elif self._token_tipo() == 'semicolon':
            self._emparejar('semicolon')
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'crear', 'falso', 'id', 'indefinido', 'minus', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'plus', 'semicolon', 'str', 'verdadero'])

    def _parse_ROMPER_OPT(self):
        if self._token_tipo() == 'romper':
            self._emparejar('romper')
            self._parse_SEMI_OPT()
        elif self._token_tipo() == 'caso' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'porDefecto':
            pass
        else:
            self._error_sintaxis(['caso', 'closing_key', 'porDefecto', 'romper'])

    def _parse_ROMPER_OPT2(self):
        if self._token_tipo() == 'romper':
            self._emparejar('romper')
            self._parse_SEMI_OPT()
        elif self._token_tipo() == 'closing_key':
            pass
        else:
            self._error_sintaxis(['closing_key', 'romper'])

    def _parse_ROMPER_STMT(self):
        if self._token_tipo() == 'romper':
            self._emparejar('romper')
            self._parse_SEMI_OPT()
        else:
            self._error_sintaxis(['romper'])

    def _parse_S(self):
        if self._token_tipo() == 'semicolon':
            self._emparejar('semicolon')
        elif self._token_tipo() == 'mut' or self._token_tipo() == 'var':
            self._parse_DECL()
        elif self._token_tipo() == 'const':
            self._parse_CONST_DECL()
        elif self._token_tipo() == 'id':
            self._parse_ASIGN_O_LLAMADA()
        elif self._token_tipo() == 'consola':
            self._parse_CONSOLA_STMT()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'Numero':
            self._parse_OBJETO_STMT()
        elif self._token_tipo() == 'Infinito' or self._token_tipo() == 'NuN' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR_STMT()
        elif self._token_tipo() == 'si':
            self._parse_SI_STMT()
        elif self._token_tipo() == 'elegir':
            self._parse_ELEGIR_STMT()
        elif self._token_tipo() == 'mientras':
            self._parse_MIENTRAS_STMT()
        elif self._token_tipo() == 'hacer':
            self._parse_HACER_STMT()
        elif self._token_tipo() == 'para':
            self._parse_PARA_STMT()
        elif self._token_tipo() == 'retornar':
            self._parse_RETORNAR_STMT()
        elif self._token_tipo() == 'romper':
            self._parse_ROMPER_STMT()
        elif self._token_tipo() == 'continuar':
            self._parse_CONTINUAR_STMT()
        elif self._token_tipo() == 'funcion':
            self._parse_FUNCION_DECL()
        elif self._token_tipo() == 'intentar':
            self._parse_INTENTAR_STMT()
        elif self._token_tipo() == 'opening_key':
            self._parse_BLOQUE()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'minus', 'mut', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'para', 'plus', 'retornar', 'romper', 'semicolon', 'si', 'str', 'var', 'verdadero'])

    def _parse_SEMI_OPT(self):
        if self._token_tipo() == 'semicolon':
            self._emparejar('semicolon')
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mut' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'para' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'caso', 'closing_key', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'minus', 'mut', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'para', 'plus', 'porDefecto', 'retornar', 'romper', 'semicolon', 'si', 'str', 'var', 'verdadero'])

    def _parse_SINO_CUERPO(self):
        if self._token_tipo() == 'si':
            self._parse_SI_STMT()
        elif self._token_tipo() == 'opening_key':
            self._parse_BLOQUE()
        else:
            self._error_sintaxis(['opening_key', 'si'])

    def _parse_SINO_OPT(self):
        if self._token_tipo() == 'sino':
            self._emparejar('sino')
            self._parse_SINO_CUERPO()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mut' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'para' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'caso', 'closing_key', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'minus', 'mut', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'para', 'plus', 'porDefecto', 'retornar', 'romper', 'semicolon', 'si', 'sino', 'str', 'var', 'verdadero'])

    def _parse_SI_STMT(self):
        if self._token_tipo() == 'si':
            self._emparejar('si')
            self._emparejar('opening_par')
            self._parse_EXPR()
            self._emparejar('closing_par')
            self._parse_BLOQUE()
            self._parse_SINO_OPT()
        else:
            self._error_sintaxis(['si'])

    def _parse_SL(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mut' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'para' or self._token_tipo() == 'plus' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            self._parse_S()
            self._parse_SL()
        elif self._token_tipo() == 'EOF' or self._token_tipo() == 'closing_key':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'closing_key', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'minus', 'mut', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'para', 'plus', 'retornar', 'romper', 'semicolon', 'si', 'str', 'var', 'verdadero'])

    def _parse_SL_CASO(self):
        if self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mut' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'para' or self._token_tipo() == 'plus' or self._token_tipo() == 'retornar' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            self._parse_S_CASO()
            self._parse_SL_CASO()
        elif self._token_tipo() == 'caso' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'romper':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'caso', 'closing_key', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'minus', 'mut', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'para', 'plus', 'porDefecto', 'retornar', 'romper', 'semicolon', 'si', 'str', 'var', 'verdadero'])

    def _parse_SUBSCRIPT_SUF(self):
        if self._token_tipo() == 'assign':
            self._emparejar('assign')
            self._parse_EXPR()
        elif self._token_tipo() == 'opening_par':
            self._emparejar('opening_par')
            self._parse_ARGS()
            self._emparejar('closing_par')
            self._parse_ENCADENADO()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'elegir' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mut' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'para' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'assign', 'caso', 'closing_key', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'minus', 'mut', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'para', 'plus', 'porDefecto', 'retornar', 'romper', 'semicolon', 'si', 'str', 'var', 'verdadero'])

    def _parse_S_CASO(self):
        if self._token_tipo() == 'semicolon':
            self._emparejar('semicolon')
        elif self._token_tipo() == 'mut' or self._token_tipo() == 'var':
            self._parse_DECL()
        elif self._token_tipo() == 'const':
            self._parse_CONST_DECL()
        elif self._token_tipo() == 'id':
            self._parse_ASIGN_O_LLAMADA()
        elif self._token_tipo() == 'consola':
            self._parse_CONSOLA_STMT()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'Numero':
            self._parse_OBJETO_STMT()
        elif self._token_tipo() == 'Infinito' or self._token_tipo() == 'NuN' or self._token_tipo() == 'crear' or self._token_tipo() == 'falso' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'minus' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'plus' or self._token_tipo() == 'str' or self._token_tipo() == 'verdadero':
            self._parse_EXPR_STMT()
        elif self._token_tipo() == 'si':
            self._parse_SI_STMT()
        elif self._token_tipo() == 'elegir':
            self._parse_ELEGIR_STMT()
        elif self._token_tipo() == 'mientras':
            self._parse_MIENTRAS_STMT()
        elif self._token_tipo() == 'hacer':
            self._parse_HACER_STMT()
        elif self._token_tipo() == 'para':
            self._parse_PARA_STMT()
        elif self._token_tipo() == 'retornar':
            self._parse_RETORNAR_STMT()
        elif self._token_tipo() == 'continuar':
            self._parse_CONTINUAR_STMT()
        elif self._token_tipo() == 'funcion':
            self._parse_FUNCION_DECL()
        elif self._token_tipo() == 'intentar':
            self._parse_INTENTAR_STMT()
        elif self._token_tipo() == 'opening_key':
            self._parse_BLOQUE()
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'consola', 'const', 'continuar', 'crear', 'elegir', 'falso', 'funcion', 'hacer', 'id', 'indefinido', 'intentar', 'mientras', 'minus', 'mut', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'para', 'plus', 'retornar', 'semicolon', 'si', 'str', 'var', 'verdadero'])

    def _parse_TERNARIO_OPT(self):
        if self._token_tipo() == 'ternary':
            self._emparejar('ternary')
            self._parse_EXPR()
            self._emparejar('colon')
            self._parse_EXPR()
        elif self._token_tipo() == 'Arreglo' or self._token_tipo() == 'Booleano' or self._token_tipo() == 'Cadena' or self._token_tipo() == 'EOF' or self._token_tipo() == 'Infinito' or self._token_tipo() == 'Mate' or self._token_tipo() == 'Matriz' or self._token_tipo() == 'NuN' or self._token_tipo() == 'Numero' or self._token_tipo() == 'and' or self._token_tipo() == 'caso' or self._token_tipo() == 'closing_bra' or self._token_tipo() == 'closing_key' or self._token_tipo() == 'closing_par' or self._token_tipo() == 'colon' or self._token_tipo() == 'comma' or self._token_tipo() == 'consola' or self._token_tipo() == 'const' or self._token_tipo() == 'continuar' or self._token_tipo() == 'crear' or self._token_tipo() == 'decrement' or self._token_tipo() == 'div' or self._token_tipo() == 'elegir' or self._token_tipo() == 'equal' or self._token_tipo() == 'falso' or self._token_tipo() == 'funcion' or self._token_tipo() == 'geq' or self._token_tipo() == 'greater' or self._token_tipo() == 'hacer' or self._token_tipo() == 'id' or self._token_tipo() == 'increment' or self._token_tipo() == 'indefinido' or self._token_tipo() == 'intentar' or self._token_tipo() == 'leq' or self._token_tipo() == 'less' or self._token_tipo() == 'mientras' or self._token_tipo() == 'minus' or self._token_tipo() == 'mod' or self._token_tipo() == 'mut' or self._token_tipo() == 'neq' or self._token_tipo() == 'not' or self._token_tipo() == 'nulo' or self._token_tipo() == 'num' or self._token_tipo() == 'opening_bra' or self._token_tipo() == 'opening_key' or self._token_tipo() == 'opening_par' or self._token_tipo() == 'or' or self._token_tipo() == 'para' or self._token_tipo() == 'period' or self._token_tipo() == 'plus' or self._token_tipo() == 'porDefecto' or self._token_tipo() == 'power' or self._token_tipo() == 'retornar' or self._token_tipo() == 'romper' or self._token_tipo() == 'semicolon' or self._token_tipo() == 'si' or self._token_tipo() == 'str' or self._token_tipo() == 'strict_equal' or self._token_tipo() == 'strict_neq' or self._token_tipo() == 'ternary' or self._token_tipo() == 'times' or self._token_tipo() == 'var' or self._token_tipo() == 'verdadero':
            pass
        else:
            self._error_sintaxis(['Arreglo', 'Booleano', 'Cadena', 'EOF', 'Infinito', 'Mate', 'Matriz', 'NuN', 'Numero', 'and', 'caso', 'closing_bra', 'closing_key', 'closing_par', 'colon', 'comma', 'consola', 'const', 'continuar', 'crear', 'decrement', 'div', 'elegir', 'equal', 'falso', 'funcion', 'geq', 'greater', 'hacer', 'id', 'increment', 'indefinido', 'intentar', 'leq', 'less', 'mientras', 'minus', 'mod', 'mut', 'neq', 'not', 'nulo', 'num', 'opening_bra', 'opening_key', 'opening_par', 'or', 'para', 'period', 'plus', 'porDefecto', 'power', 'retornar', 'romper', 'semicolon', 'si', 'str', 'strict_equal', 'strict_neq', 'ternary', 'times', 'var', 'verdadero'])

    def parsear(self):
        self._parse_P()
        if not self._es_eof():
            self._error_sintaxis(['EOF'])
        print('El analisis sintactico ha finalizado exitosamente.')
