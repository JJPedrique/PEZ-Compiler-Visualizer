REPOSITORIO = []

class CPP:
    def __init__(self,NOMBRE,CODIGO):
        self.NOMBRE = NOMBRE
        self.CODIGO = CODIGO
        self.ANALISIS_LEXICO = { "Tokenizacion":[], "Tokens":[]}
        self.ANALISIS_SINTACTICO = {"NodoRaiz":None}    
        self.ANALISIS_SEMANTICO = {"Simbolos":[]}