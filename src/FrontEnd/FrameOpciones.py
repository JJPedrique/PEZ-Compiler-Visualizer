import customtkinter as ctk
import FrontEnd.PopOuts as PO
from tkinter import filedialog

import os
from datetime import date
from pathlib import Path

class FrameOpciones(ctk.CTkFrame):
    def __init__(self, root, master):
        super().__init__(master)        
        self.pack(fill=ctk.BOTH, expand=True)

        self.root = root

        n=3
        self.grid_columnconfigure([i for i in range(n)],weight=1)

        TextoGestionArchivos = ctk.CTkLabel(self,text="Gestión de Archivos",font=("Consolas",15,"bold"),anchor="w")
        TextoGestionArchivos.grid(row=0,column=0,columnspan=2,sticky="snwe",padx=10)

        BotonImportar = ctk.CTkButton(self,text="Importar",command=lambda:self.Importar())
        BotonImportar.grid(row=1,column=0,sticky="we",padx=10)

        BotonExportar = ctk.CTkButton(self,text="Exportar",command=lambda:self.Exportar())
        BotonExportar.grid(row=1,column=1,sticky="we",padx=10)

        TextoPreferencias = ctk.CTkLabel(self,text="Preferencias",font=("Consolas",15,"bold"))
        TextoPreferencias.grid(row=2,column=0,columnspan=2,sticky="w",padx=10)

        TextoModo = ctk.CTkLabel(self,text="Modo:",font=("Consolas",15,"bold"),anchor="w")
        TextoModo.grid(row=3,column=0,sticky="w",padx=10)

        EntradaModo = ctk.CTkOptionMenu(self,values=["system","dark","light"],command=lambda x:ctk.set_appearance_mode(EntradaModo.get()))
        EntradaModo.grid(row=3,column=1,sticky="w",pady=5,padx=10)

        TextoTema = ctk.CTkLabel(self,text="Tema*:",font=("Consolas",15,"bold"),anchor="w")
        TextoTema.grid(row=4,column=0,sticky="w",padx=10)

        EntradaTema = ctk.CTkOptionMenu(self,values=["blue","dark-blue","green"],command=lambda x:self.EstablecerTema(EntradaTema.get()))
        EntradaTema.grid(row=4,column=1,sticky="w",pady=5,padx=10)

        TextoTema = ctk.CTkLabel(self,text="(*) - Los cambios se reflejarán despues de reiniciar el programa",font=("Consolas",10),anchor="w")
        TextoTema.grid(row=5,column=0,columnspan=2,sticky="w",padx=10)


        #TextoTamañoTexto = ctk.CTkLabel(self,text="Tamaño de Texto:",font=("Consolas",15,"bold"),anchor="w")
        #TextoTamañoTexto.grid(row=5,column=0,sticky="w",padx=10)
        
        #EntradaTexto = ctk.CTkSlider(self)
        #EntradaTexto.grid(row=5,column=1,sticky="w",pady=5,padx=10)

        TextoGestionVisualizador = ctk.CTkLabel(self,text="Gestor de Visualización",font=("Consolas",15,"bold"))
        TextoGestionVisualizador.grid(row=0,column=2,columnspan=2,sticky="snwe",padx=10)

        EntradaLexico = ctk.CTkSwitch(self,text="Visor léxico",font=("Consolas",15,"bold"),variable=ctk.BooleanVar(value=True),
        command=lambda:self.ActivarLexico())
        EntradaLexico.grid(row=1,column=2,columnspan=2,sticky="we",pady=5,padx=10)

        EntradaSintactico = ctk.CTkSwitch(self,text="Visor sintáctico",font=("Consolas",15,"bold"),variable=ctk.BooleanVar(value=True),
        command=lambda:self.ActivarSintactico())
        EntradaSintactico.grid(row=2,column=2,columnspan=2,sticky="we",pady=5,padx=10)

        EntradaSemantico = ctk.CTkSwitch(self,text="Visor semántico",font=("Consolas",15,"bold"),variable=ctk.BooleanVar(value=True),
        command=lambda:self.ActivarSemantico())
        EntradaSemantico.grid(row=3,column=2,columnspan=2,sticky="we",pady=5,padx=10)

    def ActivarLexico(self):
        self.root.FrameEditor.VISUALIZAR_LEXICO = not self.root.FrameEditor.VISUALIZAR_LEXICO

    def ActivarSintactico(self):
        self.root.FrameEditor.VISUALIZAR_SINTACTICO = not self.root.FrameEditor.VISUALIZAR_SINTACTICO

    def ActivarSemantico(self):
        self.root.FrameEditor.VISUALIZAR_SEMANTICO = not self.root.FrameEditor.VISUALIZAR_SEMANTICO

    def EstablecerTema(self,tema):
        with open("scr/BackEnd/_Cache.txt","w") as file:
            file.write(tema)

    def Importar(self):
        ruta_archivo = filedialog.askopenfilenames(
            title="Seleccionar un archivos",
            initialdir="/",
            filetypes=(("Archivos C++", "*.cpp"),))
        
        if ruta_archivo == "": 
            PO.ErrorPopOut(self,["No hay Archivos por importar"])
            return

        self.root.FrameEditor.ImportarArchivos(ruta_archivo)
        PO.ImportedPopOut(self)

    def Exportar(self):
        ALL_FILES = self.root.FrameEditor.ExportarArchivos()
        if len(ALL_FILES) == 0: 
            PO.ErrorPopOut(self,["No hay Archivos por Exportar"])
            return

        dir = f"{Path.home()}/Downloads/PEZ_Compiler-{date.today()}"
        if not os.path.exists(dir): os.mkdir(dir)

        for k,v in ALL_FILES.items():
            with open(dir+"/"+k+".cpp","w") as file: file.write(v)

        PO.ImportedPopOut(self)
