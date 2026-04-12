import customtkinter as ctk
from PIL import Image

class FrameSemantico(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master,label_text="Archivos Analizados Semanticamente")
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

        Wizard = ctk.CTkLabel(self,text=None,image=ctk.CTkImage(light_image=Image.open("res/Idea.png"),size=(75,75)))
        Wizard.pack(fill=ctk.X)
        
        self.isReset = not self.isReset
        
    def AgregarArchivoSemantizado(self,File):
        if self.isReset:
            for i in self.winfo_children(): i.destroy()
            self.isReset = not self.isReset

        ArchivoSemantizado(self,File)

class ArchivoSemantizado(ctk.CTkFrame):
    def __init__(self, master,File):
        super().__init__(master)
        self.pack(fill=ctk.X)
        self.grid_columnconfigure([i for i in range(6)],weight=1)

        TextoNombreArchivo = ctk.CTkLabel(self,text=File.NOMBRE+".cpp",font=("Consolas",15,"bold"), corner_radius=100,
                                    text_color=ctk.ThemeManager.theme["CTkButton"]["text_color"],
                                    fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        TextoNombreArchivo.grid(row=0,column=0,columnspan=6,sticky="we")

        TextoNOMBRE = ctk.CTkLabel(self,text="NOMBRE",font=("Consolas",15,"bold"))
        TextoNOMBRE.grid(row=1,column=0)

        txtNombre = "\n".join([i.Name for i in File.ANALISIS_SEMANTICO["Simbolos"]])
        EntradaNombre = ctk.CTkLabel(self,text=txtNombre,anchor="n")
        EntradaNombre.grid(row=2,column=0,sticky="n")

        TextoTIPO = ctk.CTkLabel(self,text="TIPO",font=("Consolas",15,"bold"))
        TextoTIPO.grid(row=1,column=1)

        txtTipo = "\n".join([i.Type for i in File.ANALISIS_SEMANTICO["Simbolos"]])
        EntradaTipo = ctk.CTkLabel(self,text=txtTipo,anchor="n")
        EntradaTipo.grid(row=2,column=1,sticky="n")

        TextoAMBITO = ctk.CTkLabel(self,text="ÁMBITO",font=("Consolas",15,"bold"))
        TextoAMBITO.grid(row=1,column=2)

        txtAmbito = "\n".join([i.Scope for i in File.ANALISIS_SEMANTICO["Simbolos"]])
        EntradaAmbito = ctk.CTkLabel(self,text=txtAmbito,anchor="n")
        EntradaAmbito.grid(row=2,column=2,sticky="n")

        TextoTIPO = ctk.CTkLabel(self,text="NIVEL",font=("Consolas",15,"bold"))
        TextoTIPO.grid(row=1,column=3)

        txtCategoria = "\n".join([str(i.Offset) for i in File.ANALISIS_SEMANTICO["Simbolos"]])
        EntradaCategoria = ctk.CTkLabel(self,text=txtCategoria,anchor="n")
        EntradaCategoria.grid(row=2,column=3,sticky="n")

        TextoPARAMETROS = ctk.CTkLabel(self,text="PARAMETROS",font=("Consolas",15,"bold"))
        TextoPARAMETROS.grid(row=1,column=4)

        txtParametros = "\n".join([str(i.Parameter) for i in File.ANALISIS_SEMANTICO["Simbolos"]])
        EntradaParametros= ctk.CTkLabel(self,text=txtParametros,anchor="n")
        EntradaParametros.grid(row=2,column=4,sticky="n")

        TextoPARAMETROS = ctk.CTkLabel(self,text="MEMORIA",font=("Consolas",15,"bold"))
        TextoPARAMETROS.grid(row=1,column=5)

        txtMemory = "\n".join([str(i.Memory) for i in File.ANALISIS_SEMANTICO["Simbolos"]])
        EntradaMemory= ctk.CTkLabel(self,text=txtMemory,anchor="n")
        EntradaMemory.grid(row=2,column=5,sticky="n")

        Vacio = ctk.CTkLabel(self,text=None)
        Vacio.grid(row=3,column=0,columnspan=4,sticky="we")