import customtkinter as ctk
from PIL import Image
from grafo import GrafoPonderado, Aeropuerto
from cvs_manager import dataframe, diccionario
from FPart import FramePart
from FSuperficial import SuperficialFrame, SuperficialFrame2

# Crear el grafo ponderado

grafo = GrafoPonderado(len(diccionario))
asignacion_ids = {}
id = 0

# Agregar nodos (aeropuertos) al grafo
for index, row in dataframe.iterrows():
    source_code = row['Source Airport Code']
    dest_code = row['Destination Airport Code']

    # Agregar nodos source si no están en el diccionario de asignación de ids
    if source_code not in asignacion_ids:
        asignacion_ids[source_code] = id
        grafo.add_aeropuerto(Aeropuerto(source_code, row['Source Airport Name'], row['Source Airport City'], row['Source Airport Country'], row['Source Airport Latitude'], row['Source Airport Longitude'], id))
        id += 1
        
    # Agregar nodos destination si no están en el diccionario de asignación de ids
    if dest_code not in asignacion_ids:
        asignacion_ids[dest_code] = id
        grafo.add_aeropuerto(Aeropuerto(dest_code, row['Destination Airport Name'], row['Destination Airport City'], row['Destination Airport Country'], row['Destination Airport Latitude'], row['Destination Airport Longitude'], id))
        id += 1
        
# Agregar aristas (vuelos) al grafo
for index, row in dataframe.iterrows():
    sourceCode = row['Source Airport Code']
    destinationCode = row['Destination Airport Code']
    nodoSource = grafo.get_aeropuerto(sourceCode)
    nodoDestination = grafo.get_aeropuerto(destinationCode)
    if nodoSource is not None and nodoDestination is not None:
        grafo.add_vuelo(nodoSource, nodoDestination)

# Clase del frame inicial
class FrameInicial(ctk.CTkFrame):
    def __init__(self, master, background_color, foreground_color):
        super().__init__(master)
        self.configure(bg_color=background_color)
        self.configure(fg_color=foreground_color)
        
        #Imágenes
        self.logo = ctk.CTkImage(light_image=Image.open("assets/logo.png"),dark_image=Image.open("assets/logo.png"), size=(300, 300))
        self.fondo = ctk.CTkImage(light_image=Image.open("assets/fondo.png"), size=(1540, 800))
        
        #Label Imágenes
        self.fondo_label = ctk.CTkLabel(self, image=self.fondo, bg_color="#fff0af", fg_color="transparent")
        self.fondo_label.place(x=0, y=0)
        self.logo_button = ctk.CTkButton(self, image=self.logo, text="", fg_color="transparent", bg_color="#fff0af", hover=None)  # display image with a CTkLabel
        self.logo_button.place(x=620, y=150)
        
        #Botones
        self.boton_entrar = ctk.CTkButton(self, text="Embarcar", bg_color="#fff0af", fg_color="#181732", hover_color="#101A16", text_color="#fff0af", font=("Verdana", 16), width=153, height=43, corner_radius=10, command=lambda: self.master.select_frame_by_name("main"))
        self.boton_entrar.place(x=700, y=535)
        
        #Label Texto
        self.texto = ctk.CTkLabel(self, text="Airway Explorer", bg_color="#fff0af", fg_color="#fff0af", text_color="#2C4436", font=("Georgia", 32, "bold"))
        self.texto.place(x=630, y=450)        

# Clase principal de la aplicación
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        #Posicionamiento centrado en la pantalla
        self.x = self.winfo_screenwidth() // 2 - 1540 // 2
        self.y = self.winfo_screenheight() // 2 - 800 // 2
        self.posicionamiento = f"1540x800+{self.x - 10}+{self.y -35}"
        self.geometry(self.posicionamiento)
        self.resizable(False, False)
        
        #Configuración de la ventana        
        self.title("Airway Explorer")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        #Frames Inicial y Main
        self.frame_inicial = FrameInicial(self, "#fff0af", "transparent")
        self.frame_inicial.grid(row=0, column=0, sticky="nsew")
        self.frame_main = FrameMain(self, "#fff0af", "transparent")
    
    #Función para cambiar de frame
    def select_frame_by_name(self, frame_name):
        
        if frame_name == "inicial":
            self.frame_inicial.grid(row=0, column=0, sticky="nsew")
        elif frame_name == "main":
            self.frame_main.grid(row=0, column=0, sticky="nsew")
        else: 
            self.frame_inicial.grid_forget()

