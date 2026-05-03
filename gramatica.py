epsilon = 'ε'

terminales = {
    "var", "mut", "const", "si", "sino", "elegir", "hacer", "mientras", "para", 
    "retornar", "intentar", "capturar", "funcion", "consola", "id", "num", "str",
    "verdadero", "falso", "nulo", "indefinido", "NuN", "Infinito", "caso", "porDefecto",
    "Numero", "Mate", "Matriz", "Arreglo", "Booleano", "Cadena", "romper", "continuar",
    "afirmar", "limpiar", "error", "agrupar", "info", "escribir", "tabla", "crear",
    "(", ")", "{", "}", "[", "]", ";", ",", ".", ":", "=", "=>",
    "==", "===", "!=", "!==", "<", ">", "<=", ">=", "+", "-", "*", "/", "%", "!", "&&", "||", "?",
    "+=", "-=", "*=", "/=", "%=", "**=", "**"
}

simbolo_inicial = "Programa"

gramatica = {
    "Programa": [["ListaSentencias"]],
    
    "ListaSentencias": [
        ["Sentencia", "ListaSentencias"],
        [epsilon]
    ],
    
    "Sentencia": [
        ["Declaracion"],
        ["EstructuraControl"],
        ["DefinicionFuncion"],
        ["Retorno"],
        ["Intentar"],
        ["RomperContinuar"],
        ["Expresion", "OpcPuntoComa"],
        [";"]
    ],

    "OpcPuntoComa": [[";"], [epsilon]],

    # --- Caso 1 y 9: Declaraciones ---
    # Obliga a que si hay una coma, DEBE haber un 'id' después.
    "Declaracion": [
        ["var", "id", "OpcAsignacion", "MasVariables", "OpcPuntoComa"],
        ["mut", "id", "OpcAsignacion", "MasVariables", "OpcPuntoComa"],
        ["const", "id", "=", "Expresion", "MasConstantes", "OpcPuntoComa"]
    ],
    "OpcAsignacion": [["=", "Expresion"], [epsilon]],
    "MasVariables": [[",", "id", "OpcAsignacion", "MasVariables"], [epsilon]],
    "MasConstantes": [[",", "id", "=", "Expresion", "MasConstantes"], [epsilon]],

    # --- Caso 2: Intentar / Capturar ---
    # Obliga a que 'capturar' siga al bloque de 'intentar'.
    "Intentar": [["intentar", "Bloque", "capturar", "(", "id", ")", "Bloque"]],

    # --- Caso 8: Estructuras de Control ---
    "EstructuraControl": [
        ["si", "(", "Expresion", ")", "Bloque", "OpcSino"],
        ["mientras", "(", "Expresion", ")", "Bloque"],
        ["hacer", "Bloque", "mientras", "(", "Expresion", ")", "OpcPuntoComa"],
        ["para", "(", "OpcParaInit", ";", "OpcExp", ";", "OpcExp", ")", "Bloque"],
        ["elegir", "(", "Expresion", ")", "{", "ListaCasos", "}"]
    ],
    "OpcSino": [
        ["sino", "Bloque"], 
        ["sino", "si", "(", "Expresion", ")", "Bloque", "OpcSino"], 
        [epsilon]
    ],
    
    "Bloque": [["{", "ListaSentencias", "}"]],
    "OpcParaInit": [["Declaracion"], ["Expresion"], [epsilon]],
    "OpcExp": [["Expresion"], [epsilon]],

    "ListaCasos": [
        ["caso", "Expresion", ":", "ListaSentencias", "ListaCasos"],
        ["porDefecto", ":", "ListaSentencias"],
        [epsilon]
    ],

    # --- Funciones ---
    "DefinicionFuncion": [["funcion", "id", "(", "Params", ")", "Bloque"]],
    "Params": [["id", "MasParams"], [epsilon]],
    "MasParams": [[",", "id", "MasParams"], [epsilon]],
    "Retorno": [["retornar", "OpcExp", "OpcPuntoComa"]],
    "RomperContinuar": [["romper", "OpcPuntoComa"], ["continuar", "OpcPuntoComa"]],

    # --- Expresiones (Jerarquía LL1) ---
    "Expresion": [["Asignacion"]],
    
    "Asignacion": [["Ternaria", "OpcAsig"]],
    "OpcAsig": [
        ["=", "Asignacion"], ["+=", "Asignacion"], ["-=", "Asignacion"], 
        ["*=", "Asignacion"], ["/=", "Asignacion"], [epsilon]
    ],

    "Ternaria": [["LogicaOr", "OpcTern"]],
    # Caso 3: Después del '?' se espera una Expresion (que empieza por Literal/id, etc)
    "OpcTern": [["?", "Expresion", ":", "Ternaria"], [epsilon]],

    "LogicaOr": [["LogicaAnd", "LogicaOr'"]],
    "LogicaOr'": [["||", "LogicaAnd", "LogicaOr'"], [epsilon]],

    "LogicaAnd": [["Igualdad", "LogicaAnd'"]],
    "LogicaAnd'": [["&&", "Igualdad", "LogicaAnd'"], [epsilon]],

    "Igualdad": [["Relacional", "Igualdad'"]],
    "Igualdad'": [["OpIgual", "Relacional", "Igualdad'"], [epsilon]],
    "OpIgual": [["=="], ["==="], ["!="], ["!=="]],

    "Relacional": [["Aditiva", "Relacional'"]],
    "Relacional'": [["OpRel", "Aditiva", "Relacional'"], [epsilon]],
    "OpRel": [["<"], [">"], ["<="], [">="]],

    "Aditiva": [["Multiplicativa", "Aditiva'"]],
    "Aditiva'": [["+", "Multiplicativa", "Aditiva'"], ["-", "Multiplicativa", "Aditiva'"], [epsilon]],

    "Multiplicativa": [["Potencia", "Multiplicativa'"]],
    "Multiplicativa'": [["*", "Potencia", "Multiplicativa'"], ["/", "Potencia", "Multiplicativa'"], ["%", "Potencia", "Multiplicativa'"], [epsilon]],
    
    "Potencia": [["Unaria", "Potencia'"]],
    "Potencia'": [["**", "Unaria", "Potencia'"], [epsilon]],

    "Unaria": [["!", "Unaria"], ["-", "Unaria"], ["+", "Unaria"], ["Primaria"]],

    # --- Caso 4, 5, 10 y 11: Primaria y Accesos ---
    "Primaria": [
        ["Literal", "Accesos"],
        ["id", "Accesos"],
        ["consola", "Accesos"],
        ["(", "Expresion", ")", "AccesosOFlecha"]
    ],

    "AccesosOFlecha": [
        ["=>", "Expresion"],
        ["Accesos"]
    ],

    "Accesos": [
        [".", "id", "Accesos"],
        ["[", "Expresion", "]", "Accesos"],
        ["(", "Args", ")", "Accesos"],
        [epsilon]
    ],

    "Literal": [
        ["num"], ["str"], ["verdadero"], ["falso"], ["nulo"], ["indefinido"], 
        ["NuN"], ["Infinito"], ["Numero"], ["Mate"], ["Matriz"], ["Arreglo"], 
        ["Booleano"], ["Cadena"], ["LiteralArr"], ["LiteralObj"], ["LlamadaCrear"]
    ],

    # Caso 4: 'crear' debe ir seguido de tipos específicos o un id
    "LlamadaCrear": [["crear", "TipoCreable"]],
    "TipoCreable": [["Arreglo"], ["Cadena"], ["Matriz"], ["id"]],

    "LiteralArr": [["[", "Args", "]"]],
    "LiteralObj": [["{", "ListaPropiedades", "}"]],
    "ListaPropiedades": [["Propiedad", "MasPropiedades"], [epsilon]],
    "Propiedad": [
        ["id", "OpcProp"]
    ],
    "OpcProp": [
        [":", "Expresion"],
        ["(", "Params", ")", "Bloque"] # Caso 7: métodos en objetos
    ],
    "MasPropiedades": [[",", "Propiedad", "MasPropiedades"], [epsilon]],

    "Args": [["Expresion", "MasArgs"], [epsilon]],
    "MasArgs": [[",", "Expresion", "MasArgs"], [epsilon]]
}