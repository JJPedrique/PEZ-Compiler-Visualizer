import BackEnd.ManejoDeErrores as ME
import BackEnd.DiccionarioDeDatos as DD
import BackEnd.AnalizadorLexico as AL

from BackEnd.Arbol import Tree

FILE = None

#region Arboles - Parametros ()[]{}
precedencia = {
    '||':0 ,'(': 0,
    '&&':1 ,
    '==':2 ,'!=':2 ,'<':2 ,'>':2 ,'<=':2 ,'>=':2 ,
    '+':3 ,'-':3,
    '*':4 ,'/':4 ,'%':4,
    '!':5,
    'u+':6, 'u-':6,}

def CreateExpression(Tokens):
    def shuntingYard():
        output = []; opStack = []; lastToken = None
        for T in Tokens:
            if T.Type in ["IDENTIFICADOR", "LITERAL"]: 
                output.append(T)
                
            elif T.Value == '(': 
                opStack.append(T)
                
            elif T.Value == ')':
                while opStack and opStack[-1].Value != '(': 
                    output.append(opStack.pop())
                if not opStack:
                    ME.ErrorSintactico(FILE.NOMBRE, T.Line,T.Column, 0)
                    return None
                opStack.pop()

            elif T.Type in ["BI-OPERACION", "COMPARACION"]:
                if T.Value in ['+','-']:
                    if not lastToken or (lastToken.Type in ['BI-OPERACION','COMPARACION'] or lastToken.Value == '('):
                        try: T.Value = 'u'+T.Value
                        except Exception: pass
                while opStack and opStack[-1].Value != '(' and precedencia.get(T.Value,0) <= precedencia.get(opStack[-1].Value,0) and T.Value != '!':
                    output.append(opStack.pop())
                opStack.append(T)
            lastToken = T

        while opStack:
            if opStack[-1].Value == '(':
                ME.ErrorSintactico(FILE.NOMBRE, T.Line,T.Column, 0)
                return None
            output.append(opStack.pop())
        return output
    
    newTree = Tree(AL.Token(0,0,"EXPRESSION","TITTLE"))

    postfix = shuntingYard()
    if postfix is None: return newTree
    
    stack = []
    for T in postfix:
        if T.Type in ["IDENTIFICADOR", "LITERAL"]:
            stack.append(T)
            continue

        if T.Type in ["BI-OPERACION", "COMPARACION"]:
            if T.Value in ["!","u+","u-"]:
                if len(stack)<1:
                    ME.ErrorSintactico(FILE.NOMBRE, T.Line, T.Column, 7)
                    return newTree
                
                operando = stack.pop()
                SubExpTree = Tree(AL.Token(0,0,"MONO-EXPRESSION","TITTLE"))
                SubExpTree.AddNode(T)
                SubExpTree.AddTree(operando) if isinstance(operando,Tree) else SubExpTree.AddNode(operando)
                stack.append(SubExpTree)
                continue
            
            if len(stack) < 2:
                ME.ErrorSintactico(FILE.NOMBRE, T.Line, T.Column, 7)
                return newTree
        
            R = stack.pop()
            L = stack.pop()
            SubExpTree = Tree(AL.Token(0,0,"EXPRESSION","TITTLE"))
            SubExpTree.AddTree(L) if isinstance(L,Tree) else SubExpTree.AddNode(L)
            SubExpTree.AddNode(T)
            SubExpTree.AddTree(R) if isinstance(R,Tree) else SubExpTree.AddNode(R)
            stack.append(SubExpTree)

    if not stack:
        last_line = postfix[-1].Line if postfix else 0
        last_column = postfix[-1].Column if postfix else 0
        ME.ErrorSintactico(FILE.NOMBRE, last_line,last_column, 7)
        return newTree

    exprSubTree = stack.pop()
    if isinstance(exprSubTree,Tree):
        newTree.Root = exprSubTree.Root
    else:
        newTree.AddNode(exprSubTree)
    return newTree
    
