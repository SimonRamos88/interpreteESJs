import sys
from parser import Parser
from lexer import Lexer

if __name__ == '__main__':
    codigo = sys.stdin.read()
    lexer  = Lexer()
    try:
        Parser(lexer.analizar(codigo)).parsear()
    except SyntaxError as e:
        print(e)