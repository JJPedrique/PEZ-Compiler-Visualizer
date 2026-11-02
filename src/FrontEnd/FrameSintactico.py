import customtkinter as ctk
from PIL import Image

class FrameSintactico(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master,label_text="Archivos Analizados Sintácticamente")
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

        Wizard = ctk.CTkLabel(self,text=None,image=ctk.CTkImage(light_image=Image.open("res/Potion.png"),size=(75,75)))
        Wizard.pack(fill=ctk.X)
        
        self.isReset = not self.isReset
        
    def AgregarArchivoArbolizado(self,File):
        if self.isReset:
            for i in self.winfo_children(): i.destroy()
            self.isReset = not self.isReset

        ArchivoArbolizado(self,File)
        
class ArchivoArbolizado(ctk.CTkFrame):
    def __init__(self, master,File):
        super().__init__(master)
        self.pack(fill=ctk.X)
        self.grid_columnconfigure(0,weight=1)

        TextoNombreArchivo = ctk.CTkLabel(self,text=File.NOMBRE+".cpp",font=("Consolas",15,"bold"), corner_radius=100,
                                    text_color=ctk.ThemeManager.theme["CTkButton"]["text_color"],
                                    fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        TextoNombreArchivo.grid(row=0,column=0,sticky="we")

        txtARBOL = "\n".join([i for i in File.ANALISIS_SINTACTICO["NodoRaiz"].ArbolList])
        LabelARBOL = ctk.CTkLabel(self,text=txtARBOL,anchor="w",font=("Consolas",14),justify="left")
        LabelARBOL.grid(row=2,column=0,sticky="wn")

        Vacio = ctk.CTkLabel(self,text=None)
        Vacio.grid(row=3,column=0,sticky="we")