DiccionarioErrores = {
    "Lexico": 
    ["[ERROR N1 ] - Comentario no cerrado.",
     "[ERROR N2 ] - Comentario no abierto.",
     "[ERROR N3 ] - La KeyWord está mal escrita.",
     "[ERROR N4 ] - Nombre de variable muy largo.",
     "[ERROR N5 ] - Nombre de variable no debe iniciar con un número.",
     "[ERROR N6 ] - Nombre de variable no debe contener un caracter especial.",
     "[ERROR N7 ] - String no cerrado."],

    "Sintactico": 
    ["[ERROR N8 ]- Paréntesis no abiertos o no cerrados.",
     "[ERROR N9 ]- Corchetes no abiertos o no cerrados.",
     "[ERROR N10] - Llaves no abiertas o no cerradas.",
     "[ERROR N11] - Palabra no esperada.",
     "[ERROR N12] - El \"FOR \" debe tener 2 comas dentro de sus paréntesis.",
     "[ERROR N13] - Cualquier ciclo distinto a \"FOR\" no debe tener comas dentro de sus paréntesis.",
     "[ERROR N14] - Falta \";\"",
     "[ERROR N15] - Error de expresión."],

    "Semantico": 
    ["[ERROR N16] - La variable no es compatible.",
     "[ERROR N17] - La variable o función no fue declarada anteriormente.",
     "[ERROR N18] - La cantidad de parametros no coinciden con los preestablecido.",
     "[ERROR N19] - La variable tiene el nombre de una palabra reservada.",
     "[ERROR N20] - La funciones \"VOID\" no debe retornar algun valor.",
     "[ERROR N21] - La operacion no es compatible.",
     "[ERROR N22] - \"BREAK\" y \"CONTINUE\" deben estar adentro de un ciclo."],
}

ErrorCounter = []

def ErrorLexico(Archivo, Line,Column, Num):
    DE = DiccionarioErrores["Lexico"]
    ErrorCounter.append(f"Error Léxico - Archivo {Archivo}.cpp - Línea {Line} - Columna {Column}\n{DE[Num]}")

def ErrorSintactico(Archivo, Line,Column, Num):
    DE = DiccionarioErrores["Sintactico"]
    ErrorCounter.append(f"Error Sintáctico - Archivo {Archivo}.cpp - Línea {Line} - Columna {Column}\n{DE[Num]}")

def ErrorSemantico(Archivo, Line,Column, Num,A = None, B= None):
    DE = DiccionarioErrores["Semantico"]
    txt = f"Error Semántico - Archivo {Archivo}.cpp - Línea {Line} - Columna {Column}\n{DE[Num]}"

    if Num in [0,5]:
        txt += f" Error de tipo {A} <=> {B}"

    if Num == 1:
        txt += f" Variable: {A}"  

    ErrorCounter.append(txt)