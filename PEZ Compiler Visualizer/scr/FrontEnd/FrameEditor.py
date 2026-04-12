import customtkinter as ctk
from PIL import Image

import BackEnd.RepositorioDeArchivo as RA
import BackEnd.DiccionarioDeDatos as DD
import BackEnd.ManejoDeErrores as ME
import BackEnd.AnalizadorLexico as Alex
import BackEnd.AnalizadorSintactico as Asin
import BackEnd.AnalizadorSemantico as Asem

import FrontEnd.PopOuts as PO

class FrameEditor(ctk.CTkFrame):
    def __init__(self,root, master):
        super().__init__(master)
        self.pack(fill=ctk.BOTH, expand=True)
        self.root = root

        self.VISUALIZAR_LEXICO = True
        self.VISUALIZAR_SINTACTICO = True
        self.VISUALIZAR_SEMANTICO = True

        self.Archivos = {}
        self.ArchivoSeleccionado = None

        n=8;m=10
        self.grid_rowconfigure([i for i in range(1,m)],weight=1)
        self.grid_columnconfigure([i for i in range(n-2) if i != 1],weight=1)

        BotonCompilar = ctk.CTkButton(self,font=("Consolas",15,"bold"),text=None,width=25,height=25,
                                    image=ctk.CTkImage(light_image=Image.open("res/Play.png"),size=(10,10)),
                                    command=lambda:self.CompilarCodigo())
        BotonCompilar.grid(row=0,column = m-2,padx=5,pady=10,sticky="e")

        BotonAgregarArchivo = ctk.CTkButton(self,font=("Consolas",15,"bold"),text=None,width=25,height=25,
                                    image=ctk.CTkImage(light_image=Image.open("res/Create.png"),size=(10,10)),
                                    command=lambda:self.AgregarArchivo())
        BotonAgregarArchivo.grid(row=0,column = m-3,padx=5,pady=10,sticky="e")

        self.TextoNombreArchivo = ctk.CTkLabel(self,font=("Consolas",15),text="Primero, cree un Archivo .cpp ->",anchor="w")
        self.TextoNombreArchivo.grid(row=0,column = 1,columnspan = 6,sticky="we",padx=10)

        self.ScrollArchivos = ctk.CTkScrollableFrame(self,width=100,corner_radius=0,label_text="Archivos")
        self.ScrollArchivos.grid(row=0,column = 0,rowspan=m,sticky="snwe")

        self.EntradaEditor = ctk.CTkTextbox(self,corner_radius=0,font=("Consolas",15))
        self.EntradaEditor.grid(row=1,column = 2,rowspan=m,columnspan=n,sticky="snwe")

        self.EntradaEditor.bind("<Key>",self.ActualizarArchivo)
        self.EntradaEditor.bind("<KeyRelease>",self.ActualizarArchivo)

#region CRUD

    def AgregarArchivo(self):
        NuevoArchivo = ctk.CTkInputDialog(title="Nuevo Archivo", text="Ingrese nombre del archivo .cpp").get_input()
        if not NuevoArchivo or NuevoArchivo == "": return

        NuevoArchivo = NuevoArchivo.replace(" ","").lower().replace(".cpp","")
        CodigoStandard = """#include<iostream>\nusing namespace std;\nint main(){\n    //Hello World\n    cout<<"Hello World"<<endl;\n}\n"""


        if NuevoArchivo in DD.Standard_Token["Libraries"]:
            PO.ErrorPopOut(self,[f"El Script {NuevoArchivo} coincide con el nombre de otro script o librería"])
            return

        self.Archivos.update({NuevoArchivo:CodigoStandard})
        DD.Standard_Token["Libraries"].append(NuevoArchivo)

        self.TextoNombreArchivo.configure(text = NuevoArchivo + ".cpp")
        self.EntradaEditor.delete(0.0,ctk.END)
        self.EntradaEditor.insert(0.0,CodigoStandard)
        self.ArchivoSeleccionado = NuevoArchivo

        Archivo = FrameArchivo(self, NuevoArchivo)

    def RenombrarArchivo(self,Archivo):
        nuevoNombre = ctk.CTkInputDialog(title="Renombrar Archivo", text="Ingrese nuevo nombre del archivo .cpp").get_input()
        if nuevoNombre == None or nuevoNombre == "": return Archivo
        nuevoNombre = nuevoNombre.replace(" ","").lower().replace(".cpp","")

        if nuevoNombre in DD.Standard_Token["Libraries"]:
            PO.ErrorPopOut(self,[f"El Script {nuevoNombre} coincide con el nombre de otro script o librería."])
            return Archivo
        
        DD.Standard_Token["Libraries"][DD.Standard_Token["Libraries"].index(Archivo)]=nuevoNombre
        self.Archivos[nuevoNombre] = self.Archivos.pop(Archivo)

        if self.ArchivoSeleccionado == Archivo: 
            self.ArchivoSeleccionado = nuevoNombre
            self.TextoNombreArchivo.configure(text = nuevoNombre+".cpp")
        return nuevoNombre

    def BorrarArchivo(self,Archivo):
        if self.ArchivoSeleccionado == Archivo:
            self.TextoNombreArchivo.configure(text = "Seleccione o cree un nuevo archivo")
            self.EntradaEditor.delete(0.0,ctk.END)        
        
        DD.Standard_Token["Libraries"].remove(Archivo)
        self.Archivos.pop(Archivo)

    def SeleccionarArchivo(self,Archivo):
        self.ArchivoSeleccionado = Archivo

        self.TextoNombreArchivo.configure(text = Archivo +".cpp")
        self.EntradaEditor.delete(0.0,ctk.END)
        self.EntradaEditor.insert(0.0,self.Archivos[Archivo])

    def ActualizarArchivo(self,event):
        self.Archivos[self.ArchivoSeleccionado] = self.EntradaEditor.get("0.0",ctk.END)

