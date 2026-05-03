from conjuntos import Conjuntos
from generadorASDR import GeneradorASDR
from gramatica import gramatica, terminales, simbolo_inicial

set = Conjuntos(terminales, gramatica, simbolo_inicial)

generador = GeneradorASDR(set)
codigo = generador.generar()

with open("parser.py", "w") as f:
    f.write(codigo)