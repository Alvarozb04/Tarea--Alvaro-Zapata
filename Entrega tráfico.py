import networkx as nx

def adjust_capacities(G, situation):
    """
    Ajusta las capacidades de las carreteras según la situación seleccionada.
    """
    if situation == "Catástrofe Natural":
        # Establecer todas las capacidades a 0 (tráfico imposible)
        for u, v in G.edges:
            G.edges[u, v]['capacity'] = 0
    elif situation == "Hora Punta":
        # Reducir todas las capacidades al 50%
        for u, v in G.edges:
            G.edges[u, v]['capacity'] = int(G.edges[u, v]['capacity'] * 0.5)
    elif situation == "Hora de la siesta":
        # Aumentar todas las capacidades en un 50%
        for u, v in G.edges:
            G.edges[u, v]['capacity'] = int(G.edges[u, v]['capacity'] * 1.5)

def ford_fulkerson_algorithm(G, source, sink):
    # Crear un grafo residual con las mismas aristas y capacidades que el original
    residual_graph = G.copy()
    flow = 0  # Flujo máximo inicial

    # Función para encontrar un camino aumentante utilizando DFS
    def dfs_find_path(residual_graph, source, sink, path, visited):
        visited.add(source)
        if source == sink:
            return path
        for neighbor in residual_graph.neighbors(source):
            if neighbor not in visited and residual_graph.edges[source, neighbor]['capacity'] > 0:
                result = dfs_find_path(
                    residual_graph, 
                    neighbor, 
                    sink, 
                    path + [(source, neighbor)], 
                    visited
                )
                if result is not None:
                    return result
        return None

    # Buscar caminos aumentantes hasta que no haya más
    while True:
        path = dfs_find_path(residual_graph, source, sink, [], set())
        if path is None:
            break

        # Determinar la capacidad mínima a lo largo del camino aumentante
        path_flow = min(residual_graph.edges[u, v]['capacity'] for u, v in path)
        
        # Actualizar capacidades en el grafo residual
        for u, v in path:
            residual_graph.edges[u, v]['capacity'] -= path_flow
            if residual_graph.has_edge(v, u):
                residual_graph.edges[v, u]['capacity'] += path_flow
            else:
                residual_graph.add_edge(v, u, capacity=path_flow)

        # Incrementar el flujo máximo por la capacidad del camino encontrado
        flow += path_flow

    return flow

def create_road_network():
    # Crear un grafo dirigido
    G = nx.DiGraph()

    # Añadir carreteras (aristas) con capacidades (número máximo de vehículos por hora)
    edges = [
        ('A', 'B', 20),
        ('A', 'C', 10),
        ('B', 'C', 5),
        ('B', 'D', 10),
        ('C', 'D', 20),
        ('C', 'E', 5),
        ('D', 'E', 10)
    ]

    # Añadir nodos y sus conexiones al grafo
    for u, v, capacity in edges:
        G.add_edge(u, v, capacity=capacity)

    return G

def main():
    # Crear la red de carreteras
    G = create_road_network()

    # Preguntar al usuario sobre la situación del tráfico
    print("Selecciona la situación de tráfico:")
    print("1. Catástrofe Natural")
    print("2. Hora Punta")
    print("3. Hora de la siesta")
    choice = input("Elige una opción (1, 2, 3): ")

    if choice == "1":
        situation = "Catástrofe Natural"
    elif choice == "2":
        situation = "Hora Punta"
    elif choice == "3":
        situation = "Hora de la siesta"
    else:
        print("Opción no válida. Se seleccionará 'Hora Punta' por defecto.")
        situation = "Hora Punta"

    # Ajustar las capacidades según la situación elegida
    adjust_capacities(G, situation)

    # Definir la fuente y el destino
    source = 'A'
    sink = 'E'

    # Calcular el flujo máximo utilizando el algoritmo de Ford-Fulkerson
    max_flow = ford_fulkerson_algorithm(G, source, sink)
    print(f"\nSituación: {situation}")
    print(f"El flujo máximo desde {source} hasta {sink} es: {max_flow}")

if __name__ == "__main__":
    main()
        
        


