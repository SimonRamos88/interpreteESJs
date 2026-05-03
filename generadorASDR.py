from lexer import SIMBOLOS
from conjuntos import Conjuntos

class GeneradorASDR:

    INDENTACION = "    "

    def __init__(self, conjuntos: Conjuntos):
        self.conjuntos = conjuntos

    def generar(self) -> str:
        return "\n".join([
            self._generar_clase_parser(),
        ])

    def _generar_clase_parser(self) -> str:
        lineas = [
            "class Parser:",
            "",
            *self._generar_init(),
            "",
            *self._generar_metodos_auxiliares(),
            "",
        ]
        for nt in sorted(self.conjuntos.no_terminales):
            lineas += self._generar_funcion_nt(nt)
            lineas.append("")
        lineas += self._generar_parsear()
        lineas.append("")
        return "\n".join(lineas)

    def _generar_init(self) -> list[str]:
        I = self.INDENTACION
        II = I * 2
        return [
            f"{I}def __init__(self, gen):",
            f"{II}self._gen = gen",
            f"{II}self._token_actual = next(self._gen, None)",
            f"{II}self._ultima_fila = 1",
            f"{II}self._ultima_col  = 1",
        ]

    def _generar_metodos_auxiliares(self) -> list[str]:
        I = self.INDENTACION
        II = I * 2
        III = I * 3
        return [
            f"{I}def _es_eof(self) -> bool:",
            f"{II}return self._token_actual is None",
            "",
            f"{I}def _token_tipo(self) -> str:",
            f"{II}return self._token_actual.tipo if not self._es_eof() else 'EOF'",
            "",
            f"{I}def _avanzar(self):",
            f"{II}if self._token_actual is not None:",
            f"{III}self._ultima_fila = self._token_actual.fila",
            f"{III}self._ultima_col  = self._token_actual.columna",
            f"{II}self._token_actual = next(self._gen, None)",
            "",
            f"{I}def _emparejar(self, tipo_esperado: str):",
            f"{II}if self._token_tipo() == tipo_esperado:",
            f"{III}self._avanzar()",
            f"{II}else:",
            f"{III}self._error_sintaxis([tipo_esperado])",
            "",
            *self._generar_lexema_visible(),
            "",
            *self._generar_error_sintaxis(),
        ]


    def _generar_lexema_visible(self) -> list[str]:
        I = self.INDENTACION
        II = I * 2
        III = I * 3
        mapa_lineas = [
            f"{III}{repr(tipo)}: {repr(lexema)},"
            for lexema, tipo in SIMBOLOS.items()
        ]
        return [
            f"{I}def _lexema_visible(self, tipo: str) -> str:",
            f"{II}_MAPA = {{",
            *mapa_lineas,
            f"{III}'num': 'valor_numerico',",
            f"{III}'str': 'cadena_de_caracteres',",
            f"{III}'id':  'id',",
            f"{III}'EOF': 'EOF',",
            f"{II}}}",
            f"{II}return _MAPA.get(tipo, tipo)",
        ]

    def _generar_error_sintaxis(self) -> list[str]:
        I = self.INDENTACION
        II = I * 2
        III = I * 3
        return [
            f"{I}def _error_sintaxis(self, tipos_esperados: list):",
            f"{II}if not self._es_eof():",
            f"{III}fila       = self._token_actual.fila",
            f"{III}col        = self._token_actual.columna",
            f"{III}encontrado = f'\"{{self._token_actual.lexema}}\"'",
            f"{II}else:",
            f"{III}fila       = self._ultima_fila",
            f"{III}col        = self._ultima_col + 1",
            f"{III}encontrado = '\"final de archivo\"'",
            f"{II}esperados_visibles = sorted({{self._lexema_visible(t) for t in tipos_esperados}})",
            f"{II}esperados_str = ', '.join(f'\"{{e}}\"' for e in esperados_visibles)",
            f"{II}raise SyntaxError(",
            f"{III}f'<{{fila}}:{{col}}> Error sintactico: se encontro: {{encontrado}}; se esperaba: {{esperados_str}}.'",
            f"{II})",
        ]

    def _generar_funcion_nt(self, nt: str) -> list[str]:
        I = self.INDENTACION
        II = I * 2
        III = I * 3
        producciones = self.conjuntos.gramatica[nt]
        lineas = [f"{I}def {self._nombre_funcion(nt)}(self):"]

        primer_if = True
        tokens_cubiertos: set[str] = set()

        for produccion in producciones:
            clave = (nt, tuple(produccion))
            pred = self.conjuntos.prediccion_set[clave]
            pred_sin_epsilon = pred - {self.conjuntos.epsilon}
            tokens_cubiertos.update(pred_sin_epsilon)

            if not pred_sin_epsilon:
                continue

            condicion = self._condicion_prediccion(pred_sin_epsilon)
            palabra_clave = "if" if primer_if else "elif"
            primer_if = False

            lineas.append(f"{II}{palabra_clave} {condicion}:")
            cuerpo = self._generar_cuerpo_produccion(produccion)
            for instruccion in (cuerpo or ["pass"]):
                lineas.append(f"{III}{instruccion}")

        tiene_epsilon = any(
            not (self.conjuntos.prediccion_set[(nt, tuple(p))] - {self.conjuntos.epsilon})
            for p in producciones
        )

        if primer_if:
            lineas.append(f"{II}pass")
        elif tiene_epsilon:
            lineas.append(f"{II}else:")
            lineas.append(f"{III}pass")
        else:
            tokens_repr = ", ".join(repr(t) for t in sorted(tokens_cubiertos))
            lineas.append(f"{II}else:")
            lineas.append(f"{III}self._error_sintaxis([{tokens_repr}])")

        return lineas

    def _generar_cuerpo_produccion(self, produccion: list) -> list[str]:
        if not produccion or produccion == [self.conjuntos.epsilon]:
            return []
        instrucciones = []
        for simbolo in produccion:
            if simbolo in self.conjuntos.no_terminales:
                instrucciones.append(f"self.{self._nombre_funcion(simbolo)}()")
            else:
                instrucciones.append(f"self._emparejar({repr(simbolo)})")
        return instrucciones

    def _generar_parsear(self) -> list[str]:
        I = self.INDENTACION
        II = I * 2
        III = I * 3
        funcion_inicial = self._nombre_funcion(self.conjuntos.simbolo_inicial)
        return [
            f"{I}def parsear(self):",
            f"{II}self.{funcion_inicial}()",
            f"{II}if not self._es_eof():",
            f"{III}self._error_sintaxis(['EOF'])",
            f"{II}print('El analisis sintactico ha finalizado exitosamente.')",
        ]

    def _nombre_funcion(self, nt: str) -> str:
        return f"_parse_{nt.replace(chr(39), '_prima').replace(' ', '_')}"

    def _condicion_prediccion(self, pred: set) -> str:
        return " or ".join(
            f"self._token_tipo() == {repr(t)}" for t in sorted(pred)
        )