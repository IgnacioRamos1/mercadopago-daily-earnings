from sqlalchemy.orm import sessionmaker

import sys
import os
sys.path.append(os.path.abspath('..'))


from utils.db_connection import dev_engine
from manual_store import Store
from manual_product import Product, Price
from select_store import seleccionar_tienda
from manual_migrate import migrate

# Crear una sesión
Session = sessionmaker(bind=dev_engine)
session = Session()


def delete_store(store_id):
    session = Session()

    try:
        # Eliminar precios asociados a los productos de la tienda
        # Primero, encontrar todos los productos de la tienda
        products = session.query(Product).filter(Product.store_id == store_id).all()
        product_ids = [product.id for product in products]

        # Eliminar todos los precios de esos productos
        if product_ids:
            session.query(Price).filter(Price.product_id.in_(product_ids)).delete(synchronize_session=False)

        # Eliminar los productos de la tienda
        session.query(Product).filter(Product.store_id == store_id).delete(synchronize_session=False)

        # Finalmente, eliminar la tienda
        session.query(Store).filter(Store.id == store_id).delete(synchronize_session=False)

        # Confirmar los cambios
        session.commit()
        print(f"Store with ID {store_id} and all related products and prices have been deleted.")
    except Exception as e:
        # En caso de error, hacer rollback de los cambios
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        # Cerrar la sesión
        session.close()


if __name__ == "__main__":
    store_id = seleccionar_tienda(session)
    choice = input(f"Are you sure you want to delete store with ID {store_id}? (y/n): ")
    if choice.lower() == 'y':
        delete_store(store_id)
        print('---------------------------------')
        migrate()
    else:
        print("Operation cancelled.")
        session.close()

