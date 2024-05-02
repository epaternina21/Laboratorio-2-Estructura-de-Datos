import customtkinter as ctk
from tkintermapview import TkinterMapView

# Clase que hereda de CTkScrollableFrame para crear la vista superficial de la aplicación
# Esta clase permite mostrar la información de un aeropuerto y los 10 aeropuertos más lejanos
class SuperficialFrame(ctk.CTkScrollableFrame): 
    def __init__(self, master, grafo):
        super().__init__(master)
        self.configure(width= 1100, height= 700)
        self.configure(bg_color="#F8DEB5", fg_color="#FAEAD1", corner_radius=20, border_width=0, border_color="#FFE588")
        self.configure(scrollbar_button_color="#FAEAD1", scrollbar_button_hover_color = "#FAEAD1")
        self.rowconfigure(6, weight=1)
        self.columnconfigure(5, weight=1)
        self.grafo = grafo
        self.codigos = grafo.aeropuertos
        
        #labels
        self.labelTitulo = ctk.CTkLabel(self, text="CONOCE LA INFORMACIÓN DE UN AEROPUERTO", fg_color="transparent", bg_color="#FAEAD1", text_color="#181732", font=("Georgia", 28, "bold"), width=788, height=95)
        self.labelTitulo.grid(row=0, column=0, columnspan=6, pady= 20 )
        self.fix = ctk.CTkLabel(self, text="", bg_color="#FAEAD1", fg_color="transparent", width= 117, height= 1)
        self.fix.grid(row=1, column=0, columnspan=1)
        self.labelCodigo = ctk.CTkLabel(self, text="Código del Aeropuerto", fg_color="transparent", bg_color="#FAEAD1", text_color="#181732", font=("Georgia", 18), width=500, height=95)
        self.labelCodigo.grid(row=1, column=0, columnspan= 3,  padx= 30)
        
        
        # Combo Boxes
        self.comboCodigo = ctk.CTkComboBox(self, width=350, height=49, border_width=2, corner_radius=19, border_color= "#181732" , bg_color="#FAEAD1", fg_color="#F7AE22", text_color="#181732", font=("Georgia", 18), values= [codigo.source_code for codigo in self.codigos], button_color="#EE9D04", button_hover_color="#CD7601", dropdown_fg_color="#87400C", dropdown_text_color="#FFCF44", dropdown_font=("Georgia", 16), dropdown_hover_color="#2C4436", command= None)
        self.comboCodigo.set("Selecciona un código")
        self.comboCodigo.grid(row=1, column=2, columnspan=3, ipadx= 5, pady = 10, padx= 30)    
        
        # #Text Fields
        self.tbCodigo = ctk.CTkTextbox(master=self, width=850, height=341, corner_radius=18, border_width=5, border_color="#181732", bg_color="#FAEAD1", fg_color="#F7AE22", text_color="#181732", font=("Georgia", 18))
        self.tbCodigo.grid(row=3, column=1, columnspan=4, ipadx= 5, pady = 30, padx= 10, sticky="nsew")
        
        #Buttons
        self.bBuscar = ctk.CTkButton(self, text="Buscar", bg_color="#FAEAD1", fg_color="#074578", hover_color="#19629D", border_width=1, border_color= "#F7AE22", text_color="#FAEAD1", font=("Georgia", 16), width=294, height=50, corner_radius=10, command = self.buscar)
        self.bBuscar.grid(row=2, column=2, columnspan=3)
        
    # Función para buscar la información de un aeropuerto, mostrar los 10 aeropuertos más lejanos y mostrar la información en la vista de texto
    def buscar(self):
        # PUNTO 1: Mostrar la información del aeropuerto seleccionado
        self.tbCodigo.delete(0.0, "end")
        code= self.comboCodigo.get()
        aeropuerto = self.grafo.get_aeropuerto(code)
        parteA = aeropuerto.get_info() + "\n\n"
        distancias_lejanas = self.grafo.diez_distancias_mas_lejanas(aeropuerto)
        ParteC = f"\nLa información de cada uno de los aeropuertos más lejanos se muestra en la tabla\n\n"
        for aeropuerto in distancias_lejanas:
            ParteC += f"{self.grafo.get_aeropuerto(aeropuerto[0]).get_info()}\n\n"
        # Formatear Distancias Lejanas en Vista de tabla
        distancias_lejanas = "\n".join([f"{aeropuerto[0]}: {aeropuerto[1]} km" for aeropuerto in distancias_lejanas])
        parteB = f"Los 10 aeropuertos más lejanos son:\n {distancias_lejanas}"
        
        self.tbCodigo.insert(0.0 , parteA + parteB + ParteC)
            
