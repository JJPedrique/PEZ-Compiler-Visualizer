import BackEnd.ManejoDeErrores as ME
import BackEnd.DiccionarioDeDatos as DD
FILE = None

class Simbolo:
    def __init__(self,newName,newType,newScope,newOffset,newParameter="N/A"):
        self.Name = newName
        self.Type = newType
        self.Scope = newScope
        self.Offset = newOffset
        self.Parameter = newParameter
        self.Memory = hex(id(newName))

DiccionarioDeSimbolos = []

def MostrarInfo():
    global DiccionarioDeSimbolos
    print("|--------------------|--------------------|ANALIZDOR  SEMANTICO|--------------------|--------------------|")
    print("|       NOMBRE       |        TIPO        |       AMBITO       |        NIVEL       |       MEMORIA      |")
    print("|--------------------|--------------------|--------------------|--------------------|--------------------|")
    
    for v in DiccionarioDeSimbolos:
        print(f"|{v.Name:<20}|{v.Type:<20}|{v.Scope:<20}|{v.Offset:<20}|{str(v.Parameter):<20}|")

def FindCycle(Tree):
    global FILE
    if Tree.Token.Value == f"{FILE.NOMBRE.upper()}.cpp": return False
    if Tree.Token.Value.split("_")[0] == "CICLO": return True
    return FindCycle(Tree.Parent)

def ReadTree(Tree,Scope="GLOBAL",Offset = 0):
    global DiccionarioDeSimbolos,FILE
    #print(Scope,3*Offset*" "+Tree.Token.Value)

    if Tree.Token.Value == "CONDICION":
        ExpData = CheckExpresion(Tree.Children[0],Scope,Offset)

        if ExpData is None: return
        
        if ExpData != "bool":
            ME.ErrorSemantico(FILE.NOMBRE,Tree.Children[0].Children[0].Token.Line,Tree.Children[0].Children[0].Token.Column,0,ExpData,"bool")
        
        return
    
    if Tree.Token.Value in ["break","continue"]:
        if(not FindCycle(Tree)): 
            ME.ErrorSemantico(FILE.NOMBRE,Tree.Token.Line,Tree.Token.Column,6)
            return

    #VARIABLES

    #CREAR
    if Tree.Token.Value == "CREAR_VARIABLE":
        Data = Tree.Children[0].Token
        Var = Tree.Children[1].Token
        ExpData = CheckExpresion(Tree.Children[3],Scope,Offset)


        for A in DD.Keyword_Token.keys():
            if Var.Value in DD.Keyword_Token[A]:
                ME.ErrorSemantico(FILE.NOMBRE,Var.Line,Var.Column,3)
                return
            
        DiccionarioDeSimbolos.append(Simbolo(Var.Value,Data.Value,Scope,Offset))
        
        if ExpData is None: return

        if Data.Value != ExpData:
            ME.ErrorSemantico(FILE.NOMBRE,Var.Line,Var.Column,0,Data.Value,ExpData)
        
        return

    #ASIGNAR
    if Tree.Token.Value == "ASIGNAR_VARIABLE":
        Var = Tree.Children[0].Token
        ExpData = CheckExpresion(Tree.Children[2],Scope,Offset)

        try:
            VarType = [i.Type 
                        for i in DiccionarioDeSimbolos
                        if i.Name == Var.Value
                        and i.Scope in [Scope,"GLOBAL"]
                        and i.Offset <= Offset][-1]

            if VarType != ExpData:
                ME.ErrorSemantico(FILE.NOMBRE,Var.Line,Var.Column,0,VarType,ExpData)
        except:
            ME.ErrorSemantico(FILE.NOMBRE,Var.Line,Var.Column,1,Var.Value)

        return

    #MONO ASIGNAR
    if Tree.Token.Value == "MONO_ASIGNACION_VARIABLE":
        Var = Tree.Children[1 if Tree.Children[0].Token.Value in ["++","--"] else 0].Token

        try:
            VarType = [i.Type 
                        for i in DiccionarioDeSimbolos
                        if i.Name == Var.Value
                        and i.Scope in [Scope,"GLOBAL"]
                        and i.Offset <= Offset][-1]

            if VarType != "int":
                ME.ErrorSemantico(FILE.NOMBRE,Var.Line,Var.Column,0,VarType,"int")
        except:
            ME.ErrorSemantico(FILE.NOMBRE,Var.Line,Var.Column,1,Var.Value)
 
        return

    #FUNCIONES

    #LLAMAR FUNCIONES
    if Tree.Token.Value.split("_")[0] == "LLAMADO": 
        try:
            FuncName = [i.Parameter 
                        for i in DiccionarioDeSimbolos
                        if i.Name == Tree.Children[0].Token.Value
                        and i.Scope in [Scope,"GLOBAL"]
                        and i.Offset <= Offset][-1]

            if len(Tree.Children[1].Children) != len(FuncName):
                ME.ErrorSemantico(FILE.NOMBRE,Tree.Children[0].Token.Line,Tree.Children[0].Token.Column,2)
                return
            
            for j,x in enumerate(Tree.Children[1].Children):
                
                ExpData = CheckExpresion(x,Scope,Offset)
                VarType = [i.Type 
                        for i in DiccionarioDeSimbolos
                        if i.Name == FuncName[j]
                        and i.Scope in [Scope,"GLOBAL"]
                        and i.Offset <= Offset][-1]

                if ExpData is None: return

                if VarType != ExpData:
                    ME.ErrorSemantico(FILE.NOMBRE,Tree.Children[0].Token.Line,Tree.Children[0].Token.Column,0,VarType,ExpData)
                    return
        except:
            ME.ErrorSemantico(FILE.NOMBRE,Tree.Children[0].Token.Line,Tree.Children[0].Token.Column,1,Tree.Children[0].Token.Value)
            return   

    #CREAR FUNCIONES
    if Tree.Token.Value.split("_")[0] == "FUNCION": 
        Data = Tree.Children[0].Token
        Var = Tree.Children[1].Token
        ParameterName = []

        #PARAMETROS
        for P in Tree.Children[2].Children:
            DiccionarioDeSimbolos.append(Simbolo(P.Children[1].Token.Value,P.Children[0].Token.Value,Scope,Offset))
            ParameterName.append(P.Children[1].Token.Value)

        DiccionarioDeSimbolos.append(Simbolo(Var.Value,Data.Value,Scope,Offset,ParameterName))
        Scope = Var.Value

    for i in Tree.Children:
        ReadTree(i,Scope,Offset+1)

