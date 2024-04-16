from manual_product import Product


def seleccionar_producto(session, store_id):
    # Recuperar todos los productos para una tienda específica
    productos = session.query(Product).filter_by(store_id=store_id).all()

    # Crear un diccionario para manejar productos únicos basándose en el nombre
    productos_unicos = {}
    for producto in productos:
        if producto.name not in productos_unicos:
            productos_unicos[producto.name] = producto

    # Mostrar los productos únicos
    for indice, (nombre, producto) in enumerate(productos_unicos.items(), start=1):
        print(f"{indice}. {nombre}")
    print('---------------------------------')
    seleccion = int(input("Selecciona el número del producto: "))
    producto_seleccionado = list(productos_unicos.values())[seleccion - 1]
    return producto_seleccionado  # Devuelve el objeto Product completo
