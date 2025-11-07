# Programa: Tiendita con menú, listas y ticket

# Lista de productos y precios
productos = ["Manzana", "Pan", "Leche", "Huevos", "Refresco"]
precios = [5.0, 10.0, 20.0, 25.0, 18.0]

# Lista donde se guardan los productos comprados
carrito = []

while True:
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Agregar artículos")
    print("2. Ticket")
    print("3. Salir")

    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        # Mostrar lista de productos
        print("\n--- LISTA DE PRODUCTOS ---")
        for i in range(len(productos)):
            print(f"{i + 1}. {productos[i]} - ${precios[i]:.2f}")

        seleccion = input("Selecciona el número del producto que deseas agregar: ")

        if seleccion.isdigit():
            seleccion = int(seleccion)
            if 1 <= seleccion <= len(productos):
                producto_seleccionado = productos[seleccion - 1]
                carrito.append(producto_seleccionado)
                print(f"{producto_seleccionado} se agregó al carrito.")
            else:
                print("❌ Opción inválida.")
        else:
            print("❌ Ingresa un número válido.")

    elif opcion == "2":
        if len(carrito) == 0:
            print("\n🛒 No hay productos en el carrito.")
        else:
            print("\n--- TICKET DE COMPRA ---")
            total = 0
            cantidades = []
            
            # Contar la cantidad de cada producto
            for p in productos:
                cantidad = carrito.count(p)
                if cantidad > 0:
                    subtotal = cantidad * precios[productos.index(p)]
                    print(f"{p} x{cantidad}  -  ${precios[productos.index(p)]:.2f} c/u  =  ${subtotal:.2f}")
                    total += subtotal

            print(f"\nTOTAL A PAGAR: ${total:.2f}")

    elif opcion == "3":
        print("\n👋 Gracias por su compra. ¡Vuelva pronto!")
        break

    else:
        print("❌ Opción no válida. Intente de nuevo.")