#region Arboles Codigos
def CreateConditionTree(stack,ConditionStack,BodyStack):
    newTree = Tree(AL.Token(0,0,"CONDICIONAL","TITTLE"))

    for s in stack:
        if s.Value not in DD.Keyword_Token["CONDICIONAL"]: 
            ME.ErrorSintactico(FILE.NOMBRE,s.Line,s.Column,3)            
        newTree.AddNode(s)

    if stack[-1].Value == "if":
        ConditionTree = Tree(AL.Token(0,0,"CONDICION","TITTLE"))
        ConditionTree.AddTree(CreateExpression(ConditionStack[1:-1]))
        newTree.AddTree(ConditionTree)

    BodyTree = CreateBodyTree("CUERPO",BodyStack[1:-1])
    newTree.AddTree(BodyTree)

    return newTree

def CreateParameterTree(stack,Call = False):
    
    newTree = Tree(AL.Token(0,0,"PARAMETROS","TITTLE"))
    if len(stack)==0:return newTree
    
    indexComa = []
    for i in range(len(stack)):
        if stack[i].Value == ",": indexComa.append(i)
    
    lastIndex = 0
    if len(indexComa)>0:
        for i in indexComa:
            if Call:
                newTree.AddTree(CreateExpression(stack[lastIndex:i]))
            else:
                newTree.AddTree(CreateStatementTree(stack[lastIndex:i]))
            lastIndex = i+1
    if Call:
        newTree.AddTree(CreateExpression(stack[lastIndex:]))
    else:
        newTree.AddTree(CreateStatementTree(stack[lastIndex:]))
    
    return newTree

#WHILE - FOR - FOR EACH - DO WHILE
#TODO DO WHILE 
def CreateLoopTree(stack,ConditionStack,BodyStack):
    newTree = Tree(AL.Token(0,0,f"CICLO_{stack[0].Value.upper()}","TITTLE"))

    for s in stack:
        if s.Value not in DD.Keyword_Token["CICLO"]: 
            ME.ErrorSintactico(FILE.NOMBRE,s.Line,s.Column,3)            
    
    newTree.AddNode(stack[0])

    ConditionTree = Tree(AL.Token(0,0,"CENTINELA","TITTLE"))

    indexComa = []
    for i in range(len(ConditionStack)):
        if ConditionStack[i].Value == ";": indexComa.append(i)
    
    if stack[0].Value == "for":
        if len(indexComa) == 2:
            LComa = indexComa[0]+1; RComa = indexComa[1]
            ConditionTree.AddTree(CreateStatementTree(ConditionStack[1:LComa])) 

            C = Tree(AL.Token(0,0,"CONDICION","TITTLE"))
            C.AddTree(CreateExpression(ConditionStack[LComa:RComa])) 
            ConditionTree.AddTree(C)


            ConditionTree.AddTree(CreateStatementTree(ConditionStack[RComa+1:-1])) 
        else: 
            ME.ErrorSintactico(FILE.NOMBRE,stack[0].Line,stack[0].Column,4)
    else:
        if not indexComa:
            C = Tree(AL.Token(0,0,"CONDICION","TITTLE"))
            C.AddTree(CreateExpression(ConditionStack[1:-1])) 
            ConditionTree.AddTree(C)
        else: 
            ME.ErrorSintactico(FILE.NOMBRE,stack[0].Line,stack[0].Column,5)

    BodyTree = CreateBodyTree("CUERPO",BodyStack[1:-1])


    if stack[0].Value == "do":
        newTree.AddTree(BodyTree)
        newTree.AddNode(stack[1])
        newTree.AddTree(ConditionTree)
    else:
        newTree.AddTree(ConditionTree)
        newTree.AddTree(BodyTree)

    return newTree

#MAIN - CUALQUIER OTRA FUNCION
def CreateFunctionTree(stack,ConditionStack,BodyStack):
    newTree = Tree(AL.Token(0,0,f"FUNCION_{stack[1].Value.upper()}","TITTLE"))

    for s in stack:
        newTree.AddNode(s)
    
    newTree.AddTree(CreateParameterTree(ConditionStack[1:-1]))

    BodyTree = CreateBodyTree("CUERPO",BodyStack[1:-1])
    newTree.AddTree(BodyTree)

    return newTree