#region CRUD

    def ImportarArchivos(self,ruta_archivo):
        for i in ruta_archivo:
            with open(i,"r") as File:
                NuevoArchivo = File.name.split("/")[-1].replace(" ","").lower().replace(".cpp","")
                CodigoArchivo = "\n".join([line[:-1] for line in File.readlines()])

                if NuevoArchivo in DD.Standard_Token["Libraries"]:
                    PO.ErrorPopOut(self,[f"El Script {NuevoArchivo} coincide con el nombre de otro script o libreria"])
                    continue

                self.Archivos.update({NuevoArchivo:CodigoArchivo})
                DD.Standard_Token["Libraries"].append(NuevoArchivo)
                Archivo = FrameArchivo(self, NuevoArchivo)

    def ExportarArchivos(self):
        return self.Archivos

#region NUCLEO

    def CompilarCodigo(self):
        if len(self.ScrollArchivos.winfo_children())==0: return

        #Reset
        RA.REPOSITORIO.clear()
        ME.ErrorCounter.clear()
        self.root.FrameLexico.Reset()
        self.root.FrameSintactico.Reset()
        self.root.FrameSemantico.Reset()

        #Compilation
        for k,v in self.Archivos.items():
            nuevoArchivo = RA.CPP(k,v)
            
            Alex.AnalisisLexico(nuevoArchivo)
            Asin.AnalisisSintactico(nuevoArchivo)
            Asem.AnalisisSemantico(nuevoArchivo)

            RA.REPOSITORIO.append(nuevoArchivo)

        #THE BIG GATE 
        if len(ME.ErrorCounter)>0: PO.ErrorPopOut(self,ME.ErrorCounter); return
        else: PO.CompildedPopOut(self)
    
        #Rendering
        for File in RA.REPOSITORIO: 
            if self.VISUALIZAR_LEXICO: self.root.FrameLexico.AgregarArchivoTokenizado(File)
            if self.VISUALIZAR_SINTACTICO: self.root.FrameSintactico.AgregarArchivoArbolizado(File)
            if self.VISUALIZAR_SEMANTICO: self.root.FrameSemantico.AgregarArchivoSemantizado(File)

#region NUCLEO

class FrameArchivo(ctk.CTkFrame):    
    def __init__(self,master,Nombre):
        super().__init__(master.ScrollArchivos)
        self.pack(fill = ctk.X)
        self.grid_columnconfigure(0,weight=1)

        self.VISUALIZAR_LEXICO = True
        self.VISUALIZAR_SINTACTICO = True
        self.VISUALIZAR_SEMANTICO = True

        self.root = master
        self.NOMBRE= Nombre

        self.TextoNombre = ctk.CTkLabel(self,text=self.NOMBRE+".cpp",anchor="w")
        self.TextoNombre.grid(row=0,column=0,sticky="we")
        self.TextoNombre.bind("<Button-1>",self.SeleccionarArchivo)

        BotonEditar = ctk.CTkButton(self,font=("Consolas",15,"bold"),text=None,width=25,height=25,
                                    image=ctk.CTkImage(light_image=Image.open("res/Edit.png"),size=(10,10)),
                                    command=lambda:self.RenombrarArchivo())
        BotonEditar.grid(row=0,column = 1,padx=5,pady=10,sticky="e")

        BotonBorrar = ctk.CTkButton(self,font=("Consolas",15,"bold"),text=None,width=25,height=25,
                                    image=ctk.CTkImage(light_image=Image.open("res/Delete.png"),size=(10,10)),
                                    command=lambda:self.BorrarArchivo())
        BotonBorrar.grid(row=0,column = 2,padx=5,pady=10,sticky="e")

    def SeleccionarArchivo(self,event):
        self.root.SeleccionarArchivo(self.NOMBRE)

    def RenombrarArchivo(self):
        self.NOMBRE = self.root.RenombrarArchivo(self.NOMBRE)
        self.TextoNombre.configure(text=self.NOMBRE+".cpp")

    def BorrarArchivo(self):
        self.root.BorrarArchivo(self.NOMBRE)
        self.destroy()
