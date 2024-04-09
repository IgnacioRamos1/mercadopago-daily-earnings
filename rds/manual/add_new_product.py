from sqlalchemy.orm import sessionmaker
import sys
import os
sys.path.append(os.path.abspath('..'))

from manual_product import Product, Price
from manual_migrate import migrate
from utils.db_connection import dev_engine
from select_store import seleccionar_tienda
from select_product import seleccionar_producto
from manage_prices import manage_product_prices

Session = sessionmaker(bind=dev_engine)

def main():
    session = Session()

    # Se solicita el ID de la tienda una vez al principio
    store_id = seleccionar_tienda(session)
    print('---------------------------------')

    while True:
        choice = input("Do you want to add a new product (1), update an existing one (2), or delete a product (3)? (q to quit): ")
        print('---------------------------------')

        if choice == '1':
            name = input("Enter the name of the product: ")
            print('---------------------------------')
            price = float(input("Enter the price of the product: "))
            print('---------------------------------')

            new_product = Product(name=name, store_id=store_id)
            session.add(new_product)
            session.commit()

            new_price = Price(amount=price, product_id=new_product.id)
            session.add(new_price)
            session.commit()

            multiple_prices = input("Do you want to add more prices? (y/n): ")
            print('---------------------------------')
            while multiple_prices.lower() == 'y':
                price = float(input("Enter the price of the product: "))
                print('---------------------------------')
                new_price = Price(amount=price, product_id=new_product.id)
                session.add(new_price)
                session.commit()
                multiple_prices = input("Do you want to add more prices? (y/n): ")
                print('---------------------------------')


            # Aquí deberías añadir la lógica para manejar el precio de manera adecuada
            print(f"Product {new_product.name} added successfully!")

        elif choice == '2':
            product = seleccionar_producto(session, store_id)
            print('---------------------------------')

            if product:
                print(f"Has seleccionado: {product.name}")
                print('---------------------------------')
                print("Precios actuales:")
                for index, price in enumerate(product.prices, start=1):
                    print(f"{index}. ${price.amount}")
                print('---------------------------------')
                # Llama a manage_product_prices para gestionar los precios del producto seleccionado
                manage_product_prices(session, product)
            else:
                print("Producto no encontrado o no seleccionado.")
        
        elif choice == '3':
            product = seleccionar_producto(session, store_id)
            print('---------------------------------')

            if product:
                confirm = input(f"Are you sure you want to delete {product.name} and all its prices? (y/n): ")
                print('---------------------------------')
                if confirm.lower() == 'y':
                    # Eliminar todos los precios asociados primero para mantener la integridad referencial
                    prices_to_delete = session.query(Price).filter(Price.product_id == product.id).all()
                    for price in prices_to_delete:
                        session.delete(price)

                    # Ahora, eliminar el producto
                    session.delete(product)
                    session.commit()
                    print(f"{product.name} and all its prices have been deleted successfully!")
                    print('---------------------------------')
                else:
                    print("Deletion cancelled.")
            else:
                print("Producto no encontrado o no seleccionado.")


        elif choice.lower() == 'q':
            break

        else:
            print("Invalid choice.")

    session.close()
    migrate()

if __name__ == "__main__":
    main()
