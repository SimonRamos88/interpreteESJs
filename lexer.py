import re

RESERVADAS = {
    "var", "mut", "const", "capturar", "caso", "continuar", "crear",
    "elegir", "hacer", "mientras", "para", "retornar", "sino", "si",
    "intentar", "romper", "porDefecto", "funcion", "falso", "nulo",
    "verdadero", "indefinido", "Infinito", "NuN", "consola", "Numero",
    "Mate", "Matriz", "Arreglo", "Booleano", "Cadena", "afirmar",
    "limpiar", "error", "agrupar", "info", "escribir", "tabla"
}

SIMBOLOS = {
    '&&': 'and',        '||': 'or',           '??': 'nulish',
    '...': 'spread',    '=>': 'arrow',         '!': 'not',
    '.': 'period',      ',': 'comma',          ';': 'semicolon',
    ':': 'colon',       '?': 'ternary',
    '{': 'opening_key', '}': 'closing_key',
    '[': 'opening_bra', ']': 'closing_bra',
    '(': 'opening_par', ')': 'closing_par',
    '++': 'increment',  '--': 'decrement',
    '+=': 'plus_assign',   '-=': 'minus_assign',
    '*=': 'times_assign',  '/=': 'div_assign',
    '%=': 'mod_assign',    '**=': 'power_assign',
    '+': 'plus',  '-': 'minus', '*': 'times',
    '/': 'div',   '**': 'power', '%': 'mod',
    '===': 'strict_equal', '==': 'equal',
    '!==': 'strict_neq',   '!=': 'neq',
    '<=': 'leq', '>=': 'geq', '<': 'less', '>': 'greater',
    '=': 'assign',
}

IGNORADOS = {'space', 'comment_line'}

_R_COMMENT_LINE  = r'//.*'
_R_COMMENT_BEGIN = r'/\*'
_R_COMMENT_END   = r'\*/'
_R_SPACE         = r'[ \t]+'
_R_STR           = r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''
_R_REG           = r'/(?:\\.|[^/\\\[]|\[(?:\\.|[^\]\\])*\])+/'
_R_NUM           = r'\d+(?:\.\d+)?'
_R_ID            = (
    r'(?:[^\W\d]|[$_]|\\u[0-9a-fA-F]{4}|\\u\{[0-9a-fA-F]+\})'
    r'(?:[\w$]|\\u[0-9a-fA-F]{4}|\\u\{[0-9a-fA-F]+\})*'
)
_R_SIMBOL        = (
    r'\|\||&&|===|%=|/=|\*=|-=|\+=|\?\?|!==|\*\*=|>=|<=|==|!='
    r'|\+\+|--|=>|\.\.\.|\*\*|[+\-*/%=<>!.,;:{}\[\]()?]'
)

_TOKENS_REGEX = [
    ('comment_line',  _R_COMMENT_LINE),
    ('comment_begin', _R_COMMENT_BEGIN),
    ('space',         _R_SPACE),
    ('str',           _R_STR),
    ('reg',           _R_REG),
    ('num',           _R_NUM),
    ('id',            _R_ID),
    ('simbol',        _R_SIMBOL),
]

MASTER_REGEX = re.compile(
    '|'.join(f'(?P<{name}>{pattern})' for name, pattern in _TOKENS_REGEX)
)

COMMENT_END_REGEX = re.compile(_R_COMMENT_END)

class Token:
    def __init__(self, tipo: str, lexema: str, fila: int, columna: int):
        self.tipo    = tipo
        self.lexema  = lexema
        self.fila    = fila
        self.columna = columna
        self._resolver()

    def __str__(self) -> str:
        if self.tipo == self.lexema:
            return f'<{self.tipo},{self.fila},{self.columna}>'
        if self.tipo in ('str', 'num', 'reg'):
            return f'<tkn_{self.tipo},{self.lexema},{self.fila},{self.columna}>'
        if self.tipo != 'id':
            return f'<tkn_{self.tipo},{self.fila},{self.columna}>'
        return f'<{self.tipo},{self.lexema},{self.fila},{self.columna}>'

    def _resolver(self):
        if self.lexema in RESERVADAS:
            self.tipo = self.lexema
        elif self.tipo in ('str', 'reg'):
            self.lexema = self.lexema[1:-1]
        elif self.lexema in SIMBOLOS:
            self.tipo = SIMBOLOS[self.lexema]


class ErrorLexico(Exception):
    def __init__(self, fila: int, columna: int):
        self.fila    = fila
        self.columna = columna

    def __str__(self) -> str:
        return f'>>> Error lexico (linea: {self.fila}, posicion: {self.columna})'


class Lexer:
    def __init__(self):
        self._en_comentario  = False
        self._inicio_comentario = None  # (fila, columna)

    def _procesar_linea(self, n_fila: int, linea: str):
        pos = 0
        while pos < len(linea):

            if self._en_comentario:
                match = COMMENT_END_REGEX.search(linea, pos)
                if match:
                    self._en_comentario = False
                    self._inicio_comentario = None
                    pos = match.end()
                else:
                    return
                continue

            match = MASTER_REGEX.match(linea, pos)
            if not match:
                raise ErrorLexico(n_fila, pos + 1)

            tipo    = match.lastgroup
            lexema  = match.group()
            columna = pos + 1

            if tipo == 'comment_begin':
                self._en_comentario = True
                self._inicio_comentario = (n_fila, columna)

            elif tipo not in IGNORADOS:
                yield Token(tipo, lexema, n_fila, columna)

            pos = match.end()

    def analizar(self, codigo: str):
        for n_fila, linea in enumerate(codigo.splitlines(), start=1):
            yield from self._procesar_linea(n_fila, linea)

        if self._en_comentario:
            raise ErrorLexico(*self._inicio_comentario)