# Clase que hereda de CTkScrollableFrame para crear la vista superficial de la aplicación
# Esta clase permite mostrar en un mapa la ruta entre dos aeropuertos y los aeropuertos intermedios
class SuperficialFrame2(ctk.CTkScrollableFrame): 
    def __init__(self, master, grafo):
        super().__init__(master)
        self.configure(width= 1100, height= 700)
        self.configure(bg_color="#F8DEB5", fg_color="#FAEAD1", corner_radius=20, border_width=0, border_color="#FFE588")
        self.configure(scrollbar_button_color="#FA972B", scrollbar_button_hover_color = "#F05D17")
        self.rowconfigure(7, weight=1)
        self.columnconfigure(5, weight=1)
        self.grafo = grafo
        self.codigos = self.grafo.aeropuertos
        
        
    
        #labels
        self.labelTitulo = ctk.CTkLabel(self, text="CONOCE LA INFORMACIÓN ENTRE AEROPUERTOS", fg_color="transparent", bg_color="#FAEAD1", text_color="#181732", font=("Georgia", 28, "bold"), width=788, height=95)
        self.labelTitulo.grid(row=0, column=0, columnspan=6, pady= 20 )
        self.fix = ctk.CTkLabel(self, text="", bg_color="#FAEAD1", fg_color="transparent", width= 117, height= 1)
        self.fix.grid(row=1, column=0, columnspan=1)
        self.labelCodigo = ctk.CTkLabel(self, text="Código del Aeropuerto 1", fg_color="transparent", bg_color="#FAEAD1", text_color="#181732", font=("Georgia", 18), width=300, height=95)
        self.labelCodigo.grid(row=1, column=1, columnspan= 2,  padx= 30)
        self.labelCodigo = ctk.CTkLabel(self, text="Código del Aeropuerto 2", fg_color="transparent", bg_color="#FAEAD1", text_color="#181732", font=("Georgia", 18), width=300, height=95)
        self.labelCodigo.grid(row=2, column=1, columnspan= 2,  padx= 30)
        
        
        # Combo Boxes
        self.comboCodigo = ctk.CTkComboBox(self, width=300, height=49, border_width=2, corner_radius=19, border_color= "#181732" , bg_color="#FAEAD1", fg_color="#F7AE22", text_color="#181732", font=("Georgia", 18), values= [codigo.source_code for codigo in self.codigos], button_color="#EE9D04", button_hover_color="#CD7601", dropdown_fg_color="#87400C", dropdown_text_color="#FFCF44", dropdown_font=("Georgia", 16), dropdown_hover_color="#2C4436", command= None)
        self.comboCodigo.set("Selecciona un código")
        self.comboCodigo.grid(row=1, column=3, columnspan=2, ipadx= 5, pady = 10, padx= 30)
        self.comboCodigo2 = ctk.CTkComboBox(self, width=300, height=49, border_width=2, corner_radius=19, border_color= "#181732" , bg_color="#FAEAD1", fg_color="#F7AE22", text_color="#181732", font=("Georgia", 18), values= [codigo.source_code for codigo in self.codigos], button_color="#EE9D04", button_hover_color="#CD7601", dropdown_fg_color="#87400C", dropdown_text_color="#FFCF44", dropdown_font=("Georgia", 16), dropdown_hover_color="#2C4436", command= None)
        self.comboCodigo2.set("Selecciona un código")
        self.comboCodigo2.grid(row=2, column=3, columnspan=2, ipadx= 5, pady = 10, padx= 30)    

        # Mapa
        self.mapa = TkinterMapView(self, width= 1100, height= 700, bg_color="#FAEAD1", corner_radius=20)
        self.mapa.grid(row=4, column=0, columnspan=6,  pady = 30, sticky="nsew")
        self.mapa.set_tile_server("https://mt0.google.com/vt/lyrs=m&x={x}&y={y}&z={z}&s=Ga", max_zoom= 25)
        self.mapa.set_position(4.570868, -74.297332, 10) #Bogotá
        self.mapa.set_zoom(6)

        #Buttons
        self.bBuscar = ctk.CTkButton(self, text="Buscar", bg_color="#FAEAD1", fg_color="#074578", hover_color="#19629D", border_width=1, border_color= "#F7AE22", text_color="#FAEAD1", font=("Georgia", 16), width=150, height=50, corner_radius=10, command = self.buscar)
        self.bBuscar.grid(row=3, column=2, columnspan=3)
    
    # Función para buscar los aeropuertos intermedios entre dos aeropuertos, mostrar la distancia entre ellos y trazar la ruta en el mapa
    def buscar(self):
        self.mapa.delete_all_marker()
        self.mapa.delete_all_path()
        aeropuerto1 = self.grafo.get_aeropuerto(self.comboCodigo.get())
        aeropuerto2 = self.grafo.get_aeropuerto(self.comboCodigo2.get())
        resultado_dijkstra =self.grafo.dijkstra(aeropuerto1)
        distancias_del_aeropuerto1 = resultado_dijkstra[0]
        
        # PUNTO 2: Mostrar la distancia entre dos aeropuertos
        distancia = distancias_del_aeropuerto1[aeropuerto2.id]
        
        #Mostrar los aeropuertos intermedios
        aeropuertos_intermedios = resultado_dijkstra[1]
        conversion = [self.grafo.aeropuertos[aeropuerto].source_code for aeropuerto in aeropuertos_intermedios[aeropuerto2.id]]
        parteB = f"Los aeropuertos intermedios son {conversion}"
    
        
        print( f"La distancia entre {aeropuerto1.source_code} y {aeropuerto2.source_code} es de {distancia} km y\n {parteB}")
        
        # PUNTO 3: Trazar la ruta en el mapa
        self.mapa.set_marker(aeropuerto1.source_latitude, aeropuerto1.source_longitude, text= f"Código Aeropuerto Salida: {aeropuerto1.source_code}\nNombre Aeropuerto Salida: {aeropuerto1.source_name}\nCiudad Aeropuerto Salida: {aeropuerto1.source_city}\nPaís Aeropuerto Salida: {aeropuerto1.source_country}\nLatitud Aeropuerto Salida: {aeropuerto1.source_latitude}\nLongitud Aeropuerto Salida: {aeropuerto1.source_longitude}")
        self.mapa.set_marker(aeropuerto2.source_latitude, aeropuerto2.source_longitude, text= f"Código Aeropuerto Llegada: {aeropuerto2.source_code}\nNombre Aeropuerto Llegada: {aeropuerto2.source_name}\nCiudad Aeropuerto Llegada: {aeropuerto2.source_city}\nPaís Aeropuerto Llegada: {aeropuerto2.source_country}\nLatitud Aeropuerto Llegada: {aeropuerto2.source_latitude}\nLongitud Aeropuerto Llegada: {aeropuerto2.source_longitude}")
        
        #Trazado de la ruta
        self.trazar_ruta(aeropuerto1, aeropuerto2, conversion)
    
    # Función para trazar la ruta en el mapa
    def trazar_ruta(self, aeropuerto1, aeropuerto2, aeropuertos_intermedios):
        # Si no hay aeropuertos intermedios
        if len(aeropuertos_intermedios) == 1:
            self.mapa.set_path([(aeropuerto1.source_latitude, aeropuerto1.source_longitude), (aeropuerto2.source_latitude, aeropuerto2.source_longitude)])

        # si no hay conexión entre los aeropuertos
        elif len(aeropuertos_intermedios) == 0: 
            self.mapa.delete_all_marker()
            self.mapa.set_marker(aeropuerto1.source_latitude, aeropuerto1.source_longitude, text= f"Código Aeropuerto Salida: {aeropuerto1.source_code}\nNo hay conexión entre los aeropuertos")
            self.mapa.set_marker(aeropuerto2.source_latitude, aeropuerto2.source_longitude, text= f"Código Aeropuerto Llegada: {aeropuerto2.source_code}\nNo hay conexión entre los aeropuertos")
        # Si hay aeropuertos intermedios
        else:
            self.mapa.set_path([(aeropuerto1.source_latitude, aeropuerto1.source_longitude), (self.grafo.get_aeropuerto(aeropuertos_intermedios[0]).source_latitude, self.grafo.get_aeropuerto(aeropuertos_intermedios[0]).source_longitude)])
            self.mapa.set_marker(self.grafo.get_aeropuerto(aeropuertos_intermedios[0]).source_latitude, self.grafo.get_aeropuerto(aeropuertos_intermedios[0]).source_longitude, text= f"Código Aeropuerto Intermedio: {self.grafo.get_aeropuerto(aeropuertos_intermedios[0]).source_code}\nNombre Aeropuerto Intermedio: {self.grafo.get_aeropuerto(aeropuertos_intermedios[0]).source_name}\nCiudad Aeropuerto Intermedio: {self.grafo.get_aeropuerto(aeropuertos_intermedios[0]).source_city}\nPaís Aeropuerto Intermedio: {self.grafo.get_aeropuerto(aeropuertos_intermedios[0]).source_country}\nLatitud Aeropuerto Intermedio: {self.grafo.get_aeropuerto(aeropuertos_intermedios[0]).source_latitude}\nLongitud Aeropuerto Intermedio: {self.grafo.get_aeropuerto(aeropuertos_intermedios[0]).source_longitude}")
            for i in range(1, len(aeropuertos_intermedios)):
                self.mapa.set_path([(self.grafo.get_aeropuerto(aeropuertos_intermedios[i-1]).source_latitude, self.grafo.get_aeropuerto(aeropuertos_intermedios[i-1]).source_longitude), (self.grafo.get_aeropuerto(aeropuertos_intermedios[i]).source_latitude, self.grafo.get_aeropuerto(aeropuertos_intermedios[i]).source_longitude)])
                if i < len(aeropuertos_intermedios)-1:
                    self.mapa.set_marker(self.grafo.get_aeropuerto(aeropuertos_intermedios[i]).source_latitude, self.grafo.get_aeropuerto(aeropuertos_intermedios[i]).source_longitude, text= f"Código Aeropuerto Intermedio: {self.grafo.get_aeropuerto(aeropuertos_intermedios[i]).source_code}\nNombre Aeropuerto Intermedio: {self.grafo.get_aeropuerto(aeropuertos_intermedios[i]).source_name}\nCiudad Aeropuerto Intermedio: {self.grafo.get_aeropuerto(aeropuertos_intermedios[i]).source_city}\nPaís Aeropuerto Intermedio: {self.grafo.get_aeropuerto(aeropuertos_intermedios[i]).source_country}\nLatitud Aeropuerto Intermedio: {self.grafo.get_aeropuerto(aeropuertos_intermedios[i]).source_latitude}\nLongitud Aeropuerto Intermedio: {self.grafo.get_aeropuerto(aeropuertos_intermedios[i]).source_longitude}")
            self.mapa.set_path([(self.grafo.get_aeropuerto(aeropuertos_intermedios[-1]).source_latitude, self.grafo.get_aeropuerto(aeropuertos_intermedios[-1]).source_longitude), (aeropuerto2.source_latitude, aeropuerto2.source_longitude)])
    
    # Función para geolocalizar los aeropuertos en el mapa al inicio
    def geolocalizar_aeropuertos(self):
        for aeropuerto in self.codigos:
            self.mapa.set_marker(aeropuerto.source_latitude, aeropuerto.source_longitude)
            