#DEFAULT CUALQUIER SENTENCIA
def CreateStatementTree(stack):
    newTree = Tree(AL.Token(0,0,"SENTENCIA","TITTLE"))

    if "TIPO_DATO" in [i.Type for i in stack]:
        if "=" in [i.Value for i in stack]:
            if "[" in [i.Value for i in stack]:
                newTree.Root.Token.Value = "CREAR_ARREGLO"
            else:
                newTree.Root.Token.Value = "CREAR_VARIABLE"

                index = [i.Value for i in stack].index("=")+1
                for i in range(index):
                    newTree.AddNode(stack[i])
                newTree.AddTree(CreateExpression(stack[index:-1]))
                return newTree

        if "(" in [i.Value for i in stack] and ")" in [i.Value for i in stack]:
            newTree.Root.Token.Value = f"PROTOTIPO_{stack[1].Value.upper()}"
            start_Parentesis = [i.Value for i in stack].index("(")
            end_Parentesis = [i.Value for i in stack].index(")")

            for i in range(start_Parentesis):
                newTree.AddNode(stack[i])
            
            if end_Parentesis-start_Parentesis != 1: 
                newTree.AddTree(CreateParameterTree(stack[start_Parentesis+1:end_Parentesis]))
                
            return newTree
    
        newTree.Root.Token.Value = "PARAMETRO_VAR"

    if len([i.Value for i in stack if i.Value in DD.Operator_Token["MONO-OPERACION"]])>0:
        newTree.Root.Token.Value = "MONO_ASIGNACION_VARIABLE"
        for s in stack:
            newTree.AddNode(s)
        return newTree

    if len([i.Value for i in stack if i.Value in DD.Operator_Token["ASIGNACION"]])>0:
        newTree.Root.Token.Value = "ASIGNAR_VARIABLE"
        for i in range(2):
            newTree.AddNode(stack[i])
        newTree.AddTree(CreateExpression(stack[2:-1]))
        return newTree

    if "(" in [i.Value for i in stack] and ")" in [i.Value for i in stack]:
        newTree.Root.Token.Value = f"LLAMADO_{stack[0].Value.upper()}"
        start_Parentesis = [i.Value for i in stack].index("(")
        end_Parentesis = [i.Value for i in stack].index(")")

        if len(stack[:start_Parentesis])>1:ME.ErrorSintactico(FILE.NOMBRE,stack[0].Line,stack[0].Column,3)

        for i in range(start_Parentesis):
            newTree.AddNode(stack[i])
 
        newTree.AddTree(CreateParameterTree(stack[start_Parentesis+1:end_Parentesis],True))
            
        return newTree

    for s in stack:
        newTree.AddNode(s)

    return newTree

