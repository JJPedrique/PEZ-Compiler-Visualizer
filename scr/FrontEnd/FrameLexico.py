import customtkinter as ctk
from PIL import Image

class FrameLexico(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master,label_text="Archivos Analizados Léxicamente")
        self.pack(fill=ctk.BOTH, expand=True)
        self.isReset = False
        self.Reset()

    def Reset(self):
        for i in self.winfo_children(): i.destroy()
        if self.isReset: return

        TextoTitulo = ctk.CTkLabel(self,text="No hay registros",font=("Consolas",15,"bold"))
        TextoTitulo.pack(fill=ctk.X)

        EntradaTokenizacion = ctk.CTkLabel(self,text="Compile un archivo para visualizar su compilación",anchor="n")
        EntradaTokenizacion.pack(fill=ctk.X)

        Wizard = ctk.CTkLabel(self,text=None,image=ctk.CTkImage(light_image=Image.open("res/Book.png"),size=(75,75)))
        Wizard.pack(fill=ctk.X)

        self.isReset = not self.isReset

    def AgregarArchivoTokenizado(self,File):
        if self.isReset:
            for i in self.winfo_children(): i.destroy()
            self.isReset = not self.isReset

        ArchivoTokenizado(self,File)
        

class ArchivoTokenizado(ctk.CTkFrame):
    def __init__(self, master,File):
        super().__init__(master)
        self.pack(fill=ctk.X)
        self.grid_columnconfigure([i for i in range(4)],weight=1)

        TextoNombreArchivo = ctk.CTkLabel(self,text=File.NOMBRE+".cpp",font=("Consolas",15,"bold"), corner_radius=100,
                                    text_color=ctk.ThemeManager.theme["CTkButton"]["text_color"],
                                    fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        TextoNombreArchivo.grid(row=0,column=0,columnspan=4,sticky="we")

        TextoCARACTER = ctk.CTkLabel(self,text="CARACTER",font=("Consolas",15,"bold"))
        TextoCARACTER.grid(row=1,column=0)

        txtCaracter = "\n".join([i[-1] for i in File.ANALISIS_LEXICO["Tokenizacion"]])
        EntradaCaracter = ctk.CTkLabel(self,text=txtCaracter,anchor="n")
        EntradaCaracter.grid(row=2,column=0,sticky="n")

        TextoTOKENIZADOR = ctk.CTkLabel(self,text="TOKENIZACIÓN",font=("Consolas",15,"bold"))
        TextoTOKENIZADOR.grid(row=1,column=1)

        txtTokenizacion = "\n".join([i for i in File.ANALISIS_LEXICO["Tokenizacion"]])
        EntradaTokenizacion = ctk.CTkLabel(self,text=txtTokenizacion,anchor="n")
        EntradaTokenizacion.grid(row=2,column=1,sticky="n")

        TextoTOKEN = ctk.CTkLabel(self,text="TOKEN",font=("Consolas",15,"bold"))
        TextoTOKEN.grid(row=1,column=2)

        txtTokens = "\n".join([i.Value for i in File.ANALISIS_LEXICO["Tokens"]])
        EntradaTokens = ctk.CTkLabel(self,text=txtTokens,anchor="n")
        EntradaTokens.grid(row=2,column=2,sticky="n")

        TextoTIPO = ctk.CTkLabel(self,text="TIPO",font=("Consolas",15,"bold"))
        TextoTIPO.grid(row=1,column=3)

        txtTokenstype = "\n".join([i.Type for i in File.ANALISIS_LEXICO["Tokens"]])
        EntradaTipos = ctk.CTkLabel(self,text=txtTokenstype,anchor="n")
        EntradaTipos.grid(row=2,column=3,sticky="n")

        Vacio = ctk.CTkLabel(self,text=None)
        Vacio.grid(row=3,column=0,columnspan=4,sticky="we")