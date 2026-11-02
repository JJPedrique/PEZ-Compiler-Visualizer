Standard_Token={
    "Libraries":
    ["cstdio","cstdlib","cwchar","fstream","iomanip","ios","iosfwd","iostream","istream","ostream","sstream","streambuf",
    "cctype","cstring","cwctype","string",
    "bitset","deque","set","stack","vector","iterator",
    "algorithm",
    "cmath","complex","numeric","valarray",
    "cassert","cerrno","exception","stdexcept",
    "ctime","functional","memory","utility",
    "clocale","locale",
    "cfloat","climits","csetjmp","csignal",
    "cstdarg","cstddef","limits","new","typeinfo"],

    "MULTI-COMENTARIO":
    ["/*","*/"],

    "String":
    ["\"","'"],
}

#En caso de cualquier pregunta de funciones
#aqui se colocan todas las KEYWORDS de las librerias
#Mods
Library_Token={    
    "FUNC_MATH": 
    ["abs","div","acos","asin","atan","atan2","ceil","cos","cosh","exp","fabs","floor","fmod","frexp",
     "ldexp","log","log10","modf","pow","sin","sinh","sqrt","tan","tan"],
    
    "IOSTREAM_FUNC": 
    ["cin","cout","cerr","clog","wcin","wcout","wcerr","wclog","endl"],
}

Keyword_Token = {
    "CONDICIONAL": 
    ["if", "else","switch"],
    
    "TIPO_DATO":
    ["int", "char", "double", "float", "bool", "void", "long", "short","string","class","struct"],

    "CICLO":
    ["while","for","do"],

    "OTRO":
    ["case","break", "continue", "return", "goto",
     "static", "extern", "mutable", "register", "volatile",
     "public", "private", "protected", "virtual", "this", "friend",
     "namespace", "using", "typedef", "const", "sizeof", "typeid", "template", "new", "delete",
     "auto","default","enum","signed","union","unsigned",]
}

Separator_Token = {
    "ABRIR_GRUPAMIENTO":
    ["{","[","("],

    "CERRAR_GRUPAMIENTO":
    [")","]","}"],

    "ABRIR_SENTENCIA":
    [":"],

    "CERRAR_SENTENCIA":
    [";",","],
}

Operator_Token = {
    "BI-OPERACION":
    ["+","-","*","/","%"],

    "MONO-OPERACION":
    ["++","--"],
    
    "COMPARACION":
    ["<","<=",">",">=","==","!=","&&","||","!",],

    "BITS":
    ["&","|","<<",">>","~","^"],

    "ASIGNACION":
    ["=","+=","-=","*=","/=","%=","<<=",">>=","&=","^=","|="],
}