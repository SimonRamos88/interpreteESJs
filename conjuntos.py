
class Conjuntos:

    def __init__(self, terminales, gramatica, simbolo_inicial, epsilon='ε', fin_cadena='EOF'):
        self.terminales = set(terminales)
        self.gramatica = gramatica
        self.simbolo_inicial = simbolo_inicial
        self.no_terminales = set(gramatica.keys())
        self.epsilon = epsilon
        self.fin_cadena = fin_cadena

        self.primeros_set = self._calcular_primeros()
        self.siguientes_set = self._calcular_siguientes()
        self.prediccion_set = self._calcular_prediccion()




    def _calcular_primeros(self):

        primeros = {nt: set() for nt in self.no_terminales}

        for t in self.terminales:
            primeros[t] = {t}

        cambio = True
        while cambio:
            cambio = False
            for nt, producciones in self.gramatica.items():
                for produccion in producciones:
                    nuevos = self._primeros_cadena(produccion, primeros)
                    if not nuevos.issubset(primeros[nt]):
                        primeros[nt].update(nuevos)
                        cambio = True

        return primeros
    

    def _primeros_cadena(self, cadena, primeros):
        if not cadena or cadena == [self.epsilon]:
            return {self.epsilon}

        resultado = set()

        for simbolo in cadena:
            primeros_simbolo = primeros.get(simbolo, set())

            resultado.update(primeros_simbolo - {self.epsilon})

            if self.epsilon not in primeros_simbolo:
                break
        else:
            resultado.add(self.epsilon)

        return resultado


    def _calcular_siguientes(self):
        siguientes = {nt: set() for nt in self.no_terminales}

        siguientes[self.simbolo_inicial].add(self.fin_cadena)

        cambio = True
        while cambio:
            cambio = False
            for nt, producciones in self.gramatica.items():
                for produccion in producciones:
                    for i, simbolo in enumerate(produccion):
                        if simbolo not in self.no_terminales:
                            continue

                        beta = produccion[i + 1:]

                        primeros_beta = self._primeros_cadena(beta, self.primeros_set)
                        nuevos = primeros_beta - {self.epsilon}

                        if self.epsilon in primeros_beta:
                            nuevos.update(siguientes[nt])

                        if not nuevos.issubset(siguientes[simbolo]):
                            siguientes[simbolo].update(nuevos)
                            cambio = True

        return siguientes
    
    def _calcular_prediccion(self):
        prediccion = {}

        for nt, producciones in self.gramatica.items():
            for produccion in producciones:
                primeros_prod = self._primeros_cadena(produccion, self.primeros_set)

                if self.epsilon in primeros_prod:
                    pred = (primeros_prod - {self.epsilon}) | self.siguientes_set[nt]
                else:
                    pred = primeros_prod

                prediccion[(nt, tuple(produccion))] = pred

        return prediccion
    
    def mostrar_conjuntos(self):
        print("=== PRIMEROS ===")
        for simbolo, conjunto in sorted(self.primeros_set.items()):
            if simbolo in self.no_terminales:
                print(f"  PRIMEROS({simbolo}) = {conjunto}")

        print("\n=== SIGUIENTES ===")
        for simbolo, conjunto in sorted(self.siguientes_set.items()):
            print(f"  SIGUIENTES({simbolo}) = {conjunto}")

        print("\n=== PREDICCIÓN ===")
        for (nt, produccion), conjunto in sorted(self.prediccion_set.items()):
            print(f"  PRED({nt} → {' '.join(produccion)}) = {conjunto}")
