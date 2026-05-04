# ============================================================
#  Gramática LL(1) para el analizador sintáctico de EsJS
#  Práctica 2 - Lenguajes de Programación - UNAL 2026-1
# ============================================================

terminales = {
    # Palabras reservadas
    "var", "mut", "const", "capturar", "caso", "continuar", "crear",
    "elegir", "hacer", "mientras", "para", "retornar", "sino", "si",
    "intentar", "romper", "porDefecto", "funcion", "falso", "nulo",
    "verdadero", "indefinido", "Infinito", "NuN", "consola", "Numero",
    "Mate", "Matriz", "Arreglo", "Booleano", "Cadena", "afirmar",
    "limpiar", "error", "agrupar", "info", "escribir", "tabla",
    # Literales
    "num", "str", "id",
    # Operadores lógicos / relacionales / aritméticos
    "and", "or", "not",
    "equal", "strict_equal", "neq", "strict_neq",
    "less", "leq", "greater", "geq",
    "plus", "minus", "times", "div", "mod", "power",
    # Operadores de asignación
    "assign",
    "plus_assign", "minus_assign", "times_assign", "div_assign",
    "mod_assign", "power_assign",
    # Incremento / decremento
    "increment", "decrement",
    # Operador ternario y flecha
    "ternary", "arrow",
    # Símbolos de puntuación / agrupación
    "period", "comma", "semicolon", "colon",
    "opening_key", "closing_key",
    "opening_bra", "closing_bra",
    "opening_par", "closing_par",
    # Fin de entrada
    "EOF",
}

epsilon = 'ε'

simbolo_inicial = 'P'

