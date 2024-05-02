import math

# Clase Grafo Ponderado
class GrafoPonderado:

    INF = (1 << 31) - 1 # Representación del infinito

    def __init__(self, numero_nodos: int) -> None:
        self.n = numero_nodos
        
        # Nodos
        self.aeropuertos = []
        
        #Matriz de adyacencia/Pesos
        self.adj = [[0 for i in range(self.n)] for j in range(self.n)]
        

    # Agregar nodo
    def add_aeropuerto(self, aeropuerto):
        self.aeropuertos.append(aeropuerto)
        
    # Agregar arista no dirigida
    def add_vuelo(self, aeropuerto1, aeropuerto2):        
        peso = haversine(aeropuerto1.source_latitude, aeropuerto1.source_longitude, aeropuerto2.source_latitude, aeropuerto2.source_longitude)
        
        if not ((0 <= aeropuerto1.id < self.n) and (0 <= aeropuerto2.id < self.n)):
            return False
        
        self.adj[aeropuerto1.id][aeropuerto2.id] = peso
        self.adj[aeropuerto2.id][aeropuerto1.id] = peso
        
        aeropuerto1.add_conexion(aeropuerto2)
        aeropuerto2.add_conexion(aeropuerto1)
        
        return True
        
    # obtener aeropuerto por código
    def get_aeropuerto(self, s_code: str):
        for aeropuerto in self.aeropuertos:
            if aeropuerto.source_code == s_code:
                return aeropuerto
        return "Aeropuerto no encontrado"
    
    # Distancia mínima, paso del algoritmo de Dijkstra
    def min_distance(self, distancias, visitados):
        min = self.INF    
        min_index = 0
        # Encontrar el vértice con la distancia mínima
        for v in range(self.n):
            if distancias[v] < min and not visitados[v]:
                min = distancias[v]
                min_index = v
            
        return min_index

    # Algoritmo de Dijkstra
    def dijkstra(self, airport):
        matriz_distancias = [self.INF] * self.n
        matriz_distancias[airport.id] = 0
        visitados = [False] * self.n
        caminos = {airport.id: []}  # Diccionario para almacenar los caminos

        for i in range(self.n):
            u = self.min_distance(matriz_distancias, visitados)
            visitados[u] = True
                
            for v in range(self.n):
                if self.adj[u][v] > 0 and not visitados[v] and matriz_distancias[v] > matriz_distancias[u] + self.adj[u][v]:
                    matriz_distancias[v] = matriz_distancias[u] + self.adj[u][v]
                    caminos[v] = caminos[u] + [v]  # Actualizar el camino más corto hasta v

        print("Vértice \t Distancia desde el vértice origen")
        for index, aeropuerto in enumerate(self.aeropuertos):
            print(f"{aeropuerto.source_code} \t\t {matriz_distancias[index]}")

        return [matriz_distancias, caminos]
    
    # Distancia más cortas
    def diez_distancias_mas_lejanas(self, airport):
        matriz_distancias = self.dijkstra(airport)[0]
        distancias = []
        for index, aeropuerto in enumerate(self.aeropuertos):
            distancias.append((aeropuerto.source_code, matriz_distancias[index]))
        
        # Ordenar las distancias de mayor a menor
        distancias.sort(key=lambda x: x[1], reverse=True)
        #Quitar las distancias que son infinito 
        distancias = [distancia for distancia in distancias if distancia[1] != self.INF]
            
        return distancias[:10]
        

class Aeropuerto: 
    def __init__(self, code: str, name: str, city: str, country: str, lat: float, long: float, id: int):
        self.source_code = code
        self.source_name = name
        self.source_city = city
        self.source_country = country
        self.source_latitude = lat
        self.source_longitude = long
        self.id = id
        
        self.destinos = []

    # Añadir aristas
    def add_conexion(self, aeropuerto_destino):
        if aeropuerto_destino not in self.destinos:
            self.destinos.append(aeropuerto_destino)

    # Obtener información del aeropuerto
    def get_info(self):
        return f"Código del Aeropuerto: {self.source_code}\nNombre del Aeropuerto: {self.source_name}\nCiudad del Aeropuerto: {self.source_city}\nPaís del Aeropuerto: {self.source_country}\nLatitud del Aeropuerto: {self.source_latitude}\nLongitud del Aeropuerto: {self.source_longitude}"

# Función para calcular la distancia entre dos puntos
def haversine(lat1, lon1, lat2, lon2):
    R = 6372  # Radio de la Tierra en kilómetros
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distancia = R * c
    
    return distancia