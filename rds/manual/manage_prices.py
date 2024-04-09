from manual_product import Price


def manage_product_prices(session, product):
    while True:
        accion = input("¿Deseas agregar un nuevo precio, actualizar uno existente, eliminar uno, o salir? (1/2/3/q): ")
        print('---------------------------------')
        if accion == '1':
            nuevo_precio = float(input("Ingresa el nuevo precio: "))
            nuevo_registro_precio = Price(amount=nuevo_precio, product_id=product.id)
            session.add(nuevo_registro_precio)
            session.commit()
            print("Nuevo precio agregado correctamente.")
        elif accion == '2':
            precios = product.prices  # Acceder a los precios a través de la relación
            for index, price in enumerate(precios, start=1):
                print(f"{index}. ${price.amount}")
            print('---------------------------------')
            indice_precio = int(input("Número del precio a actualizar: ")) - 1
            print('---------------------------------')
            if 0 <= indice_precio < len(precios):
                nuevo_precio = float(input("Nuevo precio: "))
                precios[indice_precio].amount = nuevo_precio
                session.commit()
                print('---------------------------------')
                print("Precio actualizado correctamente.")
            else:
                print("Número de precio inválido.")
        elif accion == '3':
            precios = product.prices  # Acceder a los precios a través de la relación
            for index, price in enumerate(precios, start=1):
                print(f"{index}. ${price.amount}")
            print('---------------------------------')
            indice_precio = int(input("Número del precio a eliminar: ")) - 1
            print('---------------------------------')
            if 0 <= indice_precio < len(precios):
                session.delete(precios[indice_precio])
                session.commit()
                print("Precio eliminado correctamente.")
                print('---------------------------------')
            else:
                print("Número de precio inválido.")
        elif accion == 'q':
            break
        else:
            print("Acción no reconocida.")
            print('---------------------------------')