#Clase del frame principal "main"
class FrameMain(ctk.CTkFrame):
    def __init__(self, master, background_color, foreground_color):
        super().__init__(master)
        self.configure(bg_color=background_color)
        self.configure(fg_color=foreground_color)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
        #Definición del frame
        
        #Images
        self.im_tablero = ctk.CTkImage(light_image=Image.open("assets/info.png"),size=(50, 50))
        self.im_add = ctk.CTkImage(light_image=Image.open("assets/map.png"),size=(50, 50))
        self.im_edit = None
        self.im_info = None
        self.im_exit = ctk.CTkImage(light_image=Image.open("assets/salir.png"),size=(55, 55))
        
        #MainPartBack
        self.mainPartBack = FramePart(self, 1260, 800, "#F8DEB5", "transparent")
        self.mainPartBack.grid(row=0, column=1, sticky="nsew")
        self.mainPartBack.rowconfigure(0, weight=1)
        self.mainPartBack.columnconfigure(0, weight=1)
    
        #CodePart
        self.codePart = SuperficialFrame(self.mainPartBack, grafo)
        self.codePart.grid(row=0, column=0)
                
        #Back2
        self.back2 = FramePart(self, 1260, 800, "#F8DEB5", "transparent")
        self.back2.columnconfigure(0, weight=1)
        self.back2.rowconfigure(0, weight=1)
        self.frame_add = SuperficialFrame2(self.back2, grafo)
        self.frame_add.geolocalizar_aeropuertos()
        self.frame_add.grid(row=0, column=0)
                
        #NavBar
        self.navBar = FramePart(self, 280, 800, "#181732", "transparent")
        self.navBar.grid(row=0, column=0, sticky="nsew")
        self.navBar.rowconfigure(2, weight=1)
        self.navBar.columnconfigure(0, weight=1)
        
        #NavBarLogo
        self.navBarLogo = FrameLogo(self.navBar, "#181732", "transparent")
        self.navBarLogo.grid(row=0, column=0, sticky="nsew")
        
        #First Section Buttons
        self.firstSectionButtons = FramePart(self.navBar, 280, 66, "#EE9D04", "transparent")
        self.firstSectionButtons.grid(row=1, column=0, sticky="nsew", ipadx= 20)
        self.firstSectionButtons.rowconfigure(4, weight=1)
        self.firstSectionButtons.columnconfigure(0, weight=1)
        
        #Title
        self.titleButton= ButtonNavBar(self.firstSectionButtons, "Airway Explorer", "#181732", "transparent", "#CD7601", None, ("Georgia", 22, "bold"), None, "center")
        self.titleButton.grid(row=0, column=0, sticky="nsew")
        self.titleButton.configure(text_color="#FEFAE8")
        
        #Buttons
        self.button1 = ButtonNavBar(self.firstSectionButtons, "       Información", "#074578", "#074578", "#053F6E", command= lambda: self.select_frame("PUNTO1"), img=self.im_tablero, anchor="w")
        self.button1.grid(row=1, column=0, sticky="nsew")
        self.button1.configure(border_spacing= 15)
        self.button2 = ButtonNavBar(self.firstSectionButtons, "          Mapeo", "#1C91AA", "#1C91AA", "#146E82", command= lambda: self.select_frame("PUNTO2"), img=self.im_add, anchor="w")
        self.button2.grid(row=2, column=0, sticky="nsew")
        self.button2.configure(border_spacing= 15)
        # Margen
        self.button3 = ButtonNavBar(self.firstSectionButtons, "           ", "#181732", "#181732", "#181732", command= None,  anchor="w", )
        self.button3.grid(row=3, column=0, sticky="nsew")
        self.button3.configure(border_spacing= 15)
        self.button4 = ButtonNavBar(self.firstSectionButtons, "              ", "#181732", "#181732", "#181732", command= None, anchor="w")
        self.button4.grid(row=4, column=0, sticky="nsew")
        self.button4.configure(border_spacing= 15)
        
        #Salir
        self.button5 = ButtonNavBar(self.firstSectionButtons, "            Salir", "#074578", "#074578", "#053F6E", command= self.master.destroy, img=self.im_exit, anchor="w", )
        self.button5.grid(row=5, column=0, sticky="nsew")
        self.button5.configure(border_spacing= 16)

    def select_frame(self, frame_name): 
        if frame_name == "PUNTO1":
            self.back2.grid_forget()
            self.mainPartBack.grid(row=0, column=1, sticky="nsew")
        elif frame_name == "PUNTO2":
            self.mainPartBack.grid_forget()
            self.back2.grid(row=0, column=1, sticky="nsew")
        else: 
            self.mainPartBack.grid(row=0, column=1, sticky="nsew")
            
#Clase del frame contenedor del logo
class FrameLogo(ctk.CTkFrame):
    def __init__(self, master, background_color, foreground_color):
        super().__init__(master)
        self.configure(bg_color=background_color)
        self.configure(fg_color=foreground_color)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        #Imagen
        self.logo = ctk.CTkImage(light_image=Image.open("assets/logo.png"),dark_image=Image.open("assets/logo.png"), size=(200, 200))
        #Label Imagen
        self.logo_button = ctk.CTkButton(self, image=self.logo, text="", fg_color="transparent", bg_color="#181732", hover=None)  
        self.logo_button.grid(row=0, column=0, sticky="nsew")
        

#Clase del botón de la barra de navegación
class ButtonNavBar(ctk.CTkButton):
    def __init__(self, master, text, background_color, foreground_color, hover_color, command, font=("Helvetica", 16, "bold"), img = None, anchor= "center"):
        super().__init__(master)
        self.configure(text=text)
        self.configure(bg_color=background_color)
        self.configure(fg_color=foreground_color)
        self.configure(hover_color=hover_color)
        self.configure(font=font)
        self.configure(width=280)
        self.configure(height=66)
        self.configure(corner_radius=0)
        self.configure(command=command)
        self.configure(image=img)
        self.configure(anchor=anchor)
        self.configure(text_color="#FAEAD1")
        
        

# Crear la aplicación
app = App()
app.mainloop()