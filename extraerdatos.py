import pandas as pd
from geopy.distance import geodesic
from itertools import combinations

# Cargar los datos
df = pd.read_csv("C:/Proyectos/Tesis/Inundaciones_Chiapas.csv", encoding='latin1')

# Preprocesamiento: Limpiar y preparar los datos
# 1. Seleccionar columnas relevantes y limpiar coordenadas
df_coords = df[['Nombre_12', 'Nombre_12_', 'Latitud', 'Longitud']].copy()

# Convertir coordenadas a numérico (reemplazar comas por puntos si es necesario)
df_coords['Latitud'] = df_coords['Latitud'].astype(str).str.replace(',', '.').astype(float)
df_coords['Longitud'] = df_coords['Longitud'].astype(str).str.replace(',', '.').astype(float)

# 2. Eliminar duplicados y NaN
df_coords = df_coords.drop_duplicates(subset=['Nombre_12', 'Nombre_12_'])
df_coords = df_coords.dropna()

# 3. Crear identificador único para cada localidad
df_coords['Localidad_Unica'] = df_coords['Nombre_12'] + " - " + df_coords['Nombre_12_']

# Diccionario de ubicaciones
ubicaciones = {row['Localidad_Unica']: (row['Latitud'], row['Longitud']) 
               for _, row in df_coords.iterrows()}

# Calcular distancias entre todos los pares de localidades
distancias = {}
for (loc1, loc2) in combinations(ubicaciones.keys(), 2):
    try:
        dist = geodesic(ubicaciones[loc1], ubicaciones[loc2]).kilometers
        distancias[(loc1, loc2)] = dist
    except ValueError as e:
        print(f"Error calculando distancia entre {loc1} y {loc2}: {str(e)}")

# Convertir a DataFrame
df_distancias = pd.DataFrame([
    {'Localidad_A': loc1, 'Localidad_B': loc2, 'Distancia_km': dist}
    for (loc1, loc2), dist in distancias.items()
])

# Guardar resultados
df_distancias.to_csv("C:/Proyectos/Tesis/Distancias_Entre_Localidades.csv", index=False)

print("\n¡Proceso completado con éxito!")
print(f"Total de pares calculados: {len(distancias)}")
print(f"Archivo guardado en: C:/Proyectos/Tesis/Distancias_Entre_Localidades.csv")

# Mostrar las primeras 5 distancias calculadas
print("\nPrimeras 5 distancias calculadas:")
print(df_distancias.head())