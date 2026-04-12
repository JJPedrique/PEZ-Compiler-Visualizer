import BackEnd.DiccionarioDeDatos as DD
import BackEnd.ManejoDeErrores as ME

FILE = None
tokenizacion,tokens = [],[]
token_buffer = ""; isString = None; 
isLineComment = False; isMultiLineComment = False

class Token:
    def __init__(self,Num,Col,newValue,newType):
        self.Line = Num
        self.Column = Col 
        self.Value = newValue
        self.Type = newType

#region Tokenizacion
def Tokenizacion(Line,Column,Buffer):
    global token_buffer, isString, tokenizacion, tokens, isLineComment, isMultiLineComment

    #COMENTARIO MULTILINEA
    if not isString: 
        if not isMultiLineComment:
            if len(tokens)>1 and (tokens[-1].Value+Buffer[-1]) in DD.Standard_Token["MULTI-COMENTARIO"]:
                if not isMultiLineComment and (tokens[-1].Value+Buffer[-1]) == "*/": ME.ErrorLexico(FILE.NOMBRE,Line,Column,1) 
                isMultiLineComment = True if (tokens[-1].Value+Buffer[-1]) == "/*" else False
                tokens.pop(); tokenizacion.pop(); tokenizacion.pop()
                token_buffer = ""
                return
        else:
            if Buffer[-2:] in DD.Standard_Token["MULTI-COMENTARIO"]:
                isMultiLineComment = True if Buffer[-2:] == "/*" else False
                token_buffer = ""
                return

    if isMultiLineComment:
        tokenizacion.pop()
        return

    #STRINGS
    if Buffer[-1] in DD.Standard_Token["String"]:
        if isString != None and Buffer[-1] == isString:
            tokens.append(Token(Line,Column,Buffer,"LITERAL"))
            token_buffer=""    
            tokenizacion[-1] = tokens[-1].Value[-1]
            isString = None
        else:
            if isString == None: isString = Buffer[-1]
        return
    
    if isString != None:
        tokenizacion[-1] = Buffer[1:]
        return

    #COMENTARIO LINEAL
    if len(tokens)>1 and (tokens[-1].Value+Buffer[-1]) == "//":
        isLineComment = True
        tokens.pop(); tokenizacion.pop(); tokenizacion.pop()
        if(len(Buffer[:-2])>=1): GetIdentifier(Line,Column,Buffer[:-2])
        token_buffer = ""
        return

    #ESPACIO
    if Buffer[-1] == " ":
        if(len(Buffer[:-1])>=1): GetIdentifier(Line,Column,Buffer[:-1])
        tokenizacion[-1] = Buffer[-1]
        token_buffer=""
        return

    #SEPARADORES
    for k in DD.Separator_Token.keys():
        if Buffer[-1] in DD.Separator_Token[k]:
            if(len(Buffer[:-1])>=1): GetIdentifier(Line,Column,Buffer[:-1])

            tokens.append(Token(Line,Column,Buffer[-1],f"{k}"))
            tokenizacion[-1] = tokens[-1].Value

            token_buffer=""
            return
    
    #OPERADORES
    for k in DD.Operator_Token.keys():
        if Buffer[-1] in DD.Operator_Token[k]:
            if(len(Buffer[:-1])>=1): GetIdentifier(Line,Column,Buffer[:-1])

            tokens.append(Token(Line,Column,Buffer[-1],f"{k}"))
            tokenizacion[-1] = tokens[-1].Value
            token_buffer=""

            for ki in DD.Operator_Token.keys():
                if len(tokens)>0 and (tokens[-2].Value+tokens[-1].Value) in DD.Operator_Token[ki]:
                    tokens[-2].Value = tokens[-2].Value+tokens[-1].Value
                    tokens[-2].Type = ki
                    tokens.pop()

                    tokenizacion[-1] = tokens[-1].Value
                    token_buffer=""
                    return
        
            return

#region identificacion
def GetIdentifier(Line,Column,SubBuffer):
    global tokens

    #ENTEROS
    try: 
        int(SubBuffer)
        tokens.append(Token(Line,Column,SubBuffer,"LITERAL")); return
    except:pass

    #FLOTANTES
    try: 
        float(SubBuffer)
        tokens.append(Token(Line,Column,SubBuffer,"LITERAL")); return
    except:pass 

    #KEYWORDS
    for k in DD.Keyword_Token.keys():
        if SubBuffer in DD.Keyword_Token[k]:
            tokens.append(Token(Line,Column,SubBuffer,f"{k}")); return

    #KEYWORD DOS
    for k in DD.Library_Token.keys():
        if SubBuffer in DD.Library_Token[k]:
            tokens.append(Token(Line,Column,SubBuffer,f"{k}")); return

    #IDENTIFICADOR
    if len(SubBuffer) > 32:  ME.ErrorLexico(FILE.NOMBRE,Line,Column,3)
    if SubBuffer[0].isnumeric(): ME.ErrorLexico(FILE.NOMBRE,Line,Column,4)
    for especial in "$¡¨´'@":
        if SubBuffer.find(especial) != -1:
            ME.ErrorLexico(FILE.NOMBRE,Line,Column,5)
            break

    tokens.append(Token(Line,Column,SubBuffer,"IDENTIFICADOR")); return

#region Mostrar Info
def MostrarInfo():
    global caracteres,tokenizacion,tokens,tipos
    print("|--------------------|-----------ANALIZDOR LEXICO-----------------------------------|")
    print("|      CARACTER      |    TOKENIZACION    |       TOKEN        |      ATRIBUTO      |")
    print("|--------------------|--------------------|--------------------|--------------------|")
    
    i = 0
    while i < len(tokenizacion):
        if i < len(tokens):
            print(f"|{tokenizacion[i][-1]:<20}|{tokenizacion[i]:<20}|{tokens[i].Value:<20}|{tokens[i].Type:<20}|")  
            i+=1
            continue
        print(f"|{tokenizacion[i][-1]:<20}|{tokenizacion[i]:<20}|")  
        i+=1

#region Tokenizer
def AnalisisLexico(File):
    global FILE,token_buffer, isString, isLineComment,isMultiLineComment, tokenizacion, tokens

    #reset
    FILE = File
    tokenizacion.clear(); tokens.clear()
    token_buffer = ""
    isString = None; isLineComment = False; isMultiLineComment = False

    #for each line Tokenizer
    for i,Line in enumerate(File.CODIGO.split('\n')):
        Line = Line.split("#")[0]
        isLineComment = False

        j = 0
        for c in Line.strip():
            token_buffer += c
            tokenizacion.append(token_buffer)

            Tokenizacion(i,j,token_buffer)
            j+=1
            if isLineComment: break
            
        if (not isMultiLineComment and len(token_buffer)>0):
            GetIdentifier(i,j, token_buffer)
            token_buffer = ""
        
    if isString != None:  ME.ErrorLexico(FILE.NOMBRE,len(File.CODIGO.split('\n')),6)
    if isMultiLineComment: ME.ErrorLexico(FILE.NOMBRE,len(File.CODIGO.split('\n')),0)

    File.ANALISIS_LEXICO["Tokenizacion"] = tokenizacion.copy()
    File.ANALISIS_LEXICO["Tokens"] = tokens.copy()

    #MostrarInfo()