def CheckExpresion(Tree,Scope,Offset):
    global DiccionarioDeSimbolos

    if len(Tree.Children) == 1:
        return GetDataType(Tree.Children[0].Token,Scope,Offset)
    elif(Tree.Token.Value == "MONO-EXPRESSION"):
        return GetDataType(Tree.Children[1].Token,Scope,Offset)
    else:
        A = CheckExpresion(Tree.Children[0],Scope,Offset) if Tree.Children[0].Token.Value in ["EXPRESSION","MONO-EXPRESSION"] else GetDataType(Tree.Children[0].Token,Scope,Offset)
        B = CheckExpresion(Tree.Children[2],Scope,Offset) if Tree.Children[2].Token.Value in ["EXPRESSION","MONO-EXPRESSION"] else GetDataType(Tree.Children[2].Token,Scope,Offset)

        if(None in [A,B]): return

        if(A!=B):
            ME.ErrorSemantico(FILE.NOMBRE,Tree.Children[1].Token.Line,Tree.Children[1].Token.Column,0,A,B)
            return None
        
        if(Tree.Children[1].Token.Value in ["<","<=",">",">=","==","!="]):return "bool"
        return A

def GetDataType(Token,Scope,Offset):
    global DiccionarioDeSimbolos

    try: 
        int(Token.Value)
        return "int"
    except: pass

    try: 
        float(Token.Value)
        return "float"
    except: pass
    
    if(Token.Value == "true" or Token.Value == "false"):
        return "bool"

    if(Token.Value[0] == "\""):
        return "string"
    
    if(Token.Value[0] == "\'"):
        return "char"

    try:
        return [i.Type 
                for i in DiccionarioDeSimbolos
                if i.Name == Token.Value
                and i.Scope in [Scope,"GLOBAL"]
                and i.Offset <= Offset][-1]
    except:
        ME.ErrorSemantico(FILE.NOMBRE,Token.Line,Token.Column,1,Token.Value)
        return None
    

def AnalisisSemantico(File):
    global DiccionarioDeSimbolos,FILE
    FILE = File
    DiccionarioDeSimbolos.clear()

    ReadTree(File.ANALISIS_SINTACTICO["NodoRaiz"].Root)

    FILE.ANALISIS_SEMANTICO["Simbolos"] = DiccionarioDeSimbolos.copy()
    #MostrarInfo()