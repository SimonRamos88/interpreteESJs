epsilon = 'ε'

terminales = {
    'var', 'mut', 'const',
    'funcion', 'retornar',
    'si', 'sino',
    'elegir', 'caso', 'porDefecto', 'romper',
    'mientras', 'hacer',
    'para', 'continuar',
    'verdadero', 'falso', 'nulo', 'indefinido', 'Infinito', 'NuN',
    'consola', 'escribir', 'error', 'info', 'agrupar', 'limpiar', 'tabla',
    'Numero', 'Mate', 'Matriz', 'Arreglo', 'Booleano', 'Cadena',
    'afirmar', 'crear',
    'intentar', 'capturar', 'finalmente',
    'id', 'num', 'str',
    'assign', 'plus', 'minus', 'times', 'div', 'mod', 'power',
    'plus_assign', 'minus_assign', 'times_assign', 'div_assign',
    'mod_assign', 'power_assign',
    'increment', 'decrement',
    'equal', 'neq', 'strict_equal', 'strict_neq',
    'less', 'greater', 'leq', 'geq',
    'and', 'or', 'not',
    'ternary', 'colon',
    'opening_par', 'closing_par',
    'opening_key', 'closing_key',
    'opening_bra', 'closing_bra',
    'semicolon', 'comma', 'period',
    'arrow',
}

simbolo_inicial = 'P'

