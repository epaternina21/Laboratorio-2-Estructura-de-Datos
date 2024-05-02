import pandas as pd

# Leer el archivo csv
dataframe = pd.read_csv("flights_final.csv")

# Quitar columnas innecesarias
dataframe = dataframe.reset_index(drop=True)

# Quitar Duplicaods
dataframe = dataframe.drop_duplicates()
# Quitar filas con valores nulos
dataframe = dataframe.reset_index(drop=True)

# Obtener el numero de filas y columnas
numero_filas, numero_columnas = dataframe.shape

# Crear un diccionario para guardar los aeropuertos
diccionario = {}
id = 0

for vuelo in range(numero_filas):
    if dataframe['Source Airport Code'][vuelo] not in diccionario:
        diccionario[dataframe['Source Airport Code'][vuelo]] = id
        id += 1

for vuelo in range(numero_filas):
    if dataframe['Destination Airport Code'][vuelo] not in diccionario:
        diccionario[dataframe['Destination Airport Code'][vuelo]] = id
        id += 1


