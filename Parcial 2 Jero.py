import heapq
import pickle
import os
from datetime import datetime

# Archivo para persistencia de datos
TASKS_FILE = "tasks_data.pkl"

# Cargar tareas desde el archivo si existe
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "rb") as f:
            return pickle.load(f)
    return []

# Guardar tareas en el archivo
def save_tasks(tasks):
    with open(TASKS_FILE, "wb") as f:
        pickle.dump(tasks, f)

# Clase para manejar las tareas con sus atributos
class Task:
    def __init__(self, name, priority, dependencies, due_date):
        self.name = name
        self.priority = priority
        self.dependencies = dependencies
        self.due_date = datetime.strptime(due_date, "%Y-%m-%d")
    
    def __lt__(self, other):
        # Ordenar por prioridad primero y luego por fecha de vencimiento
        if self.priority == other.priority:
            return self.due_date < other.due_date
        return self.priority < other.priority

    def __repr__(self):
        return (f"Task(Name: {self.name}, Priority: {self.priority}, "
                f"Dependencies: {self.dependencies}, Due Date: {self.due_date.date()})")

# Función para añadir una tarea
def add_task(tasks, task_index):
    try:
        name = input("Nombre de la tarea: ").strip()
        if not name:
            raise ValueError("El nombre de la tarea no puede estar vacío.")
        if name in task_index:
            raise ValueError("Ya existe una tarea con este nombre.")
        priority = int(input("Prioridad (número entero, menor es más prioritario): "))
        dependencies = input("Dependencias (separadas por comas, o vacío si no hay): ").strip().split(",")
        dependencies = [dep.strip() for dep in dependencies if dep.strip()]
        due_date = input("Fecha de vencimiento (YYYY-MM-DD): ")
        datetime.strptime(due_date, "%Y-%m-%d")  # Validar formato de fecha
        task = Task(name, priority, dependencies, due_date)
        heapq.heappush(tasks, task)
        task_index[name] = task
        print(f"Tarea '{name}' añadida con éxito.")
    except ValueError as e:
        print(f"Error: {e}")

# Función para mostrar todas las tareas pendientes ordenadas por prioridad
def show_pending_tasks(tasks):
    if not tasks:
        print("No hay tareas pendientes.")
    else:
        print("Tareas pendientes (ordenadas por prioridad):")
        for task in sorted(tasks):
            print(task)

# Función para completar una tarea
def complete_task(tasks, task_index):
    name = input("Nombre de la tarea a completar: ").strip()
    if name in task_index:
        task_to_remove = task_index.pop(name)
        tasks.remove(task_to_remove)
        heapq.heapify(tasks)  # Reestructurar el heap
        print(f"Tarea '{name}' completada y eliminada.")
    else:
        print(f"No se encontró la tarea '{name}'.")

# Función para obtener la tarea de mayor prioridad sin eliminarla
def get_next_task(tasks):
    if not tasks:
        print("No hay tareas pendientes.")
    else:
        print(f"La siguiente tarea de mayor prioridad es: {tasks[0]}")

# Función para inicializar las tareas predefinidas
def initialize_tasks(tasks, task_index):
    predefined_tasks = [
        Task("Preparar presentación de trabajo", 1, ["Revisar informe", "Diseñar diapositivas"], "2024-12-12"),
        Task("Comprar regalos de Navidad", 2, [], "2024-12-20"),
        Task("Renovar licencia de conducir", 3, [], "2024-12-15"),
        Task("Actualizar currículum vitae", 4, ["Recopilar certificaciones"], "2024-12-18"),
        Task("Hacer limpieza general de la casa", 5, ["Comprar productos de limpieza"], "2024-12-14"),
        Task("Estudiar para el examen final de algoritmos", 1, ["Revisar notas de clase", "Resolver ejercicios del libro"], "2024-12-10"),
        Task("Pagar las facturas de servicios", 2, [], "2024-12-13"),
    ]
    for task in predefined_tasks:
        if task.name not in task_index:
            heapq.heappush(tasks, task)
            task_index[task.name] = task
    save_tasks(tasks)

# Menú principal
def main():
    tasks = load_tasks()
    heapq.heapify(tasks)  # Asegurar que las tareas se comporten como un heap
    task_index = {task.name: task for task in tasks}  # Crear índice para búsquedas rápidas

    # Inicializar tareas predefinidas si no existen
    initialize_tasks(tasks, task_index)

    while True:
        try:
            print("\nSistema de Gestión de Tareas")
            print("1. Añadir tarea")
            print("2. Mostrar tareas pendientes")
            print("3. Completar tarea")
            print("4. Obtener siguiente tarea de mayor prioridad")
            print("5. Salir")
            choice = input("Selecciona una opción: ").strip()

            if choice == "1":
                add_task(tasks, task_index)
            elif choice == "2":
                show_pending_tasks(tasks)
            elif choice == "3":
                complete_task(tasks, task_index)
            elif choice == "4":
                get_next_task(tasks)
            elif choice == "5":
                save_tasks(tasks)  # Guardar al salir
                print("Saliendo del sistema. ¡Hasta luego!")
                break
            else:
                print("Opción inválida, intenta de nuevo.")
        except KeyboardInterrupt:
            print("\nSaliendo del sistema. ¡Hasta luego!")
            save_tasks(tasks)
            break
        except Exception as e:
            print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()
