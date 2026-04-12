import customtkinter as ctk
from FrontEnd.FrameEditor import FrameEditor
from FrontEnd.FrameLexico import FrameLexico
from FrontEnd.FrameSintactico import FrameSintactico
from FrontEnd.FrameSemantico import FrameSemantico
from FrontEnd.FrameOpciones import FrameOpciones


class App(ctk.CTk):
    def __init__(self,title="NO TITTLE",geometry="600x300",iconbitmap=None,appearance_mode="dark",color_theme="blue"):
        global FrameEditor, FrameLexico, FrameSintactico, FrameSemantico, FrameOpciones
        super().__init__()

        self.title(title)
        self.geometry(geometry)
        if iconbitmap != None: self.iconbitmap(iconbitmap)
        ctk.set_appearance_mode(appearance_mode)
        ctk.set_default_color_theme(color_theme)

        TabPrincipal = ctk.CTkTabview(self,anchor="w")
        TabPrincipal.pack(fill=ctk.BOTH, expand=True)
        
        TabPrincipal.add("Editor")
        self.FrameEditor = FrameEditor(self, TabPrincipal.tab("Editor"))
        
        TabPrincipal.add("Léxico")
        self.FrameLexico = FrameLexico(TabPrincipal.tab("Léxico"))

        TabPrincipal.add("Sintáctico")
        self.FrameSintactico = FrameSintactico(TabPrincipal.tab("Sintáctico"))

        TabPrincipal.add("Semántico")
        self.FrameSemantico = FrameSemantico(TabPrincipal.tab("Semántico"))

        TabPrincipal.add("Opciones")
        self.FrameOpciones = FrameOpciones(self, TabPrincipal.tab("Opciones"))

theme = ""
with open("scr/BackEnd/_Cache.txt","r") as file:
    theme = file.readline()

main = App(title="PEZ - C++ Compiler Visualizer",
          iconbitmap="res/Wizard.ico",
          appearance_mode="dark",
          color_theme=theme,
          geometry="600x300")

main.mainloop()