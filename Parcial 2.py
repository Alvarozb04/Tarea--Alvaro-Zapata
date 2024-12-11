import heapq
import json
from datetime import datetime

class SistemaDeTareas:
    def __init__(self, archivo_persistencia="tareas.json"):
        self.tareas = []
        self.archivo_persistencia = archivo_persistencia
        self.cargar_tareas()

    def agregar_tarea(self, nombre, prioridad, fecha_vencimiento, dependencias):
        if not isinstance(prioridad, int):
            raise ValueError("La prioridad debe ser un número entero.")
        if not isinstance(dependencias, list):
            raise ValueError("Las dependencias deben ser una lista.")
        try:
            fecha = datetime.strptime(fecha_vencimiento, "%Y-%m-%d")
        except ValueError:
            raise ValueError("La fecha de vencimiento debe tener el formato AAAA-MM-DD.")
        
        tarea = {
            "nombre": nombre,
            "prioridad": prioridad,
            "fecha_vencimiento": fecha_vencimiento,
            "dependencias": dependencias,
            "completada": False
        }
        # Insertar en el heap, comparando primero por prioridad, luego por fecha
        heapq.heappush(self.tareas, (prioridad, fecha, tarea))
        self.guardar_tareas()

    def mostrar_tareas(self):
        return [
            tarea[2] for tarea in sorted(
                self.tareas, key=lambda x: (x[0], x[1])
            )
        ]

    def completar_tarea(self, nombre):
        for i, (_, _, tarea) in enumerate(self.tareas):
            if tarea["nombre"] == nombre:
                self.tareas.pop(i)
                heapq.heapify(self.tareas)
                self.guardar_tareas()
                return f"Tarea '{nombre}' completada y eliminada."
        return f"Tarea '{nombre}' no encontrada."

    def obtener_siguiente_tarea(self):
        if self.tareas:
            return self.tareas[0][2]
        return "No hay tareas pendientes."

    def verificar_tarea_ejecutable(self, nombre):
        for _, _, tarea in self.tareas:
            if tarea["nombre"] == nombre:
                for dependencia in tarea["dependencias"]:
                    if not any(
                        t["nombre"] == dependencia and t["completada"] for _, _, t in self.tareas
                    ):
                        return False
                return True
        return False

    def guardar_tareas(self):
        with open(self.archivo_persistencia, "w") as archivo:
            json.dump(
                [(p, f.strftime("%Y-%m-%d"), t) for p, f, t in self.tareas], archivo
            )

    def cargar_tareas(self):
        try:
            with open(self.archivo_persistencia, "r") as archivo:
                self.tareas = [
                    (p, datetime.strptime(f, "%Y-%m-%d"), t)
                    for p, f, t in json.load(archivo)
                ]
        except FileNotFoundError:
            self.tareas = []

# Ejemplo de uso
sistema = SistemaDeTareas()

# Añadir tareas
sistema.agregar_tarea("Tarea 1", 1, "2024-12-12", [])
sistema.agregar_tarea("Tarea 2", 2, "2024-12-13", ["Tarea 1"])
sistema.agregar_tarea("Tarea 3", 3, "2024-12-14", [])

# Mostrar tareas pendientes
print("Tareas pendientes:")
for tarea in sistema.mostrar_tareas():
    print(tarea)

# Completar una tarea
print(sistema.completar_tarea("Tarea 1"))

# Obtener siguiente tarea
print("Siguiente tarea de mayor prioridad:")
print(sistema.obtener_siguiente_tarea())

# Verificar si una tarea es ejecutable
print("¿Tarea 2 es ejecutable?")
print(sistema.verificar_tarea_ejecutable("Tarea 2"))
