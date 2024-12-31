import random

# Parámetros del problema
zonas = 3
trabajadores_totales = 10
energia_total = 15
tamaño_poblacion = 20
generaciones = 50
probabilidad_mutacion = 0.1

# Función de evaluación (fitness)
def calcular_fitness(solucion):
    return sum((trabajadores + energia) for trabajadores, energia in solucion)

# Inicializar población
def inicializar_poblacion(tamaño, zonas, trabajadores_totales, energia_total):
    poblacion = []
    for _ in range(tamaño):
        solucion = [(random.randint(0, trabajadores_totales), random.randint(0, energia_total)) for _ in range(zonas)]
        poblacion.append(solucion)
    return poblacion

# Selección
def seleccion(poblacion, fitnesses):
    return random.choices(poblacion, weights=fitnesses, k=2)

# Cruce
def cruce(sol1, sol2):
    punto = random.randint(1, len(sol1) - 1)
    return sol1[:punto] + sol2[punto:]

# Mutación
def mutacion(solucion, trabajadores_totales, energia_total):
    indice = random.randint(0, len(solucion) - 1)
    solucion[indice] = (random.randint(0, trabajadores_totales), random.randint(0, energia_total))
    return solucion

# Algoritmo Genético
def algoritmo_genetico():
    poblacion = inicializar_poblacion(tamaño_poblacion, zonas, trabajadores_totales, energia_total)
    for _ in range(generaciones):
        fitnesses = [calcular_fitness(sol) for sol in poblacion]
        nueva_poblacion = []
        while len(nueva_poblacion) < tamaño_poblacion:
            padres = seleccion(poblacion, fitnesses)
            hijo = cruce(padres[0], padres[1])
            if random.random() < probabilidad_mutacion:
                hijo = mutacion(hijo, trabajadores_totales, energia_total)
            nueva_poblacion.append(hijo)
        poblacion = nueva_poblacion
    mejor_solucion = max(poblacion, key=calcular_fitness)
    return mejor_solucion

# Ejecutar
mejor_solucion = algoritmo_genetico()
print("Mejor solución:", mejor_solucion)