gramatica = {

    # ----------------------------------------------------------
    # PROGRAMA: secuencia (posiblemente vacía) de sentencias
    # ----------------------------------------------------------
    "P": [
        ["S", "P"],
        [epsilon],
    ],

    # ----------------------------------------------------------
    # SENTENCIA
    # ----------------------------------------------------------
    "S": [
        ["var",       "DeclVar"],       # declaración con var
        ["mut",       "DeclVar"],       # declaración con mut
        ["const",     "DeclConst"],     # declaración con const
        ["funcion",   "DeclFuncion"],   # declaración de función nombrada
        ["retornar",  "RetExpr"],       # sentencia retornar
        ["si",        "SentSi"],        # condicional si
        ["elegir",    "SentElegir"],    # elegir (switch)
        ["mientras",  "SentMientras"], # bucle mientras
        ["hacer",     "SentHacer"],    # bucle hacer…mientras
        ["para",      "SentPara"],     # bucle para
        ["intentar",  "SentIntentar"], # bloque intentar…capturar
        ["continuar", "SemiOpt"],       # continuar
        ["romper",    "SemiOpt"],       # romper
        ["opening_key", "P", "closing_key"],  # bloque anónimo { … }
        ["semicolon"],                  # sentencia vacía (;)
        ["E",         "PostExpr"],      # expresión como sentencia
    ],

    # ----------------------------------------------------------
    # DECLARACIÓN DE VARIABLES  (var / mut)
    # Permite: mut a, b = 1, c   (lista de ids con init opcional)
    # Caso 1: la coma después de id espera otro id, no expresión
    # ----------------------------------------------------------
    "DeclVar":  [["id", "InicVar", "MasVars"]],
    "InicVar":  [["assign", "E"], [epsilon]],
    "MasVars":  [["comma", "id", "InicVar", "MasVars"], [epsilon]],

    # ----------------------------------------------------------
    # DECLARACIÓN DE CONSTANTES  (const)
    # Igual que DeclVar: init es opcional sintácticamente
    # (el semántico verificará que siempre haya asignación)
    # Caso 7: el error esperado incluye "," y expresiones de inicio
    # ----------------------------------------------------------
    "DeclConst": [["id", "InicVar", "MasConst"]],
    "MasConst":  [["comma", "id", "InicVar", "MasConst"], [epsilon]],

    # ----------------------------------------------------------
    # POST-EXPRESIÓN: asignación, asign. compuesta, ++/--, o nada
    # Caso 7: +=, -=, *=, /=, %=, **= son operadores de asignación
    # ----------------------------------------------------------
    "PostExpr": [
        ["assign",       "E", "SemiOpt"],
        ["plus_assign",  "E", "SemiOpt"],
        ["minus_assign", "E", "SemiOpt"],
        ["times_assign", "E", "SemiOpt"],
        ["div_assign",   "E", "SemiOpt"],
        ["mod_assign",   "E", "SemiOpt"],
        ["power_assign", "E", "SemiOpt"],
        ["increment",    "SemiOpt"],
        ["decrement",    "SemiOpt"],
        ["SemiOpt"],
    ],

    # Punto y coma opcional (EsJS no es sensible a saltos de línea)
    "SemiOpt": [["semicolon"], [epsilon]],

    # retornar siempre espera una expresión
    "RetExpr": [["E", "SemiOpt"]],

    # ----------------------------------------------------------
    # EXPRESIONES  (jerarquía de precedencia, forma left-recursive
    # eliminada con producciones auxiliares prima)
    # ----------------------------------------------------------

    # Nivel 0: ternario  E1 (? E : E)?
    "E":        [["E1", "Ternario"]],
    "Ternario": [["ternary", "E", "colon", "E"], [epsilon]],

    # Nivel 1: OR lógico
    "E1":  [["E2",  "E1'"]],
    "E1'": [["or",  "E2", "E1'"], [epsilon]],

    # Nivel 2: AND lógico
    "E2":  [["E3",  "E2'"]],
    "E2'": [["and", "E3", "E2'"], [epsilon]],

    # Nivel 3: relacionales (no asociativos: solo un operador por cadena)
    "E3":  [["E4",  "E3'"]],
    "E3'": [
        ["equal",        "E4"],
        ["strict_equal", "E4"],
        ["neq",          "E4"],
        ["strict_neq",   "E4"],
        ["less",         "E4"],
        ["leq",          "E4"],
        ["greater",      "E4"],
        ["geq",          "E4"],
        [epsilon],
    ],

    # Nivel 4: suma / resta
    "E4":  [["E5",    "E4'"]],
    "E4'": [["plus",  "E5", "E4'"], ["minus", "E5", "E4'"], [epsilon]],

    # Nivel 5: multiplicación / división / módulo
    "E5":  [["E6",    "E5'"]],
    "E5'": [["times", "E6", "E5'"], ["div", "E6", "E5'"], ["mod", "E6", "E5'"], [epsilon]],

    # Nivel 6: potencia (asociativa a la derecha)
    "E6":  [["E7",     "E6'"]],
    "E6'": [["power",  "E6"], [epsilon]],

    # Nivel 7: unarios prefijos
    "E7": [
        ["minus", "E7"],
        ["not",   "E7"],
        ["plus",  "E7"],
        ["E8"],
    ],

    # Nivel 8: átomos y expresiones primarias
    # Caso 3:  expresión booleana puede iniciar sentencia (1>2 ? …)
    # Caso 6:  acceso a métodos y propiedades de objetos (obj.prop, obj[key])
    # Caso 8:  si() espera expresión (no cierra paren vacío)
    # Caso 9:  arrow functions  (a, b) => expr  vía SufijoOArrow
    # Caso 10: expresiones aritméticas completas
    # Caso 13: llamadas encadenadas afuera()(10)
    "E8": [
        ["num"],
        ["str"],
        ["verdadero"],
        ["falso"],
        ["nulo"],
        ["indefinido"],
        ["Infinito"],
        ["NuN"],
        # Paréntesis / arrow function:
        # (ListaExpr) => E  →  arrow function
        # (E)              →  expresión parentizada (Sufijo = ε)
        # (ListaExpr) ...  →  llamada si continúa con Sufijo
        ["opening_par", "ListaExpr", "closing_par", "SufijoOArrow"],
        # Arreglo literal: [e1, e2, ...]
        ["opening_bra", "ListaExpr", "closing_bra"],
        # Objeto literal: { prop: val, metodo() { } }
        # (solo válido como expresión, NO como sentencia — en S el { abre bloque)
        ["opening_key", "PropiedadesObj", "closing_key"],
        # new: crear Tipo(args)
        ["crear",   "TipoCrear",  "ArgsFuncion"],
        # identificador con sufijos
        ["id",      "Sufijo"],
        # consola.metodo(args) con posibles sufijos
        ["consola", "period", "MetodoConsola", "ArgsFuncion", "Sufijo"],
        # Constructores / namespaces built-in con sufijos
        ["Numero",  "Sufijo"],
        ["Mate",    "Sufijo"],
        ["Matriz",  "Sufijo"],
        ["Arreglo", "Sufijo"],
        ["Booleano","Sufijo"],
        ["Cadena",  "Sufijo"],
    ],

    # Después de (ListaExpr): flecha o sufijo normal
    # Esto resuelve el problema de arrow functions en LL(1):
    # (a, b) => expr   →  arrow
    # (expr).prop      →  sufijo point
    # (expr)(args)     →  sufijo call
    # (expr)           →  sufijo ε
    "SufijoOArrow": [
        ["arrow",  "E"],    # arrow function
        ["Sufijo"],         # expresión parentizada (posiblemente con más sufijos)
    ],

    # Sufijos postfijos: .prop, [idx], (args), ++, --
    # Caso 6:  obj.metodo(), obj['prop']
    # Caso 13: afuera()(10)  → llamada de resultado de función
    "Sufijo": [
        ["period",      "id",        "Sufijo"],
        ["opening_bra", "E",         "closing_bra", "Sufijo"],
        ["opening_par", "ListaExpr", "closing_par", "Sufijo"],
        ["increment"],
        ["decrement"],
        [epsilon],
    ],

    # Llamada de función (para crear y consola donde la llamada es obligatoria)
    "ArgsFuncion": [["opening_par", "ListaExpr", "closing_par"]],

    # Caso 15: consola solo acepta métodos específicos
    "MetodoConsola": [
        ["afirmar"], ["agrupar"], ["error"], ["escribir"],
        ["info"], ["limpiar"], ["tabla"],
    ],

    # Tipos permitidos después de "crear"
    # Caso 4: crear espera Arreglo, Cadena, Matriz o id
    "TipoCrear": [
        ["Arreglo"], ["Cadena"], ["Matriz"], ["id"],
    ],

    # Lista de expresiones (para argumentos y arreglos literales)
    # Caso 9: permite múltiples argumentos  f(a, b)
    "ListaExpr": [["E", "MasExpr"], [epsilon]],
    "MasExpr":   [["comma", "E", "MasExpr"], [epsilon]],

    # ----------------------------------------------------------
    # OBJETOS LITERALES
    # Caso 6: { propiedad: valor }  y  { metodo() { … } }
    # ----------------------------------------------------------
    "PropiedadesObj": [["PropObj", "MasProps"], [epsilon]],
    "MasProps":       [["comma", "PropObj", "MasProps"], [epsilon]],

    # Propiedad puede ser:
    #   id: E             →  clave string con valor
    #   "str": E          →  clave string literal
    #   num: E            →  clave numérica
    #   id(params){body}  →  método abreviado
    "PropObj": [
        ["id",  "ValorProp"],
        ["str", "colon", "E"],
        ["num", "colon", "E"],
    ],
    "ValorProp": [
        ["colon", "E"],                                                              # propiedad normal
        ["opening_par", "Params", "closing_par", "opening_key", "P", "closing_key"], # método abreviado
    ],

    # ----------------------------------------------------------
    # DECLARACIÓN DE FUNCIÓN NOMBRADA
    # Caso 11: debe usar { } no [ ]
    # Caso 12: debe tener id (funcion anónima inválida como sentencia)
    # Caso 13: funciones anidadas
    # ----------------------------------------------------------
    "DeclFuncion": [
        ["id", "opening_par", "Params", "closing_par", "opening_key", "P", "closing_key"],
    ],

    # Parámetros formales
    "Params":    [["id", "MasParams"], [epsilon]],
    "MasParams": [["comma", "id", "MasParams"], [epsilon]],

    # ----------------------------------------------------------
    # SENTENCIA  si … sino
    # Caso 16: si (cond) { } sino { }
    # Caso 20: sino espera "si" o "{"
    # ----------------------------------------------------------
    "SentSi": [
        ["opening_par", "E", "closing_par", "opening_key", "P", "closing_key", "SentSino"],
    ],
    "SentSino": [
        ["sino", "SinoResto"],
        [epsilon],
    ],
    "SinoResto": [
        ["si", "opening_par", "E", "closing_par", "opening_key", "P", "closing_key", "SentSino"],  # sino si
        ["opening_key", "P", "closing_key"],                                                        # sino { }
    ],

    # ----------------------------------------------------------
    # SENTENCIA  elegir (switch)
    # ----------------------------------------------------------
    "SentElegir": [
        ["opening_par", "E", "closing_par", "opening_key", "CasoList", "closing_key"],
    ],
    "CasoList": [
        ["caso",       "E", "colon", "P", "CasoList"],
        ["porDefecto", "colon", "P"],
        [epsilon],
    ],

    # ----------------------------------------------------------
    # BUCLE  mientras
    # ----------------------------------------------------------
    "SentMientras": [
        ["opening_par", "E", "closing_par", "opening_key", "P", "closing_key"],
    ],

    # ----------------------------------------------------------
    # BUCLE  hacer … mientras
    # Caso 17: mientras debe ir seguido de (
    # ----------------------------------------------------------
    "SentHacer": [
        ["opening_key", "P", "closing_key",
         "mientras", "opening_par", "E", "closing_par", "semicolon"],
    ],

    # ----------------------------------------------------------
    # BUCLE  para
    # ----------------------------------------------------------
    "SentPara": [
        ["opening_par", "InicPara", "semicolon",
         "CondPara",    "semicolon",
         "ActPara",     "closing_par",
         "opening_key", "P", "closing_key"],
    ],
    # Inicialización: puede ser var/mut decl, expresión con asign opcional, o vacía
    "InicPara": [
        ["var", "DeclVar"],
        ["mut", "DeclVar"],
        ["E",   "AsignOpt"],
        [epsilon],
    ],
    "AsignOpt": [["assign", "E"], [epsilon]],
    # Condición: expresión o vacía
    "CondPara": [["E"], [epsilon]],
    # Actualización: expresión con sufijo de asignación/inc/dec o vacía
    "ActPara": [["E", "ActSuf"], [epsilon]],
    "ActSuf": [
        ["assign",       "E"],
        ["plus_assign",  "E"],
        ["minus_assign", "E"],
        ["times_assign", "E"],
        ["div_assign",   "E"],
        ["mod_assign",   "E"],
        ["power_assign", "E"],
        ["increment"],
        ["decrement"],
        [epsilon],
    ],

    # ----------------------------------------------------------
    # BLOQUE  intentar … capturar
    # Caso 2: capturar es OBLIGATORIO (no hay finally en EsJS)
    # ----------------------------------------------------------
    "SentIntentar": [
        ["opening_key", "P", "closing_key",
         "capturar", "opening_par", "id", "closing_par",
         "opening_key", "P", "closing_key"],
    ],
}