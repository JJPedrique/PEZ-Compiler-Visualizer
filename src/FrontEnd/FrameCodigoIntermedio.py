import customtkinter as ctk
from PIL import Image

class FrameCodigoIntermedio(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master,label_text="Codigo Intermedio de los Archivos")
        self.pack(fill=ctk.BOTH, expand=True)

        TextoTitulo = ctk.CTkLabel(self,text="No hay registros",font=("Consolas",15,"bold"))
        TextoTitulo.pack(fill=ctk.X)

        EntradaTokenizacion = ctk.CTkLabel(self,text="Compile un archivo para visualizar su compilación",anchor="n")
        EntradaTokenizacion.pack(fill=ctk.X)

        Wizard = ctk.CTkLabel(self,text=None,image=ctk.CTkImage(light_image=Image.open("res/Fly.png"),size=(75,75)))
        Wizard.pack(fill=ctk.X)

    def Reset(self):
        for i in self.winfo_children(): i.destroy()