#region Arbol Sintactico Abstracto
#SENTECIAS Y BLOQUES DE CODIGO (MULTIVERSO)
def CreateBodyTree(Name,Tokens):
    newBodyTree = Tree(AL.Token(0,0,Name,"TITTLE"))

    Parentesis = 0; start_Parentesis = -1; end_Parentesis = -1
    Llaves = 0; start_Llaves = -1; end_Llaves = -1
    stack = []; i = -1

    for T in Tokens:
        i +=1;stack.append(T)

        if T.Value=="(":
            Parentesis+=1
            if  start_Parentesis == -1 and Llaves == 0: start_Parentesis = i

        if T.Value==")":
            Parentesis-=1
            if end_Parentesis == -1 and Llaves == 0 and Parentesis == 0: end_Parentesis = i+1

        if T.Value=="{":
            Llaves+=1
            if start_Llaves == -1 and Parentesis == 0: start_Llaves = i

        if T.Value=="}":
            Llaves-=1
            if end_Llaves == -1 and Parentesis == 0 and Llaves == 0: end_Llaves = i+1

        if Parentesis == 0 and Llaves == 0:
            #SENTENCIA
            if T.Value == ";":
                newBodyTree.AddTree(CreateStatementTree(stack))
                stack.clear(); i=-1
                start_Parentesis = -1; end_Parentesis = -1; start_Llaves = -1; end_Llaves = -1
                continue                  
            
            if -1 not in [start_Parentesis,end_Parentesis,start_Llaves,end_Llaves]:
                if stack[0].Type == "TIPO_DATO" and stack[1].Type == "IDENTIFICADOR":
                    newBodyTree.AddTree(CreateFunctionTree(stack[:2],stack[start_Parentesis:end_Parentesis],stack[start_Llaves:end_Llaves]))  
                    stack.clear(); i=-1
                    start_Parentesis = -1; end_Parentesis = -1; start_Llaves = -1; end_Llaves = -1
                    continue

                #FOR WHILE
                if stack[0].Type == "CICLO":
                    if stack[0].Value == "do": 
                        if end_Llaves - start_Parentesis != 0: ME.ErrorSintactico(FILE.NOMBRE,stack[0].Line,stack[0].Column,3)
                        subStack = stack[:start_Llaves]
                        subStack.extend(stack[end_Llaves:start_Parentesis])
                    else:
                        if start_Llaves - end_Parentesis != 0: ME.ErrorSintactico(FILE.NOMBRE,stack[0].Line,stack[0].Column,3)
                        subStack = stack[:start_Parentesis]

                    newBodyTree.AddTree(CreateLoopTree(subStack,stack[start_Parentesis:end_Parentesis],stack[start_Llaves:end_Llaves]))               
                    stack.clear(); i=-1
                    start_Parentesis = -1; end_Parentesis = -1; start_Llaves = -1; end_Llaves = -1
                    continue 

                #IF
                if stack[0].Type == "CONDICIONAL":
                    if start_Llaves - end_Parentesis != 0: ME.ErrorSintactico(FILE.NOMBRE,stack[0].Line,stack[0].Column,3)

                    if (stack[0].Value == "if") or (stack[0].Value == "else" and newBodyTree.Root.Children[-1].Token.Value == "CONDICIONAL"):
                        newBodyTree.AddTree(CreateConditionTree(stack[:start_Parentesis],stack[start_Parentesis:end_Parentesis],stack[start_Llaves:end_Llaves]))               
                        stack.clear(); i=-1 
                        start_Parentesis = -1; end_Parentesis = -1; start_Llaves = -1; end_Llaves = -1
                        continue

            if -1 not in [start_Llaves,end_Llaves]:
                if stack[0].Value == "else" and newBodyTree.Root.Children[-1].Token.Value == "CONDICIONAL":
                    Fuck = CreateConditionTree(stack[:start_Llaves],stack[start_Parentesis:end_Parentesis],stack[start_Llaves:end_Llaves])
                    Fuck.Root.Parent = newBodyTree.Root.Children[-1]
                    newBodyTree.Root.Children[-1].Children.append(Fuck.Root)               
                    stack.clear(); i=-1 
                    start_Parentesis = -1; end_Parentesis = -1; start_Llaves = -1; end_Llaves = -1
                    continue   

    if len(stack)>0 and stack[-1].Value != ";": ME.ErrorSintactico(FILE.NOMBRE,Tokens[0].Line,Tokens[0].Column,6)
    if Parentesis != 0: ME.ErrorSintactico(FILE.NOMBRE,Tokens[-1].Line,Tokens[-1].Column,0)
    if Llaves != 0: ME.ErrorSintactico(FILE.NOMBRE,Tokens[-1].Line,Tokens[-1].Column,2)

    return newBodyTree

#region Mostrar Info
def MostrarInfo(Node,prefix="",LastChild=True,LVL=0):
    connector = ("└─── " if LastChild else "├─── ") if LVL!=0 else ""
    LVL += 1 
    
    print(prefix+connector+str(Node.Token.Value))

    if Node.Children:
        newPrefix = prefix + (("     " if LastChild else "│    ") if LVL!=1 else "")
        for i,child in enumerate(Node.Children):
            LastChild = i == len(Node.Children)-1
            MostrarInfo(child,newPrefix,LastChild,LVL)

#region Analisis 
def AnalisisSintactico(File):
    global FILE
    FILE = File

    t = CreateBodyTree(f"{File.NOMBRE.upper()}.cpp", FILE.ANALISIS_LEXICO["Tokens"])
    t.saveTree(t.Root)
    FILE.ANALISIS_SINTACTICO["NodoRaiz"] = t
    #MostrarInfo(t.Root)