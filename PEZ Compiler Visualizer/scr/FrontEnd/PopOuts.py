import customtkinter as ctk
from PIL import Image

class CompildedPopOut(ctk.CTkToplevel):
    def __init__(self,master):
        super().__init__(master)
        self.transient(master)
        
        self.title("CÓDIGO COMPILADO")

        self.grid_columnconfigure(1,weight=1)

        TextTitulo =  ctk.CTkLabel(self,text="Excelente!\ntu código compiló correctamente",font= ("Consola",15,"bold"))
        TextTitulo.grid(row=0,column=0,columnspan=2,padx=10,pady=10)

        Texto =  ctk.CTkLabel(self,text="Revisa las otras ventanas\npara más información")
        Texto.grid(row=1,column=1,padx=10,pady=10)

        Wizard = ctk.CTkLabel(self,text=None,image=ctk.CTkImage(light_image=Image.open("res/Win.png"),size=(75,75)))
        Wizard.grid(row=1,column=0,sticky="nw",padx=10,pady=10)

class ImportedPopOut(ctk.CTkToplevel):
    def __init__(self,master):
        super().__init__(master)
        self.transient(master)
        
        self.title("CÓDIGO EXPORTADO")

        self.grid_columnconfigure(1,weight=1)

        TextTitulo =  ctk.CTkLabel(self,text="Excelente!\ntu código ha sido exportado correctamente",font= ("Consola",15,"bold"))
        TextTitulo.grid(row=0,column=0,columnspan=2,padx=10,pady=10)

        Texto =  ctk.CTkLabel(self,text="Revisa la carpeta de descargas\npara más información")
        Texto.grid(row=1,column=1,padx=10,pady=10)

        Wizard = ctk.CTkLabel(self,text=None,image=ctk.CTkImage(light_image=Image.open("res/Look.png"),size=(75,75)))
        Wizard.grid(row=1,column=0,sticky="nw",padx=10,pady=10)

class ErrorPopOut(ctk.CTkToplevel):
    def __init__(self,master,Errores):
        super().__init__(master)
        self.transient(master)
        self.geometry("600x200")
        self.title("ERROR")

        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(1,weight=1)

        TextoError =  ctk.CTkLabel(self,text="Vaya...\nHubo un problema...",font= ("Consola",15,"bold"))
        TextoError.grid(row=0,column=0,columnspan=2,padx=10,pady=10)

        Wizard = ctk.CTkLabel(self,text=None,image=ctk.CTkImage(light_image=Image.open("res/Look.png"),size=(75,75)))
        Wizard.grid(row=1,column=0,sticky="sw",padx=10,pady=10)

        self.ScrollErrores = ctk.CTkScrollableFrame(self,label_text="Errores Encontrados")
        self.ScrollErrores.grid(row=1,column=1,sticky="snwe",padx=10,pady=10)

        for i in self.ScrollErrores.winfo_children(): i.destroy()

        for Error in Errores:
            TextoError = ctk.CTkLabel(self.ScrollErrores,text=Error)
            TextoError.pack(fill=ctk.X)