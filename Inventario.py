import pulp

# Municipios candidatos
municipios = ['Agua Dulce', 'Coatzacoalcos', 'Cosoleacaque', 'Hidalgotitlan', 'Ixhuatlán del Sureste', 
              'Catemaco', 'Jáltipan', 'Minatitlán', 'Hueyapan de Ocampo', 'Moloacan', 'Lázaro Cárdenas', 
              'Pajapan', 'San Andrés Tuxtla', 'Santiago Tuxtla']

# Tiempos hacia Jesús Carranza
distancias_tiempos = {
    ('Agua Dulce', 'Jesús Carranza'): (172.34, 2.7), 
    ('Coatzacoalcos', 'Jesús Carranza'): (131.96, 2.15),
    ('Cosoleacaque', 'Jesús Carranza'): (208.04, 3.9),
    ('Hidalgotitlan', 'Jesús Carranza'): (104.24, 2.2),
    ('Ixhuatlán del Sureste', 'Jesús Carranza'): (130.98, 2.04),
    ('Catemaco', 'Jesús Carranza'): (197.21, 3.1),
    ('Jáltipan', 'Jesús Carranza'): (189.89, 3.85),
    ('Minatitlán', 'Jesús Carranza'): (111.31, 1.85),
    ('Hueyapan de Ocampo', 'Jesús Carranza'): (158.64, 2.4),
    ('Moloacan', 'Jesús Carranza'): (145.03, 2.6),
    ('Lázaro Cárdenas', 'Jesús Carranza'): (137.55, 2.43),
    ('Pajapan', 'Jesús Carranza'): (122.95, 2.3),
    ('San Andrés Tuxtla', 'Jesús Carranza'): (207.97, 3.37),
    ('Santiago Tuxtla', 'Jesús Carranza'): (225.41, 3.37),
}

# Costos fijos
costos_inventario = {m: 50000 for m in municipios}

# Demanda total
demanda_jc = 10000

# Modelo
model = pulp.LpProblem("Ubicacion_e_Inventario", pulp.LpMinimize)

# Variables de decisión
almacenes = pulp.LpVariable.dicts("Almacen", municipios, cat='Binary')
inventario = pulp.LpVariable.dicts("Inventario", municipios, lowBound=0, cat='Continuous')

# Función objetivo: minimizar el costo fijo
model += pulp.lpSum([costos_inventario[m] * almacenes[m] for m in municipios])

# Cada municipio solo puede enviar si su tiempo ≤ 3h
for m in municipios:
    tiempo = distancias_tiempos.get((m, 'Jesús Carranza'), (0, float('inf')))[1]
    # Si el tiempo > 3, entonces el inventario enviado debe ser 0
    if tiempo > 3:
        model += inventario[m] == 0, f"TiempoExcede_{m}"

# Inventario solo si hay almacén
for m in municipios:
    model += inventario[m] <= demanda_jc * almacenes[m], f"InventarioSoloSiHayAlmacen_{m}"

# Demanda total debe cumplirse
model += pulp.lpSum([inventario[m] for m in municipios]) == demanda_jc, "DemandaCumplida"

# Al menos 2 almacenes
model += pulp.lpSum([almacenes[m] for m in municipios]) >= 2, "Minimo_2_Almacenes"

# Resolver
model.solve()

# Resultados
print("Estado de la solución:", pulp.LpStatus[model.status])
for m in municipios:
    if almacenes[m].varValue == 1:
        print(f"Almacén en {m}: enviar {inventario[m].varValue:.2f} unidades")


