# Datos del almacén importados
productos_almacen = {
    "Estantería A": [{"nombre": "Chocolate Amargo", "cantidad": 20, "precio": 2.5}, {"nombre": "Mermelada de Fresa", "cantidad": 15, "precio": 3.0}],
    "Estantería B": [{"nombre": "Aceitunas Verdes", "cantidad": 50, "precio": 1.5}, {"nombre": "Aceite de Oliva Extra", "cantidad": 10, "precio": 6.0}],
    "Estantería C": [{"nombre": "Café Molido", "cantidad": 25, "precio": 5.0}, {"nombre": "Té Verde", "cantidad": 40, "precio": 2.0}],
    "Estantería D": [{"nombre": "Pasta Integral", "cantidad": 30, "precio": 1.8}, {"nombre": "Arroz Basmati", "cantidad": 20, "precio": 1.7}]
}

# Función para agregar productos
def agregar_producto(nombre, cantidad, precio, estanteria):
    if estanteria not in productos_almacen:
        productos_almacen[estanteria] = []
    productos_almacen[estanteria].append({"nombre": nombre, "cantidad": cantidad, "precio": precio})
    print(f"Producto '{nombre}' agregado correctamente a {estanteria}.")

# Función para retirar productos
def retirar_producto(nombre, cantidad):
    for estanteria, productos in productos_almacen.items():
        for producto in productos:
            if producto["nombre"] == nombre:
                if producto["cantidad"] >= cantidad:
                    producto["cantidad"] -= cantidad
                    print(f"Retirado {cantidad} de '{nombre}' en {estanteria}.")
                else:
                    print(f"Error: No hay suficiente cantidad de '{nombre}' en {estanteria}.")
                return
    print(f"Producto '{nombre}' no encontrado en el almacén.")

# Función para verificar disponibilidad
def verificar_disponibilidad(nombre):
    for estanteria, productos in productos_almacen.items():
        for producto in productos:
            if producto["nombre"] == nombre:
                print(f"{nombre} disponible en {estanteria} con cantidad {producto['cantidad']}.")
                return
    print(f"Producto '{nombre}' no encontrado en el almacén.")

# Función para verificar el estado del almacén
def estado_almacen():
    for estanteria, productos in productos_almacen.items():
        total_valor = sum([producto["cantidad"] * producto["precio"] for producto in productos])
        total_productos = sum([producto["cantidad"] for producto in productos])
        print(f"{estanteria} tiene {len(productos)} tipos de productos, {total_productos} unidades en total, valor total {total_valor:.2f}.")
        for producto in productos:
            print(f"- {producto['nombre']}: {producto['cantidad']} unidades a {producto['precio']} cada uno.")


# Función para transferir productos entre estanterías
def transferir_producto(nombre, cantidad, origen, destino):
    for producto in productos_almacen.get(origen, []):
        if producto["nombre"] == nombre:
            if producto["cantidad"] >= cantidad:
                producto["cantidad"] -= cantidad
                for prod_destino in productos_almacen.get(destino, []):
                    if prod_destino["nombre"] == nombre:
                        prod_destino["cantidad"] += cantidad
                        print(f"Transferido {cantidad} de '{nombre}' de {origen} a {destino}.")
                        return
                productos_almacen[destino].append({"nombre": nombre, "cantidad": cantidad, "precio": producto["precio"]})
                print(f"Transferido {cantidad} de '{nombre}' de {origen} a {destino}.")
                return
            else:
                print(f"Error: No hay suficiente cantidad de '{nombre}' en {origen}.")
            return
    print(f"Producto '{nombre}' no encontrado en {origen}.")


def estanteria_mayor_valor_menos_productos():
    estanteria_mayor_valor = None
    valor_mayor = 0
    estanteria_menos_productos = None
    cantidad_menor = float('inf')

    for estanteria, productos in productos_almacen.items():
        # Calcular el valor acumulado en la estantería
        valor_acumulado = sum([producto["cantidad"] * producto["precio"] for producto in productos])
        # Calcular la cantidad total de productos en la estantería
        cantidad_total_productos = sum([producto["cantidad"] for producto in productos])

        # Encontrar la estantería con el mayor valor acumulado
        if valor_acumulado > valor_mayor:
            valor_mayor = valor_acumulado
            estanteria_mayor_valor = estanteria

        # Encontrar la estantería con la menor cantidad de productos
        if cantidad_total_productos < cantidad_menor:
            cantidad_menor = cantidad_total_productos
            estanteria_menos_productos = estanteria

    print(f"Estantería con mayor valor acumulado: {estanteria_mayor_valor} con valor {valor_mayor:.2f}")
    print(f"Estantería con menos productos: {estanteria_menos_productos} con {cantidad_menor} unidades")


# Ejemplos de uso
# Agregar producto
agregar_producto("Azúcar Blanca", 50, 1.2, "Estantería A")

# Retirar producto
retirar_producto("Aceitunas Verdes", 20)

# Verificar disponibilidad
verificar_disponibilidad("Café Molido")

# Estado del almacén
estado_almacen()

# Transferir producto
transferir_producto("Pasta Integral", 10, "Estantería D", "Estantería B")

# Estanteria con mayor valor y con menor
estanteria_mayor_valor_menos_productos()

    