gramatica = {

    'P': [['SL']],

    'SL': [
        ['S', 'SL'],
        [epsilon],
    ],

    # semicolon suelto = sentencia vacía (resuelve ;;;)
    # EXPR_STMT no tiene { ni id ni NombreObjeto para evitar conflictos con BLOQUE/ASIGN/OBJETO
    'S': [
        ['semicolon'],
        ['DECL'],
        ['CONST_DECL'],
        ['ASIGN_O_LLAMADA'],
        ['CONSOLA_STMT'],
        ['OBJETO_STMT'],
        ['EXPR_STMT'],
        ['SI_STMT'],
        ['ELEGIR_STMT'],
        ['MIENTRAS_STMT'],
        ['HACER_STMT'],
        ['PARA_STMT'],
        ['RETORNAR_STMT'],
        ['ROMPER_STMT'],
        ['CONTINUAR_STMT'],
        ['FUNCION_DECL'],
        ['INTENTAR_STMT'],
        ['BLOQUE'],
    ],

    'SEMI_OPT': [
        ['semicolon'],
        [epsilon],
    ],

    # var/mut permiten lista: mut a, b = 5, c
    'DECL': [
        ['var', 'DECL_LISTA', 'SEMI_OPT'],
        ['mut', 'DECL_LISTA', 'SEMI_OPT'],
    ],

    'DECL_LISTA': [
        ['id', 'DECL_INIT', 'DECL_LISTA_RESTO'],
    ],

    'DECL_LISTA_RESTO': [
        ['comma', 'id', 'DECL_INIT', 'DECL_LISTA_RESTO'],
        [epsilon],
    ],

    'DECL_INIT': [
        ['assign', 'EXPR'],
        [epsilon],
    ],

    'CONST_DECL': [
        ['const', 'id', 'assign', 'EXPR', 'SEMI_OPT'],
    ],

    # id puede ser: asignación, asig compuesta, ++/--, llamada, acceso
    'ASIGN_O_LLAMADA': [
        ['id', 'ASIGN_O_LLAMADA_SUF', 'SEMI_OPT'],
    ],

    'ASIGN_O_LLAMADA_SUF': [
        ['assign',       'EXPR'],
        ['plus_assign',  'EXPR'],
        ['minus_assign', 'EXPR'],
        ['times_assign', 'EXPR'],
        ['div_assign',   'EXPR'],
        ['mod_assign',   'EXPR'],
        ['power_assign', 'EXPR'],
        ['increment'],
        ['decrement'],
        ['opening_bra', 'EXPR', 'closing_bra', 'SUBSCRIPT_SUF'],
        ['opening_par', 'ARGS', 'closing_par', 'ENCADENADO'],
        ['period', 'id', 'POSTFIX_LLAMADA'],
    ],

    'SUBSCRIPT_SUF': [
        ['assign', 'EXPR'],
        ['opening_par', 'ARGS', 'closing_par', 'ENCADENADO'],
        [epsilon],
    ],

    'POSTFIX_LLAMADA': [
        ['opening_par', 'ARGS', 'closing_par', 'ENCADENADO'],
        ['period', 'id', 'POSTFIX_LLAMADA'],
        [epsilon],
    ],

    'ENCADENADO': [
        ['opening_par', 'ARGS', 'closing_par', 'ENCADENADO'],
        [epsilon],
    ],

    'CONSOLA_STMT': [
        ['consola', 'period', 'METODO_CONSOLA', 'opening_par', 'ARGS', 'closing_par', 'SEMI_OPT'],
    ],

    'METODO_CONSOLA': [
        ['escribir'], ['error'], ['info'], ['agrupar'], ['limpiar'], ['tabla'], ['afirmar'],
    ],

    'OBJETO_STMT': [
        ['NOMBRE_OBJETO', 'period', 'id', 'opening_par', 'ARGS', 'closing_par', 'SEMI_OPT'],
    ],

    'NOMBRE_OBJETO': [
        ['Numero'], ['Mate'], ['Matriz'], ['Arreglo'], ['Booleano'], ['Cadena'],
    ],

    # Solo para num/str/literales/unarios/(/[ como sentencias (ej: 1>2 ? ...)
    'EXPR_STMT': [
        ['EXPR_NO_KEY', 'SEMI_OPT'],
    ],

    'BLOQUE': [
        ['opening_key', 'SL', 'closing_key'],
    ],

    'SI_STMT': [
        ['si', 'opening_par', 'EXPR', 'closing_par', 'BLOQUE', 'SINO_OPT'],
    ],

    'SINO_OPT': [
        ['sino', 'SINO_CUERPO'],
        [epsilon],
    ],

    'SINO_CUERPO': [
        ['SI_STMT'],
        ['BLOQUE'],
    ],

    'ELEGIR_STMT': [
        ['elegir', 'opening_par', 'EXPR', 'closing_par',
         'opening_key', 'CASOS', 'DEFECTO_OPT', 'closing_key'],
    ],

    'CASOS': [
        ['CASO', 'CASOS'],
        [epsilon],
    ],

    'CASO': [
        ['caso', 'EXPR', 'colon', 'SL_CASO', 'ROMPER_OPT'],
    ],

    # SL_CASO excluye ROMPER_STMT para evitar conflicto con ROMPER_OPT
    'SL_CASO': [
        ['S_CASO', 'SL_CASO'],
        [epsilon],
    ],

    'S_CASO': [
        ['semicolon'],
        ['DECL'], ['CONST_DECL'], ['ASIGN_O_LLAMADA'],
        ['CONSOLA_STMT'], ['OBJETO_STMT'], ['EXPR_STMT'],
        ['SI_STMT'], ['ELEGIR_STMT'], ['MIENTRAS_STMT'], ['HACER_STMT'],
        ['PARA_STMT'], ['RETORNAR_STMT'], ['CONTINUAR_STMT'],
        ['FUNCION_DECL'], ['INTENTAR_STMT'], ['BLOQUE'],
    ],

    'ROMPER_OPT': [
        ['romper', 'SEMI_OPT'],
        [epsilon],
    ],

    'DEFECTO_OPT': [
        ['porDefecto', 'colon', 'SL_CASO', 'ROMPER_OPT2'],
        [epsilon],
    ],

    # Copia de ROMPER_OPT con nombre distinto para evitar contaminación de SIGUIENTES
    'ROMPER_OPT2': [
        ['romper', 'SEMI_OPT'],
        [epsilon],
    ],

    'MIENTRAS_STMT': [
        ['mientras', 'opening_par', 'EXPR', 'closing_par', 'BLOQUE'],
    ],

    'HACER_STMT': [
        ['hacer', 'BLOQUE', 'mientras', 'opening_par', 'EXPR', 'closing_par', 'SEMI_OPT'],
    ],

    'PARA_STMT': [
        ['para', 'opening_par', 'PARA_INIT', 'semicolon',
         'PARA_COND', 'semicolon', 'PARA_PASO', 'closing_par', 'BLOQUE'],
    ],

    'PARA_INIT': [
        ['var', 'id', 'assign', 'EXPR'],
        ['mut', 'id', 'assign', 'EXPR'],
        ['id',  'assign', 'EXPR'],
        [epsilon],
    ],

    'PARA_COND': [
        ['EXPR'],
        [epsilon],
    ],

    'PARA_PASO': [
        ['id', 'PARA_PASO_SUF'],
        [epsilon],
    ],

    'PARA_PASO_SUF': [
        ['assign',       'EXPR'],
        ['plus_assign',  'EXPR'],
        ['minus_assign', 'EXPR'],
        ['times_assign', 'EXPR'],
        ['div_assign',   'EXPR'],
        ['mod_assign',   'EXPR'],
        ['power_assign', 'EXPR'],
        ['increment'],
        ['decrement'],
    ],

    'RETORNAR_STMT': [['retornar', 'RETORNAR_VAL']],

    'RETORNAR_VAL': [
        ['EXPR', 'SEMI_OPT'],
        ['semicolon'],
    ],

    'ROMPER_STMT':    [['romper',    'SEMI_OPT']],
    'CONTINUAR_STMT': [['continuar', 'SEMI_OPT']],

    'FUNCION_DECL': [
        ['funcion', 'id', 'opening_par', 'PARAMS', 'closing_par', 'BLOQUE'],
    ],

    'PARAMS': [
        ['id', 'PARAMS_RESTO'],
        [epsilon],
    ],

    'PARAMS_RESTO': [
        ['comma', 'id', 'PARAMS_RESTO'],
        [epsilon],
    ],

    'INTENTAR_STMT': [
        ['intentar', 'BLOQUE', 'capturar', 'opening_par', 'id',
         'closing_par', 'BLOQUE', 'FINALMENTE_OPT'],
    ],

    'FINALMENTE_OPT': [
        ['finalmente', 'BLOQUE'],
        [epsilon],
    ],

    # Expresiones completas (pueden empezar con {)
    'EXPR': [['EXPR_OR', 'TERNARIO_OPT']],

    'TERNARIO_OPT': [
        ['ternary', 'EXPR', 'colon', 'EXPR'],
        [epsilon],
    ],

    'EXPR_OR':  [['EXPR_AND',  "EXPR_OR'"]],
    "EXPR_OR'": [['or', 'EXPR_AND', "EXPR_OR'"], [epsilon]],

    'EXPR_AND':  [['EXPR_EQ',  "EXPR_AND'"]],
    "EXPR_AND'": [['and', 'EXPR_EQ', "EXPR_AND'"], [epsilon]],

    'EXPR_EQ':  [['EXPR_REL', "EXPR_EQ'"]],
    "EXPR_EQ'": [
        ['equal',        'EXPR_REL', "EXPR_EQ'"],
        ['neq',          'EXPR_REL', "EXPR_EQ'"],
        ['strict_equal', 'EXPR_REL', "EXPR_EQ'"],
        ['strict_neq',   'EXPR_REL', "EXPR_EQ'"],
        [epsilon],
    ],

    'EXPR_REL':  [['EXPR_ADD', "EXPR_REL'"]],
    "EXPR_REL'": [
        ['less',    'EXPR_ADD', "EXPR_REL'"],
        ['greater', 'EXPR_ADD', "EXPR_REL'"],
        ['leq',     'EXPR_ADD', "EXPR_REL'"],
        ['geq',     'EXPR_ADD', "EXPR_REL'"],
        [epsilon],
    ],

    'EXPR_ADD':  [['EXPR_MUL', "EXPR_ADD'"]],
    "EXPR_ADD'": [
        ['plus',  'EXPR_MUL', "EXPR_ADD'"],
        ['minus', 'EXPR_MUL', "EXPR_ADD'"],
        [epsilon],
    ],

    'EXPR_MUL':  [['EXPR_POW', "EXPR_MUL'"]],
    "EXPR_MUL'": [
        ['times', 'EXPR_POW', "EXPR_MUL'"],
        ['div',   'EXPR_POW', "EXPR_MUL'"],
        ['mod',   'EXPR_POW', "EXPR_MUL'"],
        [epsilon],
    ],

    'EXPR_POW':  [['EXPR_UNARY', "EXPR_POW'"]],
    "EXPR_POW'": [
        ['power', 'EXPR_UNARY', "EXPR_POW'"],
        [epsilon],
    ],

    'EXPR_UNARY': [
        ['not',   'EXPR_UNARY'],
        ['minus', 'EXPR_UNARY'],
        ['plus',  'EXPR_UNARY'],
        ['EXPR_POSTFIX'],
    ],

    'EXPR_POSTFIX': [['EXPR_PRIMARIO', "EXPR_POSTFIX'"]],

    "EXPR_POSTFIX'": [
        ['period',      'id',   "EXPR_POSTFIX_CALL'"],
        ['opening_bra', 'EXPR', 'closing_bra', "EXPR_POSTFIX'"],
        ['increment',   "EXPR_POSTFIX'"],
        ['decrement',   "EXPR_POSTFIX'"],
        [epsilon],
    ],

    "EXPR_POSTFIX_CALL'": [
        ['opening_par', 'ARGS', 'closing_par', "EXPR_POSTFIX'"],
        ["EXPR_POSTFIX'"],
    ],

    # EXPR_PRIMARIO: sin consola como raíz; con NombreObjeto, objeto literal, crear
    'EXPR_PRIMARIO': [
        ['num'],
        ['str'],
        ['verdadero'],
        ['falso'],
        ['nulo'],
        ['indefinido'],
        ['Infinito'],
        ['NuN'],
        ['id',           'ID_EXPR_SUF'],
        ['NOMBRE_OBJETO','period', 'id', 'opening_par', 'ARGS', 'closing_par'],
        ['opening_par',  'PAR_EXPR_O_ARROW'],
        ['opening_bra',  'LISTA_EXPR', 'closing_bra'],
        ['opening_key',  'OBJ_PROPS',  'closing_key'],
        ['crear',        'CREAR_TARGET', 'opening_par', 'ARGS', 'closing_par'],
    ],

    'ID_EXPR_SUF': [
        ['opening_par', 'ARGS', 'closing_par', 'ENCADENADO_EXPR'],
        [epsilon],
    ],

    # f()(x)(y) en expresiones
    'ENCADENADO_EXPR': [
        ['opening_par', 'ARGS', 'closing_par', 'ENCADENADO_EXPR'],
        [epsilon],
    ],

    # (expr, expr, ...) opcionalmente => cuerpo de flecha
    'PAR_EXPR_O_ARROW': [
        ['EXPR', 'PAR_RESTO', 'closing_par', 'ARROW_OPT'],
    ],

    'PAR_RESTO': [
        ['comma', 'EXPR', 'PAR_RESTO'],
        [epsilon],
    ],

    'ARROW_OPT': [
        ['arrow', 'ARROW_BODY'],
        [epsilon],
    ],

    # { = bloque; cualquier otro inicio = expresión sin {
    'ARROW_BODY': [
        ['opening_key', 'SL', 'closing_key'],
        ['EXPR_NO_KEY'],
    ],

    # Expresiones sin { como raíz — para EXPR_STMT y ARROW_BODY no-bloque
    # Sin id ni NombreObjeto en PRIMARIO para evitar conflicto con ASIGN/OBJETO en S
    'EXPR_NO_KEY':    [['EXPR_OR_NK',    'TERNARIO_OPT']],
    'EXPR_OR_NK':     [['EXPR_AND_NK',   "EXPR_OR'"]],
    'EXPR_AND_NK':    [['EXPR_EQ_NK',    "EXPR_AND'"]],
    'EXPR_EQ_NK':     [['EXPR_REL_NK',   "EXPR_EQ'"]],
    'EXPR_REL_NK':    [['EXPR_ADD_NK',   "EXPR_REL'"]],
    'EXPR_ADD_NK':    [['EXPR_MUL_NK',   "EXPR_ADD'"]],
    'EXPR_MUL_NK':    [['EXPR_POW_NK',   "EXPR_MUL'"]],
    'EXPR_POW_NK':    [['EXPR_UNARY_NK', "EXPR_POW'"]],

    'EXPR_UNARY_NK': [
        ['not',   'EXPR_UNARY'],
        ['minus', 'EXPR_UNARY'],
        ['plus',  'EXPR_UNARY'],
        ['EXPR_POSTFIX_NK'],
    ],

    'EXPR_POSTFIX_NK': [['EXPR_PRIMARIO_NK', "EXPR_POSTFIX'"]],

    # Sin id, sin NombreObjeto, sin opening_key
    'EXPR_PRIMARIO_NK': [
        ['num'], ['str'], ['verdadero'], ['falso'], ['nulo'],
        ['indefinido'], ['Infinito'], ['NuN'],
        ['opening_par', 'PAR_EXPR_O_ARROW'],
        ['opening_bra', 'LISTA_EXPR', 'closing_bra'],
        ['crear',       'CREAR_TARGET', 'opening_par', 'ARGS', 'closing_par'],
    ],

    # Objeto literal { prop: val, metodo(params){} }
    'OBJ_PROPS': [
        ['OBJ_PROP', 'OBJ_PROPS_RESTO'],
        [epsilon],
    ],

    'OBJ_PROPS_RESTO': [
        ['comma', 'OBJ_PROPS_CONT'],
        [epsilon],
    ],

    'OBJ_PROPS_CONT': [
        ['OBJ_PROP', 'OBJ_PROPS_RESTO'],
        [epsilon],
    ],

    'OBJ_PROP': [
        ['id',  'OBJ_PROP_VAL'],
        ['str', 'colon', 'EXPR'],
        ['num', 'colon', 'EXPR'],
    ],

    # id: expr   o   id(params) { bloque }  (método shorthand)
    'OBJ_PROP_VAL': [
        ['colon',       'EXPR'],
        ['opening_par', 'PARAMS', 'closing_par', 'BLOQUE'],
    ],

    'CREAR_TARGET': [
        ['id'], ['Arreglo'], ['Cadena'], ['Matriz'],
    ],

    'ARGS':       [['EXPR', 'ARGS_RESTO'],           [epsilon]],
    'ARGS_RESTO': [['comma', 'EXPR', 'ARGS_RESTO'],  [epsilon]],

    'LISTA_EXPR':       [['EXPR', 'LISTA_EXPR_RESTO'],          [epsilon]],
    'LISTA_EXPR_RESTO': [['comma', 'EXPR', 'LISTA_EXPR_RESTO'], [epsilon